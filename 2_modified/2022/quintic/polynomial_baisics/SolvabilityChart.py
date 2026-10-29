# ==============================================================================
# Scene:      SolvabilityChart
# Source:     videos/_2022/quintic/polynomial_baisics.py (lines 997-1226)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl SolvabilityChart.py SolvabilityChart -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingShapes.get_mobject_key no longer exists: a local get_mobject_key is defined (hash of the points centered and at height 1, as before)
#
# Notes:
#   It ends with self.embed() (in the original, to keep working live); with -w it is ignored and the full animation is rendered.
# ==============================================================================

from manim_imports_ext import *


# CHANGE: TransformMatchingShapes.get_mobject_key no longer exists in manimgl (it is now compared with
# has_same_shape_as); the previous computation is restored here: hash of the points of the mobject centered and at
# height 1
def get_mobject_key(mobject):
    mobject.save_state()
    mobject.center()
    mobject.set_height(1)
    result = hash(np.round(mobject.get_points(), 3).tobytes())
    mobject.restore()
    return result


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


def get_quadratic_formula(lhs="", **tex_config):
    return Tex(
        lhs + "{-{b} \\pm \\sqrt{ {b}^2 - 4{a}{c} } \\over 2{a} }",
        **tex_config
    )


def get_full_cubic_formula(lhs="", **tex_config):
    # Thanks to Mathologer and MathPix here...
    return OldTex(lhs + """
        &\\sqrt[3]{\\left(-{ {b}^{3} \\over 27 {a}^{3}}+{ {b} {c} \\over 6 {a}^{2}}
            -{ {d} \\over 2 {a} }\\right)-\\sqrt{\\left(-{ {b}^{3} \\over 27 {a}^{3}}
            +{ {b} {c} \\over 6 {a}^{2}}-{ {d} \\over 2 {a}}\\right)^{2}
            +\\left({ {c} \\over 3 {a} }-{ {b}^{2} \\over 9 {a}^{2}}\\right)^{3}}} \\\\
        +&\\sqrt[3]{\\left(-{ {b}^{3} \\over 27 {a}^{3}}+{ {b} {c} \\over 6 {a}^{2}}
            -{ {d} \\over 2 {a} }\\right)+\\sqrt{\\left(-{ {b}^{3} \\over 27 {a}^{3}}
            +{ {b} {c} \\over 6 {a}^{2}}-{ {d} \\over 2 {a}}\\right)^{2}
            +\\left({ {c} \\over 3 {a} }-{ {b}^{2} \\over 9 {a}^{2} }\\right)^{3}}} \\\\
        -&{ {b} \\over 3 {a} }
    """, **tex_config)



# ----- From _2022/quintic/polynomial_baisics.py -----

class SolvabilityChart(Scene):
    def construct(self):
        # Preliminary terms
        frame = self.camera.frame
        frame.set_height(10)

        words = self.get_words(frame)
        equations = self.get_equations(words)
        s_words = self.get_solvability_words(equations)
        gen_form_words = Text("General form")
        gen_form_words.match_x(equations, LEFT)
        gen_form_words.match_y(s_words, UP)
        lines = self.get_lines(
            rows=VGroup(s_words, *words),
            cols=VGroup(words, equations, *s_words),
        )
        row_lines, col_lines = lines
        marks = self.get_marks(equations, s_words)

        # Shift colums
        marks[1].save_state()
        s_words[1].save_state()
        frame.save_state()
        frame.set_height(9, about_edge=DL)
        frame.shift(LEFT)
        VGroup(marks[1], s_words[1]).next_to(col_lines[1], RIGHT, MED_LARGE_BUFF)

        solvable_word = OldTexText("Can you solve\\\\for $x$?")
        solvable_word.move_to(s_words[1], DOWN)

        # Cover rects
        cover_rect = Rectangle()
        cover_rect.set_fill(BLACK, 1)
        cover_rect.set_stroke(BLACK, 0)
        cover_rect.replace(frame, stretch=True)
        cover_rect.add(VectorizedPoint(cover_rect.get_top() + 0.025 * UP))
        cover_rect.move_to(row_lines[1], UL).shift(LEFT)
        right_cover_rect = cover_rect.copy()
        right_cover_rect.next_to(s_words[1], RIGHT, buff=MED_LARGE_BUFF)
        right_cover_rect.match_y(frame)

        self.add(words, equations, solvable_word)
        self.add(row_lines, col_lines[:2])
        self.add(right_cover_rect, cover_rect)

        # Axes
        axes = self.get_axes(frame)
        coefs = np.array([1, 0.5, 0, 0, 0, 0])
        coef_tracker = ValueTracker(coefs)
        get_coefs = coef_tracker.get_value
        graph = always_redraw(lambda: axes.get_graph(
            lambda x: poly(x, get_coefs()),
            stroke_color=BLUE,
            stroke_width=2,
        ))
        root_dots = GlowDot()
        root_dots.add_updater(lambda m: m.set_points([
            axes.c2p(r.real, 0)
            for r in coefficients_to_roots(get_coefs())
            if abs(r.imag) < 1e-5 and abs(r.real) < 5
        ]))
        self.add(axes)

        # Linear equation
        tex_kw = dict(tex_to_color_map=self.get_tex_to_color_map())
        lin_solution = OldTex("x = {-{b} \\over {a}}", **tex_kw)
        lin_solution.scale(1.2)
        lin_solution.next_to(equations[0], DOWN, buff=2.0)

        self.wait()
        self.play(
            ShowCreation(graph),
            FadeIn(root_dots, rate_func=squish_rate_func(smooth, 0.3, 0.4)),
        )
        self.wait()
        self.play(TransformMatchingShapes(
            equations[0].copy(), lin_solution
        ))
        self.play(Write(marks[1][0]))
        self.wait()

        # Quadratic
        quadratic_formula = get_quadratic_formula(lhs="x = ", **tex_kw)
        quadratic_formula.next_to(equations[1], DOWN, buff=2.0)
        new_coefs = 0.2 * np.array([*roots_to_coefficients([-3, 2]), 0, 0, 0])

        self.play(
            cover_rect.animate.move_to(row_lines[2], UL).shift(LEFT),
            FadeOut(lin_solution, DOWN),
        )
        self.play(coef_tracker.animate.set_value(new_coefs))
        self.wait()
        self.play(TransformMatchingShapes(
            equations[1].copy(), quadratic_formula,
        ))
        self.play(Write(marks[1][1]))
        self.wait()

        # Cubic
        key_to_color = dict([
            (get_mobject_key(OldTex(c)[0][0]), color)
            for c, color in self.get_tex_to_color_map().items()
        ])
        full_cubic = get_full_cubic_formula(lhs="x = ")
        full_cubic.set_width(9)
        full_cubic.next_to(equations[2], DOWN, buff=1.0).shift(LEFT)
        for sm in full_cubic[0]:
            key = get_mobject_key(sm)
            sm.set_color(key_to_color.get(key, WHITE))
        new_coefs = 0.05 * np.array([*roots_to_coefficients([-4, -1, 3]), 0, 0])

        self.play(
            cover_rect.animate.move_to(row_lines[3], UL).shift(LEFT),
            FadeOut(quadratic_formula, DOWN),
        )
        self.play(coef_tracker.animate.set_value(new_coefs))
        self.wait()
        self.play(TransformMatchingShapes(
            equations[2].copy(), full_cubic,
            run_time=2
        ))
        self.wait()

        # Embed
        self.embed()

    def get_words(self, frame):
        words = VGroup(*map(Text, (
            "Linear",
            "Quadratic",
            "Cubic",
            "Quartic",
            "Quintic",
            "Sextic",
        )))
        words.add(OldTex("\\vdots"))
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        words.next_to(frame.get_corner(DL), UR, buff=1.0)
        words.shift(0.5 * LEFT)
        words[-1].match_x(words[-2])
        return words

    def get_equations(self, words):
        kw = dict(tex_to_color_map=self.get_tex_to_color_map())
        equations = VGroup(
            OldTex("{a}x + {b} = 0", **kw),
            OldTex("{a}x^2 + {b}x + {c} = 0", **kw),
            OldTex("{a}x^3 + {b}x^2 + {c}x + {d} = 0", **kw),
            OldTex("{a}x^4 + \\cdots + {d}x + {e} = 0", **kw),
            OldTex("{a}x^5 + \\cdots + {e}x + {f} = 0", **kw),
            OldTex("{a}x^6 + \\cdots + {f}x + {g} = 0", **kw),
            OldTex("\\vdots", **kw),
        )
        equations.arrange(DOWN, aligned_edge=LEFT)
        equations.next_to(words, RIGHT, LARGE_BUFF)
        for eq, word in zip(equations, words):
            dy = word[-1].get_bottom()[1] - eq[0][0].get_bottom()[1]
            eq.shift(dy * UP)
        equations[-1].match_y(words[-1])
        equations[-1].match_x(equations[-2])
        return equations

    def get_solvability_words(self, equations):
        operations = ["+", "-", "\\times", "/", "\\sqrt[n]{\\quad}"]
        arith, radicals = (
            "$" + " ,\\, ".join(operations[s]) + "$"
            for s in (slice(None, -1), slice(None))
        )
        s_words = VGroup(
            OldTexText("Solvable", " using\\\\", arith),
            OldTexText("Solvable", " using\\\\", radicals),
            OldTexText("Solvable\\\\", "numerically"),
        )
        s_words.arrange(RIGHT, buff=LARGE_BUFF, aligned_edge=UP)
        s_words.next_to(equations, UR, buff=MED_LARGE_BUFF)
        s_words.shift(MED_LARGE_BUFF * RIGHT)

        return s_words

    def get_lines(self, rows, cols, color=GREY_A, width=2):
        row_line = Line(cols.get_left(), cols.get_right())
        row_lines = row_line.replicate(len(rows) - 1)
        for r1, r2, rl in zip(rows, rows[1:], row_lines):
            rl.match_y(midpoint(r1.get_bottom(), r2.get_top()))

        col_line = Line(rows.get_top(), rows.get_bottom())
        col_lines = col_line.replicate(len(cols) - 1)
        for c1, c2, cl in zip(cols, cols[1:], col_lines):
            cl.match_x(midpoint(c1.get_right(), c2.get_left()))

        col_lines[0].match_height(Group(row_lines, Point(col_lines.get_bottom())), about_edge=DOWN)

        lines = VGroup(row_lines, col_lines)
        lines.set_stroke(color, width)
        return lines

    def get_marks(self, equations, solvability_words):
        pre_marks = [
            "cxxxxxx",
            "ccccxxx",
            "ccccccc",
        ]
        marks = VGroup(*(
            VGroup(*(
                Checkmark() if pm == 'c' else Exmark()
                for pm in pm_list
            ))
            for pm_list in pre_marks
        ))
        for mark_group, s_word in zip(marks, solvability_words):
            mark_group.match_x(s_word)
            for mark, eq in zip(mark_group, equations):
                mark.match_y(eq)
        return marks

    def get_axes(self, frame):
        axes = Axes((-5, 5), (-5, 5), height=10, width=10)
        axes.set_width(4)
        axes.next_to(frame.get_corner(DR), UL)
        axes.add(OldTex("x", font_size=24).next_to(axes.x_axis.get_right(), DOWN, SMALL_BUFF))
        axes.add(OldTex("y", font_size=24).next_to(axes.y_axis.get_top(), LEFT, SMALL_BUFF))
        return axes

    def get_tex_to_color_map(self):
        chars = "abcdefg"
        colors = color_gradient([RED_B, RED_C, RED_D], len(chars))
        return dict(
            (f"{{{char}}}", color)
            for char, color in zip(chars, colors)
        )
