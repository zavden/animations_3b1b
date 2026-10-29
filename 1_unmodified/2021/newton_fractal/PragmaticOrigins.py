# ==============================================================================
# Scene:      PragmaticOrigins
# Source:     videos/_2021/newton_fractal.py (lines 202-305)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl PragmaticOrigins.py PragmaticOrigins -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2022/quintic/roots_and_coefs.py -----

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



# ----- From _2021/newton_fractal.py -----

def glow_dot(point, r_min=0.05, r_max=0.15, color=YELLOW, n=20, opacity_mult=1.0):
    result = VGroup(*(
        Dot(point, radius=interpolate(r_min, r_max, a))
        for a in np.linspace(0, 1, n)
    ))
    result.set_fill(color, opacity=opacity_mult / n)
    return result


class PragmaticOrigins(Scene):
    title = "Pragmatic origins"
    include_pi = False

    def construct(self):
        # Title
        title = Text(self.title, font_size=72)
        title.set_stroke(BLACK, 5, background=True)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Underline(title, buff=-0.05)
        underline.insert_n_curves(30)
        underline.set_stroke(BLUE, width=[0, 3, 3, 3, 0])
        underline.scale(1.5)

        # Axes
        axes = NumberPlane(
            x_range=(-3, 3),
            y_range=(-4, 4),
            width=6,
            height=8,
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            }
        )
        axes.set_height(5.0)
        axes.to_corner(DL)
        axes.shift(0.5 * UP)

        coefs = np.array([2, -3, 1, -2, -1, 1], dtype=np.float)
        roots = [
            r.real
            for r in coefficients_to_roots(coefs)
            if abs(r.imag) < 1e-2
        ]
        roots.sort()
        coefs *= 0.2

        solve = OldTexText("Solve $f(x) = 0$", font_size=36)
        solve.next_to(axes, UP, aligned_edge=LEFT)
        expr = OldTex("f(x) = x^5 - x^4 - 2x^3 + x^2 -3x + 2")
        expr.match_width(axes)
        expr.next_to(axes, DOWN)
        graph_x_range = (-2, 2.4)
        graph = axes.get_graph(
            lambda x: poly(x, coefs),
            x_range=graph_x_range
        )
        graph.set_stroke(BLUE, [0, *50 * [4], 0])
        root_dots = VGroup(*(
            glow_dot(axes.c2p(root, 0))
            for root in roots
        ))
        root_eqs = VGroup()
        root_groups = VGroup()
        for i, root, dot in zip(it.count(1), roots, root_dots):
            lhs = OldTex(f"x_{i} = ")
            rhs = DecimalNumber(root, num_decimal_places=3)
            rhs.set_color(YELLOW)
            eq = VGroup(lhs, rhs)
            eq.arrange(RIGHT, aligned_edge=DOWN)
            rhs.align_to(lhs.family_members_with_points()[0], DOWN)
            root_eqs.add(eq)
            root_groups.add(VGroup(eq, dot))
        root_eqs.arrange(RIGHT, buff=LARGE_BUFF)
        root_eqs.next_to(axes, RIGHT, aligned_edge=UP)

        self.add(axes)
        self.add(solve)
        self.add(expr)

        # Pi
        if self.include_pi:
            morty = Mortimer(height=2)
            morty.to_corner(DR)
            self.play(PiCreatureSays(
                morty, "How do you\nfind theses?",
                target_mode="tease",
                bubble_config={
                    "width": 4,
                    "height": 2.5,
                }
            ))

        # Animations
        self.add(underline, title)
        self.play(
            ShowCreation(underline),
        )
        self.wait()

        alphas = [inverse_interpolate(*graph_x_range, root) for root in roots]
        self.play(
            ShowCreation(graph, rate_func=linear),
            *(
                FadeIn(
                    rg,
                    rate_func=squish_rate_func(rush_from, a, min(a + 0.2, 1))
                )
                for rg, a in zip(root_groups, alphas)
            ),
            run_time=4,
        )
        self.wait()
