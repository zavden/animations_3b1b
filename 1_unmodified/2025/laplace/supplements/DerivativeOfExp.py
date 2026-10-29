# ==============================================================================
# Scene:      DerivativeOfExp
# Source:     videos/_2025/laplace/supplements.py (lines 372-435)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DerivativeOfExp.py DerivativeOfExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DerivativeOfExp(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        tex_kw = dict(t2c={"t": GREY_B, "s": YELLOW})
        equation = Tex(R"\frac{d}{dt} e^{st} = s \cdot e^{st}", font_size=90, **tex_kw)
        deriv_part = equation[R"\frac{d}{dt}"][0]
        exp_parts = equation[R"e^{st}"]
        equals = equation[R"="][0]
        s_dot = equation[R"s \cdot"][0]

        v_box = SurroundingRectangle(VGroup(deriv_part, exp_parts[0]))
        p_box = SurroundingRectangle(exp_parts[1])
        s_box = SurroundingRectangle(s_dot)
        s_box.match_height(p_box, stretch=True).match_y(p_box)
        boxes = VGroup(v_box, p_box, s_box)
        boxes.set_stroke(width=2)
        boxes.set_submobject_colors_by_gradient(GREEN, BLUE, YELLOW)

        v_label = Text("Velocity", font_size=48).match_color(v_box)
        p_label = Text("Position", font_size=48).match_color(p_box)
        s_label = Text("Modifier", font_size=48).match_color(s_box)
        v_label.next_to(v_box, UP, MED_SMALL_BUFF)
        p_label.next_to(p_box, UP, MED_SMALL_BUFF, aligned_edge=LEFT)
        s_label.next_to(s_box, DOWN, MED_SMALL_BUFF)
        labels = VGroup(v_label, p_label, s_label)

        frame.move_to(exp_parts[0])

        self.add(exp_parts[0])
        self.wait()
        self.play(Write(deriv_part))
        self.play(
            TransformFromCopy(*exp_parts, path_arc=90 * DEG),
            Write(equals),
            frame.animate.center(),
        )
        self.play(
            TransformFromCopy(exp_parts[1][1], s_dot[0], path_arc=90 * DEG),
            Write(s_dot[1]),
        )
        self.wait()

        # Show labels
        for box, label in zip(boxes, labels):
            self.play(ShowCreation(box), FadeIn(label))

        self.wait()
        full_group = VGroup(equation, boxes, labels)

        # Set s equal to 1
        s_eq_1 = Tex(R"s = 1", font_size=72, **tex_kw)
        simple_equation = Tex(R"\frac{d}{dt} e^{t} = e^{t}", font_size=72, **tex_kw)
        simple_equation.to_edge(UP).shift(2 * LEFT)
        s_eq_1.next_to(simple_equation, RIGHT, buff=2.5)
        arrow = Arrow(s_eq_1, simple_equation, thickness=5, buff=0.35).shift(0.05 * DOWN)

        self.play(
            Write(s_eq_1),
            GrowArrow(arrow),
            TransformMatchingTex(equation.copy(), simple_equation, run_time=1.5, lag_ratio=0.02),
            full_group.animate.shift(DOWN).scale(0.75).fade(0.15)
        )
        self.wait()
