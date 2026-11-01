#!/bin/sh
# Commit and push the knowledge graph once graphify's post-commit rebuild settles.
#
# graphify's post-commit hook rebuilds graphify-out/ in a detached background
# process, so the regenerated files land *after* the commit that triggered them.
# This script follows it: wait for the rebuild to finish, commit only the
# committed graphify files (see CLAUDE.md), and push the current branch.
#
# Wired in by .git/hooks/post-commit (local, not versioned):
#     sh scripts/graphify-autopush.sh --background
#
# Never runs on main, a detached HEAD, or during a rebase/merge/cherry-pick.
# Set GRAPHIFY_AUTOPUSH=0 to turn it off for one command or a whole shell.

[ "${GRAPHIFY_AUTOPUSH:-1}" = "0" ] && exit 0
# Our own commit fires post-commit again; stop there.
[ "${GRAPHIFY_AUTOPUSH_RUNNING:-0}" = "1" ] && exit 0

top=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$top" || exit 0

if [ "${1:-}" = "--background" ]; then
    log="${GRAPHIFY_AUTOPUSH_LOG:-$HOME/.cache/graphify-autopush.log}"
    mkdir -p "$(dirname "$log")"
    nohup sh "$0" >>"$log" 2>&1 </dev/null &
    exit 0
fi

gitdir=$(git rev-parse --git-dir)
[ -d "$gitdir/rebase-merge" ] || [ -d "$gitdir/rebase-apply" ] && exit 0
[ -f "$gitdir/MERGE_HEAD" ] || [ -f "$gitdir/CHERRY_PICK_HEAD" ] && exit 0

branch=$(git symbolic-ref --short -q HEAD) || exit 0
case "$branch" in
    main | master) exit 0 ;;
esac

# Wait for the rebuild: give it a moment to take the lock, then wait (up to
# 10 minutes) for the lock to go away.
lock=graphify-out/.rebuild.lock
sleep 3
waited=0
while [ -e "$lock" ] && [ "$waited" -lt 600 ]; do
    sleep 2
    waited=$((waited + 2))
done
if [ -e "$lock" ]; then
    echo "$(date '+%F %T') [$branch] rebuild still running after 10 min; skipped"
    exit 0
fi

# Only the files CLAUDE.md lists as committed. .graphify_root must stay
# relative: a rebuild sometimes rewrites it to this machine's absolute path.
paths="graphify-out/graph.json graphify-out/GRAPH_REPORT.md graphify-out/manifest.json
graphify-out/.graphify_labels.json graphify-out/.graphify_labels.json.sig"
if [ "$(cat graphify-out/.graphify_root 2>/dev/null)" = "." ]; then
    paths="$paths graphify-out/.graphify_root"
fi

existing=""
for p in $paths; do
    [ -e "$p" ] && existing="$existing $p"
done
# shellcheck disable=SC2086
if [ -z "$(git status --porcelain -- $existing)" ]; then
    exit 0  # the rebuild changed nothing that is committed
fi

# `git commit -- <paths>` commits only these paths; anything else the user has
# staged stays staged and out of this commit.
# shellcheck disable=SC2086
git add -- $existing &&
    GRAPHIFY_AUTOPUSH_RUNNING=1 GRAPHIFY_SKIP_HOOK=1 git commit -q --no-verify \
        -m "chore(graphify): refresh the knowledge graph" -- $existing || {
    echo "$(date '+%F %T') [$branch] commit failed"
    exit 0
}

if git push -q -u origin "HEAD:refs/heads/$branch"; then
    echo "$(date '+%F %T') [$branch] committed and pushed $(git rev-parse --short HEAD)"
else
    echo "$(date '+%F %T') [$branch] committed $(git rev-parse --short HEAD); push failed"
fi
