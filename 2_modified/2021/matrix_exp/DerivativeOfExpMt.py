# ==============================================================================
# Scene:      DerivativeOfExpMt
# Source:     videos/_2021/matrix_exp.py (lines 5632-5861)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DerivativeOfExpMt.py DerivativeOfExpMt -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes: TransformMatchingTex requires a current Tex (get_symbol_substrings) and here the source/target are parts of OldTex.
# ==============================================================================

from manim_imports_ext import *

class DerivativeOfExpMt(Scene):
    def construct(self):
        # For all tex
        v0_tex = "\\vec{\\textbf{v} }_0"
        kw = {
            "tex_to_color_map": {
                "M": GREY_B,
                "{t}": YELLOW,
                v0_tex: BLUE,
                "=": WHITE,
                "\\cdots": WHITE,
                "+": WHITE,
                "\\left(": WHITE,
                "\\right)": WHITE,
            }
        }

        # Show claim
        solution = OldTex("\\vec{\\textbf{v} }({t}) = e^{M {t} } " + v0_tex, **kw)
        equation = OldTex("{d \\over dt} \\vec{\\textbf{v} }({t}) = M \\vec{\\textbf{v} }({t})", **kw)
        arrow = Vector(1.5 * RIGHT)
        top_line = VGroup(solution, arrow, equation)
        top_line.arrange(RIGHT, buff=MED_LARGE_BUFF)
        top_line.set_width(FRAME_WIDTH - 1)

        solves = Text("Solves(?)", font_size=24)
        solves.next_to(arrow, UP, SMALL_BUFF)

        self.add(solution)
        self.play(
            GrowArrow(arrow),
            FadeIn(equation, RIGHT),
            FadeIn(solves, lag_ratio=0.1)
        )
        self.wait()

        arrow.add(solves)

        # Try it...

        # Show calculations...
        tex_expressions = [
            """
            e^{ {t}M } v_0 =
            \\left( {t}^0 M^0 +
            {t}^1 M^1 +
            { {t}^2 \\over 2} M^2 +
            { {t}^3 \\over 6} M^3 +
            \\cdots +
            { {t}^n \\over n!} M^n +
            \\cdots
            \\right) v_0
            """,
            """
            e^{ {t}M } v_0 =
            {t}^0 M^0 v_0 +
            {t}^1 M^1 v_0 +
            { {t}^2 \\over 2} M^2 v_0 +
            { {t}^3 \\over 6} M^3 v_0 +
            \\cdots +
            { {t}^n \\over n!} M^n v_0 +
            \\cdots
            """,
            """
            {d \\over dt}
            e^{ {t}M } v_0 =
            0 +
            1 \\cdot {t}^0 M^1 v_0 +
            {2 {t}^1 \\over 2} M^2 v_0 +
            {3 {t}^2 \\over 6} M^3 v_0 +
            \\cdots +
            {n {t}^{n - 1} \\over n!} M^n v_0 +
            \\cdots
            """,
            """
            {d \\over dt}
            e^{ {t}M } v_0 =
            0 +
            1 \\cdot {t}^0 M^1 v_0 +
            {t}^1 M^2 v_0 +
            { {t}^2 \\over 2} M^3 v_0 +
            \\cdots +
            { {t}^{n - 1} \\over (n - 1)!} M^n v_0 +
            \\cdots
            """,
            """
            {d \\over dt}
            e^{ {t}M } v_0 =
            M \\left(
            {t}^0 M^0 v_0 +
            {t}^1 M^1 v_0 +
            { {t}^2 \\over 2} M^2 v_0 +
            \\cdots +
            { {t}^{n - 1} \\over (n - 1)!} M^{n - 1} v_0 +
            \\cdots
            \\right)
            """,
            """
            {d \\over dt}
            e^{ {t}M } v_0 =
            M \\left( e^{ {t}M } v_0  \\right)
            """
        ]

        lines = VGroup(*(
            OldTex(tex.replace("v_0", v0_tex), **kw)
            for tex in tex_expressions
        ))
        lines.set_width(FRAME_WIDTH - 1)
        max_height = 1.0
        for line in lines:
            line.set_width(FRAME_WIDTH - 2)
            if line.get_height() > max_height:
                line.set_height(max_height)
            line.center()

        def match_lines(l1, l2):
            eq_centers = [eq.get_part_by_tex("=").get_center() for eq in (l1, l2)]
            l1.shift(eq_centers[1] - eq_centers[0])

        # Line 0
        self.play(top_line.animate.set_width(6).to_edge(UP))
        lines[0].set_y(1)
        # CHANGE: TransformMatchingTex requires a current Tex (get_symbol_substrings) and OldTex gives VGroup/parts; TransformMatchingShapes is used
        self.play(TransformMatchingShapes(solution[4:].copy(), lines[0]), run_time=2)
        self.wait()

        # 0 -> 1
        match_lines(lines[1], lines[0])
        lines[1].set_y(-1)
        self.play(
            TransformMatchingShapes(
                VGroup(*(
                    sm
                    for sm in lines[0][5:]
                    if sm.get_tex() not in ["\\left(", "\\right)"]
                )).copy(),
                lines[1][5:]
            ),
            TransformFromCopy(lines[0][:5], lines[1][:5])
        )
        self.play(
            lines[1].animate.set_y(1),
            FadeOut(lines[0], UP)
        )
        self.wait()

        # 1 -> 2 -> 3
        match_lines(lines[2], lines[1])
        match_lines(lines[3], lines[2])
        lines[2:4].set_y(-1)
        self.play(FadeIn(lines[2], DOWN))

        l1_indices, l2_indices, l3_indices = [
            [
                lines[i].index_of_part(part)
                for part in it.chain(lines[i].get_parts_by_tex("="), lines[i].get_parts_by_tex("+"))
            ]
            for i in (1, 2, 3)
        ]

        last_rects = VMobject()
        for l1i, l1j, l2i, l2j in zip(l1_indices, l1_indices[1:], l2_indices, l2_indices[1:]):
            if l1i is l1_indices[4]:
                continue
            r1 = SurroundingRectangle(lines[1][l1i + 1:l1j])
            r2 = SurroundingRectangle(lines[2][l2i + 1:l2j])
            rects = VGroup(r1, r2)
            self.play(FadeIn(rects), FadeOut(last_rects))
            self.wait(0.5)
            last_rects = rects
        self.play(FadeOut(last_rects))
        self.play(
            lines[2].animate.set_y(1),
            FadeOut(lines[1]),
            FadeIn(lines[3]),
        )
        self.wait()

        last_rects = VMobject()
        for l2i, l2j, l3i, l3j in zip(l2_indices, l2_indices[1:], l3_indices, l3_indices[1:]):
            # Such terrible style...please no on look
            if l2i in [l2_indices[0], l2_indices[1], l2_indices[4]]:
                continue
            r2 = SurroundingRectangle(lines[2][l2i + 1:l2j])
            r3 = SurroundingRectangle(lines[3][l3i + 1:l3j])
            rects = VGroup(r2, r3)
            self.play(FadeIn(rects), FadeOut(last_rects))
            self.wait(0.5)
            last_rects = rects
        self.play(FadeOut(last_rects))
        self.wait()

        # 3 -> 4
        match_lines(lines[4], lines[3])
        lines[4].set_y(-1)

        self.play(
            FadeIn(lines[1], DOWN),
            FadeOut(lines[2], DOWN)
        )
        self.wait()
        self.play(LaggedStart(*(
            FlashUnder(sm, time_width=2, run_time=1)
            for sm in lines[3].get_parts_by_tex("M")[1:]
        ), lag_ratio=0.2))
        self.wait()

        self.play(
            TransformMatchingShapes(lines[3][:5], lines[4][:5]),
            FadeTransform(lines[3][5:], lines[4][7:34]),
            FadeIn(lines[4].get_part_by_tex("\\left(")),
            FadeIn(lines[4].get_part_by_tex("\\right)")),
            TransformFromCopy(
                lines[3].get_parts_by_tex("M")[1:],
                VGroup(lines[4][5]),
                path_arc=-45 * DEGREES,
            )
        )
        self.wait()

        # 4 -> 5
        match_lines(lines[5], lines[4])
        lines[5].set_y(-3)

        self.play(
            TransformFromCopy(lines[4][:7], lines[5][:7]),
            TransformFromCopy(lines[4][34], lines[5][11]),
            FadeTransform(lines[4][7:34].copy(), lines[5][7:11], stretch=False),
        )
        self.wait()
