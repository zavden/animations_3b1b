# ==============================================================================
# Scene:      PhaseSpaceOfPopulationModel
# Source:     videos/_2018/div_curl.py (lines 2896-3186)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhaseSpaceOfPopulationModel.py PhaseSpaceOfPopulationModel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

FOX_COLOR = "#DF7F20"


RABBIT_COLOR = "#C6D6EF"


def preditor_prey_vector_field(point):
    alpha = 30.0
    beta = 1.0
    gamma = 30.0
    delta = 1.0
    x, y = point[:2]
    result = 0.05 * np.array([
        alpha * x - beta * x * y,
        delta * x * y - gamma * y,
        0,
    ])
    return rotate(result, 1 * DEGREES)


class ShowTwoPopulations(Scene):
    CONFIG = {
        "total_num_animals": 80,
        "start_num_foxes": 40,
        "start_num_rabbits": 20,
        "animal_height": 0.5,
        "final_wait_time": 30,
        "count_word_scale_val": 1,
    }

    def construct(self):
        self.introduce_animals()
        self.evolve_system()

    def introduce_animals(self):
        foxes = self.foxes = VGroup(*[
            self.get_fox()
            for n in range(self.total_num_animals)
        ])
        rabbits = self.rabbits = VGroup(*[
            self.get_rabbit()
            for n in range(self.total_num_animals)
        ])
        foxes[self.start_num_foxes:].set_fill(opacity=0)
        rabbits[self.start_num_rabbits:].set_fill(opacity=0)

        fox, rabbit = examples = VGroup(foxes[0], rabbits[0])
        for mob in examples:
            mob.save_state()
            mob.set_height(3)
        examples.arrange(LEFT, buff=2)

        preditor, prey = words = VGroup(
            OldTexText("Predator"),
            OldTexText("Prey")
        )
        for mob, word in zip(examples, words):
            word.scale(1.5)
            word.next_to(mob, UP)
            self.play(
                FadeInFromDown(mob),
                Write(word, run_time=1),
            )
        self.play(
            LaggedStartMap(
                ApplyMethod, examples,
                lambda m: (m.restore,)
            ),
            LaggedStartMap(FadeOut, words),
            *[
                LaggedStartMap(
                    FadeIn,
                    group[1:],
                    run_time=4,
                    lag_ratio=0.1,
                    rate_func=lambda t: np.clip(smooth(2 * t), 0, 1)
                )
                for group in [foxes, rabbits]
            ]
        )

    def evolve_system(self):
        foxes = self.foxes
        rabbits = self.rabbits
        phase_point = VectorizedPoint(
            self.start_num_rabbits * RIGHT +
            self.start_num_foxes * UP
        )
        self.add(move_along_vector_field(
            phase_point,
            preditor_prey_vector_field,
        ))

        def get_num_rabbits():
            return phase_point.get_center()[0]

        def get_num_foxes():
            return phase_point.get_center()[1]

        def get_updater(pop_size_getter):
            def update(animals):
                target_num = pop_size_getter()
                for n, animal in enumerate(animals):
                    animal.set_fill(
                        opacity=np.clip(target_num - n, 0, 1)
                    )
                target_int = int(np.ceil(target_num))
                tail = animals.submobjects[target_int:]
                random.shuffle(tail)
                animals.submobjects[target_int:] = tail

            return update

        self.add(Mobject.add_updater(
            foxes, get_updater(get_num_foxes)
        ))
        self.add(Mobject.add_updater(
            rabbits, get_updater(get_num_rabbits)
        ))

        # Add counts for foxes and rabbits
        labels = self.get_pop_labels()
        num_foxes = Integer(10)
        num_foxes.scale(self.count_word_scale_val)
        num_foxes.next_to(labels[0], RIGHT)
        num_foxes.align_to(labels[0][0][1], DOWN)
        num_rabbits = Integer(10)
        num_rabbits.scale(self.count_word_scale_val)
        num_rabbits.next_to(labels[1], RIGHT)
        num_rabbits.align_to(labels[1][0][1], DOWN)

        num_foxes.add_updater(lambda d: d.set_value(get_num_foxes()))
        num_rabbits.add_updater(lambda d: d.set_value(get_num_rabbits()))

        self.add(num_foxes, num_rabbits)

        for count in num_foxes, num_rabbits:
            self.add(Mobject.add_updater(
                count, self.update_count_color,
            ))

        self.play(
            FadeIn(labels),
            *[
                UpdateFromAlphaFunc(count, lambda m, a: m.set_fill(opacity=a))
                for count in (num_foxes, num_rabbits)
            ]
        )

        self.wait(self.final_wait_time)

    # Helpers

    def get_animal(self, name, color):
        result = SVGMobject(
            file_name=name,
            height=self.animal_height,
            fill_color=color,
        )
        # for submob in result.family_members_with_points():
            # if submob.is_subpath:
            #     submob.is_subpath = False
            #     submob.set_fill(
            #         interpolate_color(color, BLACK, 0.8),
            #         opacity=1
            #     )
        x_shift, y_shift = [
            (2 * random.random() - 1) * max_val
            for max_val in [
                FRAME_WIDTH / 2 - 2,
                FRAME_HEIGHT / 2 - 2
            ]
        ]
        result.shift(x_shift * RIGHT + y_shift * UP)
        return result

    def get_fox(self):
        return self.get_animal("fox", FOX_COLOR)

    def get_rabbit(self):
        # return self.get_animal("rabbit", WHITE)
        return self.get_animal("bunny", RABBIT_COLOR)

    def get_pop_labels(self):
        labels = VGroup(
            OldTexText("\\# Foxes: "),
            OldTexText("\\# Rabbits: "),
        )
        for label in labels:
            label.scale(self.count_word_scale_val)
        labels.arrange(RIGHT, buff=2)
        labels.to_edge(UP)
        return labels

    def update_count_color(self, count):
        count.set_fill(interpolate_color(
            BLUE, RED, (count.number - 20) / 30.0
        ))
        return count


class PhaseSpaceOfPopulationModel(ShowTwoPopulations, PiCreatureScene, MovingCameraScene):
    CONFIG = {
        "origin": 5 * LEFT + 2.5 * DOWN,
        "vector_field_config": {
            "max_magnitude": 50,
        },
        "pi_creatures_start_on_screen": False,
        "default_pi_creature_kwargs": {
            "height": 1.8
        },
        "flow_time": 10,
    }

    def setup(self):
        MovingCameraScene.setup(self)
        PiCreatureScene.setup(self)

    def construct(self):
        self.add_axes()
        self.add_example_point()
        self.write_differential_equations()
        self.add_vectors()
        self.show_phase_flow()

    def add_axes(self):
        axes = self.axes = Axes(
            x_min=0,
            x_max=55,
            x_axis_config={"unit_size": 0.15},
            y_min=0,
            y_max=55,
            y_axis_config={"unit_size": 0.09},
            axis_config={
                "tick_frequency": 10,
            },
        )
        axes.shift(self.origin)
        for axis in axes.x_axis, axes.y_axis:
            axis.add_numbers(*list(range(10, 60, 10)))

        axes_labels = self.axes_labels = VGroup(*[
            VGroup(
                method().set_height(0.75),
                OldTexText("Population"),
            ).arrange(RIGHT, buff=MED_SMALL_BUFF)
            for method in (self.get_rabbit, self.get_fox)
        ])
        for axis, label, vect in zip(axes, axes_labels, [RIGHT, UP]):
            label.next_to(
                axis, vect,
                submobject_to_align=label[0]
            )

        self.add(axes, axes_labels)

    def add_example_point(self):
        axes = self.axes
        origin = self.origin
        x = self.start_num_rabbits
        y = self.start_num_foxes
        point = axes.coords_to_point(x, y)
        x_point = axes.coords_to_point(x, 0)
        y_point = axes.coords_to_point(0, y)
        v_line = DashedLine(x_point, point)
        h_line = DashedLine(y_point, point)
        v_line.set_color(FOX_COLOR)
        h_line.set_color(GREY_B)
        dot = Dot(point)

        coord_pair = OldTex(
            "(10, 10)", isolate=["10"]
        )
        pop_sizes = VGroup(Integer(10), Integer(10))
        pop_sizes[0].set_color(GREY_B)
        pop_sizes[1].set_color(FOX_COLOR)
        tens = coord_pair.get_parts_by_tex("10")
        tens.fade(1)

        def get_pop_size_update(i):
            return ContinualChangingDecimal(
                pop_sizes[i],
                lambda a: int(np.round(
                    axes.point_to_coords(dot.get_center())[i]
                )),
                position_update_func=lambda m: m.move_to(tens[i])
            )
        coord_pair.add_background_rectangle()
        coord_pair_update = Mobject.add_updater(
            coord_pair, lambda m: m.next_to(dot, UR, SMALL_BUFF)
        )
        pop_sizes_updates = [get_pop_size_update(i) for i in (0, 1)]

        phase_space = OldTexText("``Phase space''")
        phase_space.set_color(YELLOW)
        phase_space.scale(1.5)
        phase_space.to_edge(UP)
        phase_space.shift(2 * RIGHT)

        self.play(ShowCreation(v_line))
        self.play(ShowCreation(h_line))
        dot.save_state()
        dot.move_to(origin)
        self.add(coord_pair_update)
        self.add(*pop_sizes_updates)
        self.play(
            dot.restore,
            VFadeIn(coord_pair),
            UpdateFromAlphaFunc(pop_sizes, lambda m, a: m.set_fill(opacity=a)),
        )
        self.wait()
        self.play(Write(phase_space))
        self.wait(2)
        self.play(FadeOut(VGroup(h_line, v_line, phase_space)))
        self.play(Rotating(
            dot,
            about_point=axes.coords_to_point(30, 30),
            rate_func=smooth,
        ))

        self.dot = dot
        self.coord_pair = coord_pair
        self.coord_pair_update = coord_pair_update
        self.pop_sizes = pop_sizes
        self.pop_sizes_updates = pop_sizes_updates

    def write_differential_equations(self):
        equations = self.get_equations()
        equations.shift(2 * DOWN)
        rect = SurroundingRectangle(equations, color=YELLOW)
        rect.set_fill(BLACK, 0.8)
        title = OldTexText("Differential equations")
        title.next_to(rect, UP)
        title.set_color(rect.get_stroke_color())
        self.differential_equation_group = VGroup(
            rect, equations, title
        )
        self.differential_equation_group.to_corner(UR)

        randy = self.pi_creature
        randy.next_to(rect, DL)

        self.play(
            Write(title, run_time=1),
            ShowCreation(rect)
        )
        self.play(
            LaggedStartMap(FadeIn, equations),
            randy.change, "confused", equations,
            VFadeIn(randy),
        )
        self.wait(3)

    def add_vectors(self):
        origin = self.axes.coords_to_point(0, 0)
        dot = self.dot
        randy = self.pi_creature

        def rescaled_field(point):
            x, y = self.axes.point_to_coords(point)
            result = preditor_prey_vector_field(np.array([x, y, 0]))
            return self.axes.coords_to_point(*result[:2]) - origin

        self.vector_field_config.update({
            "x_min": origin[0] + 0.5,
            "x_max": self.axes.get_right()[0] + 1,
            "y_min": origin[1] + 0.5,
            "y_max": self.axes.get_top()[1],
        })
        vector_field = VectorField(
            rescaled_field, **self.vector_field_config
        )

        def get_dot_vector():
            vector = vector_field.get_vector(dot.get_center())
            vector.scale(1, about_point=vector.get_start())
            return vector

        dot_vector = get_dot_vector()

        self.play(
            LaggedStartMap(GrowArrow, vector_field),
            randy.change, "thinking", dot,
            Animation(self.differential_equation_group)
        )
        self.wait(3)
        self.play(
            Animation(dot),
            vector_field.set_fill, {"opacity": 0.2},
            Animation(self.differential_equation_group),
            GrowArrow(dot_vector),
            randy.change, "pondering",
        )
        self.wait()
        self.play(
            dot.move_to, dot_vector.get_end(),
            dot.align_to, dot, RIGHT,
            run_time=3,
        )
        self.wait(2)
        self.play(
            dot.move_to, dot_vector.get_end(),
            run_time=3,
        )
        self.wait(2)
        for x in range(6):
            new_dot_vector = get_dot_vector()
            fade_anims = [
                FadeOut(dot_vector),
                FadeIn(new_dot_vector),
                Animation(dot),
            ]
            if x == 4:
                fade_anims += [
                    vector_field.set_fill, {"opacity": 0.5},
                    FadeOut(randy),
                    FadeOut(self.differential_equation_group),
                ]
            self.play(*fade_anims)
            dot_vector = new_dot_vector
            self.play(dot.move_to, dot_vector.get_end())

        dot_movement = move_along_vector_field(
            dot, lambda p: 0.3 * vector_field.func(p)
        )
        self.add(dot_movement)
        self.play(FadeOut(dot_vector))
        self.wait(10)
        self.play(
            vector_field.set_fill, {"opacity": 1.0},
            VFadeOut(dot),
            VFadeOut(self.coord_pair),
            UpdateFromAlphaFunc(self.pop_sizes, lambda m, a: m.set_fill(opacity=1 - a)),
        )
        self.remove(
            dot_movement,
            self.coord_pair_update,
            *self.pop_sizes_updates
        )
        self.wait()

        self.vector_field = vector_field

    def show_phase_flow(self):
        vector_field = self.vector_field
        stream_lines = StreamLines(
            vector_field.func,
            start_points_generator_config={
                "x_min": vector_field.x_min,
                "x_max": vector_field.x_max,
                "y_min": vector_field.y_min,
                "y_max": vector_field.y_max,
                "delta_x": 0.25,
                "delta_y": 0.25,
            },
            min_magnitude=vector_field.min_magnitude,
            max_magnitude=vector_field.max_magnitude,
            virtual_time=4,
        )
        stream_line_animation = AnimatedStreamLines(
            stream_lines,
        )
        self.add(stream_line_animation)
        self.add_foreground_mobjects(vector_field)
        self.wait(self.flow_time)
        self.play(
            self.camera_frame.scale, 1.5, {"about_point": self.origin},
            run_time=self.flow_time,
        )
        self.wait(self.flow_time)

    #
    def get_equations(self):
        variables = ["X", "YY"]
        equations = OldTex(
            """
                {dX \\over dt} =
                X \\cdot (\\alpha - \\beta YY \\,) \\\\
                \\quad \\\\
                {dYY \\over dt} =
                YY \\cdot (\\delta X - \\gamma)
            """,
            isolate=variables
        )
        animals = [self.get_rabbit(), self.get_fox().flip()]
        for char, animal in zip(variables, animals):
            for part in equations.get_parts_by_tex(char):
                animal_copy = animal.copy()
                animal_copy.set_height(0.5)
                animal_copy.move_to(part, DL)
                part.become(animal_copy)
        return equations
