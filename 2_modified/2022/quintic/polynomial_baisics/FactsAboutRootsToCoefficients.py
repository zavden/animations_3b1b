# ==============================================================================
# Scene:      FactsAboutRootsToCoefficients
# Source:     videos/_2022/quintic/polynomial_baisics.py (lines 647-989)
# Category:   2 · Renders with modifications
# Includes code copied from: _2022/quintic/roots_and_coefs.py
#
# Run from this folder:
#     manimgl FactsAboutRootsToCoefficients.py FactsAboutRootsToCoefficients -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - FadeIn(..., suspend_updating=True) -> suspend_mobject_updating=True (current name of Animation's argument)
#   - TransformMatchingTex(l1, l2) -> TransformMatchingShapes: the lines are OldTex and TransformMatchingTex now requires the new Tex (get_symbol_substrings)
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



# ----- From _2022/quintic/polynomial_baisics.py -----

class FactsAboutRootsToCoefficients(RootCoefScene):
    coefs = [-5, 14, -7, 1]
    coef_plane_config = {
        "x_range": (-15.0, 15.0, 5.0),
        "y_range": (-10, 10, 5),
        "background_line_style": {
            "stroke_color": GREY,
            "stroke_width": 1.0,
        },
        "height": 20,
        "width": 30,
    }
    root_plane_config = {
        "x_range": (-1.0, 6.0),
        "y_range": (-3.0, 3.0),
        "background_line_style": {
            "stroke_color": BLUE_E,
            "stroke_width": 1.0,
        }
    }
    plane_height = 3.5
    planes_center = 1.5 * DOWN

    def construct(self):
        # Play with coefficients, confined to real axis
        self.wait()
        self.add_constant_decimals()
        self.add_graph()
        self.lock_coef_imag = True
        self.wait(note="Move around c0")
        self.lock_coef_imag = False

        self.decimal_poly.clear_updaters()
        self.play(
            FadeOut(self.decimal_poly, DOWN),
            FadeOut(self.graph_group, DOWN),
        )

        # Show the goal
        self.add_system()
        self.add_solver_functions()

        # Why that's really weird
        self.play(
            self.coef_system.animate.set_opacity(0.2),
            self.root_system[1:].animate.set_opacity(0.2),
        )
        self.wait(note="Show loops with c0")

        # Why something like this must be possible
        brace = Brace(self.coef_system, RIGHT)
        properties = VGroup(
            Text("Continuous"),
            Text("Symmetric"),
        )
        properties.arrange(DOWN, buff=MED_LARGE_BUFF)
        properties.next_to(brace, RIGHT)

        self.play(
            GrowFromCenter(brace),
            self.root_system.animate.set_opacity(0),
            self.coef_system.animate.set_opacity(1),
        )
        self.wait()
        for words in properties:
            self.play(Write(words, run_time=1))
            self.wait()

        self.swap_root_symbols()
        self.wait(note="Physically swap roots")

        # What this implies about our functions
        brace.generate_target()
        brace.target.rotate(PI)
        brace.target.next_to(self.root_system, LEFT)
        left_group = VGroup(properties, self.coef_system)
        left_group.generate_target()
        left_group.target.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        left_group.target.set_height(1)
        left_group.target.to_corner(UL)
        left_group.target.set_opacity(0.5)

        self.play(
            MoveToTarget(brace, path_arc=PI / 2),
            MoveToTarget(left_group),
            self.root_system.animate.set_opacity(1)
        )
        self.wait()

        restriction = VGroup(
            Text("Cannot(!) be both"),
            Text("Continuous and single-valued", t2c={
                "Continuous": YELLOW,
                "single-valued": BLUE,
            })
        )
        restriction.scale(0.8)
        restriction.arrange(DOWN)
        restriction.next_to(brace, LEFT)

        self.play(FadeIn(restriction))
        self.wait(note="Move c0, emphasize multiplicity of outputs")

        # Impossibility result
        words = Text("Cannot be built from ")
        symbols = OldTex(
            "+,\\,", "-,\\,", "\\times,\\,", "/,\\,", "\\text{exp}\\\\",
            "\\sin,\\,", "\\cos,\\,", "| \\cdot |,\\,", "\\dots",
        )
        impossibility = VGroup(words, symbols)
        impossibility.arrange(RIGHT)
        impossibility.match_width(restriction)
        impossibility.next_to(restriction, DOWN, aligned_edge=RIGHT)
        impossible_rect = SurroundingRectangle(impossibility)
        impossible_rect.set_stroke(RED, 2)

        arrow = OldTex("\\Downarrow", font_size=36)
        arrow.next_to(impossible_rect, UP, SMALL_BUFF)
        restriction.generate_target()
        restriction.target.scale(1.0).next_to(arrow, UP, SMALL_BUFF)

        self.play(
            FadeIn(impossibility[0]),
            FadeIn(arrow),
            ShowCreation(impossible_rect),
            MoveToTarget(restriction),
        )
        for symbol in symbols:
            self.wait(0.25)
            self.add(symbol)
        self.wait()

        # Show discontinuous example
        to_fade = VGroup(
            restriction[0],
            restriction[1].get_part_by_text("Continuous and"),
            arrow,
            impossibility,
            impossible_rect,
        )
        to_fade.save_state()
        self.play(*(m.animate.fade(0.8) for m in to_fade))

        root_tracers = VGroup(*(d.tracer for d in self.root_dots))
        self.remove(root_tracers)
        self.continuous_roots = False
        self.root_dots[0].set_fill(BLUE)
        self.r_dot_labels[0].set_fill(BLUE)
        self.root_dots[1].set_fill(GREEN)
        self.r_dot_labels[1].set_fill(GREEN)
        self.wait(note="Show discontinuous behavior")
        self.add(self.get_tracers(self.root_dots))
        self.wait(note="Turn tracers back on")
        self.continuous_roots = True

        # Represent as a multivalued function
        f_name = "\\text{cubic\\_solve}"
        t2c = dict([
            (f"{sym}_{i}", color)
            for i in range(3)
            for sym, color in [
                ("r", self.root_color),
                ("c", self.coef_color),
            ]
        ])
        t2c[f_name] = GREY_A
        mvf = OldTex(
            f"{f_name}(c_0, c_1, c_2)\\\\", "=\\\\", "\\left\\{r_0, r_1, r_2\\right\\}",
            tex_to_color_map=t2c
        )
        mvf.get_part_by_tex("=").rotate(PI / 2).match_x(mvf.slice_by_tex(None, "="))
        mvf.slice_by_tex("left").match_x(mvf.get_part_by_tex("="))
        mvf.move_to(self.root_system, LEFT)

        self.play(
            TransformMatchingShapes(self.root_system, mvf),
            restriction[1].get_part_by_text("single-valued").animate.fade(0.8),
        )
        self.wait(note="Labeling is an artifact")
        self.play(FadeOut(self.r_dot_labels))
        self.wait()

    def add_c_labels(self):
        super().add_c_labels()
        self.c_dot_labels[2].clear_updaters()
        self.c_dot_labels[2].add_updater(
            lambda l: l.next_to(l.dot, DL, buff=0)
        )
        return self.c_dot_labels

    def add_constant_decimals(self):
        dummy = "+10.00"
        polynomial = OldTex(
            f"x^3 {dummy}x^2 {dummy}x {dummy}",
            isolate=[dummy],
            font_size=40,
        )
        polynomial.next_to(self.coef_poly, UP, LARGE_BUFF)
        decimals = DecimalNumber(100, include_sign=True, edge_to_fix=LEFT).replicate(3)
        for dec, part in zip(decimals, polynomial.get_parts_by_tex(dummy)):
            dec.match_height(part)
            dec.move_to(part, LEFT)
            part.set_opacity(0)
            polynomial.add(dec)
        polynomial.decimals = decimals

        def update_poly(polynomial):
            for dec, coef in zip(polynomial.decimals, self.get_coefs()[-2::-1]):
                dec.set_value(coef.real)
            polynomial.decimals.set_fill(RED, 1)
            return polynomial

        update_poly(polynomial)
        VGroup(polynomial[0], decimals[0]).next_to(
            polynomial[2], LEFT, SMALL_BUFF, aligned_edge=DOWN
        )

        # CHANGE: suspend_updating is not an argument of Animation (the original ignored it); the current name is suspend_mobject_updating
        self.play(FadeIn(polynomial, UP, suspend_mobject_updating=True))
        polynomial.add_updater(update_poly)
        self.decimal_poly = polynomial

    def add_graph(self):
        self.decimal_poly
        axes = Axes(
            (0, 6), (-4, 10),
            axis_config=dict(tick_size=0.025),
            width=3, height=2,
        )
        axes.set_height(2)
        axes.move_to(self.root_plane)
        axes.to_edge(UP, buff=SMALL_BUFF)

        graph = always_redraw(
            lambda: axes.get_graph(
                lambda x: poly(x, self.get_coefs()).real
            ).set_stroke(BLUE, 2)
        )

        root_dots = GlowDot()
        root_dots.add_updater(lambda d: d.set_points([
            axes.c2p(r.real, 0)
            for r in self.get_roots()
            if abs(r.imag) < 1e-5
        ]))

        arrow = Arrow(self.decimal_poly.get_right(), axes)

        graph_group = Group(axes, graph, root_dots)

        self.play(
            ShowCreation(arrow),
            FadeIn(graph_group, shift=UR),
        )

        graph_group.add(arrow)
        self.graph_group = graph_group

    def add_system(self):
        c_parts = self.get_c_symbols(self.coef_poly)
        system = get_symmetric_system(
            (f"c_{i}" for i in reversed(range(len(self.coef_dots)))),
            signed=True,
        )
        system.scale(0.8)
        system.next_to(self.coef_poly, UP, LARGE_BUFF)
        system.align_to(self.coef_plane, LEFT)

        self.add(system)

        kw = dict(lag_ratio=0.8, run_time=2.5)
        self.play(
            LaggedStart(*(
                TransformFromCopy(c, line[0])
                for c, line in zip(c_parts, system)
            ), **kw),
            LaggedStart(*(
                FadeIn(line[1:], lag_ratio=0.1)
                for line in system
            ), **kw)
        )
        self.add(system)
        self.coef_system = system
        self.wait()

    def add_solver_functions(self):
        func_name = "\\text{cubic\\_solve}"
        t2c = dict((
            (f"{sym}_{i}", color)
            for i in range(3)
            for sym, color in [
                ("c", self.coef_color),
                ("r", self.root_color),
                (func_name, GREY_A),
            ]
        ))
        kw = dict(tex_to_color_map=t2c)
        lines = VGroup(*(
            OldTex(f"r_{i} = {func_name}_{i}(c_0, c_1, c_2)", **kw)
            for i in range(3)
        ))
        lines.scale(0.8)
        lines.arrange(DOWN, aligned_edge=LEFT)
        lines.match_y(self.coef_system)
        lines.align_to(self.root_plane, LEFT)

        kw = dict(lag_ratio=0.7, run_time=2)
        self.play(
            LaggedStart(*(
                TransformFromCopy(r, line[0])
                for r, line in zip(self.get_r_symbols(self.root_poly), lines)
            ), **kw),
            LaggedStart(*(
                FadeIn(line[1:], lag_ratio=0.1)
                for line in lines
            ), **kw),
        )
        self.add(lines)
        self.root_system = lines
        self.wait()

    def swap_root_symbols(self):
        system = self.coef_system
        cs = [f"c_{i}" for i in reversed(range(len(self.coef_dots)))]
        rs = [f"r_{{{i}}}" for i in range(len(self.root_dots))]

        for tup in [(1, 2, 0), (2, 0, 1), (0, 1, 2)]:
            rs = [f"r_{{{i}}}" for i in tup]
            alt_system = get_symmetric_system(cs, roots=rs, signed=True)
            alt_system.replace(system)
            # CHANGE: TransformMatchingTex now requires the new Tex (StringMobject) and here the lines are OldTex; TransformMatchingShapes is used
            self.play(*(
                TransformMatchingShapes(
                    l1, l2,
                    path_arc=PI / 2,
                    lag_ratio=0.01,
                    run_time=2
                )
                for l1, l2 in zip(system, alt_system)
            ))
            self.remove(system)
            system = alt_system
            self.add(system)
            self.wait()
        self.coef_system = system
