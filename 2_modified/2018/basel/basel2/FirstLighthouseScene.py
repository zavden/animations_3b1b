# ==============================================================================
# Scene:      FirstLighthouseScene
# Source:     videos/_2018/basel/basel2.py (lines 906-1140)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FirstLighthouseScene.py FirstLighthouseScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
# ==============================================================================

# CHANGE: import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


LIGHT_COLOR = YELLOW


INDICATOR_RADIUS = 0.7


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


OPACITY_FOR_UNIT_INTENSITY = 0.2


NUM_CONES = 7 # in first lighthouse scene


NUM_VISIBLE_CONES = 5 # ibidem


LIGHT_COLOR = YELLOW


DEGREES = TAU/360


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint, scale, cutoff: inverse_power_law(maxint,scale,cutoff,2)


class LightIndicator(Mobject):
    CONFIG = {
        "radius": 0.5,
        "reading_height" : 0.25,
        "intensity": 0,
        "opacity_for_unit_intensity": 1,
        "fill_color" : YELLOW,
        "precision": 3,
        "show_reading": True,
        "measurement_point": ORIGIN,
        "light_source": None
    }

    def init_points(self):
        self.background = Circle(color=BLACK, radius = self.radius)
        self.background.set_fill(opacity = 1.0)
        self.foreground = Circle(color=self.color, radius = self.radius)
        self.foreground.set_stroke(
            color=INDICATOR_STROKE_COLOR,
            width=INDICATOR_STROKE_WIDTH
        )
        self.foreground.set_fill(color = self.fill_color)

        self.add(self.background, self.foreground)
        self.reading = DecimalNumber(self.intensity,num_decimal_places = self.precision)
        self.reading.set_fill(color=INDICATOR_TEXT_COLOR)
        self.reading.set_height(self.reading_height)
        self.reading.move_to(self.get_center())
        if self.show_reading:
            self.add(self.reading)

    def set_intensity(self, new_int):
        self.intensity = new_int
        new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
        self.foreground.set_fill(opacity=new_opacity)
        ChangeDecimalToValue(self.reading, new_int).update(1)
        if new_int > 1.1:
            self.reading.set_fill(color = BLACK)
        else:
            self.reading.set_fill(color = WHITE)
        return self

    def get_measurement_point(self):
        if self.measurement_point is not None:
            return self.measurement_point
        else:
            return self.get_center()

    def measured_intensity(self):
        distance = get_norm(
            self.get_measurement_point() - 
            self.light_source.get_source_point()
        )
        intensity = self.light_source.opacity_function(distance) / self.opacity_for_unit_intensity
        return intensity

    def update_mobjects(self):
        if self.light_source == None:
            print("Indicator cannot update, reason: no light source found")
        self.set_intensity(self.measured_intensity())


class UpdateLightIndicator(AnimationGroup):

    def __init__(self, indicator, intensity, **kwargs):
        if not isinstance(indicator,LightIndicator):
            raise Exception("This transform applies only to LightIndicator")
        
        target_foreground = indicator.copy().set_intensity(intensity).foreground
        change_opacity = Transform(
            indicator.foreground, target_foreground
        )
        changing_decimal = ChangeDecimalToValue(indicator.reading, intensity)

        AnimationGroup.__init__(self, changing_decimal, change_opacity, **kwargs)
        self.mobject = indicator


class FirstLighthouseScene(PiCreatureScene):
    CONFIG = {
        "num_levels" : 100,
        "opacity_function" : inverse_quadratic(1,2,1),
    }
    def construct(self):
        self.remove(self.pi_creature)
        self.show_lighthouses_on_number_line()
        self.describe_brightness_of_each()
        self.ask_about_rearrangements()

    def show_lighthouses_on_number_line(self):
        number_line = self.number_line = NumberLine(
            x_min = 0,
            color = WHITE,
            number_at_center = 1.6,
            stroke_width = 1,
            big_tick_numbers = list(range(1,6)),
            numbers_to_show = list(range(1,6)),
            unit_size = 2,
            tick_frequency = 0.2,
            line_to_number_buff = LARGE_BUFF,
            label_direction = DOWN,
        )

        number_line.add_numbers()
        self.add(number_line)

        origin_point = number_line.number_to_point(0)

        morty = self.pi_creature
        morty.scale(0.75)
        morty.flip()
        right_pupil = morty.eyes[1]
        morty.next_to(origin_point, LEFT, buff = 0, submobject_to_align = right_pupil)


        light_sources = VGroup()
        for i in range(1,NUM_CONES+1):
            light_source = LightSource(
                opacity_function = self.opacity_function,
                num_levels = self.num_levels,
                radius = 12.0,
            )
            point = number_line.number_to_point(i)
            light_source.move_source_to(point)
            light_sources.add(light_source)

        lighthouses = self.lighthouses = VGroup(*[
            ls.lighthouse
            for ls in light_sources[:NUM_VISIBLE_CONES+1]
        ])

        morty.save_state()
        morty.scale(3)
        morty.fade(1)
        morty.center()
        self.play(morty.restore)
        self.play(
            morty.change, "pondering",
            LaggedStartMap(
                FadeIn, lighthouses,
                run_time = 1
            )
        )
        self.play(LaggedStartMap(
            SwitchOn, VGroup(*[
                ls.ambient_light
                for ls in light_sources
            ]),
            run_time = 5,
            lag_ratio = 0.1,
            rate_func = rush_into,
        ), Animation(lighthouses))
        self.wait()

        self.light_sources = light_sources

    def describe_brightness_of_each(self):
        number_line = self.number_line
        morty = self.pi_creature
        light_sources = self.light_sources
        lighthouses = self.lighthouses

        light_indicator = LightIndicator(
            radius = INDICATOR_RADIUS,
            opacity_for_unit_intensity = OPACITY_FOR_UNIT_INTENSITY,
            color = LIGHT_COLOR
        )
        light_indicator.reading.scale(0.8)
        light_indicator.set_intensity(0)
        intensities = np.cumsum(np.array([1./n**2 for n in range(1,NUM_CONES+1)]))
        opacities = intensities * light_indicator.opacity_for_unit_intensity

        bubble = ThoughtBubble(
            direction = RIGHT,
            width = 2.5, height = 3.5
        )
        bubble.pin_to(morty)
        bubble.add_content(light_indicator)

        euler_sum_above = OldTex(
            "1", "+", 
            "{1\over 4}", "+", 
            "{1\over 9}", "+", 
            "{1\over 16}", "+", 
            "{1\over 25}", "+", 
            "{1\over 36}"
        )
        euler_sum_terms = euler_sum_above[::2]
        plusses = euler_sum_above[1::2]

        for i, term in enumerate(euler_sum_above):
            #horizontal alignment with tick marks
            term.next_to(number_line.number_to_point(0.5*i+1), UP , buff = 2)
            # vertical alignment with light indicator
            old_y = term.get_center()[1]
            new_y = light_indicator.get_center()[1]
            term.shift([0,new_y - old_y,0])

        # show limit value in light indicator and an equals sign
        limit_reading = OldTex("{\pi^2 \over 6}")
        limit_reading.move_to(light_indicator.reading)

        equals_sign = OldTex("=")
        equals_sign.next_to(morty, UP)
        old_y = equals_sign.get_center()[1]
        new_y = euler_sum_above.get_center()[1]
        equals_sign.shift([0,new_y - old_y,0])

        #Triangle of light to morty's eye
        ls0 = light_sources[0]
        ls0.save_state()
        eye = morty.eyes[1]
        triangle = Polygon(
            number_line.number_to_point(1),
            eye.get_top(), eye.get_bottom(),
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 1,
        )
        triangle_anim = GrowFromPoint(
            triangle, triangle.get_right(), 
            point_color = YELLOW
        )

        # First lighthouse has apparent reading
        self.play(LaggedStartMap(FadeOut, light_sources[1:]))
        self.wait()
        self.play(
            triangle_anim,
            # Animation(eye)
        )
        for x in range(4):
            triangle_copy = triangle.copy()
            self.play(
                FadeOut(triangle.copy()),
                triangle_anim,
            )
        self.play(
            FadeOut(triangle),
            ShowCreation(bubble),
            FadeIn(light_indicator),
        )
        self.play(
            UpdateLightIndicator(light_indicator, 1),
            FadeIn(euler_sum_terms[0])
        )
        self.wait(2)

        # Second lighthouse is 1/4, third is 1/9, etc.
        for i in range(1, 5):
            self.play(
                ApplyMethod(
                    ls0.move_to, light_sources[i],
                    run_time = 3
                ),
                UpdateLightIndicator(light_indicator, 1./(i+1)**2, run_time = 3),
                FadeIn(
                    euler_sum_terms[i],
                    run_time = 3,
                    rate_func = squish_rate_func(smooth, 0.5, 1)
                ),
            )
            self.wait()
        self.play(
            ApplyMethod(ls0.restore),
            UpdateLightIndicator(light_indicator, 1)
        )

        #Switch them all on
        self.play(
            LaggedStartMap(FadeIn, lighthouses[1:]),
            morty.change, "hooray",
        )
        self.play(
            LaggedStartMap(
                SwitchOn, VGroup(*[
                    ls.ambient_light
                    for ls in light_sources[1:]
                ]),
                run_time = 5,
                rate_func = rush_into,
            ),
            Animation(lighthouses),
            Animation(euler_sum_above),
            Write(plusses),
            UpdateLightIndicator(light_indicator, np.pi**2/6, run_time = 5),
            morty.change, "happy",
        )
        self.wait()
        self.play(
            FadeOut(light_indicator.reading),
            FadeIn(limit_reading),
            morty.change, "confused",
        )
        self.play(Write(equals_sign))
        self.wait()

    def ask_about_rearrangements(self):
        light_sources = self.light_sources
        origin = self.number_line.number_to_point(0)
        morty = self.pi_creature

        self.play(
            LaggedStartMap(
                Rotate, light_sources,
                lambda m : (m, (2*random.random()-1)*90*DEGREES),
                about_point = origin, 
                rate_func = lambda t : wiggle(t, 4),
                run_time = 10,
                lag_ratio = 0.9,
            ), 
            morty.change, "pondering",
        )
