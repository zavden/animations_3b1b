# ==============================================================================
# Scene:      ReferenceDerivatives
# Source:     videos/_2026/print_gallery/supplements.py (lines 415-457)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceDerivatives.py ReferenceDerivatives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceDerivatives(InteractiveScene):
    def construct(self):
        # Test
        groups = VGroup(
            self.get_group("z^2", "2z"),
            self.get_group("z^3", "3z^2"),
            self.get_group("e^z", "e^z"),
            self.get_group(R"\ln(z)", R"{1 \over z}"),
        )
        groups.arrange(DOWN, buff=LARGE_BUFF)

        self.add(*(g[0] for g in groups))
        self.play(
            LaggedStart(
                (TransformMatchingTex(g[0].copy(), g[2])
                for g in groups),
                lag_ratio=0.2,
            ),
            LaggedStart(
                (GrowArrow(g[1]) for g in groups),
                lag_ratio=0.2,
            ),
            LaggedStart(
                (FadeIn(g[3], 0.25 * RIGHT) for g in groups),
                lag_ratio=0.2,
            ),
            run_time=3
        )
        self.wait()

    def get_group(self, in_tex, out_tex):
        kw = dict(font_size=60, t2c={"z": BLUE})
        group = VGroup(
            Tex(in_tex, **kw),
            Vector(1.5 * RIGHT, thickness=4),
            Tex(out_tex, **kw),
        )
        group.arrange(RIGHT)
        deriv_label = Tex(R"d / dz", **kw)
        deriv_label.scale(0.5)
        deriv_label.next_to(group[1], UP, SMALL_BUFF)
        group.add(deriv_label)
        return group
