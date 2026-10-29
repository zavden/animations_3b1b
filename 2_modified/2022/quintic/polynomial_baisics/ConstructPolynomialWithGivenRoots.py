# ==============================================================================
# Scene:      ConstructPolynomialWithGivenRoots
# Source:     videos/_2022/quintic/polynomial_baisics.py (lines 20-644)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl ConstructPolynomialWithGivenRoots.py ConstructPolynomialWithGivenRoots -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The misspelled kwarg widith= is removed from Axes (the original ignored it through CONFIG; today it raises TypeError)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/quintic/roots_and_coefs.py -----

def roots_to_coefficients(roots):
    n = len(list(roots))
    return [
        ((-1)**(n - k)) * sum(
            np.prod(tup)
            for tup in it.combinations(roots, n - k)
        )
        for k in range(n)
    ] + [1]


def poly(x, coefs):
    return sum(coefs[k] * x**k for k in range(len(coefs)))


def dpoly(x, coefs):
    return sum(k * coefs[k] * x**(k - 1) for k in range(1, len(coefs)))


def find_root(func, dfunc, seed=complex(1, 1), tol=1e-8, max_steps=100):
    # Use newton's method
    last_seed = np.inf
    for n in range(max_steps):
        if abs(seed - last_seed) < tol:
            break
        last_seed = seed
        seed = seed - func(seed) / dfunc(seed)
    return seed


def coefficients_to_roots(coefs):
    if len(coefs) == 0:
        return []
    elif coefs[-1] == 0:
        return coefficients_to_roots(coefs[:-1])
    roots = []
    # Find a root, divide out by (x - root), repeat
    for i in range(len(coefs) - 1):
        root = find_root(
            lambda x: poly(x, coefs),
            lambda x: dpoly(x, coefs),
        )
        roots.append(root)
        new_reversed_coefs, rem = np.polydiv(coefs[::-1], [1, -root])
        coefs = new_reversed_coefs[::-1]
    return roots


def x_power_tex(power, base="x"):
    if power == 0:
        return ""
    elif power == 1:
        return base
    else:
        return f"{base}^{{{power}}}"


def poly_tex(coefs, prefix="P(x) = ", coef_color=RED_B):
    n = len(coefs) - 1
    coefs = [f"{{{coef}}}" for coef in coefs]
    terms = [prefix, x_power_tex(n)]
    for k in range(n - 1, -1, -1):
        coef = coefs[k]
        if not coef[1] == "-":
            terms.append("+")
        terms.append(str(coef))
        terms.append(x_power_tex(k))
    t2c = dict([(coef, coef_color) for coef in coefs])
    return OldTex(*terms, tex_to_color_map=t2c)


def factored_poly_tex(roots, prefix="P(x) = ", root_colors=[YELLOW, YELLOW]):
    roots = list(roots)
    root_colors = color_gradient(root_colors, len(roots))
    root_texs = [str(r) for r in roots]
    parts = []
    if prefix:
        parts.append(prefix)
    for root_tex in root_texs:
        parts.extend(["(", "x", "-", root_tex, ")"])
    t2c = dict((
        (rt, root_color)
        for rt, root_color in zip(root_texs, root_colors)
    ))
    return OldTex(*parts, tex_to_color_map=t2c)


def sym_poly_tex_args(roots, k, abbreviate=False):
    result = []
    subsets = list(it.combinations(roots, k))
    if k in [1, len(roots)]:
        abbreviate = False
    if abbreviate:
        subsets = [*subsets[:2], subsets[-1]]
    for subset in subsets:
        if abbreviate and subset is subsets[-1]:
            result.append(" \\cdots ")
            result.append("+")
        for r in subset:
            result.append(str(r))
            result.append(" \\cdot ")
        result.pop()
        result.append("+")
    result.pop()
    return result


def expanded_poly_tex(roots, vertical=True, root_colors=[YELLOW, YELLOW], abbreviate=False):
    roots = list(roots)
    root_colors = color_gradient(root_colors, len(roots))
    n = len(roots)
    kw = dict(
        tex_to_color_map=dict((
            (str(r), root_color)
            for r, root_color in zip(roots, root_colors)
        )),
        arg_separator=" "
    )
    result = VGroup()
    result.add(OldTex(f"x^{{{n}}}"))
    for k in range(1, n + 1):
        sym_poly = sym_poly_tex_args(
            roots, k,
            abbreviate=abbreviate
        )
        line = OldTex(
            "+" if k % 2 == 0 else "-",
            "\\big(", *sym_poly, "\\big)",
            x_power_tex(n - k),
            **kw,
        )
        result.add(line)
    for line in result:
        line[-1].set_color(WHITE)
    if vertical:
        result.arrange(DOWN, aligned_edge=LEFT)
    else:
        result.arrange(RIGHT, buff=SMALL_BUFF)
        result[0].shift(result[0].get_height() * UP / 4)
    return result


def get_symmetric_system(lhss,
                         roots=None,
                         root_colors=[YELLOW, YELLOW],
                         lhs_color=RED_B,
                         abbreviate=False,
                         signed=False,
                         ):
    lhss = [f"{{{lhs}}}" for lhs in lhss]
    if roots is None:
        roots = [f"r_{{{i}}}" for i in range(len(lhss))]
    root_colors = color_gradient(root_colors, len(roots))
    t2c = dict([
        (root, root_color)
        for root, root_color in zip(roots, root_colors)
    ])
    t2c.update(dict([
        (str(lhs), lhs_color)
        for lhs in lhss
    ]))
    kw = dict(tex_to_color_map=t2c)
    equations = VGroup(*(
        OldTex(
            lhs, "=",
            "-(" if neg else "",
            *sym_poly_tex_args(roots, k, abbreviate=abbreviate),
            ")" if neg else "",
            **kw
        )
        for k, lhs in zip(it.count(1), lhss)
        for neg in [signed and k % 2 == 1]
    ))
    equations.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
    for eq in equations:
        eq.shift((equations[0][1].get_x() - eq[1].get_x()) * RIGHT)
    return equations



# ----- From _2022/quintic/polynomial_baisics.py -----

class ConstructPolynomialWithGivenRoots(Scene):
    root_color = YELLOW

    def construct(self):
        # Add axes
        axes = self.add_axes()

        # Add challenge
        challenge = VGroup(
            Text("Can you construct a cubic polynomial"),
            OldTex(
                "P(x) = x^3 + c_2 x^2 + c_1 x + c_0",
                tex_to_color_map={
                    "c_2": RED_B,
                    "c_1": RED_B,
                    "c_0": RED_B,
                }
            ),
            OldTexText(
                "with roots at $x = 1$, $x = 2$, and $x = 4$?",
                tex_to_color_map={
                    "$x = 1$": self.root_color,
                    "$x = 2$": self.root_color,
                    "$x = 4$": self.root_color,
                }
            )
        )
        challenge.scale(0.7)
        challenge.arrange(DOWN, buff=MED_LARGE_BUFF)
        challenge.to_corner(UL)

        self.add(challenge)

        # Add graph
        roots = [1, 2, 4]
        coefs = roots_to_coefficients(roots)
        graph = axes.get_graph(lambda x: poly(x, coefs))
        graph.set_color(BLUE)

        root_dots = Group(*(GlowDot(axes.c2p(x, 0)) for x in roots))
        root_dots.set_color(self.root_color)

        x_terms = challenge[2].get_parts_by_tex("x = ")

        self.wait()
        self.play(
            LaggedStart(*(
                FadeTransform(x_term.copy(), dot)
                for x_term, dot in zip(x_terms, root_dots)
            ), lag_ratio=0.7, run_time=3)
        )
        self.add(graph, root_dots)
        self.play(ShowCreation(graph, run_time=3, rate_func=linear))
        self.wait()

        # Show factored solution
        factored = factored_poly_tex(roots)
        factored.match_height(challenge[1])
        factored.next_to(challenge, DOWN, LARGE_BUFF)

        rects = VGroup(*(
            SurroundingRectangle(
                factored[i:i + 5],
                stroke_width=1,
                stroke_color=BLUE,
                buff=0.05
            )
            for i in range(1, 12, 5)
        ))
        arrows = VGroup(*(
            Vector(DOWN).next_to(dot, UP, buff=0)
            for dot in root_dots
        ))
        zeros_eqs = VGroup(*(
            OldTex(
                f"P({r}) = 0",
                font_size=24
            ).next_to(rect, UP, SMALL_BUFF)
            for r, rect in zip(roots, rects)
        ))

        self.play(FadeIn(factored, DOWN))
        self.wait()
        to_fade = VGroup()
        for rect, arrow, eq in zip(rects, arrows, zeros_eqs):
            self.play(
                ShowCreation(rect),
                FadeIn(eq),
                ShowCreation(arrow),
                FadeOut(to_fade)
            )
            self.wait(2)
            to_fade = VGroup(rect, arrow, eq)
        self.play(FadeOut(to_fade))

        # Expand solution
        x_terms = factored[2::5]
        root_terms = VGroup(*(
            VGroup(m1, m2)
            for m1, m2 in zip(factored[3::5], factored[4::5])
        ))

        expanded = OldTex(
            "&x^3 ",
            "-1x^2", "-2x^2", "-4x^2 \\\\",
            "&+(-1)(-2)x", "+(-1)(-4)x", "+(-2)(-4)x\\\\",
            "&+(-1)(-2)(-4)",
        )
        for i, part in enumerate(expanded):
            if i in [1, 2, 3]:
                part[:2].set_color(self.root_color)
            elif i in [4, 5, 6, 7]:
                part[2:4].set_color(self.root_color)
                part[6:8].set_color(self.root_color)
            if i == 7:
                part[10:12].set_color(self.root_color)

        expanded.scale(0.7)
        expanded.next_to(factored[1], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        equals = factored[0][-1].copy()
        equals.match_y(expanded[0][0])

        self.add(equals)
        expanded_iter = iter(expanded)
        for k in range(4):
            for tup in it.combinations(range(3), k):
                factored[1:].set_opacity(0.5)
                rects = VGroup()
                for i in range(3):
                    mob = root_terms[i] if (i in tup) else x_terms[i]
                    mob.set_opacity(1)
                    rect = SurroundingRectangle(mob, buff=SMALL_BUFF)
                    rect.set_min_height(0.45, about_edge=DOWN)
                    rects.add(rect)
                rects.set_stroke(BLUE, 2)
                expanded_term = next(expanded_iter)
                expanded_rect = SurroundingRectangle(
                    expanded_term, buff=SMALL_BUFF
                )
                expanded_rect.match_style(rects)

                self.add(rects, expanded_rect)
                self.add(expanded_term)
                self.wait()
                self.remove(rects, expanded_rect)
        factored.set_opacity(1)
        self.add(expanded)
        self.wait()

        # Cleaner expansion
        cleaner_expanded = expanded_poly_tex(roots, vertical=False)
        cleaner_expanded.scale(0.7)
        cleaner_expanded.shift(expanded[0][0].get_center() - cleaner_expanded[0][0][0].get_center())

        self.play(
            FadeTransform(expanded[0], cleaner_expanded[0]),
            TransformMatchingShapes(
                expanded[1:4],
                cleaner_expanded[1],
            ),
            expanded[4:].animate.next_to(cleaner_expanded[1], DOWN, aligned_edge=LEFT)
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                expanded[4:7],
                cleaner_expanded[2],
            )
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                expanded[7],
                cleaner_expanded[3],
            )
        )
        back_rect = BackgroundRectangle(cleaner_expanded, buff=SMALL_BUFF)
        self.add(back_rect, cleaner_expanded)
        self.play(FadeIn(back_rect))
        self.wait()

        # Evaluate
        answer = OldTex(
            "= x^3 -7x^2 + 14x -8",
            tex_to_color_map={
                "-7": RED_B,
                "14": RED_B,
                "-8": RED_B,
            }
        )
        answer.scale(0.7)
        answer.next_to(equals, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(FadeIn(answer, DOWN))
        self.wait()

        # Note the symmetry
        randy = Randolph(height=1)
        randy.to_corner(DL, buff=MED_SMALL_BUFF)

        randy.change("tease")
        randy.save_state()
        randy.change("plain").set_opacity(0)

        bubble = SpeechBubble(width=3, height=1, stroke_width=2)
        bubble.move_to(randy.get_corner(UR), LEFT)
        bubble.shift(0.45 * UP + 0.1 * LEFT)
        bubble.add_content(Text("Note the symmetry!"))

        self.play(Restore(randy))
        self.play(ShowCreation(bubble), Write(bubble.content))
        self.play(Blink(randy))
        self.wait()

        factored.save_state()
        cleaner_expanded.save_state()
        for alt_roots in [(2, 4, 1), (4, 2, 1), (1, 4, 2), (1, 2, 4)]:
            alt_factored = factored_poly_tex(alt_roots)
            alt_factored.replace(factored)
            alt_expanded = expanded_poly_tex(alt_roots, vertical=False)
            alt_expanded.replace(cleaner_expanded)
            movers, targets = [
                VGroup(*(
                    group.get_parts_by_tex(str(root))
                    for root in alt_roots
                    for group in groups
                ))
                for groups in [(factored, *cleaner_expanded), (alt_factored, *alt_expanded)]
            ]

            self.play(
                TransformMatchingShapes(movers, targets, path_arc=PI / 2, run_time=1.5),
                randy.animate.look_at(movers),
            )
            self.remove(targets, factored, cleaner_expanded)
            factored.become(alt_factored)
            cleaner_expanded.become(alt_expanded)
            self.add(factored, cleaner_expanded)
            self.wait()
        factored.restore()
        cleaner_expanded.restore()
        self.play(
            FadeOut(randy),
            FadeOut(bubble),
            FadeOut(bubble.content),
        )

        # Reverse question
        top_lhs = OldTex("P(x)").match_height(factored)
        top_lhs.next_to(answer, LEFT).align_to(factored, LEFT)
        top_lhs.set_opacity(0)
        coef_poly = VGroup(top_lhs, answer)
        coef_poly.generate_target()
        coef_poly.target.set_opacity(1).to_edge(UP)

        full_factored = VGroup(back_rect, factored, equals, cleaner_expanded)
        full_factored.generate_target()
        full_factored.target.next_to(coef_poly.target, DOWN, buff=0.75, aligned_edge=LEFT)
        full_factored.target.set_opacity(0.5)

        self.add(full_factored, coef_poly)
        self.play(
            FadeOut(challenge, UP),
            MoveToTarget(full_factored),
            MoveToTarget(coef_poly),
        )

        new_challenge = Text("Find the roots!")
        new_challenge.add_background_rectangle(buff=0.1)
        arrow = Vector(LEFT)
        arrow.next_to(coef_poly, RIGHT)
        new_challenge.next_to(arrow, RIGHT)

        self.play(
            ShowCreation(arrow),
            FadeIn(new_challenge, 0.5 * RIGHT),
        )
        self.wait()

        # Show general expansion
        rs = [f"r_{i}" for i in range(3)]
        gen_factored = factored_poly_tex(rs, root_colors=[YELLOW, GREEN])
        gen_expanded = expanded_poly_tex(rs, vertical=False, root_colors=[YELLOW, GREEN])
        for gen, old in (gen_factored, factored), (gen_expanded, cleaner_expanded):
            gen.match_height(old)
            gen.move_to(old, LEFT)

        self.play(FadeTransformPieces(factored, gen_factored))
        self.wait()
        for i in range(1, 4):
            self.play(
                cleaner_expanded[0].animate.set_opacity(1),
                equals.animate.set_opacity(1),
                FadeTransformPieces(cleaner_expanded[i], gen_expanded[i]),
                cleaner_expanded[i + 1:].animate.next_to(gen_expanded[i], RIGHT, SMALL_BUFF)
            )
            self.wait()
        self.remove(cleaner_expanded)
        self.add(gen_expanded)

        full_factored = VGroup(back_rect, gen_factored, equals, gen_expanded)

        # Show system of equations
        system = get_symmetric_system([7, 14, 8], root_colors=[YELLOW, GREEN])
        system.next_to(full_factored, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        coef_terms = answer[1::2]
        rhss = [term[2:-2] for term in gen_expanded[1:]]

        for coef, rhs, eq in zip(coef_terms, rhss, system):
            self.play(
                FadeTransform(coef.copy(), eq[0]),
                FadeIn(eq[1]),
                FadeTransform(rhs.copy(), eq[2:]),
            )
            self.wait()

        cubic_example = VGroup(coef_poly, full_factored, system)

        # Show quintic
        q_roots = [-1, 1, 2, 4, 6]
        q_coefs = roots_to_coefficients(q_roots)
        q_poly = poly_tex(q_coefs)
        q_poly_factored = factored_poly_tex(
            [f"r_{i}" for i in range(5)],
            root_colors=[YELLOW, GREEN]
        )
        VGroup(q_poly, q_poly_factored).scale(0.8)
        q_poly.to_corner(UL)
        q_poly_factored.next_to(q_poly, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(
            FadeOut(cubic_example, DOWN),
            FadeOut(VGroup(arrow, new_challenge), DOWN),
            FadeIn(q_poly, DOWN)
        )

        y_scale_factor = 0.1
        new_graph = axes.get_graph(
            lambda x: y_scale_factor * poly(x, q_coefs),
            x_range=(-1.2, 6.2)
        )
        new_root_dots = Group(*(
            GlowDot(axes.c2p(x, 0))
            for x in q_roots
        ))
        new_graph.match_style(graph)
        axes.save_state()
        graph.save_state()
        root_dots.save_state()
        self.play(
            Transform(graph, new_graph),
            Transform(root_dots, new_root_dots),
        )
        self.wait()

        root_terms = q_poly_factored.get_parts_by_tex("r_")
        self.play(
            FadeIn(q_poly_factored, lag_ratio=0.1, run_time=2),
            LaggedStart(*(
                FadeTransform(dot.copy(), term, remover=True)
                for dot, term in zip(root_dots, root_terms)
            ), lag_ratio=0.5, run_time=3)
        )
        self.wait()

        # Quintic system
        signed_coefs = [
            (-1)**k * c for
            k, c in zip(it.count(1), q_coefs[-2::-1])
        ]
        q_system, q_system_full = [
            get_symmetric_system(
                signed_coefs,
                abbreviate=abbrev,
                root_colors=[YELLOW, GREEN],
            )
            for abbrev in [True, False]
        ]
        for mob in q_system, q_system_full:
            mob.scale(0.8)
            mob.next_to(q_poly_factored, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        root_tuple_groups = VGroup(*(
            VGroup(*(
                VGroup(*tup)
                for tup in it.combinations(root_terms, k)
            ))
            for k in range(1, 6)
        ))

        for equation, tuple_group in zip(q_system, root_tuple_groups):
            self.play(FadeIn(equation))
            self.wait(0.25)

            rects_group = VGroup(*(
                VGroup(*(
                    SurroundingRectangle(term).set_stroke(BLUE, 2)
                    for term in tup
                ))
                for tup in tuple_group
            ))
            terms_column = VGroup(*(
                VGroup(*tup).copy().arrange(RIGHT, buff=SMALL_BUFF)
                for tup in tuple_group
            ))
            terms_column.arrange(DOWN)
            terms_column.move_to(4 * RIGHT).to_edge(UP)

            anims = [
                ShowSubmobjectsOneByOne(rects_group, rate_func=linear),
                ShowIncreasingSubsets(terms_column, rate_func=linear, int_func=np.ceil),
            ]
            if equation is q_system[1]:
                anims.append(
                    Group(axes, graph, root_dots).animate.scale(
                        0.5, about_point=axes.c2p(5, -3)
                    )
                )
            self.play(*anims, run_time=0.25 * len(terms_column))
            self.remove(rects_group)
            self.wait()
            self.play(FadeOut(terms_column))
            self.wait()
        self.wait()

        frame = self.camera.frame
        frame.save_state()
        self.play(
            frame.animate.replace(q_system_full, dim_to_match=0).scale(1.1),
            FadeIn(q_system_full, lag_ratio=0.1),
            FadeOut(q_system),
            Group(axes, graph, root_dots).animate.shift(2 * DOWN),
            run_time=2,
        )
        self.wait(2)

        # Back to cubic
        self.play(
            Restore(axes),
            Restore(graph),
            Restore(root_dots),
            FadeOut(q_system_full, 2 * DOWN),
            FadeOut(q_poly, 2 * DOWN),
            FadeOut(q_poly_factored, 2 * DOWN),
            FadeIn(cubic_example, 2 * DOWN),
            Restore(frame),
            run_time=2,
        )
        self.wait()

        # Can you always factor?
        question = Text("Is this always possible?")
        question.add_background_rectangle(buff=0.1)
        question.next_to(gen_factored, RIGHT, buff=2)
        question.to_edge(UP, buff=MED_SMALL_BUFF)
        arrow = Arrow(question.get_left(), gen_factored.get_corner(UR))

        self.play(
            FadeIn(question),
            ShowCreation(arrow),
            FlashAround(gen_factored, run_time=3)
        )
        self.wait()
        self.play(FadeOut(question), FadeOut(arrow))

        const_dec = DecimalNumber(8)
        top_const_dec = const_dec.copy()
        for dec, mob, vect in (const_dec, system[2][0], RIGHT), (top_const_dec, answer[-1][1], LEFT):
            dec.match_height(mob)
            dec.move_to(mob, vect)
            dec.set_color(RED)
            mob.set_opacity(0)
            self.add(dec)
        answer[-1][0].set_color(RED)

        top_const_dec.add_updater(lambda m: m.set_value(const_dec.get_value()))

        def get_coefs():
            return [-const_dec.get_value(), 14, -7, 1]

        def get_roots():
            return coefficients_to_roots(get_coefs())

        def update_graph(graph):
            graph.become(axes.get_graph(lambda x: poly(x, get_coefs())))
            graph.set_stroke(BLUE, 3)

        def update_root_dots(dots):
            roots = get_roots()
            for root, dot in zip(roots, dots):
                if abs(root.imag) > 1e-8:
                    dot.set_opacity(0)
                else:
                    dot.move_to(axes.c2p(root.real, 0))
                    dot.set_opacity(1)

        graph.add_updater(update_graph)
        self.remove(*root_dots, *new_root_dots)
        root_dots = root_dots[:3]
        root_dots.add_updater(update_root_dots)
        self.add(root_dots)

        example_constants = [5, 6, 9, 6.28]
        for const in example_constants:
            self.play(
                ChangeDecimalToValue(const_dec, const),
                run_time=3,
            )
            self.wait()

        # Show complex plane
        plane = ComplexPlane(
            (-1, 6), (-3, 3)
        )
        plane.replace(axes.x_axis.ticks, dim_to_match=0)
        plane.add_coordinate_labels(font_size=24)
        plane.save_state()
        plane.rotate(PI / 2, LEFT)
        plane.set_opacity(0)

        real_label = Text("Real numbers")
        real_label.next_to(root_dots, UP, SMALL_BUFF)
        complex_label = Text("Complex numbers")
        complex_label.set_backstroke()
        complex_label.next_to(plane.saved_state.get_corner(UR), DL, SMALL_BUFF)

        graph.clear_updaters()
        root_dots.clear_updaters()
        axes.generate_target(use_deepcopy=True)
        axes.target.y_axis.set_opacity(0)
        axes.target.x_axis.numbers.set_opacity(1)
        self.play(
            Uncreate(graph),
            Write(real_label),
            MoveToTarget(axes),
        )
        self.wait(2)
        self.add(plane, root_dots, real_label)
        self.play(
            Restore(plane),
            FadeOut(axes.x_axis),
            FadeTransform(real_label, complex_label),
            run_time=2,
        )
        self.wait(2)

        self.play(
            VGroup(coef_poly, top_const_dec).animate.next_to(plane, UP),
            gen_factored.animate.next_to(plane, UP, buff=1.2),
            FadeOut(equals),
            FadeOut(gen_expanded),
            frame.animate.shift(DOWN),
            run_time=2,
        )
        self.wait()

        eq_zero = OldTex("= 0")
        eq_zero.scale(0.7)
        eq_zero.next_to(top_const_dec, RIGHT, SMALL_BUFF)
        eq_zero.shift(0.2 * LEFT)
        self.play(
            Write(eq_zero),
            VGroup(coef_poly, top_const_dec).animate.shift(0.2 * LEFT),
        )
        self.wait()

        # Show constant tweaking again
        def update_complex_roots(root_dots):
            for root, dot in zip(get_roots(), root_dots):
                dot.move_to(plane.n2p(root))

        root_dots.add_updater(update_complex_roots)

        self.play(
            FlashAround(const_dec),
            FlashAround(top_const_dec),
            run_time=2,
        )

        self.play(
            ChangeDecimalToValue(const_dec, 4),
            run_time=3,
        )
        self.wait()
        root_eqs = VGroup(*(
            VGroup(OldTex(f"r_{i} ", "="), DecimalNumber(root, num_decimal_places=3)).arrange(RIGHT)
            for i, root in enumerate(get_roots())
        ))
        root_eqs.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        for eq in root_eqs:
            eq[0][0].set_color(YELLOW)
        root_eqs.next_to(system, UP)
        root_eqs.align_to(gen_factored, UP)
        self.play(
            FadeIn(root_eqs),
            VGroup(system, const_dec).animate.next_to(root_eqs, DOWN, LARGE_BUFF),
        )
        self.wait(2)
        self.play(FadeOut(root_eqs))

        example_constants = [4, 7, 9, 5]
        for const in example_constants:
            self.play(
                ChangeDecimalToValue(const_dec, const),
                run_time=3,
            )
            self.wait()

    def add_axes(self):
        x_range = (-1, 6)
        y_range = (-3, 11)
        axes = Axes(
            x_range, y_range,
            axis_config=dict(include_tip=False, numbers_to_exclude=[]),
            # CHANGE: the misspelled kwarg `widith` is removed (the original ignored it; now Axes raises TypeError)
            height=abs(op.sub(*y_range)),
        )
        axes.set_height(FRAME_HEIGHT - 1)
        axes.to_edge(RIGHT)
        axes.x_axis.add_numbers(font_size=24)
        axes.x_axis.numbers[1].set_opacity(0)

        self.add(axes)
        return axes
