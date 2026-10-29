# ==============================================================================
# Scene:      FirstLighthouseScene
# Source:     videos/_2018/basel/basel.py (lines 565-725)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FirstLighthouseScene.py FirstLighthouseScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
# ==============================================================================

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


INDICATOR_UPDATE_TIME = 0.2


FAST_INDICATOR_UPDATE_TIME = 0.1


OPACITY_FOR_UNIT_INTENSITY = 0.2


SWITCH_ON_RUN_TIME = 1.5


FAST_SWITCH_ON_RUN_TIME = 0.1


NUM_CONES = 7 # in first lighthouse scene


NUM_VISIBLE_CONES = 5 # ibidem


NUM_LEVELS = 15


AMBIENT_SCALE = 2.0


AMBIENT_RADIUS = 20.0


LIGHT_COLOR = YELLOW


INDICATOR_RADIUS = 0.6


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint,scale,cutoff: inverse_power_law(maxint,scale,cutoff,2)


class LightIndicator(VMobject):
    CONFIG = {
        "radius": 0.5,
        "intensity": 0,
        "opacity_for_unit_intensity": 1,
        "precision": 3,
        "show_reading": True,
        "measurement_point": ORIGIN,
        "light_source": None
    }

    def init_points(self):
        self.background = Circle(color=BLACK, radius = self.radius)
        self.background.set_fill(opacity=1.0)
        self.foreground = Circle(color=self.color, radius = self.radius)
        self.foreground.set_stroke(color=INDICATOR_STROKE_COLOR,width=INDICATOR_STROKE_WIDTH)

        self.add(self.background, self.foreground)
        self.reading = DecimalNumber(self.intensity,num_decimal_places = self.precision)
        self.reading.set_fill(color=INDICATOR_TEXT_COLOR)
        self.reading.move_to(self.get_center())
        if self.show_reading:
            self.add(self.reading)

    def set_intensity(self, new_int):
        self.intensity = new_int
        new_opacity = min(1, new_int * self.opacity_for_unit_intensity)
        self.foreground.set_fill(opacity=new_opacity)
        ChangeDecimalToValue(self.reading, new_int).update(1)
        return self

    def get_measurement_point(self):
        # CHANGE: numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
        if self.measurement_point is not None:
            return self.measurement_point
        else:
            return self.get_center()


    def measured_intensity(self):
        distance = get_norm(self.get_measurement_point() - 
            self.light_source.get_source_point())
        intensity = self.light_source.opacity_function(distance) / self.opacity_for_unit_intensity
        return intensity

    def update_mobjects(self):
        if self.light_source == None:
            print("Indicator cannot update, reason: no light source found")
        self.set_intensity(self.measured_intensity())


class FirstLighthouseScene(PiCreatureScene):

    def construct(self):
        self.remove(self.get_primary_pi_creature())
        self.show_lighthouses_on_number_line()



    def show_lighthouses_on_number_line(self):

        self.number_line = NumberLine(
            x_min = 0,
            color = WHITE,
            number_at_center = 1.6,
            stroke_width = 1,
            big_tick_numbers = list(range(1,5)),
            numbers_to_show = list(range(1,5)),
            unit_size = 2,
            tick_frequency = 0.2,
            line_to_number_buff = LARGE_BUFF,
            label_direction = UP,
        )

        self.number_line.label_direction = DOWN

        self.number_line_labels = self.number_line.get_number_mobjects()
        self.add(self.number_line,self.number_line_labels)
        self.wait()

        origin_point = self.number_line.number_to_point(0)

        self.default_pi_creature_class = Randolph
        randy = self.get_primary_pi_creature()

        randy.scale(0.5)
        randy.flip()
        right_pupil = randy.pupils[1]
        randy.next_to(origin_point, LEFT, buff = 0, submobject_to_align = right_pupil)



        light_indicator = LightIndicator(radius = INDICATOR_RADIUS,
            opacity_for_unit_intensity = OPACITY_FOR_UNIT_INTENSITY,
            color = LIGHT_COLOR)
        light_indicator.reading.scale(0.8)

        bubble = ThoughtBubble(direction = RIGHT,
                            width = 2.5, height = 3.5)
        bubble.next_to(randy,LEFT+UP)
        bubble.add_content(light_indicator)
        self.wait()
        self.play(
            randy.change, "wave_2",
            ShowCreation(bubble),
            FadeIn(light_indicator)
        )

        light_sources = []


        euler_sum_above = OldTex("1", "+", "{1\over 4}", 
            "+", "{1\over 9}", "+", "{1\over 16}", "+", "{1\over 25}", "+", "{1\over 36}")

        for (i,term) in zip(list(range(len(euler_sum_above))),euler_sum_above):
            #horizontal alignment with tick marks
            term.next_to(self.number_line.number_to_point(0.5*i+1),UP,buff = 2)
            # vertical alignment with light indicator
            old_y = term.get_center()[1]
            new_y = light_indicator.get_center()[1]
            term.shift([0,new_y - old_y,0])
            


        for i in range(1,NUM_CONES+1):
            light_source = LightSource(
                opacity_function = inverse_quadratic(1,AMBIENT_SCALE,1),
                num_levels = NUM_LEVELS,
                radius = AMBIENT_RADIUS,
            )
            point = self.number_line.number_to_point(i)
            light_source.move_source_to(point)
            light_sources.append(light_source)

        self.wait()
        for ls in light_sources:
            self.add_foreground_mobject(ls.lighthouse)

        light_indicator.set_intensity(0)

        intensities = np.cumsum(np.array([1./n**2 for n in range(1,NUM_CONES+1)]))
        opacities = intensities * light_indicator.opacity_for_unit_intensity

        self.remove_foreground_mobjects(light_indicator)


        # slowly switch on visible light cones and increment indicator
        for (i,light_source) in zip(list(range(NUM_VISIBLE_CONES)),light_sources[:NUM_VISIBLE_CONES]):
            indicator_start_time = 1.0 * (i+1) * SWITCH_ON_RUN_TIME/light_source.radius * self.number_line.unit_size
            indicator_stop_time = indicator_start_time + INDICATOR_UPDATE_TIME
            indicator_rate_func = squish_rate_func(
                smooth,indicator_start_time,indicator_stop_time)
            self.play(
                SwitchOn(light_source.ambient_light),
                FadeIn(euler_sum_above[2*i], run_time = SWITCH_ON_RUN_TIME,
                    rate_func = indicator_rate_func),
                FadeIn(euler_sum_above[2*i - 1], run_time = SWITCH_ON_RUN_TIME,
                    rate_func = indicator_rate_func),
                # this last line *technically* fades in the last term, but it is off-screen
                ChangeDecimalToValue(light_indicator.reading,intensities[i],
                    rate_func = indicator_rate_func, run_time = SWITCH_ON_RUN_TIME),
                ApplyMethod(light_indicator.foreground.set_fill,None,opacities[i],
                    rate_func = indicator_rate_func, run_time = SWITCH_ON_RUN_TIME)
            )

            if i == 0:
                self.wait()
                # move a copy out of the thought bubble for comparison
                light_indicator_copy = light_indicator.copy()
                old_y = light_indicator_copy.get_center()[1]
                new_y = self.number_line.get_center()[1]
                self.play(
                    light_indicator_copy.shift,[0, new_y - old_y,0]
                )

            self.wait()

        self.wait()

        # quickly switch on off-screen light cones and increment indicator
        for (i,light_source) in zip(list(range(NUM_VISIBLE_CONES,NUM_CONES)),light_sources[NUM_VISIBLE_CONES:NUM_CONES]):
            indicator_start_time = 0.5 * (i+1) * FAST_SWITCH_ON_RUN_TIME/light_source.radius * self.number_line.unit_size
            indicator_stop_time = indicator_start_time + FAST_INDICATOR_UPDATE_TIME
            indicator_rate_func = squish_rate_func(#smooth, 0.8, 0.9)
                smooth,indicator_start_time,indicator_stop_time)
            self.play(
                SwitchOn(light_source.ambient_light, run_time = FAST_SWITCH_ON_RUN_TIME),
                ChangeDecimalToValue(light_indicator.reading,intensities[i-1],
                    rate_func = indicator_rate_func, run_time = FAST_SWITCH_ON_RUN_TIME),
                ApplyMethod(light_indicator.foreground.set_fill,None,opacities[i-1])
            )


        # show limit value in light indicator and an equals sign
        limit_reading = OldTex("{\pi^2 \over 6}")
        limit_reading.move_to(light_indicator.reading)

        equals_sign = OldTex("=")
        equals_sign.next_to(randy, UP)
        old_y = equals_sign.get_center()[1]
        new_y = euler_sum_above.get_center()[1]
        equals_sign.shift([0,new_y - old_y,0])

        self.play(
            FadeOut(light_indicator.reading),
            FadeIn(limit_reading),
            FadeIn(equals_sign),
        )

            

        self.wait()
