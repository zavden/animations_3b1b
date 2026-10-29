# ==============================================================================
# Scene:      OldTwoKeyProperties
# Source:     videos/_2023/gauss_int/herschel.py (lines 1252-1589)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OldTwoKeyProperties.py OldTwoKeyProperties -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OldTwoKeyProperties(InteractiveScene):
    def construct(self):
        # Setup equations
        kw = dict(
            t2c={"x": BLUE, "y": YELLOW, "{r}": RED, "{c}": PINK}
        )
        one_var = Tex("f_1(x) = e^{-x^2}", **kw)
        two_var = Tex("f_2(x, y) = e^{-(x^2 + y^2)}", **kw)
        factored = Tex("= f_1(x)f_1(y)", **kw)
        factored_exp = Tex("= e^{-x^2} e^{-y^2}", **kw)
        radial_exp = Tex(R"= e^{-{r}^2}", **kw)
        radial = Tex(R"= f_1({r})", **kw)
        radial_full = Tex(R"= f_1(\sqrt{x^2 + y^2})", **kw)

        expressions = VGroup(
            one_var,
            two_var,
            factored_exp,
            factored,
            radial_exp,
            radial,
            radial_full,
        )

        expressions.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        expressions.to_corner(UL)
        expressions.set_backstroke()

        rhs1 = VGroup(factored_exp, factored)
        rhs2 = VGroup(radial_exp, radial, radial_full)
        for rhs in [rhs1, rhs2]:
            rhs.arrange(RIGHT)
            rhs.next_to(two_var, RIGHT)

        for mob in expressions[2:]:
            mob.shift((two_var["="].get_y() - mob["="].get_y()) * UP)

        # From one to two
        self.add(one_var, two_var)
        self.wait()

        rects = VGroup(SurroundingRectangle(one_var), SurroundingRectangle(two_var))
        rects.set_stroke(TEAL, 2)
        rect_words = VGroup(Text("1 variable"), Text("2 variable"))
        for rect, words in zip(rects, rect_words):
            words.next_to(rect, RIGHT)

        arrow = Arrow(
            one_var.get_right(),
            two_var.get_corner(UR) + 0.5 * LEFT,
            path_arc=-PI,
        )
        words = Text("Two interpretations")
        words.next_to(arrow, RIGHT)

        self.play(
            FadeIn(rects[0]),
            FadeIn(rect_words[0]),
        )
        self.wait()
        self.play(
            ReplacementTransform(*rects),
            FadeTransform(*rect_words),
        )
        self.wait()

        two_var_copy = two_var.copy()
        self.play(
            FadeOut(rects[1]),
            FadeOut(rect_words[1]),
            ShowCreation(arrow),
            TransformMatchingTex(one_var.copy(), two_var_copy, run_time=1),
            Write(words, run_time=1)
        )
        self.remove(two_var_copy)
        self.wait()

        # Factored
        self.play(LaggedStart(
            Write(factored_exp["="]),
            TransformFromCopy(one_var["e^{-x^2}"], factored_exp["e^{-x^2}"]),
            TransformFromCopy(one_var["e^{-x^2}"], factored_exp["e^{-y^2}"]),
            run_time=2,
            lag_ratio=0.4,
        ))
        self.wait()
        self.play(LaggedStart(
            Write(factored["="]),
            TransformFromCopy(one_var["f_1(x)"], factored["f_1(x)"], path_arc=PI / 4),
            TransformFromCopy(one_var["f_1(x)"], factored["f_1(y)"], path_arc=PI / 4),
            run_time=3,
            lag_ratio=0.5,
        ))
        self.wait()

        # Rearrange
        rhs1.generate_target()
        rhs1.target.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        rhs1.target.next_to(two_var["="], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        rhs1.target.set_fill(opacity=0.5)
        self.play(MoveToTarget(rhs1, path_arc=-PI / 2))

        # Radial
        self.play(
            Write(radial_exp["="]),
            TransformFromCopy(one_var["e^{-x^2}"], radial_exp["e^{-{r}^2}"]),
        )
        self.wait()
        self.play(
            Write(radial["="]),
            TransformFromCopy(one_var["f_1(x)"], radial["f_1({r})"]),
        )
        self.wait()
        self.play(FadeIn(radial_full, lag_ratio=0.1))
        self.wait()

        # Consolidate
        prop = VGroup(factored, radial)
        prop.generate_target()
        prop.target.arrange(RIGHT)
        prop.target.center().move_to(UP)
        prop.target.set_opacity(1)
        prop.target.scale(1.5)
        prop.target[0]["="].set_opacity(0).scale(0, about_edge=RIGHT)
        prop.target.shift(0.5 * LEFT)

        f2_eq = VGroup(two_var, radial_exp, factored_exp)
        f2_eq.generate_target()
        f2_eq.target.set_fill(opacity=0.5)
        f2_eq.target[-1].next_to(f2_eq.target[-2], RIGHT)
        f2_eq.target.to_corner(UR)

        one_var.generate_target()
        one_var.target.scale(1.5, about_edge=UL)

        self.play(LaggedStart(
            FadeOut(arrow),
            FadeOut(words),
            MoveToTarget(prop),
            MoveToTarget(f2_eq),
            FadeOut(radial_full),
            lag_ratio=0.15,
            run_time=3,
        ))
        self.wait()
        self.play(
            FlashAround(one_var.target, time_width=1.0, run_time=2),
            MoveToTarget(one_var),
        )
        self.wait()
        self.play(FlashUnder(factored[1:]))
        self.wait()
        self.play(FlashUnder(radial))
        self.wait()

        radial_full.set_opacity(1)
        radial_full.scale(1.5)
        radial_full.move_to(radial, LEFT)
        radial_full.shift(0.1 * UP)
        left_shift = 2.0 * LEFT
        radial_full.shift(left_shift)

        self.play(
            FadeIn(radial_full),
            radial.animate.next_to(radial_full, RIGHT),
            factored.animate.shift(left_shift)
        )
        self.wait()

        # Flip the question
        prop = VGroup(factored, radial_full, radial)
        prop.generate_target()
        prop.target.scale(1 / 1.5).to_edge(UP).shift(1.5 * RIGHT)

        question = Text("What are all the functions \n with this property?")
        question.next_to(prop.target, DOWN, buff=1.5)
        question.to_edge(LEFT)
        arrow = Arrow(question, prop.target[0], buff=0.5)

        self.play(
            one_var.animate.scale(1 / 1.5).to_corner(DL).set_opacity(0.5),
            FadeOut(f2_eq, UP),
            MoveToTarget(prop),
        )
        self.play(
            FadeIn(question, lag_ratio=0.1),
            GrowArrow(arrow),
        )
        self.wait()

        # Substitute h
        h_eq = Tex(R"h(x^2) h(y^2) = h(x^2 + y^2)", **kw)
        h_eq.next_to(prop, DOWN, buff=MED_LARGE_BUFF)
        h_eq.shift((prop[1]["="].get_x() - h_eq["="].get_x()) * RIGHT)
        h_def = Tex(R"h(x) = f_1(\sqrt{x})", **kw)
        h_def.to_edge(LEFT).match_y(h_eq)
        h_def2 = Tex(R"h(x^2) = f_1(x)", **kw)
        h_def2.next_to(h_def, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        example_box = Rectangle(4, 4)
        example_box.set_stroke(TEAL, 2)
        example_box.set_fill(TEAL, 0.2)
        example_box.to_corner(DL, buff=0)
        example_word = Text("For example", font_size=30)
        example_word.next_to(example_box.get_top(), DOWN, SMALL_BUFF)
        one_var.generate_target()
        one_var.target.set_opacity(1)
        one_var.target.next_to(example_word, DOWN, MED_LARGE_BUFF)
        one_var.target.to_edge(LEFT)
        h_example = Tex(R"h(x) = e^{-x}", **kw)
        h_example.next_to(one_var.target, DOWN, MED_LARGE_BUFF)
        h_example.to_edge(LEFT)

        self.play(
            FadeOut(question, DOWN),
            FadeOut(arrow, DOWN),
            Write(h_def)
        )
        self.wait()
        self.play(TransformMatchingTex(h_def.copy(), h_def2))
        self.wait()

        self.add(example_box, one_var)
        self.play(
            FadeIn(example_box),
            FadeIn(example_word),
            MoveToTarget(one_var),
        )
        self.wait()
        self.play(FadeIn(h_example, DOWN))
        self.wait()

        self.play(FlashAround(prop[:2], time_width=1, run_time=2))
        self.play(
            TransformFromCopy(factored, h_eq["h(x^2) h(y^2)"][0]),
            TransformFromCopy(radial_full, h_eq["= h(x^2 + y^2)"][0]),
        )
        self.wait()

        # Exponential property
        h_box = SurroundingRectangle(h_eq)
        exp_words = Text("Exponential property!")
        exp_words.next_to(h_box, DOWN)

        sum_box = SurroundingRectangle(h_eq["x^2 + y^2"])
        prod_box = SurroundingRectangle(h_eq["h(x^2) h(y^2)"])
        sum_words = Text("Adding inputs", font_size=30)
        sum_words.next_to(sum_box, DOWN)
        prod_words = Text("Multiplying outputs", font_size=30)
        prod_words.next_to(prod_box, DOWN)

        VGroup(h_box, sum_box, prod_box).set_stroke(TEAL, 2)
        VGroup(exp_words, sum_words, prod_words).set_color(TEAL)

        self.play(
            ShowCreation(sum_box),
            FadeIn(sum_words, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            ReplacementTransform(sum_box, prod_box),
            FadeTransform(sum_words, prod_words),
        )
        self.wait()
        self.play(
            ReplacementTransform(prod_box, h_box),
            FadeTransform(prod_words, exp_words),
        )
        self.wait()

        # Exponent
        implies = Tex(R"\Downarrow", font_size=72)
        implies.next_to(h_eq, DOWN)
        implies.rotate(PI)
        h_exp = Tex(R"h(x) = a \cdot b^x", **kw)
        h_exp.next_to(implies, DOWN)
        h_exp2 = Tex(R"h(x) = a \cdot e^{{c}x}", **kw)
        h_exp2.move_to(h_exp)
        h_exp0 = Tex(R"h(x) = b^x", **kw)
        h_exp0.move_to(h_exp)
        assumption = TexText("Assuming $h$ is continuous", font_size=24)
        assumption.next_to(implies, RIGHT)

        b_rect = SurroundingRectangle(h_exp["b"], buff=SMALL_BUFF)
        b_rect.set_stroke(PINK, 2)
        b_words = Text("Some constant", font_size=30)
        b_words.next_to(b_rect, DOWN, SMALL_BUFF, LEFT)
        b_words.match_color(b_rect)

        self.play(
            FadeTransform(h_box, implies),
            FadeTransform(exp_words, h_exp0),
        )
        self.wait()
        self.play(TransformMatchingTex(h_exp0, h_exp, run_time=1))
        self.wait()
        self.play(
            Rotate(implies, PI),
            FadeIn(assumption, lag_ratio=0.1)
        )
        self.wait()

        self.play(
            ShowCreation(b_rect),
            Write(b_words, run_time=1)
        )
        self.wait()
        c = h_exp2["{c}"][0][0]
        c_copy = c.copy()
        c.set_opacity(0)
        self.play(
            ReplacementTransform(b_rect, c_copy),
            TransformMatchingTex(h_exp, h_exp2),
            FadeOut(b_words, 0.2 * DOWN),
        )
        self.remove(c_copy)
        c.set_opacity(1)
        self.add(h_exp2)
        self.wait()

        # Final form
        implies2 = implies.copy()
        implies2.next_to(h_exp2, DOWN, MED_LARGE_BUFF)
        f_eq = Tex(R"f_1(x) = a \cdot e^{{c}x^2}", **kw)
        f_eq.next_to(implies2, DOWN)
        rect = SurroundingRectangle(f_eq)
        rect.set_stroke(YELLOW, 1)

        self.play(
            TransformMatchingTex(h_exp2.copy(), f_eq),
            Write(implies2, run_time=1)
        )
        self.wait()
        self.play(
            ShowCreation(rect, run_time=2),
            FlashAround(f_eq, time_width=1, run_time=2, stroke_width=5),
        )
        self.wait()
