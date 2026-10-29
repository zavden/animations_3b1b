# ==============================================================================
# Scene:      EnergyOfWavesWavePortion
# Source:     videos/_2017/waves.py (lines 2201-2332)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EnergyOfWavesWavePortion.py EnergyOfWavesWavePortion -w -m --fps 15
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


class IntroduceEMWave(ThreeDScene):
    CONFIG = {
        "EMWave_config" : {
            "requires_start_up" : True
        }
    }
    def setup(self):
        self.axes = ThreeDAxes()
        self.add(self.axes)
        self.em_wave = EMWave(**self.EMWave_config)
        self.add(self.em_wave)
        self.set_camera_orientation(0.8*np.pi/2, -0.7*np.pi)
        self.begin_ambient_camera_rotation()

    def construct(self):
        words = OldTexText(
            "Electro", "magnetic", " radiation",
            arg_separator = ""
        )
        words.set_color_by_tex_to_color_map({
            "Electro" : E_COLOR,
            "magnetic" : M_COLOR,
        })
        words.next_to(ORIGIN, LEFT, MED_LARGE_BUFF)
        words.to_edge(UP)
        words.rotate(np.pi/2, RIGHT)

        self.wait(7)
        self.play(Write(words, run_time = 2))
        self.wait(20)


class DirectWaveOutOfScreen(IntroduceEMWave):
    CONFIG = {
        "EMWave_config" : {
            "requires_start_up" : False,
            "amplitude" : 2,
            "start_point" : FRAME_X_RADIUS*LEFT,
            "A_vect" : [0, 1, 0],
            "start_up_time" : 0,
        }
    }
    def setup(self):
        IntroduceEMWave.setup(self)
        self.remove(self.axes)
        for ov in self.em_wave.continual_animations:
            ov.vector.normal_vector = RIGHT
        self.set_camera_orientation(0.9*np.pi/2, -0.3*np.pi)

    def construct(self):
        self.move_into_position()
        self.fade_M_vects()
        self.fade_all_but_last_E_vects()

    def move_into_position(self):
        self.wait(2)
        self.update_mobjects()
        faded_vectors = VGroup(*[
            ov.vector
            for ov in self.em_wave.continual_animations[:-2]
        ])
        self.move_camera(
            0.99*np.pi/2, -0.01,
            run_time = 2,
            added_anims = [faded_vectors.set_fill, None, 0.5]
        )
        self.stop_ambient_camera_rotation()
        self.move_camera(
            np.pi/2, 0,
            added_anims = [faded_vectors.set_fill, None, 0.05],
            run_time = 2,
        )
        self.faded_vectors = faded_vectors

    def fade_M_vects(self):
        self.play(
            self.em_wave.M_vects.set_fill, None, 0
        )
        self.wait(2)

    def fade_all_but_last_E_vects(self):
        self.play(self.faded_vectors.set_fill, None, 0)
        self.wait(4)


class EnergyOfWavesWavePortion(DirectWaveOutOfScreen):
    CONFIG = {
        "EMWave_config" : {
            "A_vect" : [0, 1, 1],
            "amplitude" : 4,
            "start_point" : FRAME_X_RADIUS*LEFT + 2*DOWN,
        }
    }
    def construct(self):
        self.grow_arrows()
        self.move_into_position()
        self.fade_M_vects()
        self.label_A()
        self.add_components()
        self.scale_up_and_down()

    def grow_arrows(self):
        for ov in self.em_wave.continual_animations:
            ov.vector.rectangular_stem_width = 0.1
            ov.vector.tip_length = 0.5

    def label_A(self):
        brace = Brace(Line(ORIGIN, 4*RIGHT))
        brace.rotate(np.pi/4, OUT)
        brace.A = brace.get_tex("A", buff = MED_SMALL_BUFF)
        brace.A.scale(2)
        brace.A.set_color(GREEN)
        brace_group = VGroup(brace, brace.A)
        self.position_brace_group(brace_group)
        self.play(Write(brace_group, run_time = 1))
        self.wait(12)

        self.brace = brace

    def add_components(self):
        h_wave = self.em_wave.copy()
        h_wave.A_vect = [0, 1, 0]
        v_wave = self.em_wave.copy()
        v_wave.A_vect = [0, 0, 1]
        length = 4/np.sqrt(2)
        for wave in h_wave, v_wave:
            for ov in wave.continual_animations:
                ov.A_vect = length*np.array(wave.A_vect)

        h_brace = Brace(Line(ORIGIN, length*RIGHT))
        v_brace = Brace(Line(ORIGIN, length*UP), LEFT)
        for brace, c in (h_brace, "x"), (v_brace, "y"):
            brace.A = brace.get_tex("A_%s"%c, buff = MED_LARGE_BUFF)
            brace.A.scale(2)
            brace.A.set_color(GREEN)
        brace_group = VGroup(h_brace, h_brace.A, v_brace, v_brace.A)
        self.position_brace_group(brace_group)

        rhs = OldTex("= \\sqrt{A_x^2 + A_y^2}")
        rhs.scale(2)
        for i in 3, 5, 7, 9:
            rhs[i].set_color(GREEN)
        rhs.rotate(np.pi/2, RIGHT)
        rhs.rotate(np.pi/2, OUT)

        period = 1./self.em_wave.frequency
        self.add(h_wave, v_wave)
        self.play(
            FadeIn(h_wave.mobject),
            FadeIn(v_wave.mobject),
            self.brace.A.move_to, self.brace,
            self.brace.A.shift, SMALL_BUFF*(2*UP+IN),
            ReplacementTransform(self.brace, h_brace),
            Write(h_brace.A)
        )
        self.wait(6)

        self.play(
            ReplacementTransform(h_brace.copy(), v_brace),
            Write(v_brace.A)
        )
        self.wait(6)
        rhs.next_to(self.brace.A, UP, SMALL_BUFF)
        self.play(Write(rhs))
        self.wait(2*period)

        self.h_brace = h_brace
        self.v_brace = v_brace
        self.h_wave = h_wave
        self.v_wave = v_wave

    def scale_up_and_down(self):
        for scale_factor in 1.25, 0.4, 1.5, 0.3, 2:
            self.scale_wave(scale_factor)
            self.wait()
        self.wait(4)

    ######

    def position_brace_group(self, brace_group):
        brace_group.rotate(np.pi/2, RIGHT)
        brace_group.rotate(np.pi/2, OUT)
        brace_group.shift(2*DOWN)

    def scale_wave(self, factor):
        def generate_vect_update(ov):
            prev_A = np.array(ov.A_vect)
            new_A = factor*prev_A
            def update(vect, alpha):
                ov.A_vect = interpolate(
                    prev_A, new_A, alpha
                )
                return vect
            return update
        h_brace = self.h_brace
        v_brace = self.v_brace

        h_brace.generate_target()
        h_brace.target.stretch_about_point(
            factor, 1, h_brace.get_bottom()
        )
        v_brace.generate_target()
        v_brace.target.stretch_about_point(
            factor, 2, v_brace.get_nadir()
        )
        self.play(
            MoveToTarget(h_brace),
            MoveToTarget(v_brace),
            *[
                UpdateFromAlphaFunc(ov.vector, generate_vect_update(ov))
                for ov in it.chain(
                    self.em_wave.continual_animations,
                    self.h_wave.continual_animations,
                    self.v_wave.continual_animations,
                )
            ]
        )
