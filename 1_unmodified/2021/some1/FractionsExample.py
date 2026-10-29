# ==============================================================================
# Scene:      FractionsExample
# Source:     videos/_2021/some1.py (lines 565-667)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FractionsExample.py FractionsExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FractionsExample(Scene):
    def construct(self):
        expr = OldTex("{2 \\over 3}", "+", "{1 \\over 5}")
        expr.scale(1.5)
        h_line = DashedLine(ORIGIN, FRAME_WIDTH * RIGHT).center()

        quantities = Text("Quantities")
        quantities.to_corner(UL, buff=MED_SMALL_BUFF)
        quantities.shift(FRAME_HEIGHT * DOWN / 2)
        numbers = Text("Numbers")
        numbers.to_corner(UL, buff=MED_SMALL_BUFF)

        def get_pie(numer, denom, color=BLUE, height=1.5):
            pie = VGroup(*(
                AnnularSector(
                    angle=TAU / denom,
                    start_angle=i * TAU / denom,
                    inner_radius=0.0,
                    outer_radius=1.0,
                )
                for i in range(denom)
            ))
            pie.set_stroke(WHITE, 2)
            pie.set_fill(BLACK, 1)
            pie[:numer].set_fill(color)
            pie.set_height(height)
            return pie

        pies = VGroup(
            get_pie(2, 3, color=BLUE_C),
            OldTex("+"),
            get_pie(1, 5, color=BLUE_D),
        )
        pies.arrange(RIGHT)
        pies.move_to(FRAME_HEIGHT * DOWN / 4)

        self.add(expr)
        self.wait()
        self.play(
            expr.animate.move_to(FRAME_HEIGHT * UP / 4),
            ShowCreation(h_line),
            Write(numbers),
        )
        self.play(
            *(
                FadeTransform(expr[i].copy(), pies[i])
                for i in range(len(pies))
            ),
            FadeTransform(numbers.copy(), quantities)
        )
        self.wait()

        # Evaluate bottom
        bottom_eq = OldTex("=")
        bottom_eq.move_to(pies[2])
        self.play(
            pies.animate.next_to(bottom_eq, LEFT),
            Write(bottom_eq),
        )

        bottom_rhs = VGroup(
            *pies[0][:2].copy(),
            pies[2][0].copy()
        )
        bottom_rhs.generate_target()
        bottom_rhs.target[2].shift(pies[0].get_center() - pies[2].get_center())
        bottom_rhs.target[2].rotate(TAU * 2 / 3, about_point=pies[0].get_center())
        bottom_rhs.target.next_to(bottom_eq, RIGHT)

        self.play(MoveToTarget(bottom_rhs))
        self.wait()

        # Evaluate top
        rhs = OldTex(
            "=",
            "{10 \\over 15}",
            "+",
            "{3 \\over 15}",
            "=",
            "{13 \\over 15}"
        )
        rhs.match_height(expr)
        rhs.next_to(expr, RIGHT)
        expr.generate_target()
        VGroup(expr.target, rhs).set_x(0)

        self.play(
            MoveToTarget(expr),
            FadeIn(rhs, lag_ratio=0.1)
        )
        self.wait()

        # Show overlays
        overlays = VGroup()
        for pie in (*pies[::2], bottom_rhs):
            overlay = get_pie(0, 15)
            overlay.set_fill(BLACK, 0)
            overlay.set_stroke(WHITE, 1, opacity=0.5)
            overlay.move_to(pie)
            overlays.add(overlay)

        self.play(ShowCreation(overlays))
        self.wait()
