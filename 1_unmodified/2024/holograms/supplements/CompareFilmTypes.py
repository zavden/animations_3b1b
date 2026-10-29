# ==============================================================================
# Scene:      CompareFilmTypes
# Source:     videos/_2024/holograms/supplements.py (lines 1121-1162)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareFilmTypes.py CompareFilmTypes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareFilmTypes(InteractiveScene):
    def construct(self):
        # Test
        categories = VGroup(
            Text("Polaroid instant film"),
            Text("Microfilm"),
            Text("What we used (Bayfol HX200)"),
        )
        categories[2]["(Bayfol HX200)"].set_color(GREY_B)

        resolutions = VGroup(
            Text("10-20 lines per mm"),
            Text("100-200 lines per mm"),
            Text("> 5,000 lines per mm"),
        )

        arrows = Vector(RIGHT, thickness=4).replicate(3)

        last_group = VGroup()
        for text, res, arrow in zip(categories, resolutions, arrows):
            arrow = Vector(RIGHT)
            group = VGroup(text, arrow, res)
            group.arrange(RIGHT)
            res.align_to(text, UP)
            group.to_edge(UP)

            text.save_state()
            text.set_x(0)

            self.play(
                FadeOut(last_group, 0.5 * UP),
                FadeIn(text, 0.5 * UP),
            )
            self.wait()
            self.play(
                Restore(text),
                GrowArrow(arrow),
                FadeIn(res, RIGHT)
            )
            self.wait()

            last_group = group
