# ==============================================================================
# Scene:      ExpectedValueComputation
# Source:     videos/_2019/hyperdarts.py (lines 1601-1782)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpectedValueComputation.py ExpectedValueComputation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpectedValueComputation(Scene):
    def construct(self):
        t2c = {
            "0": MAROON_C,
            "1": BLUE,
            "2": GREEN,
            "3": YELLOW,
            "4": RED,
        }

        line1 = OldTex(
            "E[S]", "=",
            "1 \\cdot", "P(S = 1)", "+",
            "2 \\cdot", "P(S = 2)", "+",
            "3 \\cdot", "P(S = 3)", "+",
            "\\cdots",
            tex_to_color_map=t2c
        )
        line2 = OldTex(
            "=&\\phantom{-}",
            "1 \\cdot", "\\big(", "P(S > 0)", "-", "P(S > 1)", "\\big)", "\\\\&+",
            "2 \\cdot", "\\big(", "P(S > 1)", "-", "P(S > 2)", "\\big)", "\\\\&+",
            "3 \\cdot", "\\big(", "P(S > 2)", "-", "P(S > 3)", "\\big)", "\\\\&+",
            "\\cdots",
            tex_to_color_map=t2c
        )
        line2[1:12].align_to(line2[13], LEFT)
        line3 = OldTex(
            "=",
            "P(S > 0)", "+",
            "P(S > 1)", "+",
            "P(S > 2)", "+",
            "P(S > 3)", "+",
            "\\cdots",
            tex_to_color_map=t2c,
        )

        line1.to_corner(UL)
        line2.next_to(line1, DOWN, buff=MED_LARGE_BUFF)
        line2.align_to(line1[1], LEFT)
        line3.next_to(line2, DOWN, buff=MED_LARGE_BUFF)
        line3.align_to(line1[1], LEFT)

        # Write line 1
        self.add(line1[:2])
        self.play(Write(line1[2:7]))
        self.wait()
        self.play(FadeIn(line1[7]))
        self.play(Write(line1[8:13]))
        self.wait()
        self.play(FadeIn(line1[13]))
        self.play(Write(line1[14:19]))
        self.wait()
        self.play(Write(line1[19:]))
        self.wait()

        # line 2 scaffold
        kw = {
            "path_arc": 90 * DEGREES
        }
        bigs = line2.get_parts_by_tex("big")
        self.play(
            LaggedStart(
                TransformFromCopy(
                    line1.get_part_by_tex("="),
                    line2.get_part_by_tex("="),
                    **kw
                ),
                TransformFromCopy(
                    line1.get_parts_by_tex("\\cdot"),
                    line2.get_parts_by_tex("\\cdot"),
                    **kw
                ),
                TransformFromCopy(
                    line1.get_parts_by_tex("+"),
                    line2.get_parts_by_tex("+"),
                    **kw
                ),
                TransformFromCopy(
                    line1.get_part_by_tex("1"),
                    line2.get_part_by_tex("1"),
                    **kw
                ),
                TransformFromCopy(
                    line1.get_part_by_tex("2"),
                    line2.get_part_by_tex("2"),
                    **kw
                ),
                TransformFromCopy(
                    line1.get_part_by_tex("3"),
                    line2.get_part_by_tex("3"),
                    **kw
                ),
                run_time=3,
                lag_ratio=0,
            ),
            LaggedStart(*[
                GrowFromCenter(bigs[i:i + 2])
                for i in range(0, len(bigs), 2)
            ])
        )
        self.wait()

        # Expand out sum
        for n in range(3):
            i = 6 * n
            j = 12 * n

            rect1 = SurroundingRectangle(line1[i + 4:i + 7])
            rect2 = SurroundingRectangle(line2[j + 4:j + 11])
            color = line1[i + 5].get_color()
            VGroup(rect1, rect2).set_stroke(color, 2)

            self.play(ShowCreation(rect1))
            self.play(
                TransformFromCopy(
                    line1[i + 4:i + 7],
                    line2[j + 4:j + 7],
                ),
                TransformFromCopy(
                    line1[i + 4:i + 7],
                    line2[j + 8:j + 11],
                ),
                FadeIn(line2[j + 7]),
                ReplacementTransform(rect1, rect2),
            )
            self.play(FadeOut(rect2))

        # Show telescoping
        line2.generate_target()
        line2.target.set_opacity(0.2)
        line2.target[4:7].set_opacity(1)

        self.play(MoveToTarget(line2))
        self.wait()
        self.play(
            TransformFromCopy(line2[0], line3[0]),
            TransformFromCopy(line2[4:7], line3[1:4]),
        )
        self.wait()

        line2.target.set_opacity(0.2)
        VGroup(
            line2.target[1:4],
            line2.target[7:12],
            line2.target[12:19],
            line2.target[23],
        ).set_opacity(1)

        self.play(MoveToTarget(line2))
        self.wait()
        self.play(
            TransformFromCopy(line2[12], line3[4]),
            TransformFromCopy(line2[16:19], line3[5:8]),
        )
        self.wait()

        n = 12
        line2.target.set_opacity(0.2)
        VGroup(
            line2.target[n + 1:n + 4],
            line2.target[n + 7:n + 12],
            line2.target[n + 12:n + 19],
            line2.target[n + 23],
        ).set_opacity(1)

        self.play(MoveToTarget(line2))
        self.wait()
        self.play(
            TransformFromCopy(line2[n + 12], line3[8]),
            TransformFromCopy(line2[n + 16:n + 19], line3[9:12]),
        )
        self.wait()
        self.play(Write(line3[12:]))
        self.wait()

        rect = SurroundingRectangle(line3, buff=MED_SMALL_BUFF)
        rect.set_stroke(WHITE, 2)
        self.play(ShowCreation(rect))
        self.wait()

        self.wait(3)
