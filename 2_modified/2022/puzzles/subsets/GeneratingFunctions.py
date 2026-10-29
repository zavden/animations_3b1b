# ==============================================================================
# Scene:      GeneratingFunctions
# Source:     videos/_2022/puzzles/subsets.py (lines 1849-2040)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GeneratingFunctions.py GeneratingFunctions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - time_range= -> time_span= (current name of Animation's argument)
# ==============================================================================

from manim_imports_ext import *

def get_set_tex(values, max_shown=7, **kwargs):
    if len(values) > max_shown:
        value_mobs = [
            *map(Integer, values[:max_shown - 2]),
            Tex("\\dots"),
            Integer(values[-1], group_with_commas=False),
        ]
    else:
        value_mobs = list(map(Integer, values))

    commas = Tex(",").replicate(len(value_mobs) - 1)
    result = VGroup()
    result.add(Tex("\\{"))
    result.add(*it.chain(*zip(value_mobs, commas)))
    if len(value_mobs) > 0:
        result.add(value_mobs[-1].align_to(value_mobs[0], UP))
    result.add(Tex("\\}"))
    result.arrange(RIGHT, buff=SMALL_BUFF)
    if len(values) > 0:
        commas.set_y(value_mobs[0].get_y(DOWN))
    if len(values) > max_shown:
        result[-4].match_y(commas)
    result.values = values
    return result


def get_subsets(full_set):
    return list(it.chain(*(
        it.combinations(full_set, k)
        for k in range(len(full_set) + 1)
    )))


class GeneratingFunctions(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Generating functions!", font_size=72)
        title.to_edge(UP)
        title.set_color(BLUE)
        underline = Underline(title, buff=-0.05)
        underline.scale(1.25)
        underline.insert_n_curves(50)
        underline.set_stroke(BLUE_B, width=[0, 3, 3, 3, 0])
        self.play(
            Write(title),
            ShowCreation(underline),
            run_time=1
        )

        # First poly
        degree = 10
        poly = OldTex(
            "f(x) = 1+1 x^{1}+1 x^{2}+2 x^{3}+2 x^{4}+"
            "3 x^{5}+4 x^{6}+5x^{7}+6x^{8}+"
            "8x^{9} + 10x^{10} + \\cdots",
            isolate=["=", "+", "x"]
        )
        seps = [poly.get_part_by_tex("="), *poly.get_parts_by_tex("+")]
        shifter = 0.05
        for sep in seps:
            i = poly.submobjects.index(sep)
            poly[i:].shift(shifter * LEFT)
            poly[i + 1:].shift(shifter * LEFT)
        poly.set_width(FRAME_WIDTH - 0.5)
        poly.next_to(underline, DOWN, LARGE_BUFF)

        self.add(poly)

        subsets = get_subsets(list(range(1, degree + 1)))
        subset_groups = VGroup().replicate(degree + 1)
        for subset in subsets:
            index = sum(subset)
            if index <= degree:
                subset_groups[index].add(get_set_tex(subset))

        subset_groups.set_width(1.0)
        subset_groups.set_color(BLUE_B)

        self.play(FadeIn(poly, DOWN))
        self.wait()

        rects = VGroup()
        for ssg, sep in zip(subset_groups, seps[:-1]):
            coef = poly[poly.submobjects.index(sep) + 1]
            ssg.arrange(DOWN, buff=SMALL_BUFF)
            ssg.next_to(coef, DOWN, buff=MED_LARGE_BUFF)
            rect = SurroundingRectangle(coef, buff=0.1)
            rect.round_corners()
            rect.set_stroke(BLUE, 1)
            rects.add(rect)
            coef.set_color(BLUE_B)

            self.add(rect, ssg)
            self.play(ShowIncreasingSubsets(
                ssg,
                int_func=np.ceil,
                run_time=max(0.5, 0.1 * len(ssg)),
                rate_func=linear,
            ))
            self.wait(0.5)
            self.remove(rect)

        # Fibbonacci poly
        fib_poly = OldTex(
            "F(x) = 0+1 x^{1}+1 x^{2}+2 x^{3}+3 x^{4}+"
            "5 x^{5}+ 8 x^{6} + 13 x^{7}+21 x^{8}+\\cdots",
            isolate=["=", "+", "x"]
        )
        coefs = VGroup(*(
            fib_poly[fib_poly.submobjects.index(sep) + 1]
            for sep in (fib_poly.get_part_by_tex("="), *fib_poly.get_parts_by_tex("+"))
        ))
        coefs.set_color(RED)
        fib_poly.match_width(poly)
        fib_poly.move_to(poly)

        fib_name = Text("Fibonacci numbers")
        fib_name.match_color(coefs)
        fib_name.next_to(fib_poly, DOWN, LARGE_BUFF)

        coefs.set_opacity(0)
        self.play(
            FadeOut(poly, DOWN),
            FadeIn(fib_poly, DOWN),
            LaggedStartMap(FadeOut, subset_groups, shift=DOWN),
            Write(fib_name),
        )
        coefs.set_opacity(1)
        self.play(FadeIn(coefs, lag_ratio=0.5, run_time=3))
        self.wait()

        # Show Fibbonaci property
        prop = Tex("f_{n} = f_{n - 1} + f_{n - 2}")
        func_prop1 = Tex("F(x) = xF(x) + x^2 F(x) + x")
        func_prop2 = Tex("F(x) = \\frac{x}{1 - x - x^2}")

        arrow = Tex("\\Updownarrow")

        prop.next_to(fib_poly, DOWN, LARGE_BUFF)
        prop.shift(3 * RIGHT)
        arrow.next_to(prop, DOWN)
        func_prop1.next_to(arrow, DOWN)
        func_prop2.next_to(func_prop1, DOWN, MED_LARGE_BUFF)

        def get_coef_arrows(n):
            return VGroup(*(
                Arrow(
                    coefs[i].get_top(), coefs[n + 2].get_top(),
                    path_arc=-75 * DEGREES,
                    stroke_color=RED,
                    stroke_width=3,
                )
                for i in (n, n + 1)
            ))

        coef_arrows = get_coef_arrows(0)

        self.play(
            fib_name.animate.to_edge(LEFT),
            Write(prop),
            ShowCreation(coef_arrows, lag_ratio=0.5, run_time=1.5),
        )
        self.wait()
        for n in range(1, 7):
            new_arrows = get_coef_arrows(n)
            self.play(
                FadeOut(coef_arrows),
                ShowCreation(new_arrows, lag_ratio=0.5)
            )
            coef_arrows = new_arrows
        self.play(
            Write(arrow),
            Write(func_prop1),
        )
        self.wait()
        self.play(
            TransformMatchingShapes(func_prop1.copy(), func_prop2)
        )
        self.wait()

        # Show details
        left_group = VGroup(prop, arrow, func_prop1, func_prop2)
        details_box = Rectangle(7, 4.5)
        details_box.set_fill(GREY_E, 1)
        details_box.set_stroke(WHITE, 1)
        details_box.to_corner(DR)
        details_title = Text("Gritty details for the curious...", font_size=36)
        details_title.next_to(details_box.get_top(), DOWN, SMALL_BUFF)
        details_box.add(details_title)

        func_prop2.generate_target()
        func_prop2.target.scale(0.5)
        func_prop2.target.next_to(details_title, DOWN, MED_LARGE_BUFF).align_to(details_box, LEFT).shift(SMALL_BUFF * RIGHT)

        rhs = Tex(
            " = {x \\over (1 - \\varphi x)(1 + \\frac{1}{\\varphi} x)}"
            "= {1 / \\sqrt{5} \\over (1 - \\varphi x)} - {1 / \\sqrt{5} \\over (1 + \\frac{1}{\\varphi}x)}",
            font_size=24,
        )
        rhs.next_to(func_prop2.target, RIGHT, SMALL_BUFF, submobject_to_align=rhs[0])

        expansion = Tex(
            "\\frac{1}{\\sqrt{5}}\\sum_{n = 0}^\\infty \\varphi^n x^n - "
            "\\frac{1}{\\sqrt{5}}\\sum_{n = 0}^\\infty \\left({-1 \\over \\varphi}\\right)^n x^n",
            font_size=24
        )
        expansion.next_to(rhs, DOWN, MED_LARGE_BUFF)
        expansion.match_x(details_box)

        implication = Tex(
            "\\Rightarrow f_n = {\\varphi^n - (-1 / \\varphi)^n \\over \\sqrt{5}}",
            font_size=24,
        )
        implication.next_to(expansion, DOWN, MED_LARGE_BUFF)

        self.play(
            left_group.animate.to_edge(LEFT),
            FadeOut(fib_name, LEFT),
            # CHANGE: time_range -> time_span (current name of Animation's argument)
            FadeIn(details_box, LEFT, time_span=(0.5, 1.5))
        )
        self.play(MoveToTarget(func_prop2))
        self.play(Write(rhs))
        self.play(FadeIn(expansion, DOWN))
        self.play(FadeIn(implication, DOWN))
        self.wait()
