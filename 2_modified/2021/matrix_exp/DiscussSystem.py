# ==============================================================================
# Scene:      DiscussSystem
# Source:     videos/_2021/matrix_exp.py (lines 1811-1929)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DiscussSystem.py DiscussSystem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(..., thickness=X) -> FillArrow(...): the thickness in the 2021 code is in scene units and the current Arrow multiplies it by 0.015 (invisible arrows).
#   - OldTex/OldTexText with {{ }}: manimgl removed that convention (Apr 2021) and no longer splits the text into parts; the double braces are removed and isolate=[...] is passed with the same pieces.
#   - ThoughtBubble(height=4, width=4) -> OldThoughtBubble(height=4, width=4).body: the current one is no longer a VGroup of 4 pieces (3 circles + cloud) and the scene uses bubble[:3] and bubble[3].
# ==============================================================================

from manim_imports_ext import *

class DiscussSystem(Scene):
    def construct(self):
        # Setup equations
        equations = VGroup(
            # CHANGE: OldTex no longer splits on {{ }} (convention removed from manimgl in Apr 2021); they are removed and isolate=[...] is used with the same pieces
            OldTex("{dx \\over dt} = -y(t)", isolate=["=", "y(t)"]),
            OldTex("{dy \\over dt} = x(t)", isolate=["=", "x(t)"]),
        )
        equations.arrange(RIGHT, buff=LARGE_BUFF)
        equations.to_edge(UP, buff=1.5)

        eq_rect = SurroundingRectangle(equations, stroke_width=2, buff=0.25)
        sys_label = Text("System of differential equations")
        sys_label.next_to(eq_rect, UP)

        self.add(equations)

        self.play(
            FadeIn(sys_label, 0.5 * UP),
            ShowCreation(eq_rect),
        )
        style = {"color": BLUE, "time_width": 3, "run_time": 2}
        self.play(LaggedStart(
            FlashAround(sys_label.get_part_by_text("differential"), **style),
            FlashAround(equations[0].get_part_by_tex("dx"), **style),
            FlashAround(equations[1].get_part_by_tex("dy"), **style),
        ))
        self.wait()

        # Ask for explicit solutions
        solutions = VGroup(
            # CHANGE: OldTex no longer splits on {{ }} (convention removed from manimgl in Apr 2021); they are removed and isolate=[...] is used with the same pieces
            OldTex("x(t) = (\\text{expression with } t)", isolate=["="]),
            OldTex("y(t) = (\\text{expression with } t)", isolate=["="]),
        )
        for solution in solutions:
            solution.set_color_by_tex("expression", GREY_B)
        solutions.arrange(DOWN, buff=0.5)
        solutions.move_to(equations)
        solutions.set_x(3)

        self.play(
            sys_label.animate.match_width(eq_rect).to_edge(LEFT),
            VGroup(equations, eq_rect).animate.to_edge(LEFT),
            LaggedStartMap(FadeIn, solutions, shift=0.5 * UP, lag_ratio=0.3),
        )
        self.wait()

        # Show a guess
        guess_rhss = VGroup(
            OldTex("\\cos(t)", color=GREY_B)[0],
            OldTex("\\sin(t)", color=GREY_B)[0],
        )
        temp_rhss = VGroup()
        for rhs, solution in zip(guess_rhss, solutions):
            temp_rhss.add(solution[2])
            rhs.move_to(solution[2], LEFT)

        # CHANGE: the current ThoughtBubble is no longer a VGroup of 4 pieces (3 circles + cloud) indexed as bubble[3]; the OldThoughtBubble
        # CHANGE: (SVG) it is one, but inside .body
        bubble = OldThoughtBubble(height=4, width=4).body
        bubble.flip()
        bubble.set_fill(opacity=0)
        bubble[:3].rotate(30 * DEGREES, about_point=bubble[3].get_center() + 0.2 * RIGHT)
        bubble.shift(solutions.get_left() + 0.7 * LEFT - bubble[3].get_left())

        self.remove(temp_rhss)
        self.play(
            ShowCreation(bubble),
            *(
                TransformMatchingShapes(temp_rhs.copy(), guess_rhs)
                for temp_rhs, guess_rhs in zip(temp_rhss, guess_rhss)
            ),
        )
        self.wait()

        # Not enough!
        not_enough = Text("Not enough!", font_size=40)
        not_enough.next_to(bubble[3].get_corner(UR), DR)
        not_enough.set_color(RED)

        self.play(LaggedStartMap(FadeIn, not_enough, run_time=1, lag_ratio=0.1))
        self.wait()
        self.remove(guess_rhss)
        self.play(
            LaggedStartMap(FadeOut, VGroup(*bubble, *not_enough)),
            *(
                TransformMatchingShapes(guess_rhs.copy(), temp_rhs)
                for temp_rhs, guess_rhs in zip(temp_rhss, guess_rhss)
            ),
        )

        # Initial condition
        solutions.generate_target()
        initial_conditions = VGroup(
            OldTex("x(0) = x_0"),
            OldTex("y(0) = y_0"),
        )
        full_requirement = VGroup(*solutions.target, *initial_conditions)
        full_requirement.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        full_requirement.scale(0.8)
        full_requirement.move_to(solutions)
        full_requirement.to_edge(UP)

        self.play(
            MoveToTarget(solutions),
            LaggedStartMap(FadeIn, initial_conditions, shift=0.1 * UP, lag_ratio=0.3),
        )
        self.wait()

        ic_label = Text("Initial condition", font_size=30)
        ic_label.set_color(BLUE)
        ic_label.next_to(initial_conditions, RIGHT, buff=1.0)
        ic_arrows = VGroup(*(
            # CHANGE: Arrow(thickness=...) -> FillArrow: thickness in scene units (the current Arrow multiplies it by 0.015)
            FillArrow(ic_label.get_left(), eq.get_right(), buff=0.1, fill_color=BLUE, thickness=0.025)
            for eq in initial_conditions
        ))

        self.play(
            FadeIn(ic_label),
            LaggedStartMap(GrowArrow, ic_arrows, run_time=1)
        )
        self.wait()
