# ==============================================================================
# Scene:      IntroduceElectricField
# Source:     videos/_2017/waves.py (lines 565-729)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceElectricField.py IntroduceElectricField -w -m --fps 15
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
