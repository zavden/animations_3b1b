# ==============================================================================
# Scene:      YTStatement
# Source:     videos/_2022/some2/winners.py (lines 311-330)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YTStatement.py YTStatement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class YTStatement(InteractiveScene):
    def construct(self):
        # Start
        words = VGroup(
            Text("Shared viewer base"),
            OldTex("\\Downarrow", font_size=96).set_stroke(WHITE, 0),
            Text("""
                YT is more likely to
                recommend one video
                to viewers of another.
            """, alignment="LEFT")
        )
        words.arrange(DOWN, buff=MED_LARGE_BUFF)

        self.add(words[0])
        self.play(
            Write(words[1]),
            FadeIn(words[2], DOWN)
        )
        self.wait()
