# CLAUDE.md

## graphify

This project has a knowledge graph at `graphify-out/` (code via AST + markdown docs), committed so it
travels with the repo. Global lookup rules live in `~/.claude/GRAPHIFY.md`; the essentials:

- When `graphify-out/graph.json` exists, run `graphify query "<question>" --budget 1500` before your first
  grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that
  explores code. Read raw files only for lines the graph already located (`rtk read <file> -l minimal`).
- Use `graphify path "<A>" "<B>"` for relationships, `graphify explain "<concept>"` for one concept, and
  `graphify affected "<node>"` before refactors.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review.
- After modifying code, run `graphify update .` (AST-only, no API cost). The post-commit hook also does
  this when installed (`graphify hook install`). After changing docs, run `/graphify . --update`.
- A committed `graphify-out/graph.json` is rewritten whole on every build, so a large diff to it is
  expected. Do not flag it as churn or suggest skipping the rebuild or its hooks.

### First time on a new machine

```bash
uv tool install 'graphifyy[sql]'
graphify hook install                              # local .git/hooks, not committed
graphify export obsidian && graphify export html   # regenerate the vault + HTML (gitignored)
```

Then in Obsidian: "Open folder as vault" → `graphify-out/obsidian`.
