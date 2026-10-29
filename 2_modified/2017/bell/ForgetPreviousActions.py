# ==============================================================================
# Scene:      ForgetPreviousActions
# Source:     videos/_2017/bell.py (lines 895-995)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/waves.py
#
# Run from this folder:
#     manimgl ForgetPreviousActions.py ForgetPreviousActions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 `sorted(seq, cmp)` with cmp() -> key function.
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2017/waves.py -----

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
        # CHANGE: Python 2 `sorted(seq, cmp)` with cmp() -> key function.
        filters = sorted(
            self.pol_filters,
            key=lambda pf: pf.get_center()[0],
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



# ----- From _2017/bell.py -----

class PhotonPassesCompletelyOrNotAtAll(DirectionOfPolarizationScene):
    CONFIG = {
        "pol_filter_configs" : [{
            "include_arrow_label" : False,
            "label_tex" : "\\text{Filter}",
        }],
        "EMWave_config" : {
            "wave_number" : 0,
            "A_vect" : [0, 1, 1],
            "start_point" : FRAME_X_RADIUS*LEFT + DOWN + 1.5*OUT,
        },
        "start_theta" : -0.9*np.pi,
        "target_theta" : -0.6*np.pi,
        "apply_filter" : True,
        "lower_portion_shift" : 3*IN,
        "show_M_vects" : True,
    }
    def setup(self):
        DirectionOfPolarizationScene.setup(self)
        if not self.show_M_vects:
            for M_vect in self.em_wave.M_vects:
                M_vect.set_fill(opacity = 0)
        self.update_mobjects()
        for vect in it.chain(self.em_wave.E_vects, self.em_wave.M_vects):
            vect.reset_normal_vector()
        self.remove(self.em_wave)

    def construct(self):
        pol_filter = self.pol_filter
        pol_filter.shift(0.5*OUT)
        lower_filter = pol_filter.copy()
        lower_filter.save_state()
        pol_filter.remove(pol_filter.label)

        passing_words = OldTexText("Photon", "passes through\\\\", "entirely")
        passing_words.set_color(GREEN)
        filtered_words = OldTexText("Photon", "is blocked\\\\", "entirely")
        filtered_words.set_color(RED)
        for words in passing_words, filtered_words:
            words.next_to(ORIGIN, UP+LEFT)
            words.shift(2*UP)
            words.add_background_rectangle()
            words.rotate(np.pi/2, RIGHT)
        filtered_words.shift(self.lower_portion_shift)

        passing_photon = WavePacket(
            run_time = 2,
            get_filtered = False,
            em_wave = self.em_wave.copy()
        )
        lower_em_wave = self.em_wave.copy()
        lower_em_wave.mobject.shift(self.lower_portion_shift)
        lower_em_wave.start_point += self.lower_portion_shift
        filtered_photon = WavePacket(
            run_time = 2,
            get_filtered = True,
            em_wave = lower_em_wave.copy()
        )
        green_flash = ApplyMethod(
            pol_filter.set_fill, GREEN,
            rate_func = squish_rate_func(there_and_back, 0.4, 0.6),
            run_time = passing_photon.run_time
        )

        self.play(
            DrawBorderThenFill(pol_filter),
            Write(pol_filter.label, run_time = 2),
        )
        self.move_camera(theta = self.target_theta)
        self.play(
            FadeIn(passing_words),
            passing_photon,
            green_flash,
        )
        self.play(
            lower_filter.restore,
            lower_filter.shift, self.lower_portion_shift,
            FadeIn(filtered_words)
        )
        red_flash = ApplyMethod(
            lower_filter.set_fill, RED,
            rate_func = squish_rate_func(there_and_back, 0.4, 0.6),
            run_time = filtered_photon.run_time
        )
        for x in range(4):
            self.play(
                passing_photon,
                filtered_photon,
                green_flash,
                red_flash,
            )
            self.wait()


class PhotonsThroughPerpendicularFilters(PhotonPassesCompletelyOrNotAtAll):
    CONFIG = {
        "filter_x_coordinates" : [-2, 2],
        "pol_filter_configs" : [
            {"filter_angle" : 0},
            {"filter_angle" : np.pi/2},
        ],
        "start_theta" : -0.9*np.pi,
        "target_theta" : -0.6*np.pi,
        "EMWave_config" : {
            "A_vect" : [0, 0, 1],
            "start_point" : FRAME_X_RADIUS*LEFT + DOWN + OUT,
        },
        "apply_filter" : False,
    }
    def construct(self):
        photons = self.get_photons()
        prob_text = self.get_probability_text()
        self.pol_filters = VGroup(*reversed(self.pol_filters))
        ninety_filter, zero_filter = self.pol_filters
        self.remove(*self.pol_filters)

        self.play(DrawBorderThenFill(zero_filter), run_time = 1)
        self.add_foreground_mobject(zero_filter)
        self.move_camera(
            theta = self.target_theta,
            added_anims = [ApplyFunction(
                self.reposition_filter_label,
                zero_filter
            )]
        )
        self.reposition_filter_label(ninety_filter)
        self.play(self.get_photons()[2])
        self.play(FadeIn(ninety_filter))
        self.add_foreground_mobject(ninety_filter)
        self.shoot_photon()
        self.shoot_photon()
        self.play(FadeIn(prob_text))
        for x in range(6):
            self.shoot_photon()

    def reposition_filter_label(self, pf):
        pf.arrow_label.rotate(np.pi/2, OUT)
        pf.arrow_label.next_to(pf.arrow, RIGHT)
        return pf


    def shoot_photon(self, *added_anims):
        photon = self.get_photons()[1]
        pol_filter = self.pol_filters[0]
        absorption = self.get_filter_absorption_animation(pol_filter, photon)
        self.play(photon, absorption)


    def get_photons(self):
        self.reference_line.rotate(np.pi/4)
        self.update_mobjects()
        return [
            WavePacket(
                filter_distance = FRAME_X_RADIUS + x,
                get_filtered = True,
                em_wave = self.em_wave.copy(),
                run_time = 1,
            )
            for x in (-2, 2, 10)
        ]

    def get_probability_text(self, prob = 0):
        prob_text = OldTex(
            "P(", "\\substack", "{\\text{photons that make it} \\\\ ", 
            " \\text{here } ", "\\text{make it}", 
            " \\text{ here} }", ")", "=", str(int(prob*100)), "\\%",
            arg_separator = ""
        )
        here1, here2 = prob_text.get_parts_by_tex("here")
        here1.set_color(GREEN)
        here2.set_color(RED)
        prob_text.add_background_rectangle()
        prob_text.next_to(ORIGIN, UP+RIGHT)
        prob_text.shift(2.5*UP+LEFT)
        prob_text.rotate(np.pi/2, RIGHT)
        arrows = [
            Arrow(
                here.get_edge_center(IN),
                DOWN+OUT + x*RIGHT,
                color = here.get_color(),
                normal_vector = DOWN+OUT,
            )
            for here, x in ((here1, 0), (here2, 4))
        ]
        prob_text.add(*arrows)

        return prob_text


class ShowVariousFilterPairsWithPhotonsOverTime(PhotonsThroughPerpendicularFilters):
    CONFIG = {
        "filter_x_coordinates" : [-2, 2, 2, 2, 2],
        "pol_filter_configs" : [
            {"filter_angle" : angle}
            for angle in (0, 0, np.pi/2, np.pi/4, np.pi/8)
        ],
        "apply_filter" : False,
    }
    def setup(self):
        PhotonsThroughPerpendicularFilters.setup(self)
        self.new_filters = self.pol_filters[2:]
        self.remove(*self.new_filters)
        self.pol_filters = self.pol_filters[:2]

    def construct(self):
        self.photons = self.get_photons()

        self.add_filters()
        self.add_probability_text()
        self.show_photons()
        for pol_filter in self.new_filters:
            self.change_to_new_filter(pol_filter)
            self.show_photons()

    def add_filters(self):
        self.remove(*self.pol_filters[1:])
        self.wait()
        self.play(ReplacementTransform(
            self.pol_filters[0].copy().set_fill(BLACK, 1),
            self.pol_filters[1]
        ))
        self.move_camera(
            theta = -0.65*np.pi,
            added_anims = list(it.chain(*[
                 [
                    pf.arrow_label.rotate, np.pi/2, OUT,
                    pf.arrow_label.next_to, pf.arrow, RIGHT
                 ]
                for pf in self.pol_filters[:2]
            ]))
        )
        for pf in self.new_filters:
            pf.arrow_label.rotate(np.pi/2, OUT)
            pf.arrow_label.next_to(pf.arrow, RIGHT)

        self.second_filter = self.pol_filters[1]
        self.add_foreground_mobject(self.second_filter)

    def add_probability_text(self):
        prob_text = self.get_probability_text(self.get_prob())
        self.play(FadeIn(prob_text))
        self.prob_text = prob_text

    def show_photons(self, n_photons = 5):
        p = self.get_prob()
        blocked_photon = copy.deepcopy(self.photons[0])
        blocked_photon.rate_func = squish_rate_func(
            lambda x : x, 0, 0.5,
        )
        first_absorption = self.get_filter_absorption_animation(
            self.pol_filters[0], blocked_photon
        )
        first_absorption.rate_func = squish_rate_func(
            first_absorption.rate_func, 0, 0.5,
        )

        photons = [
            copy.deepcopy(self.photons[2 if q <= p else 1])
            for q in np.arange(0, 1, 1./n_photons)
        ]
        random.shuffle(photons)
        for photon in photons:
            photon.rate_func = squish_rate_func(
                lambda x : x, 0.5, 1
            )
            added_anims = []
            if photon.filter_distance == FRAME_X_RADIUS + 2:
                absorption = self.get_filter_absorption_animation(
                    self.second_filter, photon
                )
                absorption.rate_func = squish_rate_func(
                    absorption.rate_func, 0.5, 1
                )
                added_anims.append(absorption)
            self.play(
                blocked_photon,
                first_absorption,
                photon, 
                *added_anims
            )
        self.wait()
        
    def change_to_new_filter(self, pol_filter, added_anims = None):
        if added_anims is None:
            added_anims = []
        self.play(
            Transform(self.second_filter, pol_filter),
            *added_anims
        )
        self.second_filter.filter_angle = pol_filter.filter_angle
        new_prob_text = self.get_probability_text(self.get_prob())
        new_prob_text[1][-2].set_color(YELLOW)
        self.play(Transform(self.prob_text, new_prob_text))

    ####

    def get_prob(self, pol_filter = None):
        if pol_filter is None:
            pol_filter = self.second_filter
        return np.cos(pol_filter.filter_angle)**2


class ShowVariousFilterPairs(ShowVariousFilterPairsWithPhotonsOverTime):
    CONFIG = {
        "filter_x_coordinates" : [],
        "filter_z_coordinates" : [2.5, 0, -2.5],
        "angles" : [0, np.pi/4, np.pi/2],
        "n_lines" : 20,
        "new_group_shift_val" : 2.5*IN,
        "prev_group_shift_val" : 1.75*IN,
        "ambient_rotation_rate" : 0.015,
        "line_start_length" : 16,
        "line_end_length" : 16,
        "lines_depth" : 1.2,
        "lines_shift_vect" : SMALL_BUFF*OUT,
    }
    def setup(self):
        ShowVariousFilterPairsWithPhotonsOverTime.setup(self)
        self.remove(*self.pol_filters)
        self.prev_groups = VGroup()
        self.remove(self.axes)
        self.setup_filters()
        self.stop_ambient_camera_rotation()
        self.prob_texts = VGroup()

    def setup_filters(self):
        self.filter_pairs = []
        zs = self.filter_z_coordinates
        for non_zero_angle, z in zip(self.angles, zs):
            filter_pair = VGroup()
            for angle, x in (0, -3), (non_zero_angle, 3):
                pf = PolarizingFilter(filter_angle = angle)
                pf.scale(0.7)
                pf.rotate(np.pi/2, RIGHT)
                pf.rotate(np.pi/2, IN)
                pf.shift(x*RIGHT + z*OUT)
                pf.arrow_label.rotate(np.pi/2, OUT)
                pf.arrow_label.next_to(pf.arrow, RIGHT, SMALL_BUFF)

                filter_pair.add(pf)
            self.filter_pairs.append(filter_pair)

    def construct(self):
        self.add_top_filters()
        self.show_light(self.filter_pairs[0])
        self.turn_one_filter_pair_into_another(0, 2)
        self.show_light(self.filter_pairs[2])
        self.turn_one_filter_pair_into_another(2, 1)
        self.show_light(self.filter_pairs[1])

    def add_top_filters(self):
        pf1, pf2 = pair = self.filter_pairs[0]
        for pf in pair:
            pf.save_state()
            pf.arrow_label.rotate(np.pi/2, IN)
            pf.arrow_label.next_to(pf.arrow, UP, SMALL_BUFF)
            pf.shift(2*IN)

        self.add(pf1)
        self.play(
            ReplacementTransform(pf1.copy().fade(1), pf2),
            Animation(pf1)
        )
        self.move_camera(
            0.9*np.pi/2, -0.6*np.pi,
            added_anims = [
                pf.restore 
                for pf in pair
            ]
        )

    def show_light(self, filter_pair):
        pf1, pf2 = filter_pair
        lines_to_pf1 = self.get_lines(None, pf1)
        vect = lines_to_pf1[1].get_center() - lines_to_pf1[0].get_center()
        lines_to_pf1.add(*lines_to_pf1.copy().shift(vect/2))
        lines_to_pf2 = self.get_lines(pf1, pf2)
        lines_from_pf2 = self.get_lines(pf2)

        prob = self.get_prob(pf2)
        n_black = int(prob*len(lines_from_pf2))
        VGroup(*lines_from_pf2[n_black:]).set_stroke(BLACK, 0)

        kwargs = {
            "rate_func" : None,
            "lag_ratio" : 0,
        }

        self.play(ShowCreation(lines_to_pf1, run_time = 2./3, **kwargs))
        self.play(
            ShowCreation(lines_to_pf2, **kwargs),
            Animation(VGroup(pf1, lines_to_pf1)),
            run_time = 1./6,
        )
        self.play(
            ShowCreation(lines_from_pf2, **kwargs),
            Animation(VGroup(pf2, lines_to_pf2, pf1, lines_to_pf1)),
            run_time = 2./3,
        )

        group = VGroup(
            lines_from_pf2, pf2, lines_to_pf2, pf1, lines_to_pf2
        )

        #Write probability
        prob_text = self.get_probability_text(pf2)
        self.play(Write(prob_text, run_time = 1))
        self.wait()

        self.prob_texts.add(prob_text)

    def turn_one_filter_pair_into_another(self, i1, i2):
        mover = self.filter_pairs[i1].copy()
        mover.set_stroke(width = 0)
        mover.set_fill(opacity = 0)
        target = self.filter_pairs[i2]
        self.play(ReplacementTransform(mover, target))

    def get_probability_text(self, pol_filter = None):
        if pol_filter is None:
            pol_filter = self.second_filter
        prob = self.get_prob(pol_filter)
        prob_mob = OldTexText(str(int(prob*100)) + "\\%", " pass")
        prob_mob.scale(0.7)
        prob_mob.rotate(np.pi/2, RIGHT)
        prob_mob.next_to(pol_filter.arrow_label, RIGHT)
        prob_mob.set_color(
            list(Color(RED).range_to(GREEN, 11))[int(prob*10)]
        )
        return prob_mob


    #####

    def get_lines(
        self, filter1 = None, filter2 = None, 
        ratio = 1.0,
        remove_from_bottom = False,
        ):
        # n = int(ratio*self.n_lines)
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
        if remove_from_bottom:
            to_block = lines[:n_to_block]
        else:
            to_block = lines[len(lines)-n_to_block:]
        VGroup(*to_block).set_stroke(width = 0)
        return lines


class ForgetPreviousActions(ShowVariousFilterPairs):
    CONFIG = {
        "filter_x_coordinates" : [-6, -2, 2, 2, 2],
        "pol_filter_configs" : [
            {"filter_angle" : angle}
            for angle in (np.pi/4, 0, np.pi/4, np.pi/3, np.pi/6)
        ],
        "start_theta" : -0.6*np.pi,
        "EMWave_config" : {
            "wave_number" : 0,
            "start_point" : FRAME_X_RADIUS*LEFT + DOWN,
        },
        "apply_filter" : False,
    }
    def setup(self):
        PhotonsThroughPerpendicularFilters.setup(self)
        self.remove(self.axes)

        VGroup(*self.pol_filters).shift(IN)

        for pf in self.pol_filters:
            pf.arrow_label.rotate(np.pi/2, OUT)
            pf.arrow_label.next_to(pf.arrow, RIGHT)

        self.stop_ambient_camera_rotation()

    def construct(self):
        front_filter = self.pol_filters[0]
        first_filter = self.pol_filters[1]
        possible_second_filters = self.pol_filters[2:]
        for pf in possible_second_filters:
            prob_text = self.get_probability_text(pf)
            prob_text.scale(1.3, about_point = prob_text.get_left())
            pf.add(prob_text)

        second_filter = possible_second_filters[0].copy()
        self.second_filter = second_filter
        self.pol_filters = VGroup(
            first_filter, second_filter
        )
        self.remove(front_filter)
        self.remove(*possible_second_filters)
        self.add(second_filter)
        self.apply_filter = True
        self.update_mobjects()
        self.photons = self.get_photons()[1:]

        group = VGroup(*self.pol_filters)
        rect1 = SurroundingRectangle(group)
        rect1.rotate(np.pi/2, RIGHT)
        rect1.rescale_to_fit(group.get_depth()+MED_SMALL_BUFF, 2, True)
        rect1.stretch_in_place(1.2, 0)
        prob_words = OldTexText(
            "Probabilities depend only\\\\",
            "on this angle difference"
        )
        prob_words.add_background_rectangle()
        prob_words.rotate(np.pi/2, RIGHT)
        prob_words.next_to(rect1, OUT)

        self.add(rect1)
        self.play(FadeIn(prob_words))
        for index in 1, 2:
            self.shoot_photon()
            self.play(Transform(
                second_filter, possible_second_filters[index]
            ))

        rect2 = SurroundingRectangle(front_filter, color = RED)
        rect2.rotate(np.pi/2, RIGHT)
        rect2.rescale_to_fit(front_filter.get_depth()+MED_SMALL_BUFF, 2, True)
        rect2.stretch_in_place(1.5, 0)
        ignore_words = OldTexText("Photon \\\\", "``forgets'' this")
        ignore_words.add_background_rectangle()
        ignore_words.rotate(np.pi/2, RIGHT)
        ignore_words.next_to(rect2, OUT)

        self.play(
            ShowCreation(rect2), 
            Write(ignore_words, run_time = 1),
            FadeIn(front_filter),
            run_time = 1.5,
        )
        self.shoot_photon()
        for index in 0, 1, 2:
            self.play(Transform(
                second_filter, possible_second_filters[index]
            ))
            self.shoot_photon()

    def shoot_photon(self):
        photon = random.choice(self.photons)
        added_anims = []
        if photon.filter_distance == FRAME_X_RADIUS + 2:
            added_anims.append(
                ApplyMethod(
                    self.second_filter.set_color, RED,
                    rate_func = squish_rate_func(there_and_back, 0.5, 0.7)
                )
            )
        self.play(photon, *added_anims, run_time = 1.5)
