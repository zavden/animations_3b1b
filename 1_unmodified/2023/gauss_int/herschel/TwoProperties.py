# ==============================================================================
# Scene:      TwoProperties
# Source:     videos/_2023/gauss_int/herschel.py (lines 500-1088)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoProperties.py TwoProperties -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TwoProperties(InteractiveScene):
    def construct(self):
        # Name properties
        properties = VGroup(
            VGroup(
                Text("Property 1"),
                TexText(R"""
                    The probability (density) depends \\
                    only on the distance from the origin
                """, alignment="", font_size=36, color=GREY_A),
            ),
            VGroup(
                Text("Property 2"),
                TexText(R"""
                    The $x$ and $y$ coordinates are \\
                    independent from each other.
                """, alignment="", font_size=36, color=GREY_A),
            ),
        )
        for prop in properties:
            prop.arrange(DOWN, aligned_edge=LEFT)
        properties.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        properties.to_corner(UL)

        prop_boxes = VGroup(*(
            SurroundingRectangle(prop[1]).set_fill(GREY_E, 1).set_stroke(RED, 1, 0.5)
            for prop in properties
        ))

        for prop, box in zip(properties, prop_boxes):
            self.play(FadeIn(prop[0], lag_ratio=0.1), FadeIn(box))

        # Formula
        implies = Tex(R"\Downarrow", font_size=72)
        implies.next_to(properties, DOWN, MED_LARGE_BUFF)

        kw = dict(
            t2c={"x": BLUE, "y": YELLOW, R"\sigma": RED, "{r}": RED}
        )
        form1, form2, form3 = forms = VGroup(
            Tex(R"f_2(x, y) = e^{-(x^2 + y^2)}", **kw),
            Tex(R"f_2(x, y) = e^{-(x^2 + y^2) / 2 \sigma^2}", **kw),
            Tex(R"f_2(x, y) = {1 \over 4 \sigma^2 \pi} e^{-(x^2 + y^2) / 2 \sigma^2}", **kw),
        )
        forms.next_to(implies, DOWN, MED_SMALL_BUFF)

        form1.save_state()
        self.play(
            Write(implies),
            FadeIn(form1, DOWN)
        )
        self.wait()
        self.play(TransformMatchingTex(form1, form2, run_time=1, lag_ratio=0.05))
        self.wait(2)
        self.play(TransformMatchingTex(form2, form3, run_time=1, lag_ratio=0.05))
        self.wait(2)
        form1.restore()
        self.play(TransformMatchingTex(form3, form1, run_time=2, lag_ratio=0.05))
        self.wait(2)

        # Property 1
        lhs = form1["f_2(x, y)"][0]

        self.add(properties[0][1], prop_boxes[0])
        self.play(
            prop_boxes[0].animate.stretch(0, 0, about_edge=RIGHT).set_opacity(0),
            FadeOut(implies),
            FadeOut(form1["= e^{-(x^2 + y^2)}"]),
        )
        self.remove(prop_boxes[0])
        self.add(lhs)
        self.wait()
        phrase = properties[0][1]["only on the distance"]
        self.play(
            FlashUnder(phrase, color=TEAL, buff=0),
            phrase.animate.set_color(TEAL),
        )
        self.wait(2)

        # Function of radius
        lhs.generate_target()
        lhs.target.to_edge(LEFT)
        radial_rhs = Tex(R"= f({r})", **kw)
        full_radial_rhs = Tex(R"= f(\sqrt{x^2 + y^2})", **kw)
        radial_rhs.next_to(lhs.target, RIGHT, SMALL_BUFF)
        full_radial_rhs.next_to(radial_rhs, RIGHT, MED_SMALL_BUFF)
        full_radial_rhs.shift((radial_rhs["="].get_y() - full_radial_rhs["="].get_y()) * UP)

        lhs_rect = SurroundingRectangle(lhs)
        f_rect = SurroundingRectangle(radial_rhs["f"], buff=0.05)
        f_rect.set_stroke(BLUE, 2)
        f_words = Text("Some single-variable function", font_size=36)
        f_words.next_to(f_rect, UP, SMALL_BUFF, aligned_edge=LEFT)
        f_words.match_color(f_rect)

        self.play(ShowCreation(lhs_rect))
        self.wait()
        self.play(lhs_rect.animate.replace(lhs[1], stretch=True).set_stroke(width=1).scale(1.1))
        self.play(FadeOut(lhs_rect))
        self.wait()
        self.play(
            MoveToTarget(lhs),
            Write(radial_rhs),
        )
        self.play(
            ShowCreation(f_rect),
            FadeIn(f_words, lag_ratio=0.1)
        )
        self.wait(2)
        self.play(FadeOut(f_words), FadeOut(f_rect))
        self.play(TransformMatchingTex(radial_rhs.copy(), full_radial_rhs))
        self.wait(2)

        # Property 2
        self.add(properties[1][1], prop_boxes[1])
        self.play(
            prop_boxes[1].animate.stretch(0, 0, about_edge=RIGHT).set_opacity(0),
        )
        self.remove(prop_boxes[0])
        self.wait()

        phrase = properties[1][1]["independent"]
        self.play(
            FlashUnder(phrase, color=TEAL, buff=0),
            phrase.animate.set_color(TEAL)
        )
        self.wait()

        # Factored expression
        lhs.generate_target()
        lhs.target.next_to(properties, DOWN, buff=0.7, aligned_edge=LEFT)
        radial_rhss = VGroup(radial_rhs, full_radial_rhs)

        factored_rhs = Tex(R"= g(x) h(y)", **kw)
        simpler_rhs = Tex(R"= g(x) g(y)", **kw)
        for rhs in factored_rhs, simpler_rhs:
            rhs.next_to(lhs.target, RIGHT)

        g_box = SurroundingRectangle(factored_rhs["g(x)"], buff=0.05).set_stroke(BLUE, 2)
        h_box = SurroundingRectangle(factored_rhs["h(y)"], buff=0.05).set_stroke(YELLOW, 2)
        g_words = TexText("Distribution of $x$", font_size=30).next_to(g_box, DOWN, 0.2)
        h_words = TexText("Distribution of $y$", font_size=30).next_to(h_box, DOWN, 0.2)

        self.play(
            MoveToTarget(lhs),
            radial_rhss.animate.to_edge(LEFT).shift(0.5 * DOWN).set_opacity(0.35),
        )
        self.play(
            TransformMatchingShapes(lhs.copy(), factored_rhs)
        )
        self.wait()
        self.play(
            ShowCreation(g_box),
            FadeIn(g_words)
        )
        self.wait()
        self.play(
            ReplacementTransform(g_box, h_box),
            ReplacementTransform(g_words, h_words),
        )
        self.wait()
        self.play(FadeOut(h_box), FadeOut(h_words))
        self.wait()
        self.play(
            FadeOut(factored_rhs["h(y)"], 0.5 * UP),
            FadeIn(simpler_rhs["g(y)"], 0.5 * UP),
        )
        self.wait()
        self.remove(factored_rhs)
        self.add(simpler_rhs)

        # Show proportionality
        arrow = Arrow(simpler_rhs, radial_rhs)
        self.play(
            GrowArrow(arrow),
            radial_rhs.animate.set_opacity(1),
            FadeOut(full_radial_rhs),
        )
        self.wait()
        radial_rhs.generate_target()
        radial_rhs.target.next_to(lhs, RIGHT),
        self.play(
            MoveToTarget(radial_rhs),
            simpler_rhs.animate.next_to(radial_rhs.target, RIGHT),
            Uncreate(arrow),
        )
        self.wait()

        xs = VGroup(lhs[3], simpler_rhs["x"][0][0])
        ys = VGroup(lhs[5], simpler_rhs["y"][0][0])
        rs = Tex("{r}", **kw).replicate(2)
        zeros = Tex("0", **kw).replicate(2)
        zeros.set_color(YELLOW)
        for x, r in zip(xs, rs):
            r.move_to(x, DOWN)
        for x, y, zero in zip(xs, ys, zeros):
            zero.move_to(y)
            zero.align_to(x, DOWN)

        const_rect = SurroundingRectangle(simpler_rhs["g(y)"], buff=0.05)
        const_rect.set_stroke(YELLOW, 1)
        const_words = Text("Some constant", font_size=36)
        const_words.match_color(const_rect)
        const_words.next_to(const_rect, DOWN)

        self.play(
            LaggedStartMap(FadeOut, VGroup(*xs, *ys), shift=0.5 * UP),
            LaggedStartMap(FadeIn, VGroup(*rs, *zeros), shift=0.5 * UP),
        )
        self.wait()
        self.play(
            ShowCreation(const_rect),
            FadeIn(const_words)
        )
        self.wait()

        # Assume this constant is 1
        assumption = TexText("Assume this is 1", font_size=36)
        assumption.move_to(const_words)
        assumption.match_color(const_words)

        f_eq_g = Tex("f = g", **kw)
        f_eq_g.next_to(radial_rhs, DOWN, LARGE_BUFF)

        f_rhs = Tex(R"= f(x)f(y)", **kw)
        f_rhs.move_to(simpler_rhs, LEFT)
        gs = simpler_rhs["g"]
        fs = f_rhs["f"]

        self.play(
            FadeIn(assumption, 0.5 * DOWN),
            FadeOut(const_words, 0.5 * DOWN),
        )
        self.wait()

        self.play(
            TransformFromCopy(
                VGroup(radial_rhs[1], *simpler_rhs[:2]),
                f_eq_g
            )
        )
        self.wait()

        self.play(
            LaggedStartMap(FadeIn, VGroup(*xs, *ys), shift=0.5 * DOWN),
            LaggedStartMap(FadeOut, VGroup(*rs, *zeros), shift=0.5 * DOWN),
            FadeOut(const_rect),
            FadeOut(assumption),
        )
        self.wait()
        self.play(
            TransformMatchingShapes(f_eq_g[0].copy(), fs),
            ReplacementTransform(simpler_rhs, f_rhs),
        )
        self.wait()

        # Highlight key equation
        key_equation = VGroup(*radial_rhs[1:], *f_rhs)

        self.play(
            key_equation.animate.set_x(0.25 * FRAME_WIDTH).to_edge(UP),
            FadeOut(f_eq_g),
            FadeOut(lhs),
            FadeOut(radial_rhs[0]),
        )
        self.play(FlashAround(key_equation, time_width=1, run_time=2))

        full_radial_rhs.set_opacity(1)
        full_radial_rhs.move_to(key_equation).shift(LEFT)

        self.play(
            GrowFromCenter(full_radial_rhs, lag_ratio=0.02),
            radial_rhs[1:].animate.next_to(full_radial_rhs, LEFT, aligned_edge=DOWN),
            key_equation[4:].animate.next_to(full_radial_rhs, RIGHT),
        )
        self.wait()

        # Name as a functional equation
        func_eq_name = Text("Functional\nequation")
        func_eq_name.to_corner(UL)
        func_eq_name.match_y(key_equation)
        arrow = Arrow(func_eq_name, radial_rhs[1].get_left(), buff=0.25)
        func_eq_name.to_edge(UP)

        self.play(LaggedStartMap(FadeOut, properties, shift=LEFT, lag_ratio=0.2))
        self.play(
            Write(func_eq_name),
            GrowArrow(arrow)
        )
        self.wait()

        # Example
        example_box = Rectangle(4, 3)
        example_box.set_stroke(TEAL, 2)
        example_box.set_fill(TEAL, 0.35)
        example_box.to_corner(DL, buff=0)
        example_word = Text("For example", font_size=30)
        example_word.next_to(example_box.get_top(), DOWN, SMALL_BUFF)
        example_f = Tex(R"f({r}) = e^{-{r}^2}", **kw)
        example_f.scale(0.75)
        example_f.next_to(example_word, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(example_box),
            FadeIn(example_word, 0.5 * DOWN)
        )
        self.play(
            TransformFromCopy(key_equation[:4], example_f[:4]),
            GrowFromPoint(example_f[4:], key_equation.get_left()),
        )
        self.wait()

        # Define h
        let = Text("Let")
        h_def = Tex(R"h({x}) = f(\sqrt{{x}})", **kw)
        h_def.next_to(key_equation, DOWN, LARGE_BUFF)
        let.next_to(h_def, LEFT, MED_LARGE_BUFF)
        h_def2 = Tex(R"h({x}^2) = f({x})", **kw)
        h_def2.next_to(h_def["h"], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        h_eq = Tex(R"h(x^2 + y^2) = h(x^2) h(y^2)", **kw)
        h_eq.to_corner(UR)
        h_eq.to_edge(RIGHT, buff=1.25)

        example_h = Tex(R"h({r}) = e^{-{r}}", **kw)
        example_h.scale(0.75)
        example_h.next_to(example_f, DOWN, MED_LARGE_BUFF)

        self.play(FadeIn(h_def, DOWN), Write(let))
        self.wait()
        self.play(TransformMatchingTex(
            h_def.copy(), h_def2,
            key_map={R"\sqrt": "^2"},
            run_time=1
        ))
        self.wait()
        self.play(
            TransformFromCopy(h_def, example_h)
        )
        self.wait(2)

        self.play(
            VGroup(key_equation, full_radial_rhs).animate.scale(0.8).to_edge(LEFT),
            VGroup(let, h_def, h_def2).animate.scale(0.8).to_edge(LEFT),
            FadeOut(func_eq_name, LEFT),
            Uncreate(arrow),
        )
        self.play(
            TransformMatchingShapes(
                VGroup(*full_radial_rhs[1:], *f_rhs).copy(),
                h_eq
            )
        )
        self.wait()

        # Exponential property
        sum_box = SurroundingRectangle(h_eq["x^2 + y^2"])
        prod_box = SurroundingRectangle(h_eq["h(x^2) h(y^2)"])
        sum_words = Text("Adding inputs", font_size=30)
        sum_words.next_to(sum_box, DOWN)
        prod_words = Text("Multiplying outputs", font_size=30)
        prod_words.next_to(prod_box, DOWN)

        VGroup(sum_box, prod_box).set_stroke(TEAL, 2)
        VGroup(sum_words, prod_words).set_color(TEAL)

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
        self.play(FadeOut(prod_box), FadeOut(prod_words))
        self.wait()

        # Multi-input property
        implies = Tex(R"\Downarrow", font_size=72)
        implies.next_to(h_eq, DOWN)
        full_h_eq = Tex(R"h(x_1 + x_2 + \cdots + x_n) = h(x_1)h(x_2) \cdots h(x_n)")
        for s, color in zip(["1", "2", "n"], color_gradient([BLUE, YELLOW], 3)):
            full_h_eq[f"x_{s}"].set_color(color)
        full_h_eq.scale(0.75)
        full_h_eq.next_to(implies, DOWN)

        self.play(
            Write(implies),
            FadeIn(full_h_eq, DOWN),
        )
        self.wait()

        # Whole numbers
        implies2 = implies.copy()
        implies2.next_to(full_h_eq, DOWN, buff=MED_LARGE_BUFF)

        five_eq = Tex(R"h(5) &= h(1 + 1 + 1 + 1 + 1) \\ &= h(1)h(1)h(1)h(1)h(1) = h(1)^5")
        five_eq.next_to(implies2, DOWN)
        five_eq.to_edge(RIGHT)

        n_eq = Tex(R"h(n) = h(1 + \cdots + 1) = h(1) \cdots h(1) = h(1)^n")
        n_eq.scale(0.75)
        n_eq.next_to(implies2, DOWN, MED_LARGE_BUFF)
        sum_brace = Brace(n_eq[R"1 + \cdots + 1"], UP, SMALL_BUFF)
        sum_tex = sum_brace.get_tex(R"n \text{ times}", buff=SMALL_BUFF).scale(0.5, about_edge=DOWN)
        prod_brace = Brace(n_eq[R"h(1) \cdots h(1)"], UP, SMALL_BUFF)
        prod_tex = prod_brace.get_tex(R"n \text{ times}", buff=SMALL_BUFF).scale(0.5, about_edge=DOWN)

        for tex in n_eq, sum_tex, prod_tex:
            tex["n"].set_color(BLUE)

        self.play(Write(five_eq["h(5)"]))
        self.wait()
        self.play(
            TransformFromCopy(five_eq["h("][0], five_eq["h("][1]),
            TransformFromCopy(five_eq[")"][0], five_eq[")"][1]),
            Write(five_eq["="][0]),
        )
        self.play(ShowIncreasingSubsets(five_eq["1 + 1 + 1 + 1 + 1"][0]))
        self.wait()
        self.play(
            FadeTransform(
                five_eq["= h(1 + 1 + 1 + 1 + 1)"].copy(),
                five_eq["= h(1)h(1)h(1)h(1)h(1)"],
            )
        )
        self.wait()
        self.play(Write(five_eq["= h(1)^5"]))
        self.wait()

        self.play(FadeOut(five_eq), FadeIn(n_eq), FadeIn(implies2))
        self.play(LaggedStart(
            GrowFromCenter(sum_brace),
            FadeIn(sum_tex, 0.25 * DOWN),
            GrowFromCenter(prod_brace),
            FadeIn(prod_tex, 0.25 * DOWN),
        ))
        self.wait()

        # Exponential equation
        exp_eq1 = Tex(R"h(n) = h(1)^n")
        exp_eq2 = Tex(R"h(n) = b^n")
        for eq in exp_eq1, exp_eq2:
            eq["n"].set_color(BLUE)
        exp_eq1.next_to(n_eq, DOWN, MED_LARGE_BUFF)
        exp_eq2.move_to(exp_eq1, LEFT)
        h1_rect = SurroundingRectangle(exp_eq1["h(1)"], buff=0.05)
        h1_rect.set_stroke(YELLOW, 1)
        h1_words = Text("Some number", font_size=30)
        h1_words.match_color(h1_rect)
        h1_words.next_to(h1_rect, DOWN, SMALL_BUFF)

        self.play(
            TransformFromCopy(n_eq["h(n)"], exp_eq1["h(n)"]),
            TransformFromCopy(n_eq["= h(1)^n"], exp_eq1["= h(1)^n"]),
        )
        self.wait()
        self.play(ShowCreation(h1_rect), FadeIn(h1_words))
        self.wait()
        self.play(
            TransformMatchingTex(exp_eq1, exp_eq2),
            FadeOut(h1_rect, scale=0.5),
            FadeOut(h1_words, scale=0.5),
        )
        self.wait()

        # Show exercises
        self.play(
            exp_eq2.animate.next_to(implies2, DOWN),
            FadeOut(VGroup(n_eq, sum_brace, sum_tex, prod_brace, prod_tex), UP),
        )
        rational_eq = Tex(R"h(p / q) = b^{\,p / q}")
        rational_eq["p / q"].set_color(RED)
        rational_eq.move_to(exp_eq2)

        exercise = TexText(R"Exercise: Show this is also true for rational inputs, $p / q$")
        exercise["p / q"].set_color(RED)
        hint = TexText(R"Hint, think about $h\left(\frac{p}{q} + \cdots + \frac{p}{q} \right)$")

        exercise.next_to(rational_eq, DOWN, LARGE_BUFF)
        exercise.to_edge(RIGHT)
        hint.scale(0.7)
        hint.set_fill(GREY_A)
        hint.next_to(exercise, DOWN)

        self.play(
            Write(exercise),
            FadeOut(VGroup(example_box, example_word, example_f, example_h), shift=DL),
        )
        self.wait()
        pq_target = rational_eq["p / q"].copy()
        self.play(
            TransformMatchingTex(exp_eq2, rational_eq),
            TransformMatchingShapes(exercise["p / q"].copy(), pq_target),
        )
        self.remove(pq_target)
        self.wait()
        self.play(FadeIn(hint, DOWN))
        self.wait(2)
        self.play(LaggedStart(
            FadeOut(exercise, 0.5 * DOWN),
            FadeOut(hint, 0.5 * DOWN),
            lag_ratio=0.25,
        ))

        # Continuity
        assumption = TexText(R"Assuming $f$ (and hence also $h$) \\ is continuous...", font_size=36)
        assumption.next_to(rational_eq, LEFT, buff=2.0, aligned_edge=UP)
        assumption.shift(0.5 * DOWN)

        hx_eq = Tex("h(x) = b^x", **kw)
        hx_eq.move_to(rational_eq)
        range1 = TexText(R"For all $x \in \mathds{R}$", **kw)
        range2 = TexText(R"For all $x \in \mathds{R}^+$", **kw)
        for ran in range1, range2:
            ran.scale(0.75)
            ran.next_to(hx_eq, DOWN, MED_LARGE_BUFF)

        arrow = Arrow(assumption, hx_eq)

        self.play(FadeIn(assumption, lag_ratio=0.1))
        self.wait()
        self.play(
            GrowArrow(arrow),
            TransformMatchingTex(rational_eq, hx_eq)
        )
        self.play(FadeIn(range1, DOWN))
        self.wait()
        self.play(FadeTransform(range1, range2))
        self.wait()

        # Swap out for e
        hx_eq2 = Tex(R"h(x) = e^{{c} x}", **kw)
        hx_eq2.move_to(hx_eq)
        hx_eq2["c"].set_color(RED)

        b_rect = SurroundingRectangle(hx_eq["b"], buff=0.05)
        b_rect.set_stroke(PINK, 2)
        b_words = Text("Some constant", font_size=30)
        b_words.next_to(b_rect, DOWN, SMALL_BUFF, LEFT)
        b_words.match_color(b_rect)

        self.play(
            FadeOut(assumption, LEFT),
            Uncreate(arrow),
            FadeOut(range2, LEFT),
            ShowCreation(b_rect),
            Write(b_words, run_time=1)
        )
        self.wait()
        c = hx_eq2["{c}"][0][0]
        c_copy = c.copy()
        c.set_opacity(0)
        self.play(
            ReplacementTransform(b_rect, c_copy),
            TransformMatchingTex(hx_eq, hx_eq2, key_map={"b": "e"}),
            FadeOut(b_words, 0.2 * DOWN),
        )
        self.remove(c_copy)
        c.set_opacity(1)
        self.add(hx_eq2)
        self.wait()

        # Write final form for f
        implies3 = implies2.copy()
        implies3.rotate(-90 * DEGREES)
        implies3.next_to(hx_eq2, LEFT)
        f_form = Tex(R"f(x) = e^{cx^2}", **kw)
        f_form["c"].set_color(RED)
        f_form.next_to(implies3, LEFT)
        f_form.align_to(hx_eq2, DOWN)

        self.play(
            Write(implies3),
            TransformMatchingTex(hx_eq2.copy(), f_form, run_time=1)
        )
        self.wait()
        f_form.generate_target()
        f_form.target.scale(1.5, about_edge=RIGHT)
        rect = SurroundingRectangle(f_form.target)
        rect.set_stroke(YELLOW, 2)
        self.play(
            MoveToTarget(f_form),
            FlashAround(f_form.target, time_width=1, run_time=2, stroke_width=5),
            ShowCreation(rect, run_time=2),
        )
        self.wait()
