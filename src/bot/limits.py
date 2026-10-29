"""Upper bounds on what one request may make the bot send."""

# Cap how many ayahs a single combined-audio request may stitch together, to bound
# download time and stay well under Telegram's 50 MB bot upload limit.
MAX_RANGE_AYAHS = 50


# How many times the repeat button plays an ayah back to back. Memorizing works by
# hearing the same ayah over and over, and three is enough to be useful without
# making a file so long that sending it is the slow part.
REPEAT_COUNT = 3
