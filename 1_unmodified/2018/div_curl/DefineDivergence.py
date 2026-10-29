# ==============================================================================
# Scene:      DefineDivergence
# Source:     videos/_2018/div_curl.py (lines 1432-1582)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineDivergence.py DefineDivergence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def divergence(vector_func, dt=1e-7):
    def result(point):
        value = vector_func(point)
        return sum([
            (vector_func(point + dt * RIGHT) - value)[i] / dt
            for i, vect in enumerate([RIGHT, UP, OUT])
        ])
    return result


def get_force_field_func(*point_strength_pairs, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in point_strength_pairs:
            to_center = center - point
            norm = get_norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            elif norm >= radius:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func


def get_charged_particles(color, sign, radius=0.1):
    result = Circle(
        stroke_color=WHITE,
        stroke_width=0.5,
        fill_color=color,
        fill_opacity=0.8,
        radius=radius
    )
    sign = OldTex(sign)
    sign.set_stroke(WHITE, 1)
    sign.set_width(0.5 * result.get_width())
    sign.move_to(result)
    result.add(sign)
    return result


def get_proton(radius=0.1):
    return get_charged_particles(RED, "+", radius)


def get_electron(radius=0.05):
    return get_charged_particles(BLUE, "-", radius)


class ChangingElectricField(Scene):
    CONFIG = {
        "vector_field_config": {}
    }

    def construct(self):
        particles = self.get_particles()
        vector_field = self.get_vector_field()

        def update_vector_field(vector_field):
            new_field = self.get_vector_field()
            Transform(vector_field, new_field).update(1)
            vector_field.func = new_field.func

        def update_particles(particles, dt):
            func = vector_field.func
            for particle in particles:
                force = func(particle.get_center())
                particle.velocity += force * dt
                particle.shift(particle.velocity * dt)

        self.add(
            Mobject.add_updater(vector_field, update_vector_field),
            Mobject.add_updater(particles, update_particles),
        )
        self.wait(20)

    def get_particles(self):
        particles = self.particles = VGroup()
        for n in range(9):
            if n % 2 == 0:
                particle = get_proton(radius=0.2)
                particle.charge = +1
            else:
                particle = get_electron(radius=0.2)
                particle.charge = -1
            particle.velocity = np.random.normal(0, 0.1, 3)
            particles.add(particle)
            particle.shift(np.random.normal(0, 0.2, 3))

        particles.arrange_in_grid(buff=LARGE_BUFF)
        return particles

    def get_vector_field(self):
        func = get_force_field_func(*list(zip(
            list(map(Mobject.get_center, self.particles)),
            [p.charge for p in self.particles]
        )))
        self.vector_field = VectorField(func, **self.vector_field_config)
        return self.vector_field


class DefineDivergence(ChangingElectricField):
    CONFIG = {
        "vector_field_config": {
            "length_func": lambda norm: 0.3,
            "min_magnitude": 0,
            "max_magnitude": 1,
        },
        "stream_line_config": {
            "start_points_generator_config": {
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            "virtual_time": 5,
            "n_anchors_per_line": 10,
            "min_magnitude": 0,
            "max_magnitude": 1,
            "stroke_width": 2,
        },
        "stream_line_animation_config": {
            "line_anim_class": ShowPassingFlash,
        },
        "flow_time": 10,
        "random_seed": 7,
    }

    def construct(self):
        self.draw_vector_field()
        self.show_flow()
        self.point_out_sources_and_sinks()
        self.show_divergence_values()

    def draw_vector_field(self):
        particles = self.get_particles()
        random.shuffle(particles.submobjects)
        particles.remove(particles[0])
        particles.arrange_in_grid(
            n_cols=4, buff=3
        )
        for particle in particles:
            particle.shift(
                np.random.normal(0, 0.75) * RIGHT,
                np.random.normal(0, 0.5) * UP,
            )
            particle.shift_onto_screen(buff=2 * LARGE_BUFF)
            particle.charge *= 0.125
        vector_field = self.get_vector_field()

        self.play(
            LaggedStartMap(GrowArrow, vector_field),
            LaggedStartMap(GrowFromCenter, particles),
            run_time=4
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, particles))

    def show_flow(self):
        stream_lines = StreamLines(
            self.vector_field.func,
            **self.stream_line_config
        )
        stream_line_animation = AnimatedStreamLines(
            stream_lines,
            **self.stream_line_animation_config
        )
        self.add(stream_line_animation)
        self.wait(self.flow_time)

    def point_out_sources_and_sinks(self):
        particles = self.particles
        self.positive_points, self.negative_points = [
            [
                particle.get_center()
                for particle in particles
                if u * particle.charge > 0
            ]
            for u in (+1, -1)
        ]
        pair_of_vector_circle_groups = VGroup()
        for point_set in self.positive_points, self.negative_points:
            vector_circle_groups = VGroup()
            for point in point_set:
                vector_circle_group = VGroup()
                for angle in np.linspace(0, TAU, 12, endpoint=False):
                    step = 0.5 * rotate_vector(RIGHT, angle)
                    vect = self.vector_field.get_vector(point + step)
                    vect.set_color(WHITE)
                    vect.set_stroke(width=2)
                    vector_circle_group.add(vect)
                vector_circle_groups.add(vector_circle_group)
            pair_of_vector_circle_groups.add(vector_circle_groups)

            self.play(
                self.vector_field.set_fill, {"opacity": 0.5},
                LaggedStartMap(
                    LaggedStartMap, vector_circle_groups,
                    lambda vcg: (GrowArrow, vcg),
                ),
            )
            self.wait(4)
            self.play(FadeOut(vector_circle_groups))
        self.play(self.vector_field.set_fill, {"opacity": 1})
        self.positive_vector_circle_groups = pair_of_vector_circle_groups[0]
        self.negative_vector_circle_groups = pair_of_vector_circle_groups[1]
        self.wait()

    def show_divergence_values(self):
        positive_points = self.positive_points
        negative_points = self.negative_points
        div_func = divergence(self.vector_field.func)

        circle = Circle(color=WHITE, radius=0.2)
        circle.add(Dot(circle.get_center(), radius=0.02))
        circle.move_to(positive_points[0])

        div_tex = OldTex(
            "\\text{div} \\, \\textbf{F}(x, y) = "
        )
        div_tex.add_background_rectangle()
        div_tex_update = Mobject.add_updater(
            div_tex, lambda m: m.next_to(circle, UP, SMALL_BUFF)
        )

        div_value = DecimalNumber(
            0,
            num_decimal_places=1,
            include_background_rectangle=True,
            include_sign=True,
        )
        div_value_update = ContinualChangingDecimal(
            div_value,
            lambda a: np.round(div_func(circle.get_center()), 1),
            position_update_func=lambda m: m.next_to(div_tex, RIGHT, SMALL_BUFF),
            include_sign=True,
        )

        self.play(
            ShowCreation(circle),
            FadeIn(div_tex),
            FadeIn(div_value),
        )
        self.add(div_tex_update)
        self.add(div_value_update)

        self.wait()
        for point in positive_points[1:-1]:
            self.play(circle.move_to, point)
            self.wait(1.5)
        for point in negative_points:
            self.play(circle.move_to, point)
            self.wait(2)
        self.wait(4)
