# Workstream H — weekly leaderboard (spec items H1, H2).
#
# Owns: /leaderboard. Ranks sessions completed in the Mon->Sun week local to the
# user (see lib/localtime.week_bounds), ties broken by streak length, opted-in
# users only. The caller's own row is always shown, even outside the top N.
# Callback prefix: "hl:" (see hifz.PREFIXES).
