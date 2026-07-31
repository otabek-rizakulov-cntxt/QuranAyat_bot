# Workstream D — plans & drills (spec items D1, D3-D5).
#
# Owns: /memorize (the setup wizard: target -> pace -> days -> preview ->
# confirm), drill delivery, the "I know this by heart" button, and the plan
# lifecycle (pause / resume / abandon / complete).
# Callback prefix: "hm:" (see hifz.PREFIXES). Wizard kinds: prefix them "plan_".
#
# Drill delivery reuses `main.send_quran` (module level since Wave 0b, so the
# scheduler can call it too) and `main.send_combined_audio`.
