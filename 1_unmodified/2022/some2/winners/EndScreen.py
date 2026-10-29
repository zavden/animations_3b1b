# ==============================================================================
# Scene:      EndScreen
# Source:     videos/_2022/some2/winners.py (lines 1386-1391)
# Category:   1 · Renders unmodified
# Includes code copied from: _2021/some1_winners.py
#
# Run from this folder:
#     manimgl EndScreen.py EndScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/some1_winners.py -----

class EndScreen(PatreonEndScreen):
    pass



# ----- From _2022/some2/winners.py -----

class EndScreen(PatreonEndScreen):
    CONFIG = {
        "title_text": "Playlist of all entries",
        "scroll_time": 30,
        "thanks_words": "Many additional thanks to these Patreon supporters"
    }
