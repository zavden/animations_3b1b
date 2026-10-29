# ==============================================================================
# Scene:      RepeatedNewton
# Source:     videos/_2021/newton_fractal.py (lines 3283-3502)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl RepeatedNewton.py RepeatedNewton -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's NewtonFractal classes (GLSL shaders) are removed and manimgl's are used (manimlib/mobject/fractals.py, WGSL shaders)
#   - The fractal orders the roots with the scene's coefficients_to_roots (like Grant), not with np.roots, so that each root keeps its color
#   - `fractal.colors` (manimgl does not store it) -> get_fractal_colors(fractal), which reads the colors from the uniform
#   - DotCloud(gloss=, shadow=) -> shading=(0.0, gloss, shadow) (Mobject.__init__ no longer accepts gloss/shadow)
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

ROOT_COLORS_BRIGHT = [RED, GREEN, BLUE, YELLOW, MAROON_B]


ROOT_COLORS_DEEP = ["#440154", "#3b528b", "#21908c", "#5dc963", "#29abca"]


def glow_dot(point, r_min=0.05, r_max=0.15, color=YELLOW, n=20, opacity_mult=1.0):
    result = VGroup(*(
        Dot(point, radius=interpolate(r_min, r_max, a))
        for a in np.linspace(0, 1, n)
    ))
    result.set_fill(color, opacity=opacity_mult / n)
    return result


def get_newton_rule(font_size=36, var="z", **kwargs):
    terms = [f"{var}_n", f"{var}_{{n + 1}}"]
    t0, t1 = terms
    return OldTex(
        t1, "=", t0, "-",
        "{P(", t0, ")", "\\over ", "P'(", t0, ")}",
        font_size=36,
        **kwargs
    )


def coefs_to_poly_string(coefs):
    n = len(coefs) - 1
    tex_str = "" if coefs[-1] == 1 else str(int(coefs[-1]))
    tex_str += f"z^{{{n}}}"
    for c, k in zip(coefs[-2::-1], it.count(n - 1, -1)):
        if c == 0:
            continue
        if isinstance(c, complex):
            num_str = "({:+}".format(int(c.real))
            num_str += "+ {:+})".format(int(c.imag))
        else:
            num_str = "{:+}".format(int(c))
        if abs(c) == 1 and k > 0:
            num_str = num_str[:-1]
        tex_str += num_str
        if k == 0:
            continue
        elif k == 1:
            tex_str += "z"
        else:
            tex_str += f"z^{{{k}}}"
    return tex_str


# CHANGE: manimgl's NewtonFractal is used (manimlib/mobject/fractals.py, WGSL shaders). Grant's
# copy, with GLSL shaders (`shader_folder`), which this manimgl cannot use, was here.

# CHANGE: manimgl orders the roots of some coefficients with np.roots; Grant ordered them with the
# coefficients_to_roots above (the one from roots_and_coefs), and which root gets which color
# depends on that order. The scene's own is used so that the basins match the root points.
import manimlib.mobject.fractals as _manimgl_fractals
_manimgl_fractals.coefficients_to_roots = coefficients_to_roots

# CHANGE: manimgl does not store `fractal.colors`; the colors of each root are read from its uniform
def get_fractal_colors(fractal):
    return [rgb_to_hex(rgba[:3]) for rgba in fractal.uniforms["colors"][:len(fractal.roots)]]


class RepeatedNewton(Scene):
    coefs = [1.0, -1.0, 1.0, 0.0, 0.0, 1.0]
    plane_config = {
        "x_range": (-4, 4),
        "y_range": (-2, 2),
        "height": 8,
        "width": 16,
    }
    dots_config = {
        "radius": 0.05,
        "color": GREY_A,
        # CHANGE: DotCloud no longer accepts gloss/shadow as arguments: they are passed as shading=(reflectiveness, gloss, shadow)
        "shading": (0.0, 0.4, 0.1),
        "opacity": 0.5,
    }
    arrow_style = {
        "stroke_color": WHITE,
        "stroke_opacity": 0.5,
    }
    dot_density = 5.0
    points_scalar = 1.0
    n_steps = 10
    colors = ROOT_COLORS_BRIGHT
    show_coloring = True
    show_arrows = True
    highlight_equation = False
    corner_group_height = 2.0
    step_run_time = 1.0
    show_fractal_background = False

    def construct(self):
        self.add_plane()
        self.add_true_roots()
        self.add_labels()
        if self.show_fractal_background:
            self.add_fractal_background()
        self.add_dots()
        self.run_iterations()
        if self.show_coloring:
            self.color_points()
            self.revert_to_original_positions()

    def add_plane(self):
        plane = self.plane = ComplexPlane(**self.plane_config)
        plane.add_coordinate_labels(font_size=24)

        self.add(plane)

    def add_labels(self):
        eq_label = self.eq_label = OldTex(
            "P(z) = " + coefs_to_poly_string(self.coefs),
            font_size=36
        )

        rule_label = self.rule_label = get_newton_rule()
        rule_label.next_to(eq_label, DOWN, MED_LARGE_BUFF)

        corner_rect = SurroundingRectangle(
            VGroup(eq_label, rule_label),
            buff=MED_SMALL_BUFF
        )
        corner_rect.set_fill(BLACK, 0.9)
        corner_rect.set_stroke(WHITE, 1)

        self.corner_group = VGroup(
            corner_rect,
            eq_label,
            rule_label,
        )
        self.corner_group.set_height(self.corner_group_height)
        self.corner_group.to_corner(UL, buff=0)
        self.add(self.corner_group)

    def add_true_roots(self):
        roots = self.roots = coefficients_to_roots(self.coefs)
        root_dots = self.root_dots = VGroup(*(
            glow_dot(self.plane.n2p(root), color=color, opacity_mult=2.0)
            for root, color in zip(roots, self.colors)
        ))

        self.add(root_dots)

    def add_dots(self):
        dots = self.dots = DotCloud(
            self.get_original_points(), **self.dots_config
        )

        self.add(dots, self.corner_group)
        self.play(ShowCreation(dots))

    def get_original_points(self):
        step = 1.0 / self.dot_density
        return self.points_scalar * np.array([
            self.plane.c2p(x, y)
            for x in np.arange(*self.plane.x_range[:2], step)
            for y in np.arange(*self.plane.y_range[:2], step)
        ])

    def run_iterations(self):
        self.points_history = []
        for x in range(self.n_steps):
            self.points_history.append(self.dots.get_points().copy())
            self.take_step(run_time=self.step_run_time)

    def update_z(self, z, epsilon=1e-6):
        denom = dpoly(z, self.coefs)
        if abs(denom) < epsilon:
            denom = epsilon
        return z - poly(z, self.coefs) / denom

    def take_step(self, run_time=1.0):
        plane = self.plane
        points = self.dots.get_points()

        zs = map(plane.p2n, points)
        new_zs = map(self.update_z, zs)
        new_points = list(map(plane.n2p, new_zs))

        added_anims = []
        if self.show_arrows:
            arrows = []
            max_len = 0.5 * plane.get_x_unit_size() / self.dot_density
            for p1, p2 in zip(points, new_points):
                vect = p2 - p1
                norm = get_norm(vect)
                if norm > max_len:
                    vect = normalize(vect) * max_len
                arrows.append(Vector(vect, **self.arrow_style).shift(p1))
            arrows = VGroup(*arrows)
            self.add(arrows, self.dots, self.corner_group)
            self.play(ShowCreation(arrows, lag_ratio=0))
            added_anims.append(FadeOut(arrows))

        self.play(
            self.dots.animate.set_points(new_points),
            *added_anims,
            run_time=run_time,
        )
        self.dots.filter_out(lambda p: get_norm(p) > FRAME_WIDTH)

    def color_points(self):
        root_points = [rd.get_center() for rd in self.root_dots]
        rgbas = list(map(color_to_rgba, self.colors))

        def get_rgba(point):
            norms = [get_norm(point - rp) for rp in root_points]
            return rgbas[np.argmin(norms)]

        rgbas = list(map(get_rgba, self.dots.get_points()))

        fractal = NewtonFractal(
            self.plane,
            coefs=self.coefs,
            colors=self.colors,
            n_steps=0,
        )
        fractal.set_opacity(0)

        self.add(fractal, self.plane, self.dots, self.corner_group)
        radius = self.dots.get_radius()
        self.play(
            fractal.animate.set_opacity(0.5),
            self.dots.animate.set_rgba_array(rgbas).set_radius(1.5 * radius),
        )
        self.play(
            fractal.animate.set_opacity(0),
            self.dots.animate.set_radius(radius),
        )
        self.remove(fractal)

    def revert_to_original_positions(self):
        for ph in self.points_history[::-1]:
            self.play(
                self.dots.animate.set_points(ph),
                run_time=0.5,
            )

    def reveal_fractal(self, **kwargs):
        plane = self.plane

        fractal = self.fractal = self.get_fractal(**kwargs)
        root_dot_backs = VGroup(*(Dot(rd.get_center(), radius=0.1) for rd in self.root_dots))
        root_dot_backs.set_stroke(BLACK, 2)
        root_dot_backs.set_fill(opacity=0)

        plane.generate_target(use_deepcopy=True)
        for lines in plane.target.background_lines, plane.target.faded_lines:
            lines.set_stroke(WHITE)
            for line in lines.family_members_with_points():
                line.set_opacity(line.get_stroke_opacity() * 0.5)

        self.root_dots.generate_target()
        # CHANGE: fractal.colors -> get_fractal_colors(fractal)
        for rd, color in zip(self.root_dots.target, get_fractal_colors(fractal)):
            rd.set_fill(color)

        self.add(fractal, *self.mobjects, root_dot_backs)
        self.play(
            FadeIn(fractal),
            FadeOut(self.dots),
            FadeIn(root_dot_backs),
            MoveToTarget(plane),
            MoveToTarget(self.root_dots),
        )
        self.wait()

    def get_fractal(self, **kwargs):
        if "colors" not in kwargs:
            kwargs["colors"] = self.colors
        self.fractal = NewtonFractal(self.plane, coefs=self.coefs, **kwargs)
        return self.fractal

    def add_fractal_background(self):
        fractal = self.get_fractal()
        fractal.set_opacity(0.1)
        fractal.set_n_steps(12)
        boundary = self.fractal_boundary = fractal.copy()
        boundary.set_colors(5 * [WHITE])
        boundary.set_julia_highlight(1e-4)
        boundary.set_opacity(0.25)
        self.add(fractal, boundary, *self.mobjects)
