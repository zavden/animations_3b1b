# ==============================================================================
# Scene:      IntroduceEField
# Source:     videos/_2023/optics_puzzles/e_field.py (lines 67-724)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl IntroduceEField.py IntroduceEField -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
#   - ChargedParticle.update(dt, recurse) did not accept frame_rate, which manimgl passes since PR #2481 (TypeError); the parameter was added
#   - The extractor did not copy the get_influence_ring function from e_field.py (a method of the same name uses it): it was added to the scene unchanged
#   - charge.init_clock() was called without start_point (a bug in the original, ChargedParticle.init_clock requires it); charge.get_center() is passed
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField
from typing import TYPE_CHECKING


# ----- From _2023/optics_puzzles/objects.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3


def points_to_particle_info(particle, points, radius=None, c=2.0):
    """
    Given an origin, a set of points, and a radius, this returns:

    1) The unit vectors directed from the origin to each point

    2) The distances from the origin to each point

    3) An adjusted version of those distances where points
    within a given radius of the origin are considered to
    be farther away, approaching infinity at the origin.
    The intent is that when this is used for coulomb/lorenz
    forces, field vectors within a radius of a particle don't
    blow up
    """
    if radius is None:
        radius = particle.get_radius()

    if particle.track_position_history:
        approx_delays = np.linalg.norm(points - particle.get_center(), axis=1) / c
        centers = particle.get_past_position(approx_delays)
    else:
        centers = particle.get_center()

    diffs = points - centers
    norms = np.linalg.norm(diffs, axis=1)[:, np.newaxis]
    unit_diffs = np.zeros_like(diffs)
    np.true_divide(diffs, norms, out=unit_diffs, where=(norms > 0))

    adjusted_norms = norms.copy()
    mask = (0 < norms) & (norms < radius)
    adjusted_norms[mask] = radius * radius / norms[mask]
    adjusted_norms[norms == 0] = np.inf

    return unit_diffs, norms, adjusted_norms


def coulomb_force(points, particle, radius=None):
    unit_diffs, norms, adjusted_norms = points_to_particle_info(particle, points, radius)
    return particle.get_charge() * unit_diffs / adjusted_norms**2


def lorentz_force(
    points,
    particle,
    radius=None,
    c=2.0,
    epsilon0=0.025,
):
    unit_diffs, norms, adjusted_norms = points_to_particle_info(particle, points, radius, c)
    delays = norms[:, 0] / c

    acceleration = particle.get_past_acceleration(delays)
    dot_prods = (unit_diffs * acceleration).sum(1)[:, np.newaxis]
    a_perp = acceleration - dot_prods * unit_diffs

    denom = 4 * PI * epsilon0 * c**2 * adjusted_norms
    return -particle.get_charge() * a_perp / denom


# CHANGE: the extractor did not copy get_influence_ring (a function from e_field.py, line 6), which the method of the same name uses; it is added as is
def get_influence_ring(center_point, color=WHITE, speed=2.0, max_width=3.0, width_decay_exp=0.5):
    ring = Circle()
    ring.set_stroke(color)
    ring.move_to(center_point)
    ring.time = 0

    def update_ring(ring, dt):
        ring.time += dt
        radius = ring.time * speed
        ring.set_width(max(2 * radius, 1e-3))
        ring.set_stroke(width=max_width / (1 + radius)**width_decay_exp)
        return ring

    ring.add_updater(update_ring)
    return ring


class ChargedParticle(Group):
    def __init__(
        self,
        point=ORIGIN,
        charge=1.0,
        mass=1.0,
        color=RED,
        show_sign=True,
        sign="+",
        radius=0.2,
        rotation=0,
        sign_stroke_width=2,
        track_position_history=True,
        history_size=7200,
        euler_steps_per_frame=10,
    ):
        self.charge = charge
        self.mass = mass

        sphere = TrueDot(radius=radius, color=color)
        sphere.make_3d()
        sphere.move_to(point)
        self.sphere = sphere

        self.track_position_history = track_position_history
        self.history_size = history_size
        self.velocity = np.zeros(3)  # Only used if force are added
        self.euler_steps_per_frame = euler_steps_per_frame
        self.init_clock(point)

        super().__init__(sphere)

        if show_sign:
            sign = Tex(sign)
            sign.set_width(radius)
            sign.rotate(rotation, RIGHT)
            sign.set_stroke(WHITE, sign_stroke_width)
            sign.move_to(sphere)
            self.add(sign)
            self.sign = sign

    # Related to updaters

    # CHANGE: Mobject.update now also receives frame_rate (manimgl PR #2481); it is accepted and passed to the parent
    def update(self, dt: float = 0, recurse: bool = True, frame_rate: float | None = None):
        super().update(dt, recurse, frame_rate)
        # Do this instead of adding an updater, because
        # otherwise all animations require the
        # suspend_mobject_updating=false flag
        self.increment_clock(dt)

    def init_clock(self, start_point):
        self.time = 0
        self.time_step = 1 / 30  # This will be updated
        self.recent_positions = np.tile(start_point, 3).reshape((3, 3))
        if self.track_position_history:
            self.position_history = np.zeros((self.history_size, 3))
            self.acceleration_history = np.zeros((self.history_size, 3))
            self.history_index = -1

    def increment_clock(self, dt):
        if dt == 0:
            return self
        self.time += dt
        self.time_step = dt
        self.recent_positions[0:2] = self.recent_positions[1:3]
        self.recent_positions[2] = self.get_center()
        if self.track_position_history:
            self.add_to_position_history()

    def add_to_position_history(self):
        self.history_index += 1
        hist_size = self.history_size
        # If overflowing, copy second half of history
        # lists to the first half, and reset index
        if self.history_index >= hist_size:
            for arr in [self.position_history, self.acceleration_history]:
                arr[:hist_size // 2, :] = arr[hist_size // 2:, :]
            self.history_index = (hist_size // 2) + 1

        self.position_history[self.history_index] = self.get_center()
        self.acceleration_history[self.history_index] = self.get_acceleration()
        return self

    def ignore_last_motion(self):
        self.recent_positions[:] = self.get_center()
        return self

    def add_force(self, force_func: Callable[[Vect3], Vect3]):
        espf = self.euler_steps_per_frame

        def update_from_force(particle, dt):
            if dt == 0:
                return
            for _ in range(espf):
                acc = force_func(particle.get_center()) / self.mass
                self.velocity += acc * dt / espf
                self.shift(self.velocity * dt / espf)

        self.add_updater(update_from_force)
        return self

    def add_spring_force(self, k=1.0, center=None):
        center = center if center is not None else self.get_center().copy()
        self.add_force(lambda p: k * (center - p))
        return self

    def add_field_force(self, field):
        charge = self.get_charge()
        self.add_force(lambda p: charge * field.get_forces([p])[0])
        return self

    def fix_x(self):
        x = self.get_x()
        self.add_updater(lambda m: m.set_x(x))

    # Getters

    def get_charge(self):
        return self.charge

    def get_radius(self):
        return self.sphere.get_radius()

    def get_internal_time(self):
        return self.time

    def scale(self, factor, *args, **kwargs):
        super().scale(factor, *args, **kwargs)
        self.sphere.set_radius(factor * self.sphere.get_radius())
        return self

    def get_acceleration(self):
        p0, p1, p2 = self.recent_positions
        # if (p0 == p1).all() or (p1 == p2).all():
        if np.isclose(p0, p1).all() or np.isclose(p1, p2).all():
            # Otherwise, starts and stops have artificially
            # high acceleration
            return np.zeros(3)
        return (p0 + p2 - 2 * p1) / self.time_step**2

    def get_info_from_delays(self, info_arr, delays):
        if not hasattr(self, "acceleration_history"):
            raise Exception("track_position_history is not turned on")

        if len(info_arr) == 0:
            return np.zeros((len(delays), 3))

        pre_indices = self.history_index - delays / self.time_step
        indices = np.clip(pre_indices, 0, self.history_index).astype(int)

        return info_arr[indices]

    def get_past_acceleration(self, delays):
        return self.get_info_from_delays(self.acceleration_history, delays)

    def get_past_position(self, delays):
        return self.get_info_from_delays(self.position_history, delays)


class AccelerationVector(Vector):
    def __init__(
        self,
        particle,
        stroke_color=PINK,
        stroke_width=4,
        flat_stroke=False,
        norm_func=lambda n: np.tanh(n),
        **kwargs
    ):
        self.norm_func = norm_func

        super().__init__(
            RIGHT,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            flat_stroke=flat_stroke,
            **kwargs
        )
        self.add_updater(lambda m: m.pin_to_particle(particle))

    def pin_to_particle(self, particle):
        a_vect = particle.get_acceleration()
        norm = get_norm(a_vect)
        if self.norm_func is not None and norm > 0:
            a_vect *= self.norm_func(norm) / norm
        center = particle.get_center()
        self.put_start_and_end_on(center, center + a_vect)


class ChargeBasedVectorField(VectorField):
    default_color = BLUE

    def __init__(self, *charges, **kwargs):
        self.charges = list(charges)
        super().__init__(
            self.get_forces,
            color=kwargs.pop("color", self.default_color),
            **kwargs
        )
        self.add_updater(lambda m: m.update_vectors())

    def get_forces(self, points):
        # To be implemented in subclasses
        return np.zeros_like(points)


class CoulombField(ChargeBasedVectorField):
    default_color = YELLOW

    def get_forces(self, points):
        return sum(
            coulomb_force(points, charge)
            for charge in self.charges
        )


class LorentzField(ChargeBasedVectorField):
    def __init__(
        self, *charges,
        radius_of_suppression=None,
        c=2.0,
        **kwargs
    ):
        self.radius_of_suppression = radius_of_suppression
        self.c = c
        super().__init__(*charges, **kwargs)

    def get_forces(self, points):
        return sum(
            lorentz_force(
                points, charge,
                radius=self.radius_of_suppression,
                c=self.c
            )
            for charge in self.charges
        )


class ColoumbPlusLorentzField(LorentzField):
    def get_forces(self, points):
        return sum(
            lorentz_force(
                points, charge,
                radius=self.radius_of_suppression,
                c=self.c
            ) + sum(
                coulomb_force(points, charge)
                for charge in self.charges
            )
            for charge in self.charges
        )



# ----- From _2023/optics_puzzles/e_field.py -----

class IntroduceEField(InteractiveScene):
    def construct(self):
        # Show two neighboring particles
        frame = self.frame
        frame.set_field_of_view(1 * DEGREES)

        charges = ChargedParticle(rotation=0).replicate(2)
        charges.arrange(RIGHT, buff=4)

        question = VGroup(
            Text("""
                How does the position
                and motion of this...
            """),
            Text("influence this?"),
        )
        for q, charge, vect in zip(question, charges, [LEFT, RIGHT]):
            q.next_to(charge, UP + vect, buff=1.0).shift(-2 * vect)

        question[1].align_to(question[0], DOWN)
        q0_bottom = question[0].get_bottom()
        arrow0 = always_redraw(lambda: Arrow(q0_bottom, charges[0]))
        arrow1 = Arrow(question[1].get_bottom(), charges[1])
        arrows = VGroup(arrow0, arrow1)

        self.play(LaggedStartMap(FadeIn, charges, shift=UP, lag_ratio=0.5))
        self.add(arrow0)
        self.play(
            Write(question[0]),
            charges[0].animate.shift(UR).set_anim_args(
                rate_func=wiggle,
                time_span=(1, 3),
            )
        )
        self.play(
            Write(question[1]),
            ShowCreation(arrow1),
        )
        self.wait()

        # Show force arrows
        def show_coulomb_force(arrow, charge1, charge2):
            root = charge2.get_center()
            vect = 4 * coulomb_force(
                charge2.get_center()[np.newaxis, :],
                charge1
            )[0]
            arrow.put_start_and_end_on(root, root + vect)

        coulomb_vects = Vector(RIGHT, stroke_width=5, stroke_color=YELLOW).replicate(2)
        coulomb_vects[0].add_updater(lambda a: show_coulomb_force(a, *charges))
        coulomb_vects[1].add_updater(lambda a: show_coulomb_force(a, *charges[::-1]))

        self.add(*coulomb_vects, *charges)
        self.play(
            FadeOut(question, time_span=(0, 1)),
            FadeOut(arrows, time_span=(0, 1)),
            charges.animate.arrange(RIGHT, buff=1.25),
            run_time=2
        )

        # Show force word
        force_words = Text("Force", font_size=48).replicate(2)
        force_words.set_fill(border_width=1)
        fw_width = force_words.get_width()

        def place_force_word_on_arrow(word, arrow):
            word.set_width(min(0.5 * arrow.get_width(), fw_width))
            word.next_to(arrow, UP, buff=0.2)

        force_words[0].add_updater(lambda w: place_force_word_on_arrow(w, coulomb_vects[0]))
        force_words[1].add_updater(lambda w: place_force_word_on_arrow(w, coulomb_vects[1]))

        self.play(LaggedStartMap(FadeIn, force_words, run_time=1, lag_ratio=0.5))
        self.add(force_words, charges)
        self.wait()

        # Add distance label
        d_line = always_redraw(lambda: DashedLine(
            charges[0].get_right(), charges[1].get_left(),
            dash_length=0.025
        ))
        d_label = Tex("r = 0.00", font_size=36)
        d_label.next_to(d_line, DOWN, buff=0.35)
        d_label.add_updater(lambda m: m.match_x(d_line))
        dist_decimal = d_label.make_number_changeable("0.00")

        def get_d():
            return get_norm(charges[0].get_center() - charges[1].get_center())

        dist_decimal.add_updater(lambda m: m.set_value(get_d()))

        # Show graph
        axes = Axes((0, 10), (0, 1, 0.25), width=10, height=5)
        axes.shift(charges[0].get_center() + 1 * UP - axes.get_origin())
        axes.add(
            Text("Distance", font_size=36).next_to(axes.c2p(10, 0), UP),
            Text("Force", font_size=36).next_to(axes.c2p(0, 0.8), LEFT),
        )
        graph = axes.get_graph(lambda x: 0.5 / x**2, x_range=(0.01, 10, 0.05))
        graph.make_jagged()
        graph.set_stroke(YELLOW, 2)

        graph_dot = GlowDot(color=WHITE)
        graph_dot.add_updater(lambda d: d.move_to(axes.i2gp(get_d(), graph)))

        d_label.update()
        self.play(
            frame.animate.move_to([3.5, 2.5, 0.0]),
            LaggedStart(
                FadeIn(axes),
                ShowCreation(graph),
                FadeIn(graph_dot),
                ShowCreation(d_line),
                FadeIn(d_label, 0.25 * UP),
            ),
            run_time=2,
        )
        self.wait()

        for buff in (0.4, 8, 1.25):
            self.play(
                charges[1].animate.next_to(charges[0], RIGHT, buff=buff),
                run_time=4
            )
            self.wait()

        # Write Coulomb's law
        coulombs_law = Tex(R"""
            F = {q_1 q_2 \over 4 \pi \epsilon_0} \cdot \frac{1}{r^2}
        """)
        coulombs_law_title = TexText("Coulomb's law")
        coulombs_law_title.move_to(axes, UP)
        coulombs_law.next_to(coulombs_law_title, DOWN, buff=0.75)

        rect = SurroundingRectangle(coulombs_law["q_1 q_2"])
        rect.set_stroke(YELLOW, 2)
        rect.set_fill(YELLOW, 0.25)

        self.play(
            FadeIn(coulombs_law_title),
            FadeIn(coulombs_law, UP),
        )
        self.wait()
        self.add(rect, coulombs_law)
        self.play(FadeIn(rect))
        self.wait()
        self.play(rect.animate.surround(coulombs_law[R"4 \pi \epsilon_0"]))
        self.wait()
        self.play(rect.animate.surround(coulombs_law[R"\frac{1}{r^2}"]))
        self.wait()
        self.play(charges[1].animate.next_to(charges[0], RIGHT, buff=3.0), run_time=3)
        self.play(FadeOut(rect))
        self.wait()

        # Remove graph
        d_line.clear_updaters()
        self.play(
            frame.animate.center(),
            VGroup(coulombs_law, coulombs_law_title).animate.to_corner(UL),
            LaggedStartMap(FadeOut, Group(
                axes, graph, graph_dot, d_line, d_label,
                force_words, coulomb_vects
            )),
            charges[0].animate.center(),
            FadeOut(charges[1]),
            run_time=2,
        )
        self.wait()

        # Show Coulomb's law vector field
        coulombs_law.add_background_rectangle()
        coulombs_law_title.add_background_rectangle()
        field = CoulombField(charges[0], x_density=3.0, y_density=3.0)
        dots = DotCloud(field.sample_points, radius=0.025, color=RED)
        dots.make_3d()

        self.add(dots, coulombs_law_title, coulombs_law)
        self.play(ShowCreation(dots))
        self.wait()
        self.add(field, coulombs_law_title, coulombs_law)
        self.play(FadeIn(field))
        for vect in [2 * RIGHT, 4 * LEFT, 2 * RIGHT]:
            self.play(charges[0].animate.shift(vect).set_anim_args(path_arc=PI, run_time=3))
        self.wait()

        # Electric field
        e_coulombs_law = Tex(R"""
            \vec{E}(\vec{r}) = {q \over 4 \pi \epsilon_0}
            \cdot \frac{1}{||\vec{r}||^2}
            \cdot \frac{\vec{r}}{||\vec{r}||}
        """)
        e_coulombs_law.move_to(coulombs_law, LEFT)
        ebr = BackgroundRectangle(e_coulombs_law)
        r_vect = Vector(2 * RIGHT + UP)
        r_vect.set_stroke(GREEN)
        r_label = e_coulombs_law[R"\vec{r}"][0].copy()
        r_label.next_to(r_vect.get_center(), UP, buff=0.1)
        r_label.set_backstroke(BLACK, 20)

        e_words = VGroup(
            Text("Electric Field:"),
            Text(
                """
                What force would be
                applied to a unit charge
                at a given point
                """,
                t2s={"would": ITALIC},
                t2c={"unit charge": RED},
                alignment="LEFT",
                font_size=36
            ),
        )
        e_words.set_backstroke(BLACK, 20)
        e_words.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        e_words.next_to(e_coulombs_law, DOWN, buff=0.5)
        e_words.to_edge(LEFT, buff=MED_SMALL_BUFF)

        rect.surround(e_coulombs_law[R"\vec{E}"])
        rect.scale(0.9, about_edge=DR)

        self.play(
            FadeOut(coulombs_law, UP),
            FadeIn(ebr, UP),
            FadeIn(e_coulombs_law, UP),
        )
        self.wait()
        self.add(ebr, rect, e_coulombs_law)
        self.play(FadeIn(rect))
        self.play(Write(e_words, stroke_color=BLACK))
        self.wait()
        self.play(
            FadeOut(e_words),
            rect.animate.surround(e_coulombs_law[R"(\vec{r})"][0], buff=0)
        )
        self.add(r_vect, charges[0])
        self.play(
            field.animate.set_stroke(opacity=0.4),
            FadeTransform(e_coulombs_law[R"\vec{r}"][0].copy(), r_label),
            ShowCreation(r_vect),
        )
        self.wait()
        self.play(
            rect.animate.surround(e_coulombs_law[R"\frac{\vec{r}}{||\vec{r}||}"])
        )
        self.wait()

        # Example E vect
        e_vect = r_vect.copy()
        e_vect.scale(0.25)
        e_vect.set_stroke(BLUE)
        e_vect.shift(r_vect.get_end() - e_vect.get_start())
        e_vect_label = Tex(R"\vec{E}", font_size=36)
        e_vect_label.set_backstroke(BLACK, 5)
        e_vect_label.next_to(e_vect.get_center(), UL, buff=0.1).shift(0.05 * UR)

        self.play(
            TransformFromCopy(r_vect, e_vect, path_arc=PI / 2),
            FadeTransform(e_coulombs_law[:2].copy(), e_vect_label),
            run_time=2
        )
        self.wait()

        # Not the full story!
        words = Text("Not the full story!", font_size=60)
        arrow = Vector(LEFT)
        arrow.next_to(coulombs_law_title, RIGHT)
        arrow.set_color(RED)
        words.set_color(RED)
        words.set_backstroke(BLACK, 20)
        words.next_to(arrow, RIGHT)
        charges[1].move_to(20 * RIGHT)

        self.remove(field)
        field = CoulombField(*charges, x_density=3.0, y_density=3.0)
        field.set_stroke(opacity=float(field.get_stroke_opacity()))
        self.add(field)

        self.play(
            FadeIn(words, lag_ratio=0.1),
            ShowCreation(arrow),
            FadeOut(rect),
            FadeOut(r_vect),
            FadeOut(r_label),
            FadeOut(e_vect),
            FadeOut(e_vect_label),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, Group(
                dots, coulombs_law_title, e_coulombs_law,
                words, arrow,
            )),
            FadeOut(ebr),
            charges[0].animate.to_edge(LEFT, buff=1.0),
            charges[1].animate.to_edge(RIGHT, buff=1.0),
            run_time=3,
        )

        # Wiggle here -> wiggle there
        tmp_charges = Group(*(ChargedParticle(track_position_history=True, charge=0.3) for x in range(2)))
        tmp_charges[0].add_updater(lambda m: m.move_to(charges[0]))
        tmp_charges[1].add_updater(lambda m: m.move_to(charges[1]))
        for charge in tmp_charges:
            charge.ignore_last_motion()
        lorentz_field = ColoumbPlusLorentzField(
            *tmp_charges,
            x_density=6.0,
            y_density=6.0,
            norm_to_opacity_func=lambda n: np.clip(0.5 * n, 0, 0.75)
        )
        self.remove(field)
        self.add(lorentz_field, *tmp_charges)

        influence_ring0 = self.get_influence_ring(charges[0].get_center()).set_stroke(opacity=0)
        influence_ring1 = self.get_influence_ring(charges[1].get_center()).set_stroke(opacity=0)
        dist = get_norm(charges[1].get_center() - charges[0].get_center())
        wiggle_kwargs = dict(
            rate_func=lambda t: wiggle(t, 3),
            run_time=1.5,
            suspend_mobject_updating=False,
        )

        self.add(influence_ring0, charges)
        self.play(charges[0].animate.shift(UP).set_anim_args(**wiggle_kwargs))
        self.wait_until(lambda: influence_ring0.get_radius() > dist, max_time=dist / 2.0)

        self.add(influence_ring1)
        self.play(charges[1].animate.shift(0.5 * DOWN).set_anim_args(**wiggle_kwargs))
        self.wait_until(lambda: influence_ring1.get_radius() > dist, max_time=dist / 2.0)
        self.play(charges[0].animate.shift(0.25 * UP).set_anim_args(**wiggle_kwargs))
        self.wait(6)
        self.play(
            FadeOut(influence_ring0),
            FadeOut(influence_ring1),
            FadeOut(lorentz_field)
        )
        self.remove(tmp_charges)

        # Show this the force
        ring = self.get_influence_ring(charges[0].get_center())

        ghost_charge = charges[0].copy().set_opacity(0.25)
        ghost_charge.shift(0.1 * IN)
        a_vect = Vector(UP).shift(charges[0].get_center())
        a_vect.set_stroke(PINK)
        a_label = Tex(R"\vec{a}(t_0)", font_size=48)
        a_label.set_color(PINK)
        a_label.next_to(a_vect, RIGHT, SMALL_BUFF)

        f_vect = Vector(1.0 * DOWN).shift(charges[1].get_center())
        f_vect.set_stroke(BLUE)
        f_label = Tex(R"\vec{F}(t)")
        f_label.set_color(BLUE)
        f_label.next_to(f_vect, LEFT, buff=0.15)

        time_label = Tex("t = 0.00")
        time_label.to_corner(UL)
        time_decimal = time_label.make_number_changeable("0.00")
        time_decimal.add_updater(lambda m: m.set_value(ring.time))

        start_point = charges[0].get_center().copy()
        speed = 2.0

        def field_func(points):
            time = ring.time
            diffs = (points - start_point)
            norms = np.linalg.norm(diffs, axis=1)
            past_times = time - (norms / speed)
            mags = np.exp(-3 * past_times)
            mags[past_times < 0] = 0
            return mags[:, np.newaxis] * DOWN

        field = VectorField(
            field_func,
            height=0,
            x_density=4.0,
            max_vect_len=1.0,
        )
        field.add_updater(lambda f: f.update_vectors())

        self.add(time_label, a_vect, a_label, charges)
        self.wait()
        self.add(ring, ghost_charge, field, charges)

        target = charges[0].get_center() + 2 * UP
        charges[0].add_updater(lambda m, dt: m.shift(3 * dt * (target - m.get_center())))
        self.wait_until(lambda: ring.get_radius() > dist)

        self.add(f_vect, f_label, charges)
        ring.suspend_updating()
        charges[0].suspend_updating()
        self.add(f_vect, charges[1])
        self.play(
            FadeIn(f_vect),
            FadeIn(f_label),
            FadeOut(field),
        )

        # Write the Lorentz force
        lorentz_law = Tex(R"""
            \vec{F}(t) = 
            {-q_1 q_2 \over 4\pi \epsilon_0 c^2}
            {1 \over r}
            \vec{a}_\perp(t - r / c)
        """)
        lorentz_law.to_edge(UP)
        lorentz_law[R"\vec{F}(t)"][0].match_style(f_label)

        a_hat_perp = lorentz_law[R"\vec{a}_\perp"][0]
        a_hat_perp.match_style(a_label)
        a_hat_perp.save_state()
        a_hat_perp[2].set_opacity(0)
        a_hat_perp[:2].move_to(a_hat_perp, RIGHT)
        a_hat_perp[:2].scale(1.25, about_edge=DR)

        lorentz_law["("][1].match_style(a_label)
        lorentz_law[")"][1].match_style(a_label)

        self.play(
            Transform(
                f_label.copy(),
                lorentz_law[R"\vec{F}(t)"][0].copy(),
                remover=True,
                run_time=1.5,
            ),
            FadeIn(lorentz_law, time_span=(1, 2))
        )
        self.wait()

        # Go through parts of the equation
        rect = SurroundingRectangle(lorentz_law["-q_1 q_2"])
        rect.set_stroke(YELLOW, 2)
        rect.set_fill(YELLOW, 0.2)

        r_line = DashedLine(ghost_charge.get_right(), charges[1].get_left())
        r_label = Tex("r").next_to(r_line, UP)

        self.add(rect, lorentz_law)
        self.play(FadeIn(rect))
        self.wait()
        self.play(rect.animate.surround(lorentz_law[R"4\pi \epsilon_0 c^2"]))
        self.wait()
        self.play(
            rect.animate.surround(lorentz_law[R"{1 \over r}"]),
            ShowCreation(r_line),
        )
        self.play(TransformFromCopy(lorentz_law[R"r"][1], r_label))
        self.wait()
        self.play(rect.animate.surround(lorentz_law[R"\vec{a}_\perp(t - r / c)"]))
        self.wait()
        self.play(rect.animate.surround(lorentz_law[R"t - r / c"], buff=0.05))
        self.wait()

        # Indicate back in time
        new_a_label = Tex(R"\vec{a}(t - r / c)")
        new_a_label.match_style(a_label)
        new_a_label.move_to(a_label, LEFT)

        ring.clear_updaters()
        time_decimal.clear_updaters()
        charges[0].clear_updaters()
        self.add(charges[0])
        self.play(
            ring.animate.scale(1e-3),
            UpdateFromFunc(time_decimal, lambda m: m.set_value(
                ring.get_radius() / 2
            )),
            charges[0].animate.shift(2 * DOWN).set_anim_args(
                time_span=(1, 4),
                rate_func=lambda t: smooth(t)**0.5,
            ),
            run_time=4,
        )
        time_decimal.set_value(0)
        self.play(
            TransformMatchingStrings(a_label, new_a_label),
            FadeOut(rect),
        )
        self.remove(rect)
        self.remove(ring)

        # Do another wiggle
        ring = self.get_influence_ring(charges[0].get_center())
        time_decimal.add_updater(lambda m: m.set_value(ring.time))

        self.add(ring)
        self.play(charges[0].animate.shift(UP).set_anim_args(**wiggle_kwargs))
        self.wait_until(lambda: ring.get_radius() > dist)
        self.play(charges[1].animate.shift(0.5 * DOWN).set_anim_args(**wiggle_kwargs))
        self.remove(ring)
        self.play(FadeOut(time_label))

        # Add back perpenducular part
        charges.target = charges.generate_target()
        charges.target.arrange(UR, buff=3).center()
        r_line.target = r_line.generate_target()
        r_line.target.become(DashedLine(
            charges.target[0].get_center(),
            charges.target[1].get_center(),
        ))
        f_vect.target = f_vect.generate_target()
        f_vect.target.rotate(45 * DEGREES)
        f_vect.target.shift(charges.target[1].get_center() - f_vect.target.get_start())
        rect = SurroundingRectangle(a_hat_perp.saved_state, buff=0.1)
        rect.set_stroke(YELLOW, 2)
        rect.set_fill(YELLOW, 0.25)

        self.add(rect, lorentz_law)
        self.play(FadeIn(rect, scale=0.5))
        self.play(Restore(a_hat_perp))
        self.wait()

        self.remove(ghost_charge)
        self.play(
            MoveToTarget(charges),
            MoveToTarget(r_line),
            MoveToTarget(f_vect),
            r_label.animate.next_to(r_line.target.get_center(), UL, SMALL_BUFF),
            f_label.animate.next_to(f_vect.target.get_center(), UR, buff=0),
            new_a_label.animate.next_to(charges.target[0], UL, buff=0),
            MaintainPositionRelativeTo(a_vect, charges[0]),
            run_time=2
        )
        self.wait()

        r_unit = normalize(charges[1].get_center() - charges[0].get_center())
        a_perp_vect = Vector(
            a_vect.get_vector() - np.dot(a_vect.get_vector(), r_unit) * r_unit,
        )
        a_perp_vect.match_style(a_vect)
        a_perp_vect.set_stroke(interpolate_color(PINK, WHITE, 0.5))
        a_perp_vect.shift(a_vect.get_end() - a_perp_vect.get_end())

        a_hat_perp2 = a_hat_perp.copy()
        a_hat_perp2.scale(0.9)
        a_hat_perp2.next_to(a_perp_vect.get_center(), UR, buff=0.1)
        a_hat_perp2.match_color(a_perp_vect)

        self.play(TransformFromCopy(a_vect, a_perp_vect))
        self.play(TransformFromCopy(a_hat_perp, a_hat_perp2))
        self.wait()
        rings = VGroup()
        for x in range(2):
            wiggle_kwargs = dict(
                run_time=2,
                rate_func=lambda t: wiggle(t, 5)
            )
            ring = self.get_influence_ring(charges[0].get_center())
            rings.add(ring)
            dist = get_norm(charges[0].get_center() - charges[1].get_center())

            self.add(ring)
            self.play(charges[0].animate.shift(0.5 * UP).set_anim_args(**wiggle_kwargs))
            self.wait_until(lambda: ring.get_radius() > dist)
            self.play(charges[1].animate.shift(0.25 * DR).set_anim_args(**wiggle_kwargs))
        self.play(FadeOut(rings))

        # Clear the canvas
        plane = NumberPlane(
            background_line_style=dict(stroke_color=GREY_D, stroke_opacity=0.75, stroke_width=1),
            axis_config=dict(stroke_opacity=(0.25))
        )
        new_lorentz = Tex(R"""
            \vec{E}_{\text{rad}}(\vec{r}, t) = 
            {-q \over 4\pi \epsilon_0 c^2}
            {1 \over ||\vec{r}||}
            \vec{a}_\perp(t - ||\vec{r}|| / c)
        """, font_size=36)
        new_lorentz.to_corner(UL)
        lhs = new_lorentz[R"\vec{E}_{\text{rad}}(\vec{r}, t)"]
        lhs.set_color(BLUE)
        new_lorentz[R"\vec{a}_\perp("].set_color(PINK)
        new_lorentz[R")"][1].set_color(PINK)

        lhs_rect = SurroundingRectangle(lhs)
        arrow = Vector(UP).next_to(lhs_rect, DOWN)

        self.add(plane, lorentz_law, *charges)
        self.remove(rect)
        self.play(
            LaggedStartMap(FadeOut, Group(
                r_line, r_label,
                a_hat_perp2, a_perp_vect,
                a_vect, new_a_label, new_a_label,
                f_vect, f_label, charges[1],
            )),
            FadeIn(plane, time_span=(1, 2)),
            charges[0].animate.center().set_anim_args(time_span=(1, 2)),
            FadeTransform(lorentz_law, new_lorentz),
        )
        self.play(
            ShowCreation(lhs_rect),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(FadeOut(lhs_rect), FadeOut(arrow))

        # Show vector field
        charge = ChargedParticle(
            track_position_history=True
        )
        field = LorentzField(
            charge,
            stroke_width=3,
            x_density=4.0,
            y_density=4.0,
            max_vect_len=0.25,
            norm_to_opacity_func=lambda n: np.clip(1.5 * n, 0, 1),
        )
        a_vect = AccelerationVector(charge)
        small_charges = DotCloud(field.sample_points, radius=0.02)
        small_charges.match_color(charges[1][0])
        small_charges.make_3d()
        new_lorentz.set_backstroke(BLACK, 20)

        self.add(small_charges, new_lorentz)
        self.play(ShowCreation(small_charges))
        self.wait()

        self.remove(charges[0])
        self.add(field, a_vect, charge, new_lorentz)
        charge.ignore_last_motion()

        # Have some fun with the charge
        wiggle_kwargs = dict(
            rate_func=lambda t: wiggle(t, 3),
            run_time=3.0,
            suspend_mobject_updating=False,
        )
        lemniscate = ParametricCurve(
            lambda t: np.sin(t)**2 * (np.cos(t) * RIGHT + np.sin(t) * UP),
            t_range=(0, TAU, TAU / 200)
        )

        self.play(
            charge.animate.shift(0.4 * UP).set_anim_args(**wiggle_kwargs),
        )
        self.wait(3)
        self.play(
            MoveAlongPath(charge, lemniscate, run_time=6)
        )
        self.wait(3)
        for point in [2 * RIGHT, ORIGIN]:
            self.play(charge.animate.move_to(point).set_anim_args(path_arc=PI, run_time=5, suspend_mobject_updating=False))
        self.wait(5)

        # Set it oscillating
        # CHANGE: init_clock needs start_point (a bug in the original: it was called without an argument); the charge's current position is used
        charge.init_clock(charge.get_center())
        charge.ignore_last_motion()
        charge.add_updater(lambda m: m.move_to(
            0.25 * np.sin(0.5 * TAU * m.get_internal_time()) * UP
        ))
        self.wait(30)

    def get_influence_ring(self, center_point, color=WHITE, speed=2.0, max_width=3.0, width_decay_exp=0.5):
        return get_influence_ring(center_point, color, speed, max_width, width_decay_exp)
