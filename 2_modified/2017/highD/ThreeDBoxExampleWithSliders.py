# ==============================================================================
# Scene:      ThreeDBoxExampleWithSliders
# Source:     videos/_2017/highD.py (lines 2245-2423)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThreeDBoxExampleWithSliders.py ThreeDBoxExampleWithSliders -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
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


class ThreeDBoxExampleWithSliders(SliderScene):
    CONFIG = {
        "n_sliders" : 3,
        "slider_config" : {
            "x_min" : -2,
            "x_max" : 2,
            "unit_size" : 1.5,
        },
        "center_point" : np.ones(3),
    }
    def setup(self):
        SliderScene.setup(self)
        self.sliders.shift(2*RIGHT)

    def construct(self):
        self.initialize_ambiant_slider_movement()
        self.name_corner_sphere()
        self.point_out_closest_point()
        self.compare_to_halfway_point()
        self.reframe_as_inner_sphere_point()
        self.place_bound_on_inner_real_estate()
        self.comment_on_inner_sphere_smallness()

    def name_corner_sphere(self):
        sphere_name = OldTexText(
            """Sphere with radius 1\\\\
            centered at (1, 1, 1)"""
        )
        sphere_name.to_corner(UP+LEFT)
        arrow = Arrow(
            sphere_name, VGroup(*self.sliders[0].numbers[-2:]),
            color = BLUE
        )

        self.play(
            LaggedStartMap(FadeIn, sphere_name,),
            ShowCreation(arrow, rate_func = squish_rate_func(smooth, 0.7, 1)),
            run_time = 3
        )
        self.wait(5)

        self.sphere_name = sphere_name
        self.arrow = arrow

    def point_out_closest_point(self):
        target_x = 1-np.sqrt(1./3)
        target_vector = np.array(3*[target_x])
        re_words = OldTexText(
            "$x$, $y$ and $z$ each have \\\\",
            "$\\frac{1}{3}$", "units of real estate"
        )
        re_words.to_corner(UP+LEFT)
        re_line = DashedLine(*[
            self.sliders[i].number_to_point(target_x) + MED_SMALL_BUFF*vect
            for i, vect in [(0, LEFT), (2, RIGHT)]
        ])
        new_arrow = Arrow(
            re_words.get_corner(DOWN+RIGHT), re_line.get_left(),
            color = BLUE
        )

        self.wind_down_ambient_movement()
        self.play(*[
            ApplyMethod(slider.set_value, x)
            for x, slider in zip(target_vector, self.sliders)
        ])
        self.play(ShowCreation(re_line))
        self.play(
            FadeOut(self.sphere_name),
            Transform(self.arrow, new_arrow),
        )
        self.play(LaggedStartMap(FadeIn, re_words))
        self.wait(2)

        self.re_words = re_words
        self.re_line = re_line

    def compare_to_halfway_point(self):
        half_line = Line(*[
            self.sliders[i].number_to_point(0.5)+MED_SMALL_BUFF*vect
            for i, vect in [(0, LEFT), (2, RIGHT)]
        ])
        half_line.set_stroke(MAROON_B, 6)
        half_label = OldTex("0.5")
        half_label.scale(self.sliders[0].number_scale_val)
        half_label.next_to(half_line, LEFT, MED_SMALL_BUFF)
        half_label.set_color(half_line.get_color())

        curr_vector = self.get_vector()
        target_vector = 0.5*np.ones(3)
        ghost_dials = VGroup(*[
            slider.dial.copy().set_fill(WHITE, 0.5)
            for slider in self.sliders
        ])

        cross = Cross(self.re_words.get_parts_by_tex("frac"))
        new_re = OldTex("(0.5)^2 = 0.25")
        new_re.next_to(cross, DOWN, MED_SMALL_BUFF, LEFT)
        new_re.set_color(MAROON_B)

        self.play(
            FadeOut(self.arrow),
            Write(half_label, run_time = 1),
            ShowCreation(half_line)
        )
        self.wait()
        self.add(ghost_dials)
        self.play(*[
            ApplyMethod(slider.set_value, 0.5)
            for slider in self.sliders
        ])
        self.play(ShowCreation(cross))
        self.play(Write(new_re))
        self.wait(3)
        self.play(
            FadeOut(new_re),
            FadeOut(cross),
            *[
                ApplyMethod(slider.set_value, x)
                for x, slider in zip(curr_vector, self.sliders)
            ]
        )

    def reframe_as_inner_sphere_point(self):
        s = self.sliders[0]
        shift_vect = s.number_to_point(0)-s.number_to_point(1)
        curr_vector = self.get_vector()
        self.set_center_point(np.zeros(3))
        self.set_to_vector(curr_vector)
        self.total_real_estate = self.get_current_total_real_estate()

        all_re_ticks = VGroup(*[
            slider.real_estate_ticks
            for slider in self.sliders
        ])
        inner_sphere_words = OldTexText(
            "Also a point on \\\\", "the inner sphere"
        )
        inner_sphere_words.next_to(self.re_line, RIGHT)
        question = OldTexText("How much \\\\", "real estate?")
        question.next_to(self.re_line, RIGHT, MED_LARGE_BUFF)

        self.play(
            Animation(self.sliders),
            FadeOut(self.re_words),
            LaggedStartMap(
                ApplyMethod, all_re_ticks,
                lambda m : (m.shift, shift_vect)
            )
        )
        self.initialize_ambiant_slider_movement()
        self.play(Write(inner_sphere_words))
        self.wait(5)
        self.wind_down_ambient_movement(0)
        self.play(*[
            ApplyMethod(slider.set_value, x)
            for slider, x in zip(self.sliders, curr_vector)
        ])
        self.play(ReplacementTransform(
            inner_sphere_words, question
        ))
        self.wait(2)

        self.re_question = question

    def place_bound_on_inner_real_estate(self):
        bound = OldTex(
            "&< 3(0.5)^2 ",
            "= 0.75"
        )
        bound.next_to(self.re_question, DOWN)
        bound.to_edge(RIGHT)

        self.play(Write(bound))
        self.wait(2)

    def comment_on_inner_sphere_smallness(self):
        self.initialize_ambiant_slider_movement()
        self.wait(15)
