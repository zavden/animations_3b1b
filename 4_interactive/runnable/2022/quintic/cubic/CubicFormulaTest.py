# ==============================================================================
# Scene:      CubicFormulaTest
# Source:     videos/_2022/quintic/cubic.py (lines 283-285)
# Category:   4 · Interactive (runnable)
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl CubicFormulaTest.py CubicFormulaTest -w -m --fps 15
#     manimgl CubicFormulaTest.py CubicFormulaTest        # interactive window
#
# How to interact:
#   Run it without -w (`manimgl CubicFormulaTest.py CubicFormulaTest`) to play in the window (construct is empty, everything is interaction). Top: the coefficient plane of x^3 + p x + q = (x - r0)(x - r1)(x - r2) (points q, p and the fixed 0 of the quadratic term) and the plane of the 3 roots. Bottom, the three steps of Cardano's formula: the square root δ1, δ2 = sqrt(q^2/4 + p^3/27) (green), the cube roots of -q/2 + δ1 and of -q/2 + δ2 (red and blue) and their sum (yellow), which coincides with the roots of the polynomial. Click a coefficient or root point to make it follow the mouse (another click drops it); the other planes update by themselves and leave trails. Hold `r` while clicking to move only horizontally; hold `a` while clicking a coefficient to keep its modulus; hold `c`, click several roots and release `c` to swap them cyclically, or with a coefficient to make it go around a full turn around the pointer. Watch how the branch of the cube/square root being used changes when the coefficient goes around.
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed background_stroke_width/background_stroke_color from OldTex's kwargs (they no longer exist in Mobject; a later set_backstroke() does the same)
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


def get_nth_roots(z, n):
    base_root = z**(1 / n)
    return [
        base_root * np.exp(complex(0, k * TAU / n))
        for k in range(n)
    ]


def sort_to_minimize_distances(unordered_points, reference_points):
    """
    Sort the initial list of points in R^n so that the sum
    of the distances between corresponding points in both lists
    is smallest
    """
    ordered_points = []
    unused_points = list(unordered_points)

    for ref_point in reference_points:
        distances = [get_norm(ref_point - up) for up in unused_points]
        index = np.argmin(distances)
        ordered_points.append(unused_points.pop(index))
    return ordered_points


def optimal_transport(dots, target_points):
    """
    Move the dots to the target points such that each dot moves a minimal distance
    """
    points = sort_to_minimize_distances(target_points, [d.get_center() for d in dots])
    for dot, point in zip(dots, points):
        dot.move_to(point)
    return dots


class RootCoefScene(Scene):
    coefs = [3, 2, 1, 0, -1, 1]
    root_plane_config = {
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
        "background_line_style": {
            "stroke_color": BLUE_E,
        }
    }
    coef_plane_config = {
        "x_range": (-4, 4),
        "y_range": (-4, 4),
        "background_line_style": {
            "stroke_color": GREY,
        }
    }
    plane_height = 5.5
    plane_buff = 1.5
    planes_center = ORIGIN
    plane_arrangement = LEFT
    cycle_run_time = 5

    root_color = YELLOW
    coef_color = RED_B

    dot_style = {
        "radius": 0.05,
        "stroke_color": BLACK,
        "stroke_width": 3,
        "stroke_behind": True,
    }
    include_tracers = True
    include_labels = True
    label_font_size = 30
    coord_label_font_size = 18
    continuous_roots = True
    show_equals = True

    def setup(self):
        self.lock_coef_imag = False
        self.lock_coef_norm = False
        self.add_planes()
        self.add_dots()
        self.active_dot_aura = Group()
        self.add(self.active_dot_aura)
        self.prepare_cycle_interaction()
        if self.include_tracers:
            self.add_all_tracers()
        if self.include_labels:
            self.add_r_labels()
            self.add_c_labels()

    def add_planes(self):
        # Planes
        planes = VGroup(
            ComplexPlane(**self.root_plane_config),
            ComplexPlane(**self.coef_plane_config),
        )
        for plane in planes:
            plane.set_height(self.plane_height)
        planes.arrange(self.plane_arrangement, buff=self.plane_buff)
        planes.move_to(self.planes_center)

        for plane in planes:
            plane.add_coordinate_labels(font_size=self.coord_label_font_size)
            plane.coordinate_labels.set_opacity(0.8)

        root_plane, coef_plane = planes

        # Lower labels
        root_plane_label = Text("Roots")
        coef_plane_label = Text("Coefficients")

        root_plane_label.next_to(root_plane, DOWN)
        coef_plane_label.next_to(coef_plane, DOWN)

        # Upper labels
        root_poly = self.get_root_poly()
        self.get_r_symbols(root_poly).set_color(self.root_color)
        root_poly.next_to(root_plane, UP)
        root_poly.set_max_width(root_plane.get_width())

        coef_poly = self.get_coef_poly()
        self.get_c_symbols(coef_poly).set_color(self.coef_color)
        coef_poly.set_max_width(coef_plane.get_width())
        coef_poly.next_to(coef_plane, UP)
        coef_poly.match_y(root_poly)

        self.add(planes)
        self.add(root_plane_label, coef_plane_label)
        self.add(root_poly, coef_poly)

        if self.show_equals:
            equals = OldTex("=")
            equals.move_to(midpoint(root_poly.get_right(), coef_poly.get_left()))
            self.add(equals)
            self.poly_equal_sign = equals

        self.root_plane = root_plane
        self.coef_plane = coef_plane
        self.root_plane_label = root_plane_label
        self.coef_plane_label = coef_plane_label
        self.root_poly = root_poly
        self.coef_poly = coef_poly

    def get_degree(self):
        return len(self.coefs) - 1

    def get_coef_poly(self):
        degree = self.get_degree()
        return OldTex(
            f"x^{degree}",
            *(
                f" + c_{n} x^{n}"
                for n in range(degree - 1, 1, -1)
            ),
            " + c_{1} x",
            " + c_{0}",
        )

    def get_root_poly(self):
        return OldTex(*(
            f"(x - r_{i})"
            for i in range(self.get_degree())
        ))

    def add_dots(self):
        self.root_dots = VGroup()
        self.coef_dots = VGroup()
        roots = coefficients_to_roots(self.coefs)
        self.add_root_dots(roots)
        self.add_coef_dots(self.coefs)

    #
    def get_all_dots(self):
        return (*self.root_dots, *self.coef_dots)

    def get_r_symbols(self, root_poly):
        return VGroup(*(part[3:5] for part in root_poly))

    def get_c_symbols(self, coef_poly):
        return VGroup(*(part[1:3] for part in coef_poly[:0:-1]))

    def get_random_root(self):
        return complex(
            interpolate(*self.root_plane.x_range[:2], random.random()),
            interpolate(*self.root_plane.y_range[:2], random.random()),
        )

    def get_random_roots(self):
        return [self.get_random_root() for x in range(self.degree)]

    def get_roots_of_unity(self):
        return [np.exp(complex(0, TAU * n / self.degree)) for n in range(self.degree)]

    def set_roots(self, roots):
        self.root_dots.set_submobjects(
            Dot(
                self.root_plane.n2p(root),
                color=self.root_color,
                **self.dot_style,
            )
            for root in roots
        )

    def set_coefs(self, coefs):
        self.coef_dots.set_submobjects(
            Dot(
                self.coef_plane.n2p(coef),
                color=self.coef_color,
                **self.dot_style,
            )
            for coef in coefs[:-1]  # Exclude highest term
        )

    def add_root_dots(self, roots=None):
        if roots is None:
            roots = self.get_roots_of_unity()
        self.set_roots(roots)
        self.add(self.root_dots)

    def add_coef_dots(self, coefs=None):
        if coefs is None:
            coefs = [0] * self.degree + [1]
        self.set_coefs(coefs)
        self.add(self.coef_dots)

    def get_roots(self):
        return [
            self.root_plane.p2n(root_dot.get_center())
            for root_dot in self.root_dots
        ]

    def get_coefs(self):
        return [
            self.coef_plane.p2n(coef_dot.get_center())
            for coef_dot in self.coef_dots
        ] + [1.0]

    def tie_coefs_to_roots(self, clear_updaters=True):
        if clear_updaters:
            self.root_dots.clear_updaters()
            self.coef_dots.clear_updaters()
        self.coef_dots.add_updater(self.update_coef_dots_by_roots)
        self.add(self.coef_dots)
        self.add(*self.root_dots)

    def update_coef_dots_by_roots(self, coef_dots):
        coefs = roots_to_coefficients(self.get_roots())
        for dot, coef in zip(coef_dots, coefs):
            dot.move_to(self.coef_plane.n2p(coef))
        return coef_dots

    def tie_roots_to_coefs(self, clear_updaters=True):
        if clear_updaters:
            self.root_dots.clear_updaters()
            self.coef_dots.clear_updaters()
        self.root_dots.add_updater(self.update_root_dots_by_coefs)
        self.add(self.root_dots)
        self.add(*self.coef_dots)

    def update_root_dots_by_coefs(self, root_dots):
        new_roots = coefficients_to_roots(self.get_coefs())
        new_root_points = map(self.root_plane.n2p, new_roots)
        if self.continuous_roots:
            optimal_transport(root_dots, new_root_points)
        else:
            for dot, point in zip(root_dots, new_root_points):
                dot.move_to(point)
        return root_dots

    def get_tracers(self, dots, time_traced=2.0, **kwargs):
        tracers = VGroup()
        for dot in dots:
            dot.tracer = TracingTail(
                dot,
                stroke_color=dot.get_fill_color(),
                time_traced=time_traced,
                **kwargs
            )
            tracers.add(dot.tracer)
        return tracers

    def add_all_tracers(self, **kwargs):
        self.tracers = self.get_tracers(self.get_all_dots())
        self.add(self.tracers)

    def get_tracking_lines(self, dots, syms, stroke_width=1, stroke_opacity=0.5):
        lines = VGroup(*(
            Line(
                stroke_color=root.get_fill_color(),
                stroke_width=stroke_width,
                stroke_opacity=stroke_opacity,
            )
            for root in dots
        ))

        def update_lines(lines):
            for sym, dot, line in zip(syms, dots, lines):
                line.put_start_and_end_on(
                    sym.get_bottom(),
                    dot.get_center()
                )

        lines.add_updater(update_lines)
        return lines

    def add_root_lines(self, **kwargs):
        self.root_lines = self.get_tracking_lines(
            self.root_dots,
            self.get_r_symbols(self.root_poly),
            **kwargs
        )
        self.add(self.root_lines)

    def add_coef_lines(self, **kwargs):
        self.coef_lines = self.get_tracking_lines(
            self.coef_dots,
            self.get_c_symbols(self.coef_poly),
            **kwargs
        )
        self.add(self.coef_lines)

    def add_dot_labels(self, labels, dots, buff=0.05):
        for label, dot in zip(labels, dots):
            label.scale(self.label_font_size / label.font_size)
            label.set_fill(dot.get_fill_color())
            label.set_stroke(BLACK, 3, background=True)
            label.dot = dot
            label.add_updater(lambda m: m.next_to(m.dot, UR, buff=buff))
        self.add(*labels)
        return labels

    def add_r_labels(self):
        self.r_dot_labels = self.add_dot_labels(
            VGroup(*(
                OldTex(f"r_{i}")
                for i in range(self.get_degree())
            )),
            self.root_dots
        )

    def add_c_labels(self):
        self.c_dot_labels = self.add_dot_labels(
            VGroup(*(
                OldTex(f"c_{i}")
                for i in range(self.get_degree())
            )),
            self.coef_dots
        )

    def add_value_label(self):
        pass  # TODO

    # Animations
    def play(self, *anims, **kwargs):
        movers = list(it.chain(*(anim.mobject.get_family() for anim in anims)))
        roots_move = any(rd in movers for rd in self.root_dots)
        coefs_move = any(cd in movers for cd in self.coef_dots)
        if roots_move and not coefs_move:
            self.tie_coefs_to_roots()
        elif coefs_move and not roots_move:
            self.tie_roots_to_coefs()
        super().play(*anims, **kwargs)

    def get_root_swap_arrows(self, i, j,
                             path_arc=90 * DEGREES,
                             stroke_width=5,
                             stroke_opacity=0.7,
                             buff=0.3,
                             **kwargs):
        di = self.root_dots[i].get_center()
        dj = self.root_dots[j].get_center()
        kwargs["path_arc"] = path_arc
        kwargs["stroke_width"] = stroke_width
        kwargs["stroke_opacity"] = stroke_opacity
        kwargs["buff"] = buff
        return VGroup(
            Arrow(di, dj, **kwargs),
            Arrow(dj, di, **kwargs),
        )

    def swap_roots(self, *indices, run_time=2, wait_time=1, **kwargs):
        self.play(CyclicReplace(
            *(
                self.root_dots[i]
                for i in indices
            ),
            run_time=run_time,
            **kwargs
        ))
        self.wait(wait_time)

    def rotate_coefs(self, indicies, center_z=0, run_time=5, wait_time=1, **kwargs):
        self.play(*(
            Rotate(
                self.coef_dots[i], TAU,
                about_point=self.coef_plane.n2p(center_z),
                run_time=run_time,
                **kwargs
            )
            for i in indicies
        ))
        self.wait(wait_time)

    def rotate_coef(self, i, **kwargs):
        self.rotate_coefs([i], **kwargs)

    # Interaction
    def add_dot_auroa(self, dot):
        glow_dot = GlowDot(color=WHITE)
        always(glow_dot.move_to, dot)
        self.active_dot_aura.add(glow_dot)

    def remove_dot_aura(self):
        if len(self.active_dot_aura) > 0:
            self.play(FadeOut(self.active_dot_aura), run_time=0.5)
            self.active_dot_aura.set_submobjects([])
            self.add(self.active_dot_aura)

    def prepare_cycle_interaction(self):
        self.dots_awaiting_cycle = []
        self.dot_awaiting_loop = None

    def handle_cycle_preparation(self, dot):
        if dot in self.root_dots and dot not in self.dots_awaiting_cycle:
            self.dots_awaiting_cycle.append(dot)
        if dot in self.coef_dots and dot is not self.dot_awaiting_loop:
            self.dot_awaiting_loop = dot
        self.add(dot)

    def carry_out_cycle(self):
        if self.dots_awaiting_cycle:
            self.tie_coefs_to_roots()
            self.play(CyclicReplace(*self.dots_awaiting_cycle, run_time=self.cycle_run_time))
            self.remove_dot_aura()
        if self.dot_awaiting_loop is not None:
            self.tie_roots_to_coefs()
            self.play(Rotate(
                self.dot_awaiting_loop,
                angle=TAU,
                about_point=self.mouse_point.get_center().copy(),
                run_time=8
            ))
            self.remove_dot_aura()
        self.prepare_cycle_interaction()

    def on_mouse_release(self, point, button, mods):
        super().on_mouse_release(point, button, mods)
        if self.root_dots.has_updaters() or self.coef_dots.has_updaters():
            # End the interaction where a dot is tied to the mouse
            self.root_dots.clear_updaters()
            self.coef_dots.clear_updaters()
            self.remove_dot_aura()
            return
        dot = self.point_to_mobject(point, search_set=self.get_all_dots(), buff=0.1)
        if dot is None:
            return
        self.add_dot_auroa(dot)
        if self.window.is_key_pressed(ord("c")):
            self.handle_cycle_preparation(dot)
            return

        # Make sure other dots are updated accordingly
        if dot in self.root_dots:
            self.tie_coefs_to_roots()
        elif dot in self.coef_dots:
            self.tie_roots_to_coefs()

        # Have this dot track with the mouse
        dot.mouse_point_diff = dot.get_center() - self.mouse_point.get_center()
        dot.add_updater(lambda d: d.move_to(self.mouse_point.get_center() + d.mouse_point_diff))
        if self.lock_coef_imag or self.window.is_key_pressed(ord("r")):
            # Fix the imaginary value
            dot.last_y = dot.get_y()
            dot.add_updater(lambda d: d.set_y(d.last_y))
        elif (self.lock_coef_norm or self.window.is_key_pressed(ord("a"))) and dot in self.coef_dots:
            # Fix the norm
            dot.last_norm = get_norm(self.coef_plane.p2c(dot.get_center()))
            dot.add_updater(lambda d: d.move_to(self.coef_plane.c2p(
                *d.last_norm * normalize(self.coef_plane.p2c(d.get_center()))
            )))

    def on_key_release(self, symbol, modifiers):
        super().on_key_release(symbol, modifiers)
        char = chr(symbol)
        if char == "c":
            self.carry_out_cycle()

    #
    def update_mobjects(self, dt):
        # Go in reverse order, since dots are often re-added
        # once they become interactive
        for mobject in reversed(self.mobjects):
            mobject.update(dt)



# ----- From _2022/quintic/cubic.py -----

class CubicFormula(RootCoefScene):
    coefs = [1, -1, 0, 1]
    coef_plane_config = {
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
        "background_line_style": {
            "stroke_color": GREY,
            "stroke_width": 1.0,
        }
    }
    root_plane_config = {
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
        "background_line_style": {
            "stroke_color": BLUE_E,
            "stroke_width": 1.0,
        }
    }
    sqrt_plane_config = {
        "x_range": (-1.0, 1.0),
        "y_range": (-1.0, 1.0),
        "background_line_style": {
            "stroke_color": GREY_B,
            "stroke_width": 1.0,
        },
        "height": 3.0,
        "width": 3.0,
    }
    crt_plane_config = {
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
        "background_line_style": {
            "stroke_color": BLUE_E,
            "stroke_width": 1.0,
        },
        "height": 3.0,
        "width": 3.0,
    }
    cf_plane_config = {
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
        "background_line_style": {
            "stroke_color": BLUE_E,
            "stroke_width": 1.0,
        },
        "height": 3.0,
        "width": 3.0,
    }
    plane_height = 3.0
    plane_buff = 1.0
    planes_center = 1.6 * UP
    lower_planes_height = 2.75
    lower_planes_buff = 2.0

    sqrt_dot_color = GREEN
    crt_dot_colors = (RED, BLUE)
    cf_dot_color = YELLOW

    def add_planes(self):
        super().add_planes()
        self.root_plane_label.next_to(self.root_plane, -self.plane_arrangement)
        self.coef_plane_label.next_to(self.coef_plane, self.plane_arrangement)
        self.add_lower_planes()

    def add_lower_planes(self):
        sqrt_plane = ComplexPlane(**self.sqrt_plane_config)
        crt_plane = ComplexPlane(**self.crt_plane_config)
        cf_plane = ComplexPlane(**self.cf_plane_config)

        planes = VGroup(sqrt_plane, crt_plane, cf_plane)
        for plane in planes:
            plane.add_coordinate_labels(font_size=16)
        planes.set_height(self.lower_planes_height)
        planes.arrange(RIGHT, buff=self.lower_planes_buff)
        planes.to_edge(DOWN, buff=SMALL_BUFF)

        kw = dict(
            font_size=24,
            tex_to_color_map={
                "\\delta_1": GREEN,
                "\\delta_2": GREEN,
            },
            # CHANGE: background_stroke_width/color are removed (they are no longer Mobject arguments; the set_backstroke() below does the same)
        )

        sqrt_label = OldTex(
            "\\delta_1, \\delta_2 = \\sqrt{ \\frac{q^2}{4} + \\frac{p^3}{27}}",
            **kw
        )
        sqrt_label.set_backstroke()
        sqrt_label.next_to(sqrt_plane, UP, SMALL_BUFF)

        crt_labels = VGroup(
            OldTex("\\cdot", "= \\sqrt[3]{-\\frac{q}{2} + \\delta_1}", **kw),
            OldTex("\\cdot", "= \\sqrt[3]{-\\frac{q}{2} + \\delta_2}", **kw),
        )
        for label, color in zip(crt_labels, self.crt_dot_colors):
            label[0].scale(4, about_edge=RIGHT)
            label[0].set_color(color)
            label.set_backstroke()
        crt_labels.arrange(RIGHT, buff=MED_LARGE_BUFF)
        crt_labels.next_to(crt_plane, UP, SMALL_BUFF)

        cf_label = OldTex(
            "\\sqrt[3]{ -\\frac{q}{2} + \\delta_1 } +",
            "\\sqrt[3]{ -\\frac{q}{2} + \\delta_2 }",
            # **kw  # TODO, What the hell is going on here...
            font_size=24,
        )
        cf_label.set_backstroke()
        cf_label.next_to(cf_plane, UP, SMALL_BUFF)

        self.add(planes)
        self.add(sqrt_label)
        self.add(crt_labels)
        self.add(cf_label)

        self.sqrt_plane = sqrt_plane
        self.crt_plane = crt_plane
        self.cf_plane = cf_plane
        self.sqrt_label = sqrt_label
        self.crt_labels = crt_labels
        self.cf_label = cf_label

    def get_coef_poly(self):
        return OldTex(
            "x^3 + {0}x^2 + {p}x + {q}",
            tex_to_color_map={
                "{0}": self.coef_color,
                "{p}": self.coef_color,
                "{q}": self.coef_color,
            }
        )

    def add_c_labels(self):
        self.c_dot_labels = self.add_dot_labels(
            VGroup(*map(Tex, ["q", "p", "0"])),
            self.coef_dots
        )

    def get_c_symbols(self, coef_poly):
        return VGroup(*(
            coef_poly.get_part_by_tex(tex)
            for tex in ["q", "p", "0"]
        ))

    #
    def add_dots(self):
        super().add_dots()
        self.add_sqrt_dots()
        self.add_crt_dots()
        self.add_cf_dots()

    def add_sqrt_dots(self):
        sqrt_dots = Dot(**self.dot_style).replicate(2)
        sqrt_dots.set_color(self.sqrt_dot_color)

        def update_sqrt_dots(dots):
            q, p, zero, one = self.get_coefs()
            disc = (q**2 / 4) + (p**3 / 27)
            roots = get_nth_roots(disc, 2)
            optimal_transport(dots, map(self.sqrt_plane.n2p, roots))
            return dots

        sqrt_dots.add_updater(update_sqrt_dots)

        self.sqrt_dots = sqrt_dots
        self.add(sqrt_dots)
        self.add(self.get_tracers(sqrt_dots))

        # Labels
        self.delta_labels = self.add_dot_labels(
            VGroup(OldTex("\\delta_1"), OldTex("\\delta_2")),
            sqrt_dots
        )

    def get_deltas(self):
        return list(map(self.sqrt_plane.p2n, (d.get_center() for d in self.sqrt_dots)))

    def add_crt_dots(self):
        crt_dots = Dot(**self.dot_style).replicate(3).replicate(2)
        for dots, color in zip(crt_dots, self.crt_dot_colors):
            dots.set_color(color)

        def update_crt_dots(dot_triples):
            q, p, zero, one = self.get_coefs()
            deltas = self.get_deltas()

            for delta, triple in zip(deltas, dot_triples):
                roots = get_nth_roots(-q / 2 + delta, 3)
                optimal_transport(triple, map(self.crt_plane.n2p, roots))
            return dot_triples

        crt_dots.add_updater(update_crt_dots)

        self.add(crt_dots)
        self.add(*(self.get_tracers(triple) for triple in crt_dots))

        self.crt_dots = crt_dots

    def get_cube_root_values(self):
        return [
            [
                self.crt_plane.p2n(d.get_center())
                for d in triple
            ]
            for triple in self.crt_dots
        ]

    def add_crt_lines(self):
        crt_lines = VGroup(*(
            Line(stroke_color=color, stroke_width=1).replicate(3)
            for color in self.crt_dot_colors
        ))

        def update_crt_lines(crt_lines):
            cube_root_values = self.get_cube_root_values()
            origin = self.crt_plane.n2p(0)
            for lines, triple in zip(crt_lines, cube_root_values):
                for line, value in zip(lines, triple):
                    line.put_start_and_end_on(origin, self.crt_plane.n2p(value))

        crt_lines.add_updater(update_crt_lines)

        self.add(crt_lines)
        self.crt_lines = crt_lines

    def add_cf_dots(self):
        cf_dots = Dot(**self.dot_style).replicate(9)
        cf_dots.set_fill(self.root_color, opacity=0.5)

        def update_cf_dots(dots):
            cube_root_values = self.get_cube_root_values()
            for dot, (z1, z2) in zip(dots, it.product(*cube_root_values)):
                dot.move_to(self.cf_plane.n2p(z1 + z2))
            return dots

        cf_dots.add_updater(update_cf_dots)

        alt_root_dots = GlowDot()
        alt_root_dots.add_updater(lambda m: m.set_points(
            list(map(self.cf_plane.n2p, self.get_roots()))
        ))

        self.cf_dots = cf_dots
        self.alt_root_dots = alt_root_dots

        self.add(cf_dots)
        self.add(self.get_tracers(cf_dots, stroke_width=0.5))
        self.add(alt_root_dots)

    def add_cf_lines(self):
        cf_lines = VGroup(
            Line(stroke_color=self.crt_dot_colors[0]).replicate(9),
            Line(stroke_color=self.crt_dot_colors[1]).replicate(3),
        )
        cf_lines.set_stroke(width=1)

        def update_cf_lines(cf_lines):
            cube_root_values = self.get_cube_root_values()
            for z1, line in zip(cube_root_values[1], cf_lines[1]):
                line.put_start_and_end_on(
                    self.cf_plane.n2p(0),
                    self.cf_plane.n2p(z1),
                )
            for line, (z1, z2) in zip(cf_lines[0], it.product(*cube_root_values)):
                line.put_start_and_end_on(
                    self.cf_plane.n2p(z2),
                    self.cf_plane.n2p(z1 + z2),
                )

        cf_lines.add_updater(update_cf_lines)

        self.cf_lines = cf_lines
        self.add(cf_lines)


class CubicFormulaTest(CubicFormula):
    def construct(self):
        pass
