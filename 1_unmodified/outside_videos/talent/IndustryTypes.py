# ==============================================================================
# Scene:      IndustryTypes
# Source:     videos/outside_videos/talent.py (lines 268-292)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IndustryTypes.py IndustryTypes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IndustryTypes(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Opportunities in:", font_size=72)
        title.set_backstroke(BLACK, 3)
        title.add_to_back(Underline(title, buff=-0.05).set_stroke(BLUE))
        title.to_corner(UL)
        words = VGroup(
            Text("Education"),
            Text("AI Safety"),
            Text("Agentic code developement"),
            Text("Social engineering defense"),
            Text("Finance"),
            Text("Cryptography research"),
            Text("Software engineering"),
            Text("More..."),
        )
        words.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        words.set_fill(GREY_A)
        words.next_to(title, DOWN, aligned_edge=LEFT, buff=0.5).shift(RIGHT)

        self.frame.set_height(10, about_edge=UL)
        self.add(title, words)
        self.play(LaggedStartMap(FadeIn, words, shift=0.5 * UP, lag_ratio=0.25, run_time=3))
        self.wait()
