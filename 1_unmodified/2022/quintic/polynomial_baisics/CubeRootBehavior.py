# ==============================================================================
# Scene:      CubeRootBehavior
# Source:     videos/_2022/quintic/polynomial_baisics.py (lines 1518-1545)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl CubeRootBehavior.py CubeRootBehavior -w -m --fps 15
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


class RadicalScene(RootCoefScene):
    n = 3
    c = 1.5
    root_plane_config = {
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
        "background_line_style": {
            "stroke_color": BLUE_E,
        }
    }
    coef_plane_config = {
        "x_range": (-2, 2),
        "y_range": (-2, 2),
        "background_line_style": {
            "stroke_color": GREY,
        }
    }
    plane_height = 4.0
    plane_buff = 3.0
    planes_center = 1.5 * DOWN
    show_equals = False

    def setup(self):
        self.coefs = [-self.c, *[0] * (self.n - 1), 1]
        super().setup()
        self.remove(self.coef_plane_label)
        self.remove(self.root_plane_label)
        self.sync_roots(self.root_dots[0])

    def get_radical_labels(self):
        left = self.coef_plane.get_right()
        right = self.root_plane.get_left()
        arrow_kw = dict(
            stroke_width=5,
            stroke_color=GREY_A,
            buff=0.5,
        )
        r_arrow = Arrow(left, right, **arrow_kw).shift(UP)
        l_arrow = Arrow(right, left, **arrow_kw).shift(DOWN)

        r_label = OldTex(f"\\sqrt[{self.n}]{{c}}")[0]
        l_label = OldTex(f"r_i^{{{self.n}}}")[0]
        r_label[3].set_color(self.coef_color)
        l_label[-3::2].set_color(self.root_color)

        if self.n == 2:
            r_label[0].set_opacity(0)

        r_label.next_to(r_arrow, UP)
        l_label.next_to(l_arrow, UP)

        return VGroup(
            VGroup(r_arrow, l_arrow),
            VGroup(r_label, l_label),
        )

    def get_angle_label(self, dot, plane, sym, get_theta):
        line = Line()
        line.set_stroke(dot.get_fill_color(), width=2)
        line.add_updater(lambda m: m.put_start_and_end_on(
            plane.get_origin(), dot.get_center()
        ))

        arc = always_redraw(lambda: ParametricCurve(
            lambda t: plane.n2p((0.25 + 0.01 * t) * np.exp(complex(0, t))),
            t_range=[0, get_theta() + 1e-5, 0.025],
            stroke_width=2,
        ))

        tex_mob = OldTex(sym, font_size=24)
        tex_mob.set_backstroke(width=8)

        def update_sym(tex_mob):
            tex_mob.set_opacity(min(1, 3 * get_theta()))
            point = arc.t_func(0.5 * get_theta())
            origin = plane.get_origin()
            w = tex_mob.get_width()
            tex_mob.move_to(origin + (1.3 + 2 * w) * (point - origin))
            return tex_mob

        tex_mob.add_updater(update_sym)

        return VGroup(line, arc, tex_mob)

    def get_c(self):
        return -self.get_coefs()[0]

    # Updates to RootCoefScene methods
    def get_coef_poly(self):
        degree = self.get_degree()
        return OldTex(f"x^{degree}", "-", "c")

    def get_c_symbols(self, coef_poly):
        return VGroup(coef_poly[-1])

    def add_c_labels(self):
        self.c_dot_labels = self.add_dot_labels(
            VGroup(OldTex("c")),
            VGroup(self.coef_dots[0]),
        )

    def get_coefs(self):
        c = self.coef_plane.p2n(self.coef_dots[0].get_center())
        return [-c, *[0] * (self.n - 1), 1]

    def set_coefs(self, coefs):
        super().set_coefs(coefs)
        self.coef_dots[0].move_to(self.coef_plane.n2p(-coefs[0]))
        self.coef_dots[1:].set_opacity(0)

    def tie_coefs_to_roots(self, *args, **kwargs):
        super().tie_coefs_to_roots(*args, **kwargs)
        # Hack
        for dot in self.root_dots:
            dot.add_updater(lambda m: m)

    def update_coef_dots_by_roots(self, coef_dots):
        controlled_roots = [
            d for d in self.root_dots
            if len(d.get_updaters()) > 1
        ]
        root_dot = controlled_roots[0] if controlled_roots else self.root_dots[0]
        root = self.root_plane.p2n(root_dot.get_center())
        coef_dots[0].move_to(self.coef_plane.n2p(root**self.n))
        # Update all the root dots
        if controlled_roots:
            self.sync_roots(controlled_roots[0])
        return coef_dots

    def sync_roots(self, anchor_root_dot):
        root = self.root_plane.p2n(anchor_root_dot.get_center())
        anchor_index = self.root_dots.submobjects.index(anchor_root_dot)
        for i, dot in enumerate(self.root_dots):
            if i != anchor_index:
                zeta = np.exp(complex(0, (i - anchor_index) * TAU / self.n))
                dot.move_to(self.root_plane.n2p(zeta * root))



# ----- From _2022/quintic/polynomial_baisics.py -----

class StudySqrt(RadicalScene):
    n = 2
    c = 2.0

    def construct(self):
        # Show simple equation
        kw = dict(tex_to_color_map={"c": self.coef_color})
        equations = VGroup(
            OldTex("x^2 - c = 0", **kw),
            OldTex("x =", "\\sqrt{c}", **kw),
        )
        equations.arrange(DOWN, buff=MED_LARGE_BUFF)
        equations.to_edge(UP)

        self.wait()
        self.play(FadeIn(equations[0], UP))
        self.wait()
        self.play(
            TransformMatchingShapes(
                equations[0].copy(),
                equations[1],
                path_arc=PI / 2,
            )
        )
        self.wait()

        sqrt_label = equations[1][1:].copy()

        # Add decimal labels, show square roots of real c
        c_label = VGroup(
            OldTex("c = ", tex_to_color_map={"c": self.coef_color}),
            DecimalNumber(self.c),
        )
        c_label.arrange(RIGHT, aligned_edge=DOWN)
        c_label.next_to(self.coef_poly, UP, buff=1.5)
        c_label[1].add_updater(lambda d: d.set_value(self.get_c().real))

        def update_root_dec(root_dec):
            c_real = self.get_c().real
            root_dec.unit = "" if c_real > 0 else "i"
            root_dec.set_value((-1)**root_dec.index * math.sqrt(abs(c_real)))

        r_labels = VGroup(*(
            VGroup(OldTex(f"r_{i}", "="), DecimalNumber(self.c, include_sign=True))
            for i in range(2)
        ))
        for i, r_label in enumerate(r_labels):
            r_label.arrange(RIGHT)
            r_label[1].align_to(r_label[0][0][0], DOWN)
            r_label[0][0].set_color(self.root_color)
            r_label[1].index = i
            r_label[1].add_updater(update_root_dec)

        r_labels.arrange(DOWN, buff=0.75)
        r_labels.match_x(self.root_plane)
        r_labels.match_y(c_label)

        sqrt_arrow = Arrow(self.coef_plane, self.root_plane)
        sqrt_arrow.match_y(c_label)

        self.play(
            FadeIn(c_label),
            ShowCreation(sqrt_arrow),
            sqrt_label.animate.next_to(sqrt_arrow, UP),
            FadeOut(equations),
        )
        self.play(FadeIn(r_labels))
        self.lock_coef_imag = True
        self.wait(note="Move c along real line")
        self.lock_coef_imag = False

        # Focus just on one root
        root_dots = self.root_dots
        root_tracers = VGroup(*(d.tracer for d in root_dots))
        root_labels = self.r_dot_labels
        self.play(
            r_labels[0].animate.match_y(c_label),
            FadeOut(r_labels[1], DOWN),
            root_dots[1].animate.set_opacity(0.5),
            root_dots[1].tracer.animate.set_stroke(opacity=0.5),
            root_labels[1].animate.set_opacity(0.5),
        )
        self.wait()
        r_label = r_labels[0]

        # Vary the angle of c
        self.show_angle_variation(c_label, r_label, sqrt_arrow)
        self.play(
            sqrt_arrow.animate.set_width(1.75).match_y(self.root_plane),
            MaintainPositionRelativeTo(sqrt_label, sqrt_arrow)
        )

        # Discontinuous square root
        option = VGroup(
            OldTexText("One option:", color=BLUE),
            OldTexText("\\\\Make", " $\\sqrt{\\quad}$", " single-valued, but discontinuous", font_size=36),
        )
        option.arrange(DOWN, buff=0.5)
        option[1][1].align_to(option[1][0], DOWN)
        option.to_edge(UP, buff=MED_SMALL_BUFF)

        np_tex = Code("Python: numpy.sqrt(c)")
        np_tex.match_width(self.root_plane)
        np_tex.next_to(self.root_plane, UP)

        sqrt_dot = Dot(**self.dot_style)
        sqrt_dot.set_color(BLUE)
        sqrt_dot.add_updater(lambda d: d.move_to(self.root_plane.n2p(np.sqrt(self.get_c()))))
        sqrt_label = Code("sqrt(c)")
        sqrt_label.scale(0.75)
        sqrt_label.add_updater(lambda m: m.next_to(sqrt_dot, UR, buff=0))

        self.play(FadeIn(option, UP))
        self.wait()
        self.remove(root_tracers)
        self.play(
            self.root_dots.animate.set_opacity(0),
            FadeOut(self.root_poly),
            FadeOut(root_labels),
            FadeIn(np_tex),
            FadeIn(sqrt_dot),
            FadeIn(sqrt_label),
        )
        self.wait(note="Show discontinuity")

        # Taylor series
        taylor_series = OldTex(
            "\\sqrt{x} \\approx",
            "1",
            "+ \\frac{1}{2}(x - 1)",
            "- \\frac{1}{8}(x - 1)^2",
            "+ \\frac{1}{16}(x - 1)^3",
            "- \\frac{5}{128}(x - 1)^4",
            "+ \\cdots",
            font_size=36,
        )
        ts_title = Text("What about a Taylor series?")
        ts_title.set_color(GREEN)
        ts_group = VGroup(ts_title, taylor_series)
        ts_group.arrange(DOWN, buff=MED_LARGE_BUFF)
        ts_group.to_edge(UP, buff=MED_SMALL_BUFF)

        def f(x, n):
            return sum((
                gen_choose(1 / 2, k) * (x - 1)**k
                for k in range(n)
            ))

        brace = Brace(taylor_series[1:-1], DOWN, buff=SMALL_BUFF)
        upper_f_label = brace.get_tex("f_4(x)", buff=SMALL_BUFF)
        upper_f_label.set_color(GREEN)

        f_dot = Dot(**self.dot_style)
        f_dot.set_color(GREEN)
        f_dot.add_updater(lambda d: d.move_to(self.root_plane.n2p(f(self.get_c(), 4))))
        f_label = OldTex("f_4(x)", font_size=24, color=GREEN)
        f_label.add_updater(lambda m: m.next_to(f_dot, DL, buff=SMALL_BUFF))

        self.play(
            FadeOut(np_tex),
            FadeIn(ts_group, UP),
            FadeOut(option, UP),
        )
        self.wait()
        self.play(
            GrowFromCenter(brace),
            FadeIn(upper_f_label, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            TransformFromCopy(upper_f_label, f_label),
            GrowFromPoint(f_dot, upper_f_label.get_center()),
        )
        self.wait()

        anims = [
            brace.animate.become(Brace(taylor_series[1:], DOWN, buff=SMALL_BUFF))
        ]
        for label in (upper_f_label, f_label):
            new_label = OldTex("f_{50}(x)")
            new_label.replace(label, 1)
            new_label.match_style(label)
            anims.append(Transform(label, new_label, suspend_updating=False))
        self.play(*anims)
        f_dot.clear_updaters()
        f_dot.add_updater(lambda d: d.move_to(self.root_plane.n2p(f(self.get_c(), 50))))
        self.wait()

        disc = Circle(radius=self.root_plane.x_axis.get_unit_size())
        disc.move_to(self.root_plane.n2p(1))
        disc.set_stroke(BLUE_B, 2)
        disc.set_fill(BLUE_B, 0.2)
        self.play(FadeIn(disc))
        self.wait()

        # Back to normal
        ts_group.add(brace, upper_f_label)
        root_labels.set_opacity(1)
        self.play(
            FadeOut(ts_group, UP),
            *map(FadeOut, (disc, f_label, f_dot, sqrt_label, sqrt_dot)),
            FadeIn(root_labels),
            FadeIn(self.root_poly),
            root_dots.animate.set_opacity(1),
        )
        self.add(root_tracers, *root_labels)
        self.wait()

    def show_angle_variation(self, c_label, r_label, arrow):
        angle_color = TEAL
        self.last_theta = 0

        def get_theta():
            angle = np.log(self.get_c()).imag
            diff = angle - self.last_theta
            diff = (diff + PI) % TAU - PI
            self.last_theta += diff
            return self.last_theta

        circle = Circle(radius=self.coef_plane.x_axis.get_unit_size())
        circle.set_stroke(angle_color, 1)
        circle.move_to(self.coef_plane.get_origin())

        left_exp_label, right_exp_label = (
            self.get_exp_label(
                get_theta=func,
                color=angle_color
            ).move_to(label[-1], DL)
            for label, func in [
                (c_label, get_theta),
                (r_label, lambda: get_theta() / self.n),
            ]
        )

        below_arrow_tex = Tex(
            "e^{x} \\rightarrow e^{x /" + str(self.n) + "}",
            font_size=36,
            tex_to_color_map={"\\theta": angle_color},
        )
        below_arrow_tex.next_to(arrow, DOWN)

        angle_labels = VGroup(
            self.get_angle_label(self.coef_dots[0], self.coef_plane, "\\theta", get_theta),
            self.get_angle_label(
                self.root_dots[0], self.root_plane,
                f"\\theta / {self.n}",
                lambda: get_theta() / self.n,
            ),
        )

        self.add(circle, self.coef_dots)
        self.lock_coef_norm = True
        self.tie_roots_to_coefs()
        self.play(
            FadeIn(circle),
            FadeIn(angle_labels),
            self.coef_dots[0].animate.move_to(self.coef_plane.n2p(1)),
        )
        self.wait()
        self.play(
            FadeOut(c_label[-1], UP),
            FadeOut(r_label[-1], UP),
            FadeIn(left_exp_label, UP),
            FadeIn(right_exp_label, UP),
        )
        self.wait(note="Rotate c a bit")
        self.play(Write(below_arrow_tex))
        self.wait(note="Show full rotation, then two rotations")

        # Remove stuff
        self.play(LaggedStart(*map(FadeOut, (
            circle, angle_labels,
            left_exp_label, right_exp_label,
            c_label[:-1], r_label[:-1],
            below_arrow_tex,
        ))))
        self.lock_coef_norm = False

    def get_exp_label(self, get_theta, color=GREEN):
        result = OldTex("e^{", "2\\pi i \\cdot", "0.00}")
        decimal = DecimalNumber()
        decimal.replace(result[2], dim_to_match=1)
        result.replace_submobject(2, decimal)
        result.add_updater(lambda m: m.note_changed_family())
        result.add_updater(lambda m: m[-1].set_color(color))
        result.add_updater(lambda m: m[-1].set_value(get_theta() / TAU))
        return result


class CubeRootBehavior(StudySqrt):
    n = 3
    c = 1.0

    def construct(self):
        arrows, labels = self.get_radical_labels()
        self.add(arrows, labels)

        c_label = OldTex("c = ", "1.00", tex_to_color_map={"c": self.coef_color})
        r_label = OldTex("r_0 = ", "1.00", tex_to_color_map={"r_0": self.root_color})
        c_label.match_x(self.coef_plane)
        c_label.to_edge(UP, buff=1.0)
        r_label.match_x(self.root_plane)
        r_label.match_y(c_label)
        right_arrow_group = VGroup(arrows[0], labels[0])
        right_arrow_group.save_state()

        self.wait()
        self.wait()
        self.play(
            right_arrow_group.animate.to_edge(UP),
            *map(FadeIn, (c_label, r_label))
        )
        self.show_angle_variation(c_label, r_label, right_arrow_group[0])
        self.play(Restore(right_arrow_group))

    def add_labeled_arrow(self):
        pass
