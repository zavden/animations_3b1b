# ==============================================================================
# Scene:      TwoLightSourcesScene
# Source:     videos/_2018/basel/basel.py (lines 1877-2052)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TwoLightSourcesScene.py TwoLightSourcesScene -w -m --fps 15
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


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


LIGHT_COLOR = YELLOW


A = np.array([5.,-3.,0.])


B = np.array([-5.,3.,0.])


C = np.array([-5.,-3.,0.])


xA = A[0]


yA = A[1]


xB = B[0]


yB = B[1]


xC = C[0]


yC = C[1]


# find the coords of the altitude point H
# as the solution of a certain LSE
prelim_matrix = np.array([[yA - yB, xB - xA], [xA - xB, yA - yB]]) # sic


prelim_vector = np.array([xB * yA - xA * yB, xC * (xA - xB) + yC * (yA - yB)])


H2 = np.linalg.solve(prelim_matrix,prelim_vector)


H = np.append(H2, 0.)


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


class ContinualLightIndicatorUpdate(ContinualAnimation):

    def update_mobject(self,dt):
        self.mobject.update_mobjects()


class TwoLightSourcesScene(PiCreatureScene):

    def construct(self):

        MAX_OPACITY = 0.4
        INDICATOR_RADIUS = 0.6
        OPACITY_FOR_UNIT_INTENSITY = 0.5

        morty = self.get_primary_pi_creature()
        morty.scale(0.3).flip()
        right_pupil = morty.pupils[1]
        morty.next_to(C, LEFT, buff = 0, submobject_to_align = right_pupil)

        horizontal = VMobject(stroke_width = 1)
        horizontal.set_points_as_corners([C,A])
        vertical = VMobject(stroke_width = 1)
        vertical.set_points_as_corners([C,B])

        self.play(
            ShowCreation(horizontal),
            ShowCreation(vertical)
        )

        indicator = LightIndicator(color = LIGHT_COLOR,
                radius = INDICATOR_RADIUS,
                opacity_for_unit_intensity = OPACITY_FOR_UNIT_INTENSITY,
                show_reading = True,
                precision = 2
        )

        indicator.next_to(morty,LEFT)

        self.play(
            Write(indicator)
        )


        ls1 = LightSource(radius = 20, num_levels = 50)
        ls2 = ls1.deepcopy()
        ls1.move_source_to(A)
        ls2.move_source_to(B)

        self.play(
            FadeIn(ls1.lighthouse),
            FadeIn(ls2.lighthouse),
            SwitchOn(ls1.ambient_light),
            SwitchOn(ls2.ambient_light)
        )

        distance1 = get_norm(C - ls1.get_source_point())
        intensity = ls1.ambient_light.opacity_function(distance1) / indicator.opacity_for_unit_intensity
        distance2 = get_norm(C - ls2.get_source_point())
        intensity += ls2.ambient_light.opacity_function(distance2) / indicator.opacity_for_unit_intensity

        self.play(
            UpdateLightIndicator(indicator,intensity)
        )

        self.wait()

        ls3 = ls1.deepcopy()
        ls3.move_to(np.array([6,3.5,0]))

        new_indicator = indicator.copy()
        new_indicator.light_source = ls3
        new_indicator.measurement_point = C
        self.add(new_indicator)
        self.play(
            indicator.shift, 2 * UP
        )



        #intensity = intensity_for_light_source(ls3)


        self.play(
            SwitchOff(ls1.ambient_light),
            #FadeOut(ls1.lighthouse),
            SwitchOff(ls2.ambient_light),
            #FadeOut(ls2.lighthouse),
            UpdateLightIndicator(new_indicator,0.0)
        )

        # create a *continual* animation for the replacement source
        updater = ContinualLightIndicatorUpdate(new_indicator)
        self.add(updater)

        self.play(
            SwitchOn(ls3.ambient_light),
            FadeIn(ls3.lighthouse),
            
        )

        self.wait()

        # move the light source around
        # TODO: moving along a path arc

        location = np.array([-3,-2.,0.])
        self.play(ls3.move_source_to,location)
        location = np.array([6.,1.,0.])
        self.play(ls3.move_source_to,location)
        location = np.array([5.,2.,0.])
        self.play(ls3.move_source_to,location)
        closer_location = interpolate(location, C, 0.5)
        self.play(ls3.move_source_to,closer_location)
        self.play(ls3.move_source_to,location)

        # maybe move in a circle around C using a loop?



        self.play(ls3.move_source_to,H)



        # draw lines to complete the geometric picture
        # and label the lengths

        line_a = VMobject()
        line_a.set_points_as_corners([B,C])
        line_b = VMobject()
        line_b.set_points_as_corners([A,C])
        line_c = VMobject()
        line_c.set_points_as_corners([A,B])
        line_h = VMobject()
        line_h.set_points_as_corners([H,C])

        label_a = OldTex("a")
        label_a.next_to(line_a, LEFT, buff = 0.5)
        label_b = OldTex("b")
        label_b.next_to(line_b, DOWN, buff = 0.5)
        label_h = OldTex("h")
        label_h.next_to(line_h.get_center(), RIGHT, buff = 0.5)

        self.play(
            ShowCreation(line_a),
            Write(label_a)
        )

        self.play(
            ShowCreation(line_b),
            Write(label_b)
        )

        self.play(
            ShowCreation(line_c),
        )

        self.play(
            ShowCreation(line_h),
            Write(label_h)
        )


        # state the IPT
        theorem_location = np.array([3.,2.,0.])
        theorem = OldTex("{1\over a^2} + {1\over b^2} = {1\over h^2}")
        theorem_name = OldTexText("Inverse Pythagorean Theorem")
        buffer = 1.2
        theorem_box = Rectangle(width = buffer*theorem.get_width(),
            height = buffer*theorem.get_height())

        theorem.move_to(theorem_location)
        theorem_box.move_to(theorem_location)
        theorem_name.next_to(theorem_box,UP)

        self.play(
            Write(theorem),
        )

        self.play(
            ShowCreation(theorem_box),
            Write(theorem_name),
        )
