# ==============================================================================
# Scene:      ShowFatouDiskExample
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3065-3110)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl ShowFatouDiskExample.py ShowFatouDiskExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal, MandelbrotFractal, JuliaFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - self.play(..., path_arc=...) -> animate(path_arc=...) in each animation (Scene.play no longer accepts path_arc)
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


class ShowFatouDiskExample(Scene):
    disk_radius = 0.1
    n_steps = 14

    def construct(self):
        c = -1.06 + 0.11j
        plane = ComplexPlane((-3, 3), (-2, 2))
        for line in plane.family_members_with_points():
            line.set_stroke(opacity=0.5 * line.get_stroke_opacity())
        plane.set_height(1.8 * FRAME_HEIGHT)
        plane.add_coordinate_labels(font_size=18)
        fractal = JuliaFractal(plane, parameter=c)

        # z0 = -1.1 + 0.1j
        z0 = -0.3 + 0.2j

        dot = Dot(plane.n2p(z0), radius=0.025)
        dot.set_fill(YELLOW)

        disk = dot.copy()
        disk.set_height(2 * self.disk_radius * plane.get_x_unit_size())
        disk.set_fill(YELLOW, 0.5)
        disk.set_stroke(YELLOW, 1.0)
        disk.insert_n_curves(1000)

        def func(point):
            return plane.n2p(plane.p2n(point)**2 + c)

        self.add(fractal, plane)
        self.add(disk, dot)
        self.play(DrawBorderThenFill(disk))

        path_arc = 10 * DEGREES
        for n in range(self.n_steps):
            point = dot.get_center()
            new_point = func(point)
            arrow = Arrow(point, new_point, path_arc=path_arc, buff=0.1)
            # CHANGE: Scene.play no longer accepts path_arc: it is passed to each animation with animate(path_arc=...)
            self.play(
                dot.animate(path_arc=path_arc).move_to(new_point),
                disk.animate(path_arc=path_arc).apply_function(func),
                ShowCreation(arrow),
            )
            self.play(FadeOut(arrow))

        self.embed()
