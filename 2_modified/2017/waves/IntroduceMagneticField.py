# ==============================================================================
# Scene:      IntroduceMagneticField
# Source:     videos/_2017/waves.py (lines 731-858)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceMagneticField.py IntroduceMagneticField -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - typo in the original (m1 undefined): sort key must use the lambda argument
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class IntroduceElectricField(PiCreatureScene):
    CONFIG = {
        "vector_field_colors" : [BLUE_B, BLUE_D],
        "max_vector_length" : 0.9,
    }
    def construct(self):
        self.write_title()
        self.draw_field()
        self.add_particle()
        self.let_particle_wander()

    def write_title(self):
        morty = self.pi_creature

        title = OldTexText(
            "Electro", "magnetic", " field",
            arg_separator = ""
        )
        title.next_to(morty, UP+LEFT)
        electric = OldTexText("Electric")
        electric.next_to(title[-1], LEFT)
        electric.set_color(BLUE)

        title.save_state()
        title.shift(DOWN)
        title.fade(1)

        self.play(
            title.restore,
            morty.change, "raise_right_hand",
        )
        self.play(
            title[0].set_color, BLUE,
            title[1].set_color, YELLOW,
        )
        self.wait()
        self.play(
            ShrinkToCenter(title[1]),
            Transform(title[0], electric)
        )

        title.add_background_rectangle()
        self.title = title

    def draw_field(self):
        morty = self.pi_creature
        vector_field = self.get_vector_field()
        self.play(
            LaggedStartMap(
                ShowCreation, vector_field, 
                run_time = 3
            ),
            self.title.center,
            self.title.scale, 1.5,
            self.title.to_edge, UP,
            morty.change, "happy", ORIGIN,
        )
        self.wait()

        self.vector_field = vector_field

    def add_particle(self):
        morty = self.pi_creature
        point = UP+LEFT + SMALL_BUFF*(UP+RIGHT)
        particle = self.get_particle()
        particle.move_to(point)

        vector = self.get_vector(particle.get_center())
        vector.set_color(RED)
        vector.scale(1.5, about_point = point)
        vector.shift(SMALL_BUFF*vector.get_vector())
        force = OldTexText("Force")
        force.next_to(ORIGIN, UP+RIGHT, SMALL_BUFF)
        force.rotate(vector.get_angle())
        force.shift(vector.get_start())

        particle.save_state()
        particle.move_to(morty.get_left() + 0.5*UP + 0.2*RIGHT)
        particle.fade(1)

        self.play(
            particle.restore,
            morty.change, "raise_right_hand",
        )
        self.play(morty.change, "thinking", particle)
        self.play(
            ShowCreation(vector),
            Write(force, run_time = 1),
        )
        self.wait(2)

        self.particle = particle
        self.force_vector = VGroup(vector, force)

    def let_particle_wander(self):
        possible_points = [v.get_start() for v in self.vector_field]
        points = random.sample(possible_points, 45)
        points.append(3*UP+3*LEFT)
        particles = VGroup(self.particle, *[
            self.particle.copy().move_to(point)
            for point in points
        ])
        for particle in particles:
            particle.velocity = np.zeros(3)

        self.play(
            FadeOut(self.force_vector),
            LaggedStartMap(FadeIn, VGroup(*particles[1:]))
        )
        self.moving_particles = particles
        self.add_foreground_mobjects(self.moving_particles, self.pi_creature)
        self.always_update_mobjects = True
        self.wait(10)

    ###

    def update_mobjects(self, *args, **kwargs):
        Scene.update_mobjects(self, *args, **kwargs)
        if hasattr(self, "moving_particles"):
            dt = self.frame_duration
            for p in self.moving_particles:
                vect = self.field_function(p.get_center())
                p.velocity += vect*dt
                p.shift(p.velocity*dt)
            self.pi_creature.look_at(self.moving_particles[-1])

    def get_particle(self):
        particle = Circle(radius = 0.2)
        particle.set_stroke(RED, 3)
        particle.set_fill(RED, 0.5)
        plus = OldTex("+")
        plus.scale(0.7)
        plus.move_to(particle)
        particle.add(plus)
        return particle

    def get_vector_field(self):
        result = VGroup(*[
            self.get_vector(point)
            for x in np.arange(-9, 9)
            for y in np.arange(-5, 5)
            for point in [x*RIGHT + y*UP]
        ])
        shading_list = list(result)
        shading_list.sort(
            # CHANGE: typo in the original (m1 undefined): sort key must use the lambda argument
            key=lambda m: m.get_length()
        )
        VGroup(*shading_list).set_color_by_gradient(*self.vector_field_colors)
        result.set_fill(opacity = 0.75)
        result.sort(get_norm)

        return result

    def get_vector(self, point):
        return Vector(self.field_function(point)).shift(point)

    def field_function(self, point):
        x, y = point[:2]
        result = y*RIGHT + np.sin(x)*UP
        return self.normalized(result)

    def normalized(self, vector):
        norm = get_norm(vector) or 1
        target_length = self.max_vector_length * sigmoid(0.1*norm)
        return target_length * vector/norm


class IntroduceMagneticField(IntroduceElectricField, ThreeDScene):
    CONFIG = {
        "vector_field_colors" : [YELLOW_C, YELLOW_D]
    }
    def setup(self):
        IntroduceElectricField.setup(self)
        self.remove(self.pi_creature)

    def construct(self):
        self.set_camera_orientation(0.1, -np.pi/2)
        self.add_title()
        self.add_vector_field()
        self.introduce_moving_charge()
        self.show_force()
        # self.many_charges()

    def add_title(self):
        title = OldTexText("Magnetic", "field")
        title[0].set_color(YELLOW)
        title.scale(1.5)
        title.to_edge(UP)
        title.add_background_rectangle()

        self.add(title)
        self.title = title

    def add_vector_field(self):
        vector_field = self.get_vector_field()

        self.play(
            LaggedStartMap(ShowCreation, vector_field, run_time = 3),
            Animation(self.title)
        )
        self.wait()

    def introduce_moving_charge(self):
        point = 3*RIGHT + UP
        particle = self.get_particle()
        particle.move_to(point)

        velocity = Vector(2*RIGHT).shift(particle.get_right())
        velocity.set_color(WHITE)
        velocity_word = OldTexText("Velocity")
        velocity_word.set_color(velocity.get_color())
        velocity_word.add_background_rectangle()
        velocity_word.next_to(velocity, UP, 0, LEFT)

        M_vect = self.get_vector(point)
        M_vect.set_color(YELLOW)
        M_vect.shift(SMALL_BUFF*M_vect.get_vector())

        particle.save_state()
        particle.shift(FRAME_WIDTH*LEFT)

        self.play(
            particle.restore,
            run_time = 2,
            rate_func=linear,
        )
        self.add(velocity)
        self.play(Write(velocity_word, run_time = 0.5))
        # self.play(ShowCreation(M_vect))
        self.wait()

        self.particle = particle

    def show_force(self):
        point = self.particle.get_center()
        F_vect = Vector(
            3*np.cross(self.field_function(point), RIGHT),
            color = GREEN
        )
        F_vect.shift(point)
        F_word = OldTexText("Force")
        F_word.rotate(np.pi/2, RIGHT)
        F_word.next_to(F_vect, OUT)
        F_word.set_color(F_vect.get_color())
        F_eq = OldTex(
            "=","q", "\\textbf{v}", "\\times", "\\textbf{B}"
        )
        F_eq.set_color_by_tex_to_color_map({
            "q" : RED,
            "B" : YELLOW,
        })
        F_eq.rotate(np.pi/2, RIGHT)
        F_eq.next_to(F_word, RIGHT)


        self.move_camera(0.8*np.pi/2, -0.55*np.pi)
        self.begin_ambient_camera_rotation()
        self.play(ShowCreation(F_vect))
        self.play(Write(F_word))
        self.wait()
        self.play(Write(F_eq))
        self.wait(8)

    def many_charges(self):
        charges = VGroup()
        for y in range(2, 3):
            charge = self.get_particle()
            charge.move_to(3*LEFT + y*UP)
            charge.velocity = (2*RIGHT).astype('float')
            charges.add(charge)

        self.revert_to_original_skipping_status()
        self.add_foreground_mobjects(*charges)
        self.moving_particles = charges
        self.wait(5)

        
    ###

    def update_mobjects(self, *args, **kwargs):
        Scene.update_mobjects(self, *args, **kwargs)
        if hasattr(self, "moving_particles"):
            dt = self.frame_duration
            for p in self.moving_particles:
                M_vect = self.field_function(p.get_center())
                F_vect = 3*np.cross(p.velocity, M_vect)
                p.velocity += F_vect*dt
                p.shift(p.velocity*dt)

    def field_function(self, point):
        x, y = point[:2]
        y += 0.5
        gauss = lambda r : np.exp(-0.5*r**2)
        result = (y**2 - 1)*RIGHT + x*(gauss(y+2) - gauss(y-2))*UP
        return self.normalized(result)
