# ==============================================================================
# Scene:      ShowParameterization
# Source:     videos/_2018/sphere_area.py (lines 2052-2088)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowParameterization.py ShowParameterization -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowParameterization(Scene):
    def construct(self):
        u_color = PINK
        v_color = GREEN
        tex_kwargs = {
            "tex_to_color_map": {
                "u": u_color,
                "v": v_color,
            }
        }
        vector = Matrix(
            [
                ["\\text{cos}(u)\\text{sin}(v)"],
                ["\\text{sin}(u)\\text{sin}(v)"],
                ["\\text{cos}(v)"]
            ],
            element_to_mobject_config=tex_kwargs,
            element_alignment_corner=DOWN,
        )
        vector.to_edge(UP)

        ranges = VGroup(
            OldTex("0 \\le u \\le 2\\pi", **tex_kwargs),
            OldTex("0 \\le v \\le \\pi", **tex_kwargs),
            OldTexText(
                "Sample $u$ and $v$ with \\\\ the same density",
                tex_to_color_map={
                    "$u$": u_color,
                    "$v$": v_color,
                }
            )
        )
        ranges.arrange(DOWN)
        ranges.next_to(vector, DOWN)

        self.add(vector)
        self.add(ranges)
