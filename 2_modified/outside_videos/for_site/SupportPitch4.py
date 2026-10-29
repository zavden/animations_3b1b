# ==============================================================================
# Scene:      SupportPitch4
# Source:     videos/outside_videos/for_site.py (lines 160-166)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SupportPitch4.py SupportPitch4 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Text does not interpret \\\\ as a line break (in 2019 it was LaTeX); \n is used
# ==============================================================================

from manim_imports_ext import *

class SupportPitch1(Scene):
    CONFIG = {
        "camera_config": {
            "background_opacity": 0.85,
        },
        "mode1": "happy",
        "mode2": "hooray",
        # CHANGE: Text does not interpret \\\\ as a line break (in 2019 it was LaTeX); \n is used
        "words1": "So what do\nyou do?",
        # CHANGE: Text does not interpret \\\\ as a line break (in 2019 it was LaTeX); \n is used
        "words2": "Oh, I make\nvideos about\nmath.",
    }

    def construct(self):
        randy = Randolph()
        randy.to_corner(DL)
        morty = Mortimer()
        morty.to_corner(DR)

        randy.change(self.mode1, morty.eyes)
        morty.change(self.mode2, randy.eyes)

        b1 = randy.get_bubble(
            self.words1,
            bubble_type=SpeechBubble,
            height=3,
            width=4,
        )
        b1.add(b1.content)
        b1.shift(0.25 * UP)
        b2 = morty.get_bubble(
            self.words2,
            bubble_type=SpeechBubble,
            height=3,
            width=4,
        )
        # b2.content.scale(0.9)
        b2.add(b2.content)
        b2.shift(0.25 * DOWN)

        self.add(randy)
        self.add(morty)
        self.add(b2)
        self.add(b1)


class SupportPitch4(SupportPitch1):
    CONFIG = {
        "mode1": "confused",
        "mode2": "hesitant",
        "words1": "Wait, what?",
        # CHANGE: Text does not interpret \\\\ as a line break (in 2019 it was LaTeX); \n is used
        "words2": "I know,\nit's weird...",
    }
