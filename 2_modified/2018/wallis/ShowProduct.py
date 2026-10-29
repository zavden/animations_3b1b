# ==============================================================================
# Scene:      ShowProduct
# Source:     videos/_2018/wallis.py (lines 454-777)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowProduct.py ShowProduct -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Scene.frame_duration does not exist in GL; use 1 / camera.fps
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


class ShowProduct(Scene):
    def construct(self):
        self.setup_axes()
        self.setup_wallis_product()
        self.show_larger_terms()
        self.show_smaller_terms()
        self.interleave_terms()
        self.show_answer()

    def setup_axes(self):
        axes = self.axes = self.get_axes(unit_size=0.75)
        self.add(axes)

    def setup_wallis_product(self):
        full_wallis_product = get_wallis_product(n_terms=16, show_result=False)
        wallis_product_parts = VGroup(*[
            full_wallis_product[i:i + 4]
            for i in range(0, len(full_wallis_product), 4)
        ])

        larger_parts = self.larger_parts = wallis_product_parts[::2]
        larger_parts.set_color(YELLOW)
        dots = OldTex("\\cdots")
        dots.move_to(larger_parts[-1][-1], LEFT)
        larger_parts[-1][-1].submobjects = dots.submobjects

        smaller_parts = self.smaller_parts = wallis_product_parts[1::2]
        smaller_parts.set_color(BLUE)

        for parts in larger_parts, smaller_parts:
            parts.arrange(RIGHT, buff=2 * SMALL_BUFF)
            # Move around the dots
            for part1, part2 in zip(parts, parts[1:]):
                dot = part1.submobjects.pop(-1)
                part2.add_to_back(dot)

        larger_parts.to_edge(UP)
        smaller_parts.next_to(larger_parts, DOWN, LARGE_BUFF)

        self.wallis_product_terms = get_wallis_product_numerical_terms(40)

    def show_larger_terms(self):
        axes = self.axes
        parts = self.larger_parts
        terms = self.wallis_product_terms[::2]
        partial_products = np.cumprod(terms)

        dots = VGroup(*[
            Dot(axes.coords_to_point(n + 1, prod))
            for n, prod in enumerate(partial_products)
        ])
        dots.match_color(parts)
        lines = VGroup(*[
            Line(d1.get_center(), d2.get_center())
            for d1, d2 in zip(dots, dots[1:])
        ])

        braces = VGroup(*[
            Brace(parts[:n + 1], DOWN)
            for n in range(len(parts))
        ])

        brace = braces[0].copy()
        decimal = DecimalNumber(partial_products[0], num_decimal_places=4)
        decimal.next_to(brace, DOWN)

        self.add(brace, decimal, dots[0], parts[0])
        tuples = list(zip(parts[1:], lines, dots[1:], partial_products[1:], braces[1:]))
        for part, line, dot, prod, new_brace in tuples:
            self.play(
                FadeIn(part),
                Transform(brace, new_brace),
                ChangeDecimalToValue(
                    decimal, prod,
                    position_update_func=lambda m: m.next_to(brace, DOWN)
                ),
                ShowCreation(line),
                GrowFromCenter(dot, rate_func=squish_rate_func(smooth, 0.5, 1)),
                run_time=0.5,
            )
            self.wait(0.5)
        N = len(parts)
        self.play(
            LaggedStartMap(ShowCreation, lines[N - 1:], lag_ratio=0.2),
            LaggedStartMap(FadeIn, dots[N:], lag_ratio=0.2),
            brace.stretch, 1.2, 0, {"about_edge": LEFT},
            ChangeDecimalToValue(
                decimal, partial_products[-1],
                position_update_func=lambda m: m.next_to(brace, DOWN)
            ),
            run_time=4,
            rate_func=linear,
        )
        self.play(
            FadeOut(brace),
            ChangeDecimalToValue(
                decimal, partial_products[-1] + 2,
                position_update_func=lambda m: m.next_to(brace, DOWN)
            ),
            UpdateFromFunc(
                # CHANGE: Scene.frame_duration does not exist in GL; use 1 / camera.fps
                decimal, lambda d: d.shift(RIGHT / self.camera.fps)
            ),
            UpdateFromAlphaFunc(
                decimal, lambda d, a: d.set_fill(opacity=1 - a)
            ),
        )
        self.remove(decimal)

        self.graph_to_remove = VGroup(dots, lines)

    def show_smaller_terms(self):
        larger_parts = self.larger_parts
        larger_parts.save_state()
        larger_parts_mover = larger_parts.copy()
        larger_parts.fade(0.5)

        smaller_parts = self.smaller_parts
        for parts in larger_parts_mover, smaller_parts:
            parts.denominators = VGroup(
                parts[0][2],
                *[part[3] for part in parts[1:]]
            )
        vect = op.sub(
            smaller_parts.denominators[1].get_left(),
            smaller_parts.denominators[0].get_left(),
        )
        smaller_parts.denominators.shift(vect)

        self.play(
            larger_parts_mover.move_to, smaller_parts, LEFT,
            FadeOut(self.graph_to_remove)
        )
        self.play(
            larger_parts_mover.denominators.shift, -vect,
            smaller_parts.denominators.shift, -vect,
            UpdateFromAlphaFunc(
                larger_parts_mover,
                lambda m, a: m.set_fill(opacity=1 - a),
                remover=True
            ),
            UpdateFromAlphaFunc(
                smaller_parts,
                lambda m, a: m.set_fill(opacity=a)
            ),
        )

        # Rescale axes
        new_axes = self.get_axes(unit_size=1.5)
        self.play(ReplacementTransform(self.axes, new_axes))
        axes = self.axes = new_axes

        # Show graph
        terms = self.wallis_product_terms[1::2]
        partial_products = np.cumprod(terms)[:15]

        dots = VGroup(*[
            Dot(axes.coords_to_point(n + 1, prod))
            for n, prod in enumerate(partial_products)
        ])
        dots.match_color(smaller_parts)
        lines = VGroup(*[
            Line(d1.get_center(), d2.get_center())
            for d1, d2 in zip(dots, dots[1:])
        ])

        self.play(
            ShowCreation(lines),
            LaggedStartMap(FadeIn, dots, lag_ratio=0.1),
            run_time=3,
            rate_func=linear,
        )
        self.wait(2)
        self.play(FadeOut(VGroup(dots, lines)))

    def interleave_terms(self):
        larger_parts = self.larger_parts
        smaller_parts = self.smaller_parts
        index = 6
        larger_parts.restore()
        for parts in larger_parts, smaller_parts:
            parts.prefix = parts[:index]
            parts.suffix = parts[index:]
            parts.prefix.generate_target()
        larger_parts.fade(0.5)
        full_product = VGroup(*it.chain(
            *list(zip(larger_parts.prefix.target, smaller_parts.prefix.target))
        ))
        for i, tex, vect in (0, "\\cdot", LEFT), (-1, "\\cdots", RIGHT):
            part = smaller_parts.prefix.target[i]
            dot = OldTex(tex)
            dot.match_color(part)
            dot.next_to(part, vect, buff=2 * SMALL_BUFF)
            part.add(dot)
        full_product.arrange(RIGHT, buff=2 * SMALL_BUFF)
        full_product.to_edge(UP)

        for parts in larger_parts, smaller_parts:
            self.play(
                MoveToTarget(parts.prefix),
                FadeOut(parts.suffix)
            )
        self.wait()

        # Dots and lines
        # In poor form, this is modified copy-pasted from show_larger_terms
        axes = self.axes
        parts = full_product
        terms = self.wallis_product_terms
        partial_products = np.cumprod(terms)
        partial_products_iter = iter(partial_products)
        print(partial_products)

        dots = VGroup(*[
            Dot(axes.coords_to_point(n + 1, prod))
            for n, prod in enumerate(partial_products)
        ])
        dots.set_color(GREEN)
        lines = VGroup(*[
            Line(d1.get_center(), d2.get_center())
            for d1, d2 in zip(dots, dots[1:])
        ])

        braces = VGroup(*[
            Brace(parts[:n + 1], DOWN)
            for n in range(len(parts))
        ])

        brace = braces[0].copy()
        decimal = DecimalNumber(next(partial_products_iter), num_decimal_places=4)
        decimal.next_to(brace, DOWN)

        self.play(*list(map(FadeIn, [brace, decimal, dots[0]])))
        tuples = list(zip(lines, dots[1:], braces[1:]))
        for line, dot, new_brace in tuples:
            self.play(
                Transform(brace, new_brace),
                ChangeDecimalToValue(
                    decimal, next(partial_products_iter),
                    position_update_func=lambda m: m.next_to(brace, DOWN)
                ),
                ShowCreation(line),
                GrowFromCenter(dot, rate_func=squish_rate_func(smooth, 0.5, 1)),
                run_time=0.5,
            )
            self.wait(0.5)

        def get_decimal_anim():
            return ChangeDecimalToValue(
                decimal, next(partial_products_iter),
                run_time=1,
                rate_func=squish_rate_func(smooth, 0, 0.5),
            )

        self.play(
            FadeIn(lines[len(parts) - 1:]),
            FadeIn(dots[len(parts):]),
            get_decimal_anim()
        )
        for x in range(3):
            self.play(get_decimal_anim())

        self.partial_product_decimal = decimal
        self.get_decimal_anim = get_decimal_anim

    def show_answer(self):
        decimal = self.partial_product_decimal
        axes = self.axes

        pi_halves = OldTex("{\\pi", "\\over", "2}")
        pi_halves.scale(1.5)
        pi_halves.move_to(decimal, UP)

        randy = Randolph(height=1.7)
        randy.next_to(decimal, DL)
        randy.change("confused")
        randy.save_state()
        randy.change("plain")
        randy.fade(1)

        h_line = DashedLine(
            axes.coords_to_point(0, np.pi / 2),
            axes.coords_to_point(20, np.pi / 2),
            color=RED
        )

        self.play(
            ShowCreation(h_line),
            randy.restore,
            self.get_decimal_anim()
        )
        self.play(Blink(randy), self.get_decimal_anim())
        self.play(self.get_decimal_anim())
        self.play(
            self.get_decimal_anim(),
            UpdateFromAlphaFunc(
                decimal,
                lambda m, a: m.set_fill(opacity=1 - a)
            ),
            ReplacementTransform(randy, pi_halves[0]),
            Write(pi_halves[1:]),
        )
        self.remove(decimal)
        self.wait()

    # Helpers

    def get_axes(self, unit_size):
        y_max = 7
        axes = Axes(
            x_min=-1,
            x_max=12.5,
            y_min=-0.5,
            y_max=y_max + 0.25,
            y_axis_config={
                "unit_size": unit_size,
                "big_tick_numbers": list(range(1, y_max + 1)),
                "tick_size": 0.05,
            },
        )
        axes.shift(6 * LEFT + 3 * DOWN - axes.coords_to_point(0, 0))

        axes.y_axis.label_direction = LEFT
        axes.y_axis.add_numbers(*list(range(1, y_max + 1)))
        return axes
