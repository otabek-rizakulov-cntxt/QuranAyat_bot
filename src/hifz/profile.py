# Workstream B — profile & registration (spec items B1-B3).
#
# Owns: /profile, the leaderboard opt-in and display name, and the timezone +
# reminder-time capture that the streak day boundary and the scheduler depend on.
# Callback prefix: "hp:" (see hifz.PREFIXES). Wizard kinds: prefix them "profile_".
#
# Wave 2 owns this file. Register handlers with the decorators — nothing outside
# this module needs to change:
#
#     from hifz import Ctx, callback, command, wizard
#
#     @command("profile")
#     async def profile(ctx: Ctx) -> None:
#         ...
