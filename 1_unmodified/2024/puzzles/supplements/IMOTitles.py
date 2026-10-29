# ==============================================================================
# Scene:      IMOTitles
# Source:     videos/_2024/puzzles/supplements.py (lines 658-685)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IMOTitles.py IMOTitles -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IMOTitles(InteractiveScene):
    def construct(self):
        # Test
        logo = ImageMobject("IMO_logo")
        logo.set_height(1.25)
        title1 = Text("International Math Olympiad 2024")
        title2 = Text("IMO 2024", font_size=60)
        for title in title1, title2:
            title.to_edge(UP)
            title.shift(logo.get_width() * RIGHT / 2)
        logo.next_to(title1, LEFT)

        self.add(logo, title1)
        self.wait()
        self.play(
            TransformMatchingStrings(
                title1, title2,
                key_map={
                    "International": "I",
                    "Math": "M",
                    "Olympiad": "O",
                },
                run_time=1.5,
                lag_ratio=0.1
            ),
            logo.animate.next_to(title2, LEFT),
        )
        self.wait()
