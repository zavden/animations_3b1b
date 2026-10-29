# ==============================================================================
# Scene:      MandelbrotSetPreview
# Source:     videos/_2021/holomorphic_dynamics.py (lines 118-140)
# Category:   2 · Renders with modifications
# Includes code copied from: _2021/newton_fractal.py, _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl MandelbrotSetPreview.py MandelbrotSetPreview -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal, MandelbrotFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
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


# CHANGE: manimgl's NewtonFractal, MandelbrotFractal are used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
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


class MandelbrotSetPreview(Scene):
    def construct(self):
        plane = ComplexPlane(
            (-2, 1), (-2, 2),
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.5,
            }
        )
        plane.set_width(0.7 * FRAME_WIDTH)
        plane.axes.set_stroke(opacity=0.5)
        plane.add_coordinate_labels(font_size=18)

        mandelbrot = MandelbrotFractal(plane)
        mandelbrot.set_n_steps(0)

        self.add(mandelbrot, plane)
        self.play(
            mandelbrot.animate.set_n_steps(300),
            rate_func=lambda a: a**3,
            run_time=10,
        )
        self.wait()
