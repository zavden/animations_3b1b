# ==============================================================================
# Scene:      DescribePhoton
# Source:     videos/_2017/waves.py (lines 2416-2883)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DescribePhoton.py DescribePhoton -w -m --fps 15
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


class DescribePhoton(ThreeDScene):
    CONFIG = {
        "x_color" : RED,
        "y_color" : GREEN,
    }
    def setup(self):
        self.axes = ThreeDAxes()
        self.add(self.axes)

        self.set_camera_orientation(phi = 0.8*np.pi/2, theta = -np.pi/4)
        em_wave = EMWave(
            start_point = FRAME_X_RADIUS*LEFT,
            A_vect = [0, 1, 1],
            wave_number = 0,
            amplitude = 3,
        )
        for ov in em_wave.continual_animations:
            ov.vector.normal_vector = RIGHT
            ov.vector.set_fill(opacity = 0.7)
        for M_vect in em_wave.M_vects:
            M_vect.set_fill(opacity = 0)
        em_wave.update(0)
        photon = WavePacket(
            em_wave = em_wave,
            run_time = 2,
        )

        self.photon = photon
        self.em_wave = em_wave

    def construct(self):
        self.add_ket_equation()
        self.shoot_a_few_photons()
        self.freeze_photon()
        self.reposition_to_face_photon_head_on()
        self.show_components()
        self.show_amplitude_and_phase()
        self.change_basis()
        self.write_different_meaning()
        self.write_components()
        self.describe_via_energy()
        self.components_not_possible_in_isolation()
        self.ask_what_they_mean()
        self.change_camera()

    def add_ket_equation(self):
        equation = OldTex(
            "|\\!\\psi\\rangle", 
            "=",
            "\\alpha", "|\\!\\rightarrow \\rangle", "+",
            "\\beta", "|\\!\\uparrow \\rangle",
        )
        equation.to_edge(UP)
        equation.set_color_by_tex("psi", E_COLOR)
        equation.set_color_by_tex("alpha", self.x_color)
        equation.set_color_by_tex("beta", self.y_color)
        rect = SurroundingRectangle(equation.get_part_by_tex("psi"))
        rect.set_color(E_COLOR)
        words = OldTexText("Polarization\\\\", "state")
        words.next_to(rect, DOWN)
        for part in words:
            bg_rect = BackgroundRectangle(part)
            bg_rect.stretch_in_place(2, 1)
            part.add_to_back(bg_rect)
        equation.rect = rect
        equation.words = words
        equation.add_background_rectangle()
        equation.add(rect, words)
        VGroup(rect, words).fade(1)

        equation.rotate(np.pi/2, RIGHT)
        equation.rotate(np.pi/2 + self.camera.get_theta(), OUT)

        self.add(equation)
        self.equation = equation
        self.superposition = VGroup(*equation[1][2:])

    def shoot_a_few_photons(self):
        for x in range(2):
            self.play(self.photon)

    def freeze_photon(self):
        self.play(
            self.photon,
            rate_func = lambda x : 0.55*x,
            run_time = 1
        )
        self.add(self.photon.mobject)
        self.photon.rate_func = lambda x : x
        self.photon.run_time = 2

    def reposition_to_face_photon_head_on(self):
        plane = NumberPlane(
            color = GREY_B,
            secondary_color = GREY_D,
            x_unit_size = 2,
            y_unit_size = 2,
            y_radius = FRAME_X_RADIUS,
        )
        plane.add_coordinates(x_vals = list(range(-3, 4)), y_vals = [])
        plane.rotate(np.pi/2, RIGHT)
        plane.rotate(np.pi/2, OUT)

        self.play(self.em_wave.M_vects.set_fill, None, 0)
        self.move_camera(
            phi = np.pi/2, theta = 0,
            added_anims = [
                Rotate(self.equation, -self.camera.get_theta())
            ]
        )
        self.play(
            Write(plane, run_time = 1), 
            Animation(self.equation)
        )

        self.xy_plane = plane

    def show_components(self):
        h_arrow, v_arrow = [
            Vector(
                1.38*direction, 
                color = color,
                normal_vector = RIGHT,
            )
            for color, direction in [(self.x_color, UP), (self.y_color, OUT)]
        ]
        v_arrow.move_to(h_arrow.get_end(), IN)
        h_part = VGroup(*self.equation[1][2:4]).copy()
        v_part = VGroup(*self.equation[1][5:7]).copy()

        self.play(
            self.equation.rect.set_stroke, BLUE, 4,
            self.equation.words.set_fill, WHITE, 1,
        )
        for part, arrow, d in (h_part, h_arrow, IN), (v_part, v_arrow, UP):
            self.play(
                part.next_to, arrow.get_center(), d,
                ShowCreation(arrow)
            )
            part.rotate(np.pi/2, DOWN)
            bg_rect = BackgroundRectangle(part)
            bg_rect.stretch_in_place(1.3, 0)
            part.add_to_back(bg_rect)
            part.rotate(np.pi/2, UP)
            self.add(part)
        self.wait()

        self.h_part_tex = h_part
        self.h_arrow = h_arrow
        self.v_part_tex = v_part
        self.v_arrow = v_arrow

    def show_amplitude_and_phase(self):
        alpha = self.h_part_tex[1]
        new_alpha = alpha.copy().shift(IN)
        rhs = OldTex(
            "=", "A_x", "e", 
            "^{i", "(2\\pi", "f", "t", "+", "\\phi_x)}"
        )
        A_rect = SurroundingRectangle(rhs.get_part_by_tex("A_x"), buff = 0.5*SMALL_BUFF)
        A_word = OldTexText("Amplitude")
        A_word.add_background_rectangle()
        A_word.next_to(A_rect, DOWN, aligned_edge = LEFT)
        A_group = VGroup(A_rect, A_word)
        A_group.set_color(YELLOW)
        phase_rect = SurroundingRectangle(VGroup(*rhs[4:]), buff = 0.5*SMALL_BUFF)
        phase_word = OldTexText("Phase")
        phase_word.add_background_rectangle()
        phase_word.next_to(phase_rect, UP)
        phase_group = VGroup(phase_word, phase_rect)
        phase_group.set_color(MAROON_B)
        rhs.add_background_rectangle()

        group = VGroup(rhs, A_group, phase_group)
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/2, OUT)
        group.next_to(new_alpha, UP, SMALL_BUFF)

        self.play(
            ReplacementTransform(alpha.copy(), new_alpha),
            FadeIn(rhs)
        )
        for word, rect in A_group, phase_group:
            self.play(
                ShowCreation(rect),
                Write(word, run_time = 1)
            )
        self.wait()
        self.play(*list(map(FadeOut, [new_alpha, group])))

    def change_basis(self):
        superposition = self.superposition
        plane = self.xy_plane
        h_arrow = self.h_arrow
        v_arrow = self.v_arrow
        h_part = self.h_part_tex
        v_part = self.v_part_tex
        axes = self.axes
        movers = [
            plane, axes,
            h_arrow, v_arrow, 
            h_part, v_part, 
            self.equation,
            superposition, 
        ]
        for mob in movers:
            mob.save_state()

        superposition.target = OldTex(
            "\\gamma", "|\\! \\nearrow \\rangle", "+",
            "\\delta", "|\\! \\nwarrow \\rangle",
        )
        superposition.target.set_color_by_tex("gamma", TEAL_D)
        superposition.target.set_color_by_tex("delta", MAROON)
        for part in superposition.target.get_parts_by_tex("rangle"):
            part[1].rotate(-np.pi/12)
        superposition.target.rotate(np.pi/2, RIGHT)
        superposition.target.rotate(np.pi/2, OUT)
        superposition.target.move_to(superposition)

        for mob in plane, axes:
            mob.generate_target()
            mob.target.rotate(np.pi/6, RIGHT)

        A = 1.9
        h_arrow.target = Vector(
            A*np.cos(np.pi/12)*rotate_vector(UP, np.pi/6, RIGHT),
            normal_vector = RIGHT,
            color = TEAL
        )
        v_arrow.target = Vector(
            A*np.sin(np.pi/12)*rotate_vector(OUT, np.pi/6, RIGHT),
            normal_vector = RIGHT,
            color = MAROON
        )
        v_arrow.target.shift(h_arrow.target.get_vector())

        h_part.target = VGroup(*superposition.target[:2]).copy()
        v_part.target = VGroup(*superposition.target[3:]).copy()
        h_part.target.next_to(
            h_arrow.target.get_center(), IN+UP, SMALL_BUFF
        )
        v_part.target.next_to(
            v_arrow.target.get_center(), UP, SMALL_BUFF
        )
        for part in h_part.target, v_part.target:
            part.rotate(np.pi/2, DOWN)
            part.add_to_back(BackgroundRectangle(part))
            part.rotate(np.pi/2, UP)

        self.equation.generate_target()

        self.play(*list(map(MoveToTarget, movers)))
        self.wait(2)
        self.play(*[mob.restore for mob in movers])
        self.wait()

    def write_different_meaning(self):
        superposition = self.superposition
        superposition.rotate(np.pi/2, DOWN)
        rect = SurroundingRectangle(superposition)
        VGroup(superposition, rect).rotate(np.pi/2, UP)
        morty = Mortimer(mode = "confused")
        blinked = morty.copy().blink()
        words = OldTexText("Means something \\\\ different...")
        for mob in morty, blinked, words:
            mob.rotate(np.pi/2, RIGHT)
            mob.rotate(np.pi/2, OUT)
        words.next_to(rect, UP)
        VGroup(morty, blinked).next_to(words, IN)

        self.play(
            ShowCreation(rect),
            Write(words, run_time = 2)
        )
        self.play(FadeIn(morty))
        self.play(Transform(
            morty, blinked, 
            rate_func = squish_rate_func(there_and_back)
        ))
        self.wait()
        self.play(*list(map(FadeOut, [
            morty, words, rect,
            self.equation.rect,
            self.equation.words,
        ])))

    def write_components(self):
        d_brace = Brace(Line(ORIGIN, 2*RIGHT), UP, buff = SMALL_BUFF)
        h_brace = Brace(Line(ORIGIN, (2/np.sqrt(2))*RIGHT), DOWN, buff = SMALL_BUFF)
        v_brace = Brace(Line(ORIGIN, (2/np.sqrt(2))*UP), RIGHT, buff = SMALL_BUFF)
        d_brace.rotate(np.pi/4)
        v_brace.shift((2/np.sqrt(2))*RIGHT)
        braces = VGroup(d_brace, h_brace, v_brace)
        group = VGroup(braces)

        tex = ["1"] + 2*["\\sqrt{1/2}"]
        colors = BLUE, self.x_color, self.y_color
        for brace, tex, color in zip(braces, tex, colors):
            brace.label = brace.get_tex(tex, buff = SMALL_BUFF)
            brace.label.add_background_rectangle()
            brace.label.set_color(color)
            group.add(brace.label)

        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/2, OUT)

        self.play(
            GrowFromCenter(d_brace),
            Write(d_brace.label)
        )
        self.wait()
        self.play(
            FadeOut(self.h_part_tex),
            FadeOut(self.v_part_tex),
            GrowFromCenter(h_brace),
            GrowFromCenter(v_brace),
        )
        self.play(
            Write(h_brace.label),
            Write(v_brace.label),
        )
        self.wait()

        self.d_brace = d_brace
        self.h_brace = h_brace
        self.v_brace = v_brace

    def describe_via_energy(self):
        energy = OldTex(
            "&\\text{Energy}", 
            "=", "(hf)", "(", "1", ")^2\\\\",
            "&=", "(hf)", "\\left(", "\\sqrt{1/2}", "\\right)^2", 
            "+", "(hf)", "\\left(", "\\sqrt{1/2}", "\\right)^2",
        )
        energy.scale(0.8)
        one = energy.get_part_by_tex("1", substring = False)
        one.set_color(BLUE)
        halves = energy.get_parts_by_tex("1/2")
        halves[0].set_color(self.x_color)
        halves[1].set_color(self.y_color)
        indices = [0, 3, 6, len(energy)]
        parts = VGroup(*[
            VGroup(*energy[i1:i2])
            for i1, i2 in zip(indices, indices[1:])    
        ])
        for part in parts:
            bg_rect = BackgroundRectangle(part)
            bg_rect.stretch_in_place(1.5, 1)
            part.add_to_back(bg_rect)

        parts.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        parts.shift(DOWN)
        parts.rotate(np.pi/2, RIGHT)
        parts.rotate(np.pi/2, OUT)

        self.play(Write(parts[0]), run_time = 2)
        self.play(Indicate(energy.get_part_by_tex("hf")))
        self.play(
            Transform(
                self.d_brace.label.copy(),
                one.copy(),
                remover = True
            ),
            Write(parts[1], run_time = 1),
        )
        self.wait()
        self.play(
            Transform(
                self.h_brace.label[1].copy(),
                halves[0].copy(),
                remover = True,
                rate_func = squish_rate_func(smooth, 0, 0.75)
            ),
            Transform(
                self.v_brace.label[1].copy(),
                halves[1].copy(),
                remover = True,
                rate_func = squish_rate_func(smooth, 0.25, 1)
            ),
            Write(parts[2]),
            run_time = 2
        )
        self.wait()

        self.energy_equation_parts = parts

    def components_not_possible_in_isolation(self):
        half_hf = VGroup(*self.energy_equation_parts[2][1:6])
        half_hf.rotate(np.pi/2, DOWN)
        rect = SurroundingRectangle(half_hf)
        VGroup(half_hf, rect).rotate(np.pi/2, UP)

        randy = Randolph()
        randy.scale(0.7)
        randy.look(UP)
        randy.rotate(np.pi/2, RIGHT)
        randy.rotate(np.pi/2, OUT)
        randy.next_to(rect, IN)

        self.play(
            ShowCreation(rect),
            FadeIn(randy)
        )
        self.play(
            randy.rotate, np.pi/2, IN,
            randy.rotate, np.pi/2, LEFT,
            randy.change, "maybe",
            randy.rotate, np.pi/2, RIGHT,
            randy.rotate, np.pi/2, OUT,
        )
        self.wait()

    def ask_what_they_mean(self):
        morty = Mortimer(mode = "confused")
        morty.scale(0.7)
        morty.to_edge(LEFT)

        bubble = morty.get_bubble()
        bubble.write("?!?")
        bubble.resize_to_content()
        bubble.add(bubble.content)
        bubble.pin_to(morty)

        group = VGroup(morty, bubble)
        group.to_corner(DOWN+RIGHT)
        group.rotate(np.pi/2, RIGHT)
        group.rotate(np.pi/2, OUT)

        component = VGroup(self.h_arrow, self.h_brace, self.h_brace.label)

        self.play(
            FadeIn(morty),
            component.next_to, morty, DOWN, OUT,
            component.shift, MED_LARGE_BUFF*(DOWN + OUT),
        )
        component.rotate(np.pi/2, DOWN)
        cross = Cross(component)
        VGroup(component, cross).rotate(np.pi/2, UP)
        cross.set_color("#ff0000")
        self.play(ShowCreation(cross))
        bubble.remove(bubble.content)
        self.play(
            ShowCreation(bubble),
            Write(bubble.content),
            morty.look_at, component,
        )
        self.wait()

    def change_camera(self):
        everything = VGroup(*self.get_top_level_mobjects())
        everything.remove(self.photon.mobject)
        everything.remove(self.axes)

        self.play(*list(map(FadeOut, everything)))
        self.move_camera(
            phi = 0.8*np.pi/2,
            theta = -0.3*np.pi, 
            run_time = 2
        )
        self.play(
            self.photon,
            rate_func = lambda x : min(x + 0.55, 1),
            run_time = 2,
        )
        self.photon.rate_func = lambda x : x
        self.play(self.photon)
        self.wait()
