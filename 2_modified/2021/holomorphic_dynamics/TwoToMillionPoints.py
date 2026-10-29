# ==============================================================================
# Scene:      TwoToMillionPoints
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2102-2144)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl TwoToMillionPoints.py TwoToMillionPoints -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal, MandelbrotFractal, JuliaFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
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



# ----- From _2021/newton_fractal.py -----

ROOT_COLORS_DEEP = ["#440154", "#3b528b", "#21908c", "#5dc963", "#29abca"]


# CHANGE: manimgl's NewtonFractal, MandelbrotFractal, JuliaFractal are used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
# copy, with GLSL shaders (`shader_folder`), which this manimgl cannot use, was here.


# ----- From _2021/holomorphic_dynamics.py -----

MANDELBROT_COLORS = [
    "#00065c",
    "#061e7e",
    "#0c37a0",
    "#205abc",
    "#4287d3",
    "#D9EDE4",
    "#F0F9E4",
    "#BA9F6A",
    "#573706",
]


class TwoToMillionPoints(Scene):
    c = -0.18 + 0.77j
    plane_height = 7

    def construct(self):
        plane, julia_fractal = self.get_plane_and_fractal()

        words = OldTexText("$\\approx 2^{1{,}000{,}000}$ solutions!")
        words.set_stroke(BLACK, 8, background=True)
        words.move_to(plane, UL)
        words.shift(MED_SMALL_BUFF * DR)

        points = self.get_julia_set_points(plane, 100000, 1000)
        dots = DotCloud(points)
        dots.set_color(YELLOW)
        dots.set_opacity(1)
        dots.set_radius(0.025)
        dots.add_updater(lambda m: m)
        dots.make_3d()

        self.add(julia_fractal, plane, words)
        self.play(ShowCreation(dots, run_time=10))

    def get_plane_and_fractal(self):
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(self.plane_height)
        fractal = JuliaFractal(plane)
        fractal.set_c(self.c)
        return plane, fractal

    def get_julia_set_points(self, plane, n_points, n_steps):
        values = np.array([
            complex(math.cos(x), math.sin(x))
            for x in np.linspace(0, TAU, n_points)
        ])

        c = self.c
        for n in range(n_steps):
            units = -1 + 2 * np.random.randint(0, 2, len(values))
            values[:] = (units * np.sqrt(values[:])) - c
        values += c

        return np.array(list(map(plane.n2p, values)))
