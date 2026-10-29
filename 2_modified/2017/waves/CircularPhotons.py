# ==============================================================================
# Scene:      CircularPhotons
# Source:     videos/_2017/waves.py (lines 4020-4182)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CircularPhotons.py CircularPhotons -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 3: sorted() takes key=, not a cmp function
#   - bug of the original (self passed twice to get_photon)
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


E_COLOR = BLUE


M_COLOR = YELLOW


class OscillatingVector(ContinualAnimation):
    CONFIG = {
        "tail" : ORIGIN,
        "frequency" : 1,
        "A_vect" : [1, 0, 0],
        "phi_vect" : [0, 0, 0],
        "vector_to_be_added_to" : None,
    }
    def setup(self):
        self.vector = self.mobject

    def update_mobject(self, dt):
        f = self.frequency
        t = self.internal_time
        angle = 2*np.pi*f*t
        vect = np.array([
            A*np.exp(complex(0, angle + phi))
            for A, phi in zip(self.A_vect, self.phi_vect)
        ]).real
        self.update_tail()
        self.vector.put_start_and_end_on(self.tail, self.tail+vect)

    def update_tail(self):
        if self.vector_to_be_added_to is not None:
            self.tail = self.vector_to_be_added_to.get_end()


class EMWave(ContinualAnimationGroup):
    CONFIG = {
        "wave_number" : 1,
        "frequency" : 0.25,
        "n_vectors" : 40,
        "propogation_direction" : RIGHT,
        "start_point" : FRAME_X_RADIUS*LEFT + DOWN + OUT,
        "length" : FRAME_WIDTH,
        "amplitude" : 1,
        "rotation" : 0,
        "A_vect" : [0, 0, 1],
        "phi_vect" : [0, 0, 0],
        "requires_start_up" : False,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        if not all(self.propogation_direction == RIGHT):
            self.matrix_transform = np.dot(
                z_to_vector(self.propogation_direction),
                np.linalg.inv(z_to_vector(RIGHT)),
            )
        else:
            self.matrix_transform = None

        vector_oscillations = []
        self.E_vects = VGroup()
        self.M_vects = VGroup()

        self.A_vect = np.array(self.A_vect)/get_norm(self.A_vect)
        self.A_vect *= self.amplitude

        for alpha in np.linspace(0, 1, self.n_vectors):
            tail = interpolate(ORIGIN, self.length*RIGHT, alpha)
            phase = -alpha*self.length*self.wave_number
            kwargs = {
                "phi_vect" : np.array(self.phi_vect) + phase,
                "frequency" : self.frequency,
                "tail" : np.array(tail),
            }
            E_ov = OscillatingVector(
                Vector(
                    OUT, color = E_COLOR,
                    normal_vector = UP,
                ),
                A_vect = self.A_vect,
                **kwargs
            )
            M_ov = OscillatingVector(
                Vector(
                    UP, color = M_COLOR,
                    normal_vector = OUT,
                ),
                A_vect = rotate_vector(self.A_vect, np.pi/2, RIGHT),
                **kwargs
            )
            vector_oscillations += [E_ov, M_ov]
            self.E_vects.add(E_ov.vector)
            self.M_vects.add(M_ov.vector)
        ContinualAnimationGroup.__init__(self, *vector_oscillations)

    def update_mobject(self, dt):
        if self.requires_start_up:
            n_wave_lengths = self.length / (2*np.pi*self.wave_number)
            prop_time = n_wave_lengths/self.frequency
            middle_alpha = interpolate(
                0.4, 1.4,
                self.external_time / prop_time
            )
            new_smooth = squish_rate_func(smooth, 0.4, 0.6)

            ovs = self.continual_animations
            for ov, alpha in zip(ovs, np.linspace(0, 1, len(ovs))):
                epsilon = 0.0001
                new_amplitude = np.clip(
                    new_smooth(middle_alpha - alpha), epsilon, 1
                )
                norm = get_norm(ov.A_vect)
                if norm != 0:
                    ov.A_vect = new_amplitude * np.array(ov.A_vect) / norm

        ContinualAnimationGroup.update_mobject(self, dt)
        self.mobject.rotate(self.rotation, RIGHT)
        if self.matrix_transform:
            self.mobject.apply_matrix(self.matrix_transform)
        self.mobject.shift(self.start_point)


class WavePacket(Animation):
    CONFIG = {
        "EMWave_config" : {
            "wave_number" : 0,
            "start_point" : FRAME_X_RADIUS*LEFT,
            "phi_vect" : np.ones(3)*np.pi/4,
        },
        "em_wave" : None,
        "run_time" : 4,
        "rate_func" : None,
        "packet_width" : 6,
        "include_E_vects" : True,
        "include_M_vects" : True,
        "filter_distance" : FRAME_X_RADIUS,
        "get_filtered" : False,
        "remover" : True,
        "width" : 2*np.pi,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        em_wave = self.em_wave
        if em_wave is None:
            em_wave = EMWave(**self.EMWave_config)
            em_wave.update(0)
            self.em_wave = em_wave

        self.vects = VGroup()
        if self.include_E_vects:
            self.vects.add(*em_wave.E_vects)
        if self.include_M_vects:
            self.vects.add(*em_wave.M_vects)
        for vect in self.vects:
            vect.save_state()

        u = em_wave.propogation_direction
        self.wave_packet_start, self.wave_packet_end = [
            em_wave.start_point - u*self.packet_width/2,
            em_wave.start_point + u*(em_wave.length + self.packet_width/2)
        ]
        Animation.__init__(self, self.vects, **kwargs)

    def interpolate_mobject(self, alpha):
        packet_center = interpolate(
            self.wave_packet_start,
            self.wave_packet_end,
            alpha
        )
        em_wave = self.em_wave
        for vect in self.vects:
            tail = vect.get_start()
            distance_from_packet = np.dot(
                tail - packet_center,
                em_wave.propogation_direction
            )
            A = em_wave.amplitude*self.E_func(distance_from_packet)
            distance_from_start = get_norm(tail - em_wave.start_point)
            if self.get_filtered and distance_from_start > self.filter_distance:
                A = 0
            epsilon = 0.05
            if abs(A) < epsilon:
                A = 0
            vect.restore()
            vect.scale(A/vect.get_length(), about_point = tail)

    def E_func(self, x):
        x0 = 2*np.pi*x/self.width
        return np.sin(x0)*np.exp(-0.25*x0*x0)


class PolarizingFilter(Circle):
    CONFIG = {
        "stroke_color" : GREY_D,
        "fill_color" : GREY_B,
        "fill_opacity" : 0.5,
        "label_tex" : None,
        "filter_angle" : 0,
        "include_arrow_label" : True,
        "arrow_length" : 0.7,
    }
    def __init__(self, **kwargs):
        Circle.__init__(self, **kwargs)

        if self.label_tex:
            self.label = OldTex(self.label_tex)
            self.label.next_to(self.get_top(), DOWN, MED_SMALL_BUFF)
            self.add(self.label)

        arrow = Arrow(
            ORIGIN, self.arrow_length*UP, 
            color = WHITE,
            buff = 0,
        )
        arrow.shift(self.get_top())
        arrow.rotate(-self.filter_angle)
        self.add(arrow)
        self.arrow = arrow
        shade_in_3d(self)

        if self.include_arrow_label:
            arrow_label = OldTex(
                "%.1f^\\circ"%(self.filter_angle*180/np.pi)
            )
            arrow_label.add_background_rectangle()
            arrow_label.next_to(arrow.get_tip(), UP)
            self.add(arrow_label)
            self.arrow_label = arrow_label


class FilterScene(ThreeDScene):
    CONFIG = {
        "filter_x_coordinates" : [0],
        "pol_filter_configs" : [{}],
        "EMWave_config" : {
            "start_point" : FRAME_X_RADIUS*LEFT + DOWN+OUT
        },
        "axes_config" : {},
        "start_phi" : 0.8*np.pi/2,
        "start_theta" : -0.6*np.pi,
        "ambient_rotation_rate" : 0.01,
    }
    def setup(self):
        self.axes = ThreeDAxes(**self.axes_config)
        self.add(self.axes)
        for x in range(len(self.filter_x_coordinates) - len(self.pol_filter_configs)):
            self.pol_filter_configs.append({})
        self.pol_filters = VGroup(*[
            PolarizingFilter(**config)
            for config in self.pol_filter_configs
        ])
        self.pol_filters.rotate(np.pi/2, RIGHT)
        self.pol_filters.rotate(-np.pi/2, OUT)
        pol_filter_shift = np.array(self.EMWave_config["start_point"])
        pol_filter_shift[0] = 0
        self.pol_filters.shift(pol_filter_shift)
        for x, pf in zip(self.filter_x_coordinates, self.pol_filters):
            pf.shift(x*RIGHT)
        self.add(self.pol_filters)
        self.pol_filter = self.pol_filters[0]

        self.set_camera_orientation(self.start_phi, self.start_theta)
        if self.ambient_rotation_rate > 0:
            self.begin_ambient_camera_rotation(self.ambient_rotation_rate)

    def get_filter_absorption_animation(self, pol_filter, photon):
        x = pol_filter.get_center()[0]
        alpha = (x + FRAME_X_RADIUS) / (FRAME_WIDTH)
        return ApplyMethod(
            pol_filter.set_fill, RED,
            run_time = photon.run_time,
            rate_func = squish_rate_func(there_and_back, alpha - 0.1, alpha + 0.1)
        )


class DirectionOfPolarizationScene(FilterScene):
    CONFIG = {
        "pol_filter_configs" : [{
            "include_arrow_label" : False,
        }],
        "target_theta" : -0.97*np.pi,
        "target_phi" : 0.9*np.pi/2,
        "ambient_rotation_rate" : 0.005,
        "apply_filter" : False,
        "quantum" : False,
    }
    def setup(self):
        self.reference_line = Line(ORIGIN, RIGHT)
        self.reference_line.set_stroke(width = 0)
        self.em_wave = EMWave(**self.EMWave_config)
        self.add(self.em_wave)

        FilterScene.setup(self)

    def change_polarization_direction(self, angle, **kwargs):
        added_anims = kwargs.get("added_anims", [])
        self.play(
            ApplyMethod(
                self.reference_line.rotate, angle,
                **kwargs
            ),
            *added_anims
        )

    def setup_rectangles(self):
        rect1 = Rectangle(
            height = 2*self.em_wave.amplitude,
            width = FRAME_X_RADIUS + 0.25,
            stroke_color = BLUE,
            fill_color = BLUE,
            fill_opacity = 0.2,
        )
        rect1.rotate(np.pi/2, RIGHT)
        pf_copy = self.pol_filter.deepcopy()
        pf_copy.remove(pf_copy.arrow)
        center = pf_copy.get_center()
        rect1.move_to(center, RIGHT)
        rect2 = rect1.copy()
        rect2.move_to(center, LEFT)

        self.rectangles = VGroup(rect1, rect2)

    def update_mobjects(self, *args, **kwargs):
        reference_angle = self.reference_line.get_angle()
        self.em_wave.rotation = reference_angle
        FilterScene.update_mobjects(self, *args, **kwargs)
        if self.apply_filter:
            self.apply_filters()
        self.update_rectangles()

    def apply_filters(self):
        vect_groups = [self.em_wave.E_vects, self.em_wave.M_vects]
        # CHANGE: Python 3: sorted() takes key=, not a cmp function
        filters = sorted(
            self.pol_filters,
            key = lambda pf : pf.get_center()[0],
        )
        for pol_filter in filters:
            filter_x = pol_filter.arrow.get_center()[0]
            for vect_group, angle in zip(vect_groups, [0, -np.pi/2]):
                target_angle = pol_filter.filter_angle + angle
                for vect_mob in vect_group:
                    vect = vect_mob.get_vector()
                    vect_angle = angle_of_vector([
                        vect[2], -vect[1]
                    ])
                    angle_diff = target_angle - vect_angle
                    angle_diff = (angle_diff+np.pi/2)%np.pi - np.pi/2
                    start, end = vect_mob.get_start_and_end()
                    if start[0] > filter_x:
                        vect_mob.rotate(angle_diff, RIGHT)
                        if not self.quantum:
                            vect_mob.scale(
                                np.cos(angle_diff),
                                about_point = start,
                            )

    def update_rectangles(self):
        if not hasattr(self, "rectangles") or self.rectangles not in self.mobjects:
            return

        r1, r2 = self.rectangles

        target_angle = self.reference_line.get_angle()
        anchors = r1.get_anchors()
        vect = anchors[0] - anchors[3]
        curr_angle = angle_of_vector([vect[2], -vect[1]])
        r1.rotate(target_angle - curr_angle, RIGHT)

        epsilon = 0.001
        curr_depth = max(r2.get_depth(), epsilon)
        target_depth = max(
            2*self.em_wave.amplitude*abs(np.cos(target_angle)),
            epsilon
        )
        r2.stretch_in_place(target_depth/curr_depth, 2)


class ShootPhotonThroughFilter(DirectionOfPolarizationScene):
    CONFIG = {
        "EMWave_config" : {
            "wave_number" : 0,
            "A_vect" : [0, 1, 1],
            "start_point" : FRAME_X_RADIUS*LEFT,
            "amplitude" : np.sqrt(2),
        },
        "pol_filter_configs" : [{
            "label_tex" : "\\text{Filter}",
            "include_arrow_label" : False,
        }],
        "apply_filter" : True,
        "quantum" : True,
        "pre_filter_alpha" : 0.35,
        "ambient_rotation_rate" : 0,
    }
    def setup(self):
        DirectionOfPolarizationScene.setup(self)
        self.em_wave.update(0)
        self.remove(self.em_wave)

    def construct(self):
        self.force_skipping()

        self.add_superposition_tex()
        self.ask_what_would_happen()
        self.expect_half_energy_to_be_absorbed()
        self.probabalistic_passing_and_blocking()
        # self.note_change_in_polarization()

    def add_superposition_tex(self):
        superposition_tex = OldTex(
            "|\\!\\nearrow\\rangle", 
            "=",
            "(\\sqrt{1/2})", "|\\!\\rightarrow \\rangle", "+",
            "(\\sqrt{1/2})", "|\\!\\uparrow \\rangle",
        )
        superposition_tex.scale(0.9)
        superposition_tex[0].set_color(E_COLOR)
        halves = superposition_tex.get_parts_by_tex("1/2")
        for half, color in zip(halves, [RED, GREEN]):
            half.set_color(color)

        h_rect = SurroundingRectangle(VGroup(*superposition_tex[2:4]))
        v_rect = SurroundingRectangle(VGroup(*superposition_tex[5:7]))
        VGroup(h_rect, v_rect).fade(1)
        superposition_tex.h_rect = h_rect
        superposition_tex.v_rect = v_rect
        superposition_tex.add(h_rect, v_rect)

        superposition_tex.next_to(ORIGIN, LEFT)
        superposition_tex.to_edge(UP)
        superposition_tex.rotate(np.pi/2, RIGHT)
        self.superposition_tex = superposition_tex

    def ask_what_would_happen(self):
        photon = self.get_photon(
            rate_func = lambda t : self.pre_filter_alpha*t,
            remover = False,
            run_time = 0.6,
        )
        question = OldTexText("What's going to happen?")
        question.add_background_rectangle()
        question.set_color(YELLOW)
        question.rotate(np.pi/2, RIGHT)
        question.next_to(self.superposition_tex, IN)

        self.pol_filter.add(
            self.pol_filter.arrow.copy().rotate(np.pi/2, OUT)
        )
        self.pol_filter.save_state()
        self.pol_filter.shift(5*OUT)

        self.set_camera_orientation(theta = -0.9*np.pi)
        self.play(self.pol_filter.restore)
        self.move_camera(
            theta = -0.6*np.pi,
        )
        self.play(
            photon,
            FadeIn(self.superposition_tex)
        )
        self.play(Write(question, run_time = 1))
        self.wait()
        self.play(FadeOut(self.pol_filter.label))
        self.pol_filter.remove(self.pol_filter.label)
        self.add(self.pol_filter)

        self.question = question
        self.frozen_photon = photon

    def expect_half_energy_to_be_absorbed(self):
        words = OldTexText("Absorbs horizontal \\\\ energy")
        words.set_color(RED)
        words.next_to(ORIGIN, UP+RIGHT, MED_LARGE_BUFF)
        words.rotate(np.pi/2, RIGHT)
        words.rotate(np.pi/2, OUT)

        lines = VGroup(*[
            Line(
                np.sin(a)*RIGHT + np.cos(a)*UP,
                np.sin(a)*LEFT + np.cos(a)*UP,
                color = RED,
                stroke_width = 2,
            )
            for a in np.linspace(0, np.pi, 15)
        ])
        lines.rotate(np.pi/2, RIGHT)
        lines.rotate(np.pi/2, OUT)

        self.move_camera(
            phi = np.pi/2, theta = 0, 
            added_anims = [
                Rotate(self.superposition_tex, np.pi/2),
            ] + [
                ApplyMethod(
                    v.rotate, 
                    -np.pi/2, 
                    method_kwargs = {"axis" : v.get_vector()}
                )
                for v in self.frozen_photon.mobject
            ]
        )
        self.play(
            Write(words, run_time = 2),
            self.superposition_tex.h_rect.set_stroke, RED, 3,
            *list(map(GrowFromCenter, lines))+\
            [
                Animation(self.pol_filter), 
                Animation(self.frozen_photon.mobject)
            ]
        )
        self.wait(2)
        self.move_camera(
            phi = 0.8*np.pi/2, theta = -0.7*np.pi,
            added_anims = [
                FadeOut(words),
                Animation(lines),
                Rotate(self.superposition_tex, -np.pi/2),
            ] + [
                ApplyMethod(
                    v.rotate, 
                    np.pi/2, 
                    method_kwargs = {"axis" : v.get_vector()}
                )
                for v in self.frozen_photon.mobject
            ]
        )
        self.play(
            FadeOut(lines), 
            FadeOut(self.question),
            self.superposition_tex.h_rect.fade, 1,
            Animation(self.pol_filter)
        )
        self.wait()

        self.absorption_words = words

    def probabalistic_passing_and_blocking(self):
        absorption = self.get_filter_absorption_animation(
            self.pol_filter, self.get_blocked_photon()
        )
        prob = OldTex("P(", "\\text{pass}", ")", "=", "1/2")
        prob.set_color_by_tex("pass", GREEN)
        prob.rotate(np.pi/2, RIGHT)
        prob.next_to(self.superposition_tex, IN, MED_SMALL_BUFF, RIGHT)

        self.remove(self.frozen_photon.mobject)
        self.play(
            self.get_photon(),
            rate_func = lambda t : min(t+self.pre_filter_alpha, 1),
        )
        self.play(
            FadeIn(prob),
            self.get_blocked_photon(),
            absorption
        )
        bools = 6*[True] + 6*[False]
        self.revert_to_original_skipping_status()
        random.shuffle(bools)
        for should_pass in bools:
            if should_pass:
                self.play(self.get_photon(), run_time = 1)
            else:
                self.play(
                    self.get_blocked_photon(), 
                    Animation(self.axes),
                    absorption,
                    run_time = 1
                )
        self.play(FadeOut(prob))

    def note_change_in_polarization(self):
        words = OldTexText(
            "``Collapses'' \\\\ from", "$|\\!\\nearrow\\rangle$",
            "to", "$|\\!\\uparrow\\rangle$"
        )
        words.set_color_by_tex("nearrow", E_COLOR)
        words.set_color_by_tex("uparrow", GREEN)
        words.next_to(ORIGIN, RIGHT, MED_LARGE_BUFF)
        words.shift(2*UP)
        words.rotate(np.pi/2, RIGHT)
        photon = self.get_photon(run_time = 4)
        for vect in photon.mobject:
            if vect.get_center()[0] > 0:
                vect.saved_state.set_fill(GREEN)

        self.play(FadeIn(words), photon)
        for x in range(3):
            self.play(photon)

    ######

    def get_photon(self, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1)
        kwargs["include_M_vects"] = False
        return WavePacket(em_wave = self.em_wave.copy(), **kwargs)

    def get_blocked_photon(self, **kwargs):
        kwargs["get_filtered"] = True
        # CHANGE: bug of the original (self passed twice to get_photon)
        return self.get_photon(**kwargs)


class CircularPhotons(ShootPhotonThroughFilter):
    CONFIG = {
        "EMWave_config" : {
            "phi_vect" : [0, -np.pi/2, 0],
            "wave_number" : 1,
            "start_point" : 10*LEFT,
            "length" : 20,
            "n_vectors" : 60,
        },
        "apply_filter" : False,
    }
    def construct(self):
        self.set_camera_orientation(theta = -0.75*np.pi)
        self.setup_filter()
        self.show_phase_difference()
        self.shoot_circular_photons()
        self.show_filter()
        self.show_vertically_polarized_light()

    def setup_filter(self):
        pf = self.pol_filter
        pf.remove(pf.label)
        pf.remove(pf.arrow)
        self.remove(pf.label, pf.arrow)
        arrows = VGroup(*[
            Arrow(
                v1, v2,
                color = WHITE,
                path_arc = np.pi,
            )
            for v1, v2 in [(LEFT, RIGHT), (RIGHT, LEFT)]
        ])
        arrows.scale(0.7)
        arrows.rotate(np.pi/2, RIGHT)
        arrows.rotate(np.pi/2, OUT)
        arrows.move_to(center_of_mass(pf.get_points()))

        pf.label = arrows
        pf.add(arrows)
        self.remove(pf)

    def show_phase_difference(self):
        equation = OldTex(
            "|\\!\\circlearrowright\\rangle", 
            "=", "\\frac{1}{\\sqrt{2}}", "|\\!\\rightarrow\\rangle",
            "+", "\\frac{i}{\\sqrt{2}}", "|\\!\\uparrow\\rangle",
        )
        equation.set_color_by_tex_to_color_map({
            "circlearrowright" : BLUE,
            "rightarrow" : RED,
            "uparrow" : GREEN,
        })
        equation.next_to(ORIGIN, LEFT, LARGE_BUFF)
        equation.to_edge(UP)
        rect = SurroundingRectangle(equation.get_part_by_tex("frac{i}"))
        words = OldTexText("Phase shift")
        words.next_to(rect, DOWN)
        words.set_color(YELLOW)

        group = VGroup(equation, rect, words)
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/4, IN)

        self.play(FadeIn(equation))
        self.play(self.get_circular_photon())
        self.play(
            ShowCreation(rect),
            Write(words, run_time = 1)
        )

        self.circ_equation_group = group

    def shoot_circular_photons(self):
        for x in range(2):
            self.play(self.get_circular_photon())

    def show_filter(self):
        pf = self.pol_filter
        pf.save_state()
        pf.shift(4*OUT)
        pf.fade(1)

        self.play(pf.restore)
        self.play(
            self.get_circular_photon(),
            Animation(self.circ_equation_group)
        )
        self.play(FadeOut(self.circ_equation_group))

    def show_vertically_polarized_light(self):
        equation = OldTex(
            "|\\!\\uparrow \\rangle", 
            "=", "\\frac{i}{\\sqrt{2}}", "|\\!\\circlearrowleft \\rangle",
            "+", "\\frac{-i}{\\sqrt{2}}", "|\\!\\circlearrowright \\rangle",
        )
        equation.set_color_by_tex_to_color_map({
            "circlearrowright" : BLUE,
            "frac{-i}" : BLUE,
            "circlearrowleft" : YELLOW,
            "frac{i}" : YELLOW,
            "uparrow" : GREEN,
        })
        equation.next_to(ORIGIN, LEFT, LARGE_BUFF)
        equation.to_edge(UP)

        prob = OldTex(
            "P(", "\\text{passing}", ")",
            "=", "\\left(", "\\frac{-i}{\\sqrt{2}}", "\\right)^2"
        )
        prob.set_color_by_tex("sqrt{2}", BLUE)
        prob.next_to(equation, DOWN)

        group = VGroup(equation, prob)
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/4, IN)

        em_wave = EMWave(
            wave_number = 0,
            amplitude = 2,
            start_point = 10*LEFT,
            length = 20,
        )
        v_photon = WavePacket(
            em_wave = em_wave, 
            include_M_vects = False,
            run_time = 2
        )
        c_photon = self.get_circular_photon()
        for v_vect in v_photon.mobject:
            v_vect.saved_state.set_fill(GREEN)
            if v_vect.get_start()[0] > 0:
                v_vect.saved_state.set_fill(opacity = 0)
        for c_vect in c_photon.mobject:
            if c_vect.get_start()[0] < 0:
                c_vect.saved_state.set_fill(opacity = 0)
        blocked_v_photon = copy.deepcopy(v_photon)
        blocked_v_photon.get_filtered = True
        blocked_v_photon.filter_distance = 10

        self.play(Write(equation, run_time = 1))
        self.play(v_photon, c_photon)
        self.play(FadeIn(prob))
        bools = 3*[True] + 3*[False]
        random.shuffle(bools)
        for should_pass in bools:
            if should_pass:
                self.play(v_photon, c_photon)
            else:
                self.play(
                    blocked_v_photon,
                    self.get_filter_absorption_animation(
                        self.pol_filter, blocked_v_photon
                    )
                )
        self.wait()

    ####

    def get_circular_photon(self, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 2)
        photon = ShootPhotonThroughFilter.get_photon(self, **kwargs)
        photon.E_func = lambda x : np.exp(-0.25*(2*np.pi*x/photon.width)**2)
        return photon
