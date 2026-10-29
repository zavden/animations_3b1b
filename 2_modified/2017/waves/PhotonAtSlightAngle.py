# ==============================================================================
# Scene:      PhotonAtSlightAngle
# Source:     videos/_2017/waves.py (lines 3430-3846)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PhotonAtSlightAngle.py PhotonAtSlightAngle -w -m --fps 15
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


class ThreeFilters(ShootPhotonThroughFilter):
    CONFIG = {
        "filter_x_coordinates" : [-4, 0, 4],
        "pol_filter_configs" : [
            {"filter_angle" : 0},
            {"filter_angle" : np.pi/4},
            {"filter_angle" : np.pi/2},
        ],
        "EMWave_config" : {
            "A_vect" : [0, 0, 1],
            "amplitude" : 1.5,
            "n_vectors" : 60,
        },
        "line_start_length" : 8,
        "line_end_length" : 8,
        "n_lines" : 20,
        "lines_depth" : 1.8,
        "lines_shift_vect" : SMALL_BUFF*OUT,
        "random_seed" : 6,
    }
    def construct(self):
        self.remove(self.axes)
        self.setup_filters()
        self.setup_lines()
        self.setup_arrows()

        self.fifty_percent_pass_second()
        self.show_changed_to_diagonal()
        self.fifty_percent_to_pass_third()
        self.show_lines_with_middle()
        self.remove_middle_then_put_back()

    def setup_filters(self):
        for pf in self.pol_filters:
            pf.arrow_label.rotate(np.pi/2, OUT)
            pf.arrow_label.next_to(pf.arrow, RIGHT)
            pf.arrow_label.rotate(np.pi/2, LEFT)
            pf.arrow_label.add_background_rectangle()
            pf.arrow_label.rotate(np.pi/2, RIGHT)
            self.add_foreground_mobject(pf.arrow_label)

    def setup_lines(self):
        lines_group = VGroup(*[
            self.get_lines(pf1, pf2, ratio)
            for pf1, pf2, ratio in zip(
                [None] + list(self.pol_filters),
                list(self.pol_filters) + [None],
                [1, 1, 0.5, 0.25]
            )
        ])
        lines = lines_group[0]
        spacing = lines[1].get_start() - lines[0].get_start()
        lines.add(lines.copy().shift(spacing/2))
        self.lines_group = lines_group

        self.A_to_C_lines = self.get_lines(
            self.pol_filters[0], self.pol_filters[2],
        )

    def setup_arrows(self):
        for E_vect in self.em_wave.E_vects:
            E_vect.normal_vector = IN+DOWN
        self.em_wave.update(0)

    def fifty_percent_pass_second(self):
        arrow = Arrow(
            ORIGIN, 3*RIGHT,
            use_rectangular_stem = False,
            path_arc = -0.8*np.pi
        )
        label = OldTex("50\\%")
        label.next_to(arrow, UP)
        group = VGroup(arrow, label)
        group.rotate(np.pi/2, RIGHT)
        group.next_to(self.pol_filters[1], OUT, buff = 0)
        group.set_color(BLUE)

        l1, l2, l3 = self.lines_group[:3]
        pf1, pf2, pf3 = self.pol_filters
        kwargs = {
            "lag_ratio" : 0,
            "rate_func" : None,
        }

        self.play(ShowCreation(l1, run_time = 1, **kwargs))
        self.play(
            ShowCreation(l2, **kwargs),
            Animation(VGroup(pf1, l1)),
            ShowCreation(arrow),
            run_time = 0.5,
        )
        self.play(
            ShowCreation(l3, **kwargs),
            Animation(VGroup(pf2, l2, pf1, l1)),
            FadeIn(label),
            run_time = 0.5, 
        )
        self.wait(2)
        self.play(
            FadeOut(l3),
            Animation(pf2), 
            FadeOut(l2),
            Animation(pf1),
            FadeOut(l1)
        )

        self.fifty_percent_arrow_group = group

    def show_changed_to_diagonal(self):
        photon = self.get_photon(
            run_time = 2,
            rate_func = lambda x : 0.6*x,
            remover = False,
        )
        brace = Brace(Line(1.5*LEFT, 1.5*RIGHT), DOWN)
        label = brace.get_text(
            "Changed to", 
            "$|\\!\\nearrow\\rangle$"
        )
        label.set_color_by_tex("rangle", BLUE)
        group = VGroup(brace, label)
        group.rotate(np.pi/2, RIGHT)
        group.shift(2*RIGHT + 0.5*IN)

        self.play(photon)
        self.play(
            GrowFromCenter(brace),
            Write(label, run_time = 1)
        )
        kwargs = {
            "run_time" : 3,
            "rate_func" : there_and_back_with_pause,
        }
        self.move_camera(
            phi = np.pi/2,
            theta = 0,
            added_anims = [
                Animation(VGroup(*self.pol_filters[:2]))
            ] + [
                Rotate(
                    v, np.pi/2, 
                    axis = v.get_vector(),
                    in_place = True,
                    **kwargs
                )
                for v in photon.mobject
            ] + [
                Animation(self.pol_filters[2]),
                Rotate(
                    label, np.pi/2, 
                    axis = OUT,
                    in_place = True,
                    **kwargs
                ),
            ],
            **kwargs
        )
        self.wait()

        self.photon = photon
        self.brace_group = VGroup(brace, label)

    def fifty_percent_to_pass_third(self):
        arrow_group = self.fifty_percent_arrow_group.copy()
        arrow_group.shift(4*RIGHT)
        arrow, label = arrow_group

        a = self.photon.rate_func(1)
        new_photon = self.get_photon(
            rate_func = lambda x : (1-a)*x + a,
            run_time = 1
        )

        self.revert_to_original_skipping_status()
        self.play(
            ShowCreation(arrow),
            Write(label, run_time = 1)
        )
        self.remove(self.photon.mobject)
        self.play(new_photon)

        self.second_fifty_percent_arrow_group = arrow_group

    def show_lines_with_middle(self):
        l1, l2, l3, l4 = self.lines_group
        pf1, pf2, pf3 = self.pol_filters

        self.play(
            FadeIn(l4),
            Animation(pf3),
            FadeIn(l3),
            Animation(pf2),
            FadeIn(l2),
            Animation(pf1),
            FadeIn(l1),
            FadeOut(self.brace_group)
        )
        self.wait(2)

    def remove_middle_then_put_back(self):
        l1, l2, l3, l4 = self.lines_group
        pf1, pf2, pf3 = self.pol_filters
        mid_lines = self.A_to_C_lines
        mover = VGroup(
            pf2, 
            self.fifty_percent_arrow_group,
            self.second_fifty_percent_arrow_group,
        )

        arrow = Arrow(
            ORIGIN, 7*RIGHT,
            path_arc = 0.5*np.pi,
        )
        labels = VGroup(*list(map(Tex, ["0\\%", "25\\%"])))
        labels.scale(1.5)
        labels.next_to(arrow, DOWN)
        group = VGroup(arrow, labels)
        group.rotate(np.pi/2, RIGHT)
        group.shift(2*LEFT + IN)
        group.set_color(GREEN)

        self.remove(l2, l3)
        self.play(
            FadeOut(l4),
            Animation(pf3),
            FadeOut(l3),
            ApplyMethod(
                mover.shift, 3*OUT,
                rate_func = running_start
            ),
            ReplacementTransform(l2.copy(), mid_lines),
            Animation(pf1),
            Animation(l1)
        )
        self.play(
            ShowCreation(arrow),
            Write(labels[0], run_time = 1)
        )
        self.wait(2)
        self.play(
            FadeIn(l4),
            Animation(pf3),
            FadeOut(mid_lines),
            FadeIn(l3),
            mover.shift, 3*IN,
            FadeIn(l2),
            Animation(pf1),
            Animation(l1)
        )
        self.play(ReplacementTransform(*labels))
        self.wait(3)


    ####

    def get_photon(self, **kwargs):
        return ShootPhotonThroughFilter.get_photon(self, width = 4, **kwargs)

    def get_lines(self, filter1 = None, filter2 = None, ratio = 1.0):
        n = self.n_lines
        start, end = [
            (f.point_from_proportion(0.75) if f is not None else None)
            for f in (filter1, filter2)
        ]
        if start is None:
            start = end + self.line_start_length*LEFT
        if end is None:
            end = start + self.line_end_length*RIGHT
        nudge = (float(self.lines_depth)/self.n_lines)*OUT
        lines = VGroup(*[
            Line(start, end).shift(z*nudge)
            for z in range(n)
        ])
        lines.set_stroke(YELLOW, 2)
        lines.move_to(start, IN+LEFT)
        lines.shift(self.lines_shift_vect)
        n_to_block = int((1-ratio)*self.n_lines)
        random.seed(self.random_seed)
        indices_to_block = random.sample(
            list(range(self.n_lines)), n_to_block
        )
        VGroup(*[lines[i] for i in indices_to_block]).set_stroke(width = 0)
        return lines


class PhotonAtSlightAngle(ThreeFilters):
    CONFIG = {
        "filter_x_coordinates" : [3],
        "pol_filter_configs" : [{
            "label_tex" : "",
            "include_arrow_label" : False,
            "radius" : 1.4,
        }],
        "EMWave_config" : {
            "wave_number" : 0,
            "A_vect" : [0, np.sin(np.pi/8), np.cos(np.pi/8)],
            "start_point" : FRAME_X_RADIUS*LEFT,
            "amplitude" : 2,
        },
        "axes_config" : {
            "z_max" : 2.5,
        },
        "radius" : 1.3,
        "lines_depth" : 2.5,
        "line_start_length" : 12,
    }
    def construct(self):
        self.force_skipping()

        self.shoot_photon()
        self.reposition_camera_to_head_on()
        self.write_angle()
        self.write_components()
        self.classical_energy_conception()
        self.reposition_camera_back()
        self.rewrite_15_percent_meaning()
        self.probabalistic_passing()

    def shoot_photon(self):
        photon = self.get_photon(
            rate_func = lambda x : 0.5*x,
            remover = False,
        )
        self.play(photon)
        self.photon = photon

    def reposition_camera_to_head_on(self):
        self.move_camera(
            phi = np.pi/2, theta = 0,
            added_anims = list(it.chain(*[
                [
                    v.rotate, np.pi/2, v.get_vector(),
                    v.set_fill, None, 0.7,
                ]
                for v in self.photon.mobject
            ])) + [Animation(self.pol_filter)]
        )

    def write_angle(self):
        arc = Arc(
            start_angle = np.pi/2, angle = -np.pi/8,
            radius = self.pol_filter.radius,
        )
        label = OldTex("22.5^\\circ")
        label.next_to(arc.get_center(), UP+RIGHT, SMALL_BUFF)

        group = VGroup(arc, label)
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/2, OUT)

        self.play(
            FadeOut(self.pol_filter),
            ShowCreation(arc),
            Write(label, run_time = 1)
        )
        self.wait()

        self.arc = arc
        self.angle_label = label

    def write_components(self):
        d_brace = Brace(Line(ORIGIN, self.radius*RIGHT), UP, buff = SMALL_BUFF)
        d_brace.rotate(np.pi/2 - np.pi/8)
        d_brace.label = d_brace.get_tex("1", buff = SMALL_BUFF)
        d_brace.label.add_background_rectangle()

        h_arrow = Vector(
            self.radius*np.sin(np.pi/8)*RIGHT,
            color = RED,
        )
        h_label = OldTex("\\sin(22.5^\\circ)")
        h_label.scale(0.7)
        h_label.set_color(RED)
        h_label.next_to(h_arrow.get_center(), DOWN, aligned_edge = LEFT)

        v_arrow = Vector(
            self.radius*np.cos(np.pi/8)*UP,
            color = GREEN
        )
        v_arrow.shift(h_arrow.get_vector())
        v_label = OldTex("\\cos(22.5^\\circ)")
        v_label.scale(0.7)
        v_label.set_color(GREEN)
        v_label.next_to(v_arrow, RIGHT, SMALL_BUFF)

        state = OldTex(
            "|\\!\\psi\\rangle", 
            "=", "\\sin(22.5^\\circ)", "|\\!\\rightarrow\\rangle", 
            "+", "\\cos(22.5^\\circ)", "|\\!\\uparrow\\rangle",
        )
        state.set_color_by_tex_to_color_map({
            "psi" : BLUE,
            "rightarrow" : RED,
            "uparrow" : GREEN,
        })
        # state.add_background_rectangle()
        state.to_edge(UP)

        sin_brace = Brace(state.get_part_by_tex("sin"), DOWN, buff = SMALL_BUFF)
        sin_brace.label = sin_brace.get_tex("%.2f"%np.sin(np.pi/8), buff = SMALL_BUFF)
        cos_brace = Brace(state.get_part_by_tex("cos"), DOWN, buff = SMALL_BUFF)
        cos_brace.label = cos_brace.get_tex("%.2f"%np.cos(np.pi/8), buff = SMALL_BUFF)

        group = VGroup(
            d_brace, d_brace.label, 
            h_arrow, h_label,
            v_arrow, v_label,
            state,
            sin_brace, sin_brace.label,
            cos_brace, cos_brace.label,
        )
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/2, OUT)

        self.play(
            GrowFromCenter(d_brace),
            Write(d_brace.label)
        )
        self.wait()
        self.play(
            GrowFromPoint(h_arrow, ORIGIN),
            Write(h_label, run_time = 1)
        )
        self.play(
            Write(VGroup(*state[:2])),
            ReplacementTransform(
                h_label.copy(), 
                state.get_part_by_tex("sin")
            ),
            ReplacementTransform(
                h_arrow.copy(), 
                state.get_part_by_tex("rightarrow")
            ),
            Write(state.get_part_by_tex("+"))
        )
        self.play(
            GrowFromCenter(sin_brace),
            Write(sin_brace.label, run_time = 1)
        )
        self.wait()
        self.play(
            GrowFromPoint(v_arrow, h_arrow.get_end()),
            Write(v_label, run_time = 1)
        )
        self.play(
            ReplacementTransform(
                v_label.copy(), 
                state.get_part_by_tex("cos")
            ),
            ReplacementTransform(
                v_arrow.copy(), 
                state.get_part_by_tex("uparrow")
            ),
        )
        self.play(
            GrowFromCenter(cos_brace),
            Write(cos_brace.label, run_time = 1)
        )
        self.wait()

        self.d_brace = d_brace
        self.state_equation = state
        self.state_equation.add(
            sin_brace, sin_brace.label,
            cos_brace, cos_brace.label,
        )
        self.sin_brace = sin_brace
        self.cos_brace = cos_brace
        self.h_arrow = h_arrow
        self.h_label = h_label
        self.v_arrow = v_arrow
        self.v_label = v_label

    def classical_energy_conception(self):
        randy = Randolph(mode = "pondering").flip()
        randy.scale(0.7)
        randy.next_to(ORIGIN, LEFT)
        randy.to_edge(DOWN)

        bubble = ThoughtBubble(direction = RIGHT)
        h_content = OldTex(
            "0.38", "^2", "= 0.15", "\\text{ energy}\\\\",
            "\\text{in the }", "\\rightarrow", "\\text{ direction}"
        )
        alt_h_content = OldTex(
            "0.38", "^2", "=& 15\\%", "\\text{ of energy}\\\\",
            "&\\text{absorbed}", "", "",
        )
        h_content.set_color_by_tex("rightarrow", RED)
        alt_h_content.set_color_by_tex("rightarrow", RED)
        alt_h_content.scale(0.8)
        v_content = OldTex(
            "0.92", "^2", "= 0.85", "\\text{ energy}\\\\",
            "\\text{in the }", "\\uparrow", "\\text{ direction}"
        )
        v_content.set_color_by_tex("uparrow", GREEN)

        bubble.add_content(h_content)
        bubble.resize_to_content()
        v_content.move_to(h_content)
        bubble_group = VGroup(bubble, h_content, v_content)
        bubble_group.scale(0.8)
        bubble_group.next_to(randy, UP+LEFT, SMALL_BUFF)

        classically = OldTexText("Classically...")
        classically.next_to(bubble[-1], UP)
        classically.set_color(YELLOW)
        alt_h_content.next_to(classically, DOWN)

        group = VGroup(randy, bubble_group, classically, alt_h_content)
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/2, OUT)

        filter_lines = self.get_filter_lines(self.pol_filter)

        self.play(
            FadeIn(randy),
            FadeIn(classically),
            ShowCreation(bubble),
        )
        self.play(
            ReplacementTransform(
                self.sin_brace.label.copy(),
                h_content[0]
            ),
            ReplacementTransform(
                self.state_equation.get_part_by_tex("rightarrow").copy(),
                h_content.get_part_by_tex("rightarrow")
            )
        )
        self.play(
            Write(VGroup(*h_content[1:5])),
            Write(h_content.get_part_by_tex("direction")),
            run_time = 2,
        )
        self.wait(2)
        self.play(h_content.shift, 2*IN)
        self.play(
            ReplacementTransform(
                self.cos_brace.label.copy(),
                v_content[0]
            ),
            ReplacementTransform(
                self.state_equation.get_part_by_tex("uparrow").copy(),
                v_content.get_part_by_tex("uparrow")
            )
        )
        self.play(
            Write(VGroup(*v_content[1:5])),
            Write(v_content.get_part_by_tex("direction")),
            run_time = 2,
        )
        self.wait(2)
        self.play(
            FadeOut(randy),
            FadeOut(bubble),
            FadeOut(v_content),
            Transform(h_content, alt_h_content),
            FadeIn(self.pol_filter),
            Animation(self.arc)
        )
        self.play(ShowCreation(filter_lines, lag_ratio = 0))
        self.play(FadeOut(filter_lines))
        self.wait()

        self.classically = VGroup(classically, h_content)

    def reposition_camera_back(self):
        self.move_camera(
            phi = 0.8*np.pi/2, theta = -0.6*np.pi,
            added_anims = [
                FadeOut(self.h_arrow),
                FadeOut(self.h_label),
                FadeOut(self.v_arrow),
                FadeOut(self.v_label),
                FadeOut(self.d_brace),
                FadeOut(self.d_brace.label),
                FadeOut(self.arc),
                FadeOut(self.angle_label),
                Rotate(self.state_equation, np.pi/2, IN),
                Rotate(self.classically, np.pi/2, IN),
            ] + [
                Rotate(
                    v, np.pi/2, 
                    axis = v.get_vector(),
                    in_place = True,
                )
                for v in self.photon.mobject
            ],
            run_time = 1.5
        )

    def rewrite_15_percent_meaning(self):
        self.classically.rotate(np.pi/2, LEFT)
        cross = Cross(self.classically)
        cross.set_color("#ff0000")
        VGroup(self.classically, cross).rotate(np.pi/2, RIGHT)

        new_conception = OldTexText(
            "$0.38^2 = 15\\%$ chance of \\\\ getting blocked"
        )
        new_conception.scale(0.8)
        new_conception.rotate(np.pi/2, RIGHT)
        new_conception.move_to(self.classically, OUT)

        a = self.photon.rate_func(1)
        finish_photon = self.get_blocked_photon(
            rate_func = lambda t : a + (1-a)*t
        )
        finish_photon.mobject.set_fill(opacity = 0.7)

        self.play(ShowCreation(cross))
        self.classically.add(cross)
        self.play(
            self.classically.shift, 4*IN,
            FadeIn(new_conception),
        )
        self.remove(self.photon.mobject)
        self.revert_to_original_skipping_status()
        self.play(
            finish_photon,
            ApplyMethod(
                self.pol_filter.set_color, RED,
                rate_func = squish_rate_func(there_and_back, 0, 0.3),
                run_time = finish_photon.run_time
            )
        )

    def probabalistic_passing(self):
        # photons = [
        #     self.get_photon()
        #     for x in range(3)
        # ] + [self.get_blocked_photon()]
        # random.shuffle(photons)
        # for photon in photons:
        #     added_anims = []
        #     if photon.get_filtered:
        #         added_anims.append(
        #             self.get_filter_absorption_animation(
        #                 self.pol_filter, photon, 
        #             )
        #         )
        #     self.play(photon, *added_anims)
        # self.wait()

        l1 = self.get_lines(None, self.pol_filter)
        l2 = self.get_lines(self.pol_filter, None, 0.85)
        for line in it.chain(l1, l2):
            if line.get_stroke_width() > 0:
                line.set_stroke(width = 3)

        arrow = Arrow(
            2*LEFT, 2*RIGHT, 
            path_arc = 0.8*np.pi,
        )
        label = OldTex("15\\% \\text{ absorbed}")
        label.next_to(arrow, DOWN)
        group = VGroup(arrow, label)
        group.set_color(RED)
        group.rotate(np.pi/2, RIGHT)
        group.shift(3*RIGHT + 1.5*IN)

        kwargs = {
            "rate_func" : None,
            "lag_ratio" : 0,
        }
        self.play(
            ShowCreation(arrow),
            Write(label, run_time = 1),
            ShowCreation(l1, **kwargs)
        )
        self.play(
            ShowCreation(l2, run_time = 0.5, **kwargs),
            Animation(self.pol_filter),
            Animation(l1)
        )
        self.wait()

    ###

    def get_filter_lines(self, pol_filter):
        lines = VGroup(*[
            Line(
                np.sin(a)*RIGHT + np.cos(a)*UP,
                np.sin(a)*LEFT + np.cos(a)*UP,
                color = RED,
                stroke_width = 2,
            )
            for a in np.linspace(0, np.pi, 15)
        ])
        lines.scale(pol_filter.radius)
        lines.rotate(np.pi/2, RIGHT)
        lines.rotate(np.pi/2, OUT)
        lines.shift(pol_filter.get_center()[0]*RIGHT)
        return lines

    def get_blocked_photon(self, **kwargs):
        return self.get_photon(
            filter_distance = FRAME_X_RADIUS + 3, 
            get_filtered = True,
            **kwargs
        )
