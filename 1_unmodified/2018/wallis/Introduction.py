# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2018/wallis.py (lines 86-166)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


def get_wallis_product_numerical_terms(n_terms=20):
    result = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        n, d = next(nd_generator)
        result.append(float(n) / d)
    return result


class Introduction(Scene):
    def construct(self):
        n_terms = 10

        number_line = NumberLine(
            x_min=0,
            x_max=2,
            unit_size=5,
            tick_frequency=0.25,
            big_tick_numbers=[0, 1, 2],
            color=GREY_B,
        )
        number_line.add_numbers()
        number_line.move_to(DOWN)

        numerical_terms = get_wallis_product_numerical_terms(400)
        partial_products = np.cumprod(numerical_terms)
        curr_product = partial_products[0]

        arrow = Vector(DOWN, color=YELLOW)

        def get_arrow_update():
            return ApplyFunction(
                lambda mob: mob.next_to(
                    number_line.number_to_point(curr_product),
                    UP, SMALL_BUFF
                ),
                arrow,
            )
        get_arrow_update().update(1)
        decimal = DecimalNumber(
            curr_product, num_decimal_places=5, show_ellipsis=True)
        decimal.next_to(arrow, UP, SMALL_BUFF, submobject_to_align=decimal[:5])
        decimal_anim = ChangingDecimal(
            decimal,
            lambda a: number_line.point_to_number(arrow.get_center()),
            tracked_mobject=arrow
        )

        product_mob = get_wallis_product(n_terms)
        product_mob.to_edge(UP)

        rects = VGroup(*[
            SurroundingRectangle(product_mob[:n])
            for n in list(range(3, 4 * n_terms, 4)) + [4 * n_terms]
        ])
        rect = rects[0].copy()

        pi_halves_arrow = Vector(UP, color=BLUE)
        pi_halves_arrow.next_to(
            number_line.number_to_point(np.pi / 2), DOWN, SMALL_BUFF
        )
        pi_halves_term = OldTex("\\pi / 2")
        pi_halves_term.next_to(pi_halves_arrow, DOWN)

        self.add(product_mob, number_line, rect, arrow, decimal)
        self.add(pi_halves_arrow, pi_halves_term)
        for n in range(1, len(rects)):
            curr_product = partial_products[n]
            self.play(
                get_arrow_update(),
                decimal_anim,
                Transform(rect, rects[n]),
                run_time=0.5
            )
            self.wait(0.5)

        for n in range(len(rects), len(numerical_terms), 31):
            curr_product = partial_products[n]
            self.play(
                get_arrow_update(),
                decimal_anim,
                run_time=0.25
            )
        curr_product = np.pi / 2
        self.play(
            get_arrow_update(),
            decimal_anim,
            run_time=0.5
        )
        self.wait()
