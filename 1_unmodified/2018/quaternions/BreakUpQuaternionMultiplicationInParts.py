# ==============================================================================
# Scene:      BreakUpQuaternionMultiplicationInParts
# Source:     videos/_2018/quaternions.py (lines 4500-4635)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BreakUpQuaternionMultiplicationInParts.py BreakUpQuaternionMultiplicationInParts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BreakUpQuaternionMultiplicationInParts(Scene):
    def construct(self):
        q1_color = MAROON_B
        q2_color = YELLOW

        product = OldTex(
            "q_1", "\\cdot", "q_2", "=",
            "\\left(", "{q_1", "\\over", "||", "q_1", "||}", "\\right)",
            "||", "q_1", "||", "\\cdot", "q_2",
        )
        product.set_color_by_tex("q_1", q1_color)
        product.set_color_by_tex("q_2", q2_color)
        lhs = product[:3]
        scale_part = product[-5:]
        rotate_part = product[4:-5]
        lhs_rect = SurroundingRectangle(lhs)
        lhs_rect.set_color(YELLOW)
        lhs_words = OldTexText("Quaternion \\\\ multiplication")
        lhs_words.next_to(lhs_rect, UP, LARGE_BUFF)
        scale_brace = Brace(scale_part, UP)
        rotate_brace = Brace(rotate_part, DOWN)
        scale_words = OldTexText("Scale", "$q_2$")
        scale_words.set_color_by_tex("q_2", q2_color)
        scale_words.next_to(scale_brace, UP)
        rotate_words = OldTexText("Apply special \\\\ 4d rotation")
        rotate_words.next_to(rotate_brace, DOWN)

        norm_equation = OldTex(
            "||", "q_1", "||", "=",
            "||", "w_1", "+",
            "x_1", "i", "+",
            "y_1", "j", "+",
            "z_1", "k", "||", "=",
            "\\sqrt",
            "{w_1^2", "+",
            "x_1^2", "+",
            "y_1^2", "+",
            "z_1^2", "}",
        )
        # norm_equation.set_color_by_tex_to_color_map({
        #     "w": YELLOW,
        #     "x": GREEN,
        #     "y": RED,
        #     "z": BLUE,
        # })
        norm_equation.set_color_by_tex("q_1", q1_color)
        norm_equation.to_edge(UP)
        norm_equation.set_background_stroke(width=0)

        line1 = Line(ORIGIN, 0.5 * LEFT + 3 * UP)
        line2 = Line(ORIGIN, UR)
        zero_dot = Dot()
        zero_label = OldTex("0")
        zero_label.next_to(zero_dot, DOWN, SMALL_BUFF)
        q1_dot = Dot(line1.get_end())
        q2_dot = Dot(line2.get_end())
        q1_label = OldTex("q_1").next_to(q1_dot, UP, SMALL_BUFF)
        q2_label = OldTex("q_2").next_to(q2_dot, UR, SMALL_BUFF)
        VGroup(q1_dot, q1_label).set_color(q1_color)
        VGroup(q2_dot, q2_label).set_color(q2_color)
        dot_group = VGroup(
            line1, line2, q1_dot, q2_dot, q1_label, q2_label,
            zero_dot, zero_label,
        )
        dot_group.set_height(3)
        dot_group.center()
        dot_group.to_edge(LEFT)

        q1_dot.add_updater(lambda d: d.move_to(line1.get_end()))
        q1_label.add_updater(lambda l: l.next_to(q1_dot, UP, SMALL_BUFF))
        q2_dot.add_updater(lambda d: d.move_to(line2.get_end()))
        q2_label.add_updater(lambda l: l.next_to(q2_dot, UR, SMALL_BUFF))

        self.add(norm_equation)
        self.wait()
        self.play(
            FadeInFromDown(lhs),
            Write(dot_group),
        )
        self.add(*dot_group)
        self.add(
            VGroup(line2, q2_dot, q2_label).copy().fade(0.5)
        )
        self.play(
            ShowCreation(lhs_rect),
            FadeIn(lhs_words)
        )
        self.play(FadeOut(lhs_rect))
        self.wait()
        self.play(
            TransformFromCopy(lhs, product[3:]),
            # FadeOut(lhs_words)
        )
        self.play(
            GrowFromCenter(scale_brace),
            Write(scale_words),
        )
        self.play(
            line2.scale, 2, {"about_point": line2.get_start()}
        )
        self.wait()
        self.play(
            GrowFromCenter(rotate_brace),
            FadeIn(rotate_words, UP),
        )
        self.play(
            Rotate(
                line2, -line1.get_angle(),
                about_point=line2.get_start(),
                run_time=3
            )
        )
        self.wait()

        # Ask
        randy = Randolph(height=2)
        randy.flip()
        randy.next_to(rotate_words, RIGHT)
        randy.to_edge(DOWN)
        q_marks = OldTex("???")
        random.shuffle(q_marks.submobjects)
        q_marks.next_to(randy, UP)
        self.play(
            FadeIn(randy)
        )
        self.play(
            randy.change, "confused", rotate_words,
            ShowCreationThenFadeAround(rotate_words),
        )
        self.play(LaggedStartMap(
            FadeInFrom, q_marks,
            lambda m: (m, LEFT),
            lag_ratio=0.8,
        ))
        self.play(Blink(randy))
        self.wait(2)
