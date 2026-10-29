# ==============================================================================
# Scene:      TwoDimensionalCaseIntro
# Source:     videos/_2017/highD.py (lines 1299-1302)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TwoDimensionalCaseIntro.py TwoDimensionalCaseIntro -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL writes negative numbers with an en dash: normalise the sign before int()
#   - numpy 2 np.cross no longer accepts 2D vectors: use the scalar z-component
# ==============================================================================

from manim_imports_ext import *

class Slider(NumberLine):
    CONFIG = {
        "color" : WHITE,
        "x_min" : -1,
        "x_max" : 1,
        "unit_size" : 2,
        "center_value" : 0,
        "number_scale_val" : 0.75,
        "label_scale_val" : 1,
        "big_tick_numbers" : [],
        "line_to_number_vect" : LEFT,
        "line_to_number_buff" : MED_LARGE_BUFF,
        "dial_radius" : 0.1,
        "dial_color" : YELLOW,
        "include_real_estate_ticks" : True,
    }
    def __init__(self, **kwargs):
        NumberLine.__init__(self, **kwargs)
        self.rotate(np.pi/2)
        self.init_dial()
        if self.include_real_estate_ticks:
            self.add_real_estate_ticks()

    def init_dial(self):
        dial = Dot(
            radius = self.dial_radius,
            color = self.dial_color,
        )
        dial.move_to(self.number_to_point(self.center_value))
        re_dial = dial.copy()
        re_dial.set_fill(opacity = 0)
        self.add(dial, re_dial)

        self.dial = dial
        self.re_dial = re_dial
        self.last_sign = -1

    def add_label(self, tex):
        label = OldTex(tex)
        label.scale(self.label_scale_val)
        label.move_to(self.get_top())
        label.shift(MED_LARGE_BUFF*UP)
        self.add(label)
        self.label = label

    def add_real_estate_ticks(
        self, 
        re_per_tick = 0.05,
        colors = [BLUE, RED],
        max_real_estate = 1,
        ):
        self.real_estate_ticks = VGroup(*[   
            self.get_tick(self.center_value + u*np.sqrt(x + re_per_tick))
            for x in np.arange(0, max_real_estate, re_per_tick)
            for u in [-1, 1]
        ])
        self.real_estate_ticks.set_stroke(width = 3)
        self.real_estate_ticks.set_color_by_gradient(*colors)
        self.add(self.real_estate_ticks)
        self.add(self.dial)
        return self.real_estate_ticks

    def set_value(self, x):
        re = (x - self.center_value)**2
        for dial, val in (self.dial, x), (self.re_dial, re):
            dial.move_to(self.number_to_point(val))
        return self

    def set_center_value(self, x):
        self.center_value = x
        return self

    def change_real_estate(self, d_re):
        left_over = 0
        curr_re = self.get_real_estate()
        if d_re < -curr_re:
            left_over = d_re + curr_re
            d_re = -curr_re
        self.set_real_estate(curr_re + d_re)
        return left_over

    def set_real_estate(self, target_re):
        if target_re < 0:
            raise Exception("Cannot set real estate below 0")
        self.re_dial.move_to(self.number_to_point(target_re))
        self.update_dial_by_re_dial()
        return self

    def get_dial_supplement_animation(self):
        return UpdateFromFunc(self.dial, self.update_dial_by_re_dial)

    def update_dial_by_re_dial(self, dial = None):
        dial = dial or self.dial
        re = self.get_real_estate()
        sign = np.sign(self.get_value() - self.center_value)
        if sign == 0:
            sign = -self.last_sign
            self.last_sign *= -1
        dial.move_to(self.number_to_point(
            self.center_value + sign*np.sqrt(abs(re))
        ))
        return dial

    def get_value(self):
        return self.point_to_number(self.dial.get_center())

    def get_real_estate(self):
        return self.point_to_number(self.re_dial.get_center())

    def copy(self):
        return self.deepcopy()


class SliderScene(Scene):
    CONFIG = {
        "n_sliders" : 4,
        "slider_spacing" : MED_LARGE_BUFF,
        "slider_config" : {},
        "center_point" : None,
        "total_real_estate" : 1,
        "ambiently_change_sliders" : False,
        "ambient_velocity_magnitude" : 1.0,
        "ambient_acceleration_magnitude" : 1.0,
        "ambient_jerk_magnitude" : 1.0/2,
    }
    def setup(self):
        if self.center_point is None:
            self.center_point = np.zeros(self.n_sliders)
        sliders = VGroup(*[
            Slider(center_value = cv, **self.slider_config)
            for cv in self.center_point
        ])
        sliders.arrange(RIGHT, buff = self.slider_spacing)
        sliders[0].add_numbers()
        sliders[0].set_value(
            self.center_point[0] + np.sqrt(self.total_real_estate)
        )
        self.sliders = sliders
        
        self.add_labels_to_sliders()
        self.add(sliders)

    def add_labels_to_sliders(self):
        if len(self.sliders) <= 4:
            for slider, char in zip(self.sliders, "xyzw"):
                slider.add_label(char)
            for slider in self.sliders[1:]:
                slider.label.align_to(self.sliders[0].label, UP)
        else:
            for i, slider in enumerate(self.sliders):
                slider.add_label("x_{%d}"%(i+1))
        return self

    def reset_dials(self, values, run_time = 1, **kwargs):
        target_vector = self.get_target_vect_from_subset_of_values(values, **kwargs)

        radius = np.sqrt(self.total_real_estate)
        def update_sliders(sliders):
            curr_vect = self.get_vector()
            curr_vect -= self.center_point
            curr_vect *= radius/get_norm(curr_vect)
            curr_vect += self.center_point
            self.set_to_vector(curr_vect)
            return sliders

        self.play(*[
            ApplyMethod(slider.set_value, value)
            for value, slider in zip(target_vector, self.sliders)
        ] + [
            UpdateFromFunc(self.sliders, update_sliders)
        ], run_time = run_time)

    def get_target_vect_from_subset_of_values(self, values, fixed_indices = None):
        if fixed_indices is None: 
            fixed_indices = []
        curr_vector = self.get_vector()
        target_vector = np.array(self.center_point, dtype = 'float')
        unspecified_vector = np.array(self.center_point, dtype = 'float')
        unspecified_indices = []
        for i in range(len(curr_vector)):
            if i < len(values) and values[i] is not None:
                target_vector[i] = values[i]
            else:
                unspecified_indices.append(i)
                unspecified_vector[i] = curr_vector[i]
        used_re = get_norm(target_vector - self.center_point)**2
        left_over_re = self.total_real_estate - used_re
        if left_over_re < -0.001:
            raise Exception("Overspecified reset")
        uv_norm = get_norm(unspecified_vector - self.center_point)
        if uv_norm == 0 and left_over_re > 0:
            unspecified_vector[unspecified_indices] = 1
            uv_norm = get_norm(unspecified_vector - self.center_point)
        if uv_norm > 0:
            unspecified_vector -= self.center_point
            unspecified_vector *= np.sqrt(left_over_re)/uv_norm
            unspecified_vector += self.center_point
        return target_vector + unspecified_vector - self.center_point

    def set_to_vector(self, vect):
        assert len(vect) == len(self.sliders)
        for slider, value in zip(self.sliders, vect):
            slider.set_value(value)

    def get_vector(self):
        return np.array([slider.get_value() for slider in self.sliders])

    def get_center_point(self):
        return np.array([slider.center_value for slider in self.sliders])

    def set_center_point(self, new_center_point):
        self.center_point = np.array(new_center_point)
        for x, slider in zip(new_center_point, self.sliders):
            slider.set_center_value(x)
        return self

    def get_current_total_real_estate(self):
        return sum([
            slider.get_real_estate()
            for slider in self.sliders
        ])

    def get_all_dial_supplement_animations(self):
        return [
            slider.get_dial_supplement_animation()
            for slider in self.sliders
        ]

    def initialize_ambiant_slider_movement(self):
        self.ambiently_change_sliders = True
        self.ambient_change_end_time = np.inf
        self.ambient_change_time = 0
        self.ambient_velocity, self.ambient_acceleration, self.ambient_jerk = [
            self.get_random_vector(magnitude)
            for magnitude in [
                self.ambient_velocity_magnitude,
                self.ambient_acceleration_magnitude,
                self.ambient_jerk_magnitude,
            ]
        ]
        ##Ensure counterclockwise rotations in 2D
        if len(self.ambient_velocity) == 2:
            # CHANGE: numpy 2 np.cross no longer accepts 2D vectors: use the scalar z-component
            v1, v2 = self.get_vector(), self.ambient_velocity
            cross = np.cross(v1, v2) if len(v1) == 3 else v1[0]*v2[1] - v1[1]*v2[0]
            if cross < 0:
                self.ambient_velocity *= -1
        self.add_foreground_mobjects(self.sliders)

    def wind_down_ambient_movement(self, time = 1, wait = True):
        self.ambient_change_end_time = self.ambient_change_time + time
        if wait:
            self.wait(time)
            if self.skip_animations:
                self.ambient_change_time += time

    def ambient_slider_movement_update(self):
        #Set velocity_magnitude based on start up or wind down
        velocity_magnitude = float(self.ambient_velocity_magnitude)
        if self.ambient_change_time <= 1:
            velocity_magnitude *= smooth(self.ambient_change_time)
        time_until_end = self.ambient_change_end_time - self.ambient_change_time
        if time_until_end <= 1:
            velocity_magnitude *= smooth(time_until_end)
        if time_until_end < 0:
            self.ambiently_change_sliders = False
            return

        center_point = self.get_center_point()
        target_vector = self.get_vector() - center_point
        if get_norm(target_vector) == 0:
            return
        vectors_and_magnitudes = [
            (self.ambient_acceleration, self.ambient_acceleration_magnitude),
            (self.ambient_velocity, velocity_magnitude),
            (target_vector, np.sqrt(self.total_real_estate)),
        ]
        jerk = self.get_random_vector(self.ambient_jerk_magnitude)
        deriv = jerk
        for vect, mag in vectors_and_magnitudes:
            vect += self.frame_duration*deriv
            if vect is self.ambient_velocity:
                unit_r_vect = target_vector / get_norm(target_vector)
                vect -= np.dot(vect, unit_r_vect)*unit_r_vect
            vect *= mag/get_norm(vect)
            deriv = vect

        self.set_to_vector(target_vector + center_point)
        self.ambient_change_time += self.frame_duration

    def get_random_vector(self, magnitude):
        result = 2*np.random.random(len(self.sliders)) - 1
        result *= magnitude / get_norm(result)
        return result

    def update_frame(self, *args, **kwargs):
        if self.ambiently_change_sliders:
            self.ambient_slider_movement_update()
        Scene.update_frame(self, *args, **kwargs)

    def wait(self, time = 1):
        if self.ambiently_change_sliders:
            self.play(Animation(self.sliders, run_time = time))
        else:
            Scene.wait(self,time)


class DismissProjection(PiCreatureScene):
    CONFIG = { 
        "screen_rect_color" : WHITE,
        "example_vect" : np.array([0.52, 0.26, 0.53, 0.60]),
    }
    def construct(self):
        self.remove(self.pi_creature)
        self.show_all_spheres()
        self.discuss_4d_sphere_definition()
        self.talk_through_animation()
        self.transition_to_next_scene()
        
    def show_all_spheres(self):
        equations = VGroup(*list(map(Tex, [
            "x^2 + y^2 = 1",
            "x^2 + y^2 + z^2 = 1",
            "x^2 + y^2 + z^2 + w^2 = 1",
        ])))
        colors = [YELLOW, GREEN, BLUE]
        for equation, edge, color in zip(equations, [LEFT, ORIGIN, RIGHT], colors):
            equation.set_color(color)
            equation.shift(3*UP)
            equation.to_edge(edge)
        equations[1].shift(LEFT)

        spheres = VGroup(
            self.get_circle(equations[0]),
            self.get_sphere_screen(equations[1], DOWN),
            self.get_sphere_screen(equations[2], DOWN),
        )
        
        for equation, sphere in zip(equations, spheres):
            self.play(
                Write(equation),
                LaggedStartMap(ShowCreation, sphere),
            )
        self.wait()

        self.equations = equations
        self.spheres = spheres

    def get_circle(self, equation):
        result = VGroup(
            NumberPlane(
                x_radius = 2.5,
                y_radius = 2,
            ).fade(0.4),
            Circle(color = YELLOW, radius = 1),
        )
        result.scale(0.7)
        result.next_to(equation, DOWN)
        return result

    def get_sphere_screen(self, equation, vect):
        square = Rectangle()
        square.set_width(equation.get_width())
        square.stretch_to_fit_height(3)
        square.next_to(equation, vect)
        square.set_color(self.screen_rect_color)
        return square

    def discuss_4d_sphere_definition(self):
        sphere = self.spheres[-1]
        equation = self.equations[-1]

        sphere_words = OldTexText("``4-dimensional sphere''")
        sphere_words.next_to(sphere, DOWN+LEFT, buff = LARGE_BUFF)
        arrow = Arrow(
            sphere_words.get_right(), sphere.get_bottom(), 
            path_arc = np.pi/3, 
            color = BLUE
        )
        descriptor = OldTex(
            "\\text{Just lists of numbers like }", 
            "(%.02f \\,, %.02f \\,, %.02f \\,, %.02f \\,)"%tuple(self.example_vect)
        )
        descriptor[1].set_color(BLUE)
        descriptor.next_to(sphere_words, DOWN)
        dot = Dot(descriptor[1].get_top())
        dot.set_fill(WHITE, opacity = 0.75)

        self.play(
            Write(sphere_words),
            ShowCreation(
                arrow,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            run_time = 3,
        )
        self.wait()
        self.play(Write(descriptor, run_time = 2))
        self.wait()
        self.play(
            dot.move_to, equation.get_left(),
            dot.set_fill, None, 0,
            path_arc = -np.pi/12
        )
        self.wait(2)

        self.sphere_words = sphere_words
        self.sphere_arrow = arrow
        self.descriptor = descriptor

    def talk_through_animation(self):
        sphere = self.spheres[-1]

        morty = self.pi_creature
        alt_dims = VGroup(*list(map(TexText, ["5D", "6D", "7D"])))
        alt_dims.next_to(morty.eyes, UP, SMALL_BUFF)
        alt_dim = alt_dims[0]

        self.play(FadeIn(morty))
        self.play(morty.change, "raise_right_hand", sphere)
        self.wait(3)
        self.play(morty.change, "confused", sphere)
        self.wait(3)
        self.play(
            morty.change, "erm", alt_dims,
            FadeIn(alt_dim)
        )
        for new_alt_dim in alt_dims[1:]:
            self.wait()
            self.play(Transform(alt_dim, new_alt_dim))
        self.wait()
        self.play(morty.change, "concerned_musician")
        self.play(FadeOut(alt_dim))
        self.wait()
        self.play(morty.change, "angry", sphere)
        self.wait(2)

    def transition_to_next_scene(self):
        equation = self.equations[-1]
        self.equations.remove(equation)
        tup = self.descriptor[1]
        self.descriptor.remove(tup)

        equation.generate_target()
        equation.target.center().to_edge(UP)
        tup.generate_target()
        tup.target.next_to(equation.target, DOWN)
        tup.target.set_color(WHITE)

        self.play(LaggedStartMap(FadeOut, VGroup(*[
            self.equations, self.spheres,
            self.sphere_words, self.sphere_arrow,
            self.descriptor,
            self.pi_creature
        ])))
        self.play(*list(map(MoveToTarget, [equation, tup])))
        self.wait()

    ###

    def create_pi_creature(self):
        return Mortimer().scale(0.8).to_corner(DOWN+RIGHT)


class Introduce4DSliders(SliderScene):
    CONFIG = {
        "slider_config" : {
            "include_real_estate_ticks" : False,
            "big_tick_numbers" : [-1, 0, 1],
            "tick_frequency" : 0.25,
            "tick_size" : 0.05,
            "dial_color" : YELLOW,
        },
        "slider_spacing" : LARGE_BUFF,
    }
    def construct(self):
        self.match_last_scene()
        self.introduce_sliders()
        self.ask_about_constraint()

    def match_last_scene(self):
        self.start_vect = DismissProjection.CONFIG["example_vect"]
        self.remove(self.sliders)

        equation = OldTex("x^2 + y^2 + z^2 + w^2 = 1")
        x, y, z, w = self.start_vect
        tup = OldTex(
            "(", "%.02f \\,"%x, 
            ",", "%.02f \\,"%y, 
            ",", "%.02f \\,"%z, 
            ",", "%.02f \\,"%w, ")"
        )
        equation.center().to_edge(UP)
        equation.set_color(BLUE)
        tup.next_to(equation, DOWN)

        self.sliders.next_to(tup, DOWN)
        self.sliders.shift(0.8*LEFT)

        self.add(equation, tup)
        self.wait()
        self.equation = equation
        self.tup = tup

    def introduce_sliders(self):
        self.set_to_vector(self.start_vect)

        numbers = self.tup.get_parts_by_tex(".")
        self.tup.remove(*numbers)
        dials = VGroup(*[slider.dial for slider in self.sliders])
        dial_copies = dials.copy()
        dials.set_fill(opacity = 0)

        self.play(LaggedStartMap(FadeIn, self.sliders))
        self.play(*[
            Transform(
                num, dial,
                run_time = 3,
                rate_func = squish_rate_func(smooth, a, a+0.5),
                remover = True
            )
            for num, dial, a in zip(
                numbers, dial_copies, 
                np.linspace(0, 0.5, len(numbers))
            )
        ])
        dials.set_fill(opacity = 1)
        self.initialize_ambiant_slider_movement()
        self.play(FadeOut(self.tup))
        self.wait(10)

    def ask_about_constraint(self):
        equation = self.equation
        rect = SurroundingRectangle(equation, color = GREEN)
        randy = Randolph().scale(0.5)
        randy.next_to(rect, DOWN+LEFT, LARGE_BUFF)

        self.play(ShowCreation(rect))
        self.play(FadeIn(randy))
        self.play(randy.change, "pondering", rect)
        self.wait()
        for mob in self.sliders, rect:
            self.play(randy.look_at, mob)
            self.play(Blink(randy))
            self.wait()
        self.wait()


class TwoDimensionalCase(Introduce4DSliders):
    CONFIG = {
        "n_sliders" : 2,
    }
    def setup(self):
        SliderScene.setup(self)
        self.sliders.shift(RIGHT)
        for number in self.sliders[0].numbers:
            # CHANGE: GL writes negative numbers with an en dash: normalise the sign before int()
            value = int(number.get_tex().replace("–", "-").replace("−", "-"))
            number.move_to(center_of_mass([
                slider.number_to_point(value)
                for slider in self.sliders
            ]))

        plane = NumberPlane(
            x_radius = 2.5,
            y_radius = 2.5,
        )
        plane.fade(0.25)
        plane.axes.set_color(GREY)
        plane.add_coordinates()
        plane.to_edge(LEFT)
        origin = plane.coords_to_point(0, 0)

        circle = Circle(radius = 1, color = WHITE)
        circle.move_to(plane.coords_to_point(*self.center_point))

        dot = Dot(color = YELLOW)
        dot.move_to(plane.coords_to_point(1, 0))

        equation = OldTex("x^2 + y^2 = 1")
        equation.to_corner(UP + RIGHT)

        self.add(plane, circle, dot, equation)
        self.add_foreground_mobjects(dot)

        self.plane = plane
        self.circle = circle
        self.dot = dot
        self.equation = equation

    def construct(self):
        self.let_values_wander()
        self.introduce_real_estate()
        self.let_values_wander(6)
        self.comment_on_cheap_vs_expensive_real_estate()
        self.nudge_x_from_one_example()
        self.note_circle_steepness()
        self.add_tick_marks()
        self.write_distance_squared()

    def let_values_wander(self, total_time = 5):
        self.initialize_ambiant_slider_movement()
        self.wait(total_time - 1)
        self.wind_down_ambient_movement()

    def introduce_real_estate(self):
        x_squared_mob = VGroup(*self.equation[:2])
        y_squared_mob = VGroup(*self.equation[3:5])
        x_rect = SurroundingRectangle(x_squared_mob)
        y_rect = SurroundingRectangle(y_squared_mob)
        rects = VGroup(x_rect, y_rect)

        decimals = VGroup(*[
            DecimalNumber(num**2) 
            for num in self.get_vector()
        ])
        decimals.arrange(RIGHT, buff = LARGE_BUFF)
        decimals.next_to(rects, DOWN, LARGE_BUFF)

        real_estate_word = OldTexText("``Real estate''")
        real_estate_word.next_to(decimals, DOWN, MED_LARGE_BUFF)
        self.play(FadeIn(real_estate_word))

        colors = GREEN, RED
        arrows = VGroup()
        for rect, decimal, color in zip(rects, decimals, colors):
            rect.set_color(color)
            decimal.set_color(color)
            arrow = Arrow(
                rect.get_bottom()+SMALL_BUFF*UP, decimal.get_top(),
                tip_length = 0.2,
            )
            arrow.set_color(color)
            arrows.add(arrow)

            self.play(ShowCreation(rect))
            self.play(
                ShowCreation(arrow),
                Write(decimal)
            )
            self.wait()

        sliders = self.sliders
        def create_update_func(i):
            return lambda alpha : sliders[i].get_real_estate()

        self.add_foreground_mobjects(decimals)
        self.decimals = decimals
        self.decimal_update_anims = [
            ChangingDecimal(decimal, create_update_func(i))
            for i, decimal in enumerate(decimals)
        ]
        self.real_estate_word = real_estate_word

    def comment_on_cheap_vs_expensive_real_estate(self):
        blue_rects = VGroup()
        red_rects = VGroup()
        for slider in self.sliders:
            for x1, x2 in (-0.5, 0.5), (0.75, 1.0), (-1.0, -0.75):
                p1, p2 = list(map(slider.number_to_point, [x1, x2]))
                rect = Rectangle(
                    stroke_width = 0,
                    fill_opacity = 0.5,
                    width = 0.25,
                    height = (p2-p1)[1]
                )
                rect.move_to((p1+p2)/2)
                if np.mean([x1, x2]) == 0:
                    rect.set_color(BLUE)
                    blue_rects.add(rect)
                else:
                    rect.set_color(RED)
                    red_rects.add(rect)

        blue_rects.save_state()
        self.play(DrawBorderThenFill(blue_rects))
        self.wait()
        self.play(ReplacementTransform(blue_rects, red_rects))
        self.wait()
        self.play(FadeOut(red_rects))

        blue_rects.restore()
        self.real_estate_rects = VGroup(blue_rects, red_rects)

    def nudge_x_from_one_example(self):
        x_re = self.decimals[0]
        rect = SurroundingRectangle(x_re)

        self.reset_dials([1, 0])
        self.wait()
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.play(FocusOn(self.dot))
        self.wait()
        self.reset_dials([0.9, -np.sqrt(0.19)])

        x_brace, y_brace = [
            Brace(
                VGroup(slider.dial, Dot(slider.number_to_point(0))),
                vect
            )
            for slider, vect in zip(self.sliders, [LEFT, RIGHT])
        ]
        x_text = x_brace.get_tex("0.9")
        y_text = y_brace.get_tex("%.02f"%self.sliders[1].get_value())

        self.play(
            GrowFromCenter(x_brace),
            Write(x_text)
        )
        self.play(ReplacementTransform(
            VGroup(x_text.copy()), x_re
        ))
        self.wait(2)
        self.play(
            GrowFromCenter(y_brace),
            Write(y_text),
        )
        self.wait(2)
        self.play(FadeIn(self.real_estate_rects))
        self.reset_dials([1, 0], run_time = 1)
        self.reset_dials([0.9, -np.sqrt(0.19)], run_time = 2)
        self.play(FadeOut(self.real_estate_rects))
        self.play(*list(map(FadeOut, [x_brace, y_brace, x_text, y_text])))
        self.wait()

    def note_circle_steepness(self):
        line = Line(
            self.plane.coords_to_point(0.5, 1),
            self.plane.coords_to_point(1.5, -1),
        )
        rect = Rectangle(
            stroke_width = 0,
            fill_color = BLUE,
            fill_opacity = 0.5,
        )
        rect.replace(line, stretch = True)

        self.play(DrawBorderThenFill(rect, stroke_color = YELLOW))
        for x, u in (1, 1), (0.8, 1), (1, 1), (0.8, -1), (1, 1):
            self.reset_dials([x, u*np.sqrt(1 - x**2)])
        self.play(FadeOut(rect))

    def add_tick_marks(self):
        self.remove_foreground_mobjects(self.sliders)
        self.add(self.sliders)
        old_ticks = VGroup()
        all_ticks = VGroup()
        for slider in self.sliders:
            slider.tick_size = 0.1
            slider.add_real_estate_ticks()
            slider.remove(slider.get_tick_marks())
            all_ticks.add(*slider.real_estate_ticks)
            old_ticks.add(*slider.get_tick_marks()[:-3])

        self.play(
            FadeOut(old_ticks),
            ShowCreation(all_ticks, run_time = 3),
            Animation(VGroup(*[slider.dial for slider in self.sliders])),
        )
        self.add_foreground_mobjects(self.sliders)
        self.wait()
        for x in np.arange(0.95, 0.05, -0.05):
            self.reset_dials(
                [np.sqrt(x), np.sqrt(1-x)],
                run_time = 0.5
            )
            self.wait(0.5)
        self.initialize_ambiant_slider_movement()
        self.wait(10)

    def write_distance_squared(self):
        d_squared = OldTex("(\\text{Distance})^2")
        d_squared.next_to(self.real_estate_word, DOWN)
        d_squared.set_color(YELLOW)

        self.play(Write(d_squared))
        self.wait(3)

    #####

    def update_frame(self, *args, **kwargs):
        if hasattr(self, "dot"):
            x, y = self.get_vector()
            self.dot.move_to(self.plane.coords_to_point(x, y))
        if hasattr(self, "decimals"):
            for anim in self.decimal_update_anims:
                anim.update(0)
        SliderScene.update_frame(self, *args, **kwargs)


class TwoDimensionalCaseIntro(TwoDimensionalCase):
    def construct(self):
        self.initialize_ambiant_slider_movement()
        self.wait(10)
