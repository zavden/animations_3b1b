# ==============================================================================
# Scene:      Question4
# Source:     videos/_2018/sphere_area.py (lines 3418-3433)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Question4.py Question4 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Question4(Scene):
    def construct(self):
        question = OldTexText(
            "Question \\#4:",
            "Explain how the shadows relate to\\\\"
            "every other ring on the sphere.",
            tex_to_color_map={
                "shadows": YELLOW,
                "every other ring": BLUE,
            }
        )

        self.add(question[0])
        self.wait()
        self.play(FadeInFromDown(question[1:]))
        self.wait()
