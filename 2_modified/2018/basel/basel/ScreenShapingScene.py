# ==============================================================================
# Scene:      ScreenShapingScene
# Source:     videos/_2018/basel/basel.py (lines 1165-1608)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ScreenShapingScene.py ScreenShapingScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - numpy 2: `array != None` is elementwise (ambiguous truth value); use `is not None`
#   - Cairo Rectangle.width attribute + init_points() regeneration: the copy is simply stretched to twice its width (it is moved to the original center right after)
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


NUM_LEVELS = 15


LIGHT_COLOR = YELLOW


DEGREES = TAU/360


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


class ScreenShapingScene(ThreeDScene):


    # TODO: Morph from Earth Scene into this scene

    def construct(self):

        #self.force_skipping()
        self.setup_elements()
        self.deform_screen()
        self.create_brightness_rect()
        self.slant_screen()
        self.unslant_screen()
        self.left_shift_screen_while_showing_light_indicator()
        self.add_distance_arrow()
        self.right_shift_screen_while_showing_light_indicator_and_distance_arrow()
        self.left_shift_again()
        #self.revert_to_original_skipping_status()
        
        self.morph_into_3d()
        self.prove_inverse_square_law()


    def setup_elements(self):

        SCREEN_THICKNESS = 10

        self.screen_height = 1.0
        self.brightness_rect_height = 1.0

        # screen
        self.screen = Line([3,-self.screen_height/2,0],[3,self.screen_height/2,0],
            path_arc = 0, num_arc_anchors = 10)
        
        # light source
        self.light_source = LightSource(
            opacity_function = inverse_quadratic(1,5,1),
            num_levels = NUM_LEVELS,
            radius = 10,
            max_opacity = 0.2
            #screen = self.screen
        )
        self.light_source.set_max_opacity_spotlight(0.2)

        self.light_source.set_screen(self.screen)
        self.light_source.move_source_to([-5,0,0])

        # abbreviations
        self.ambient_light = self.light_source.ambient_light
        self.spotlight = self.light_source.spotlight
        self.lighthouse = self.light_source.lighthouse

        
        #self.add_foreground_mobject(self.light_source.shadow)

        # Morty
        self.morty = Mortimer().scale(0.3).next_to(self.screen, RIGHT, buff = 0.5)

        # Add everything to the scene
        self.add(self.lighthouse)
        
        self.wait()
        self.play(FadeIn(self.screen))
        self.wait()

        self.add_foreground_mobject(self.screen)
        self.add_foreground_mobject(self.morty)

        self.play(SwitchOn(self.ambient_light))

        self.play(
            SwitchOn(self.spotlight),
            self.light_source.dim_ambient
        )

        screen_tracker = ScreenTracker(self.light_source)
        self.add(screen_tracker)


        self.wait()



    def deform_screen(self):

        self.wait()

        self.play(ApplyMethod(self.screen.set_path_arc, 45 * DEGREES))
        self.play(ApplyMethod(self.screen.set_path_arc, -90 * DEGREES))
        self.play(ApplyMethod(self.screen.set_path_arc, 0))




    def create_brightness_rect(self):

        # in preparation for the slanting, create a rectangle that shows the brightness

        # a rect a zero width overlaying the screen
        # so we can morph it into the brightness rect above
        brightness_rect0 = Rectangle(width = 0,
            height = self.screen_height).move_to(self.screen.get_center())
        self.add_foreground_mobject(brightness_rect0)

        self.brightness_rect = Rectangle(width = self.brightness_rect_height,
            height = self.brightness_rect_height, fill_color = YELLOW, fill_opacity = 0.5)

        self.brightness_rect.next_to(self.screen, UP, buff = 1)

        self.play(
            ReplacementTransform(brightness_rect0,self.brightness_rect)
        )

        self.unslanted_screen = self.screen.deepcopy()
        self.unslanted_brightness_rect = self.brightness_rect.copy()
        # for unslanting the screen later


    def slant_screen(self):

        SLANTING_AMOUNT = 0.1

        lower_screen_point, upper_screen_point = self.screen.get_start_and_end()

        lower_slanted_screen_point = interpolate(
            lower_screen_point, self.spotlight.get_source_point(), SLANTING_AMOUNT
        )
        upper_slanted_screen_point = interpolate(
            upper_screen_point, self.spotlight.get_source_point(), -SLANTING_AMOUNT
        )

        self.slanted_brightness_rect = self.brightness_rect.copy()
        # CHANGE: Cairo Rectangle.width attribute + init_points() regeneration: the copy is simply stretched to twice its width (it is moved to the original center right after)
        self.slanted_brightness_rect.stretch(2, 0)
        self.slanted_brightness_rect.set_fill(opacity = 0.25)

        self.slanted_screen = Line(lower_slanted_screen_point,upper_slanted_screen_point,
            path_arc = 0, num_arc_anchors = 10)
        self.slanted_brightness_rect.move_to(self.brightness_rect.get_center())

        self.play(
             Transform(self.screen,self.slanted_screen),
             Transform(self.brightness_rect,self.slanted_brightness_rect),
        )



    def unslant_screen(self):

        self.wait()        
        self.play(
            Transform(self.screen,self.unslanted_screen),
            Transform(self.brightness_rect,self.unslanted_brightness_rect),
        )




    def left_shift_screen_while_showing_light_indicator(self):

        # Scene 5: constant screen size, changing opening angle

        OPACITY_FOR_UNIT_INTENSITY = 1

        # let's use an actual light indicator instead of just rects

        self.indicator_intensity = 0.25
        indicator_height = 1.25 * self.screen_height

        self.indicator = LightIndicator(radius = indicator_height/2,
            opacity_for_unit_intensity = OPACITY_FOR_UNIT_INTENSITY,
            color = LIGHT_COLOR,
            precision = 2)
        self.indicator.set_intensity(self.indicator_intensity)

        self.indicator.move_to(self.brightness_rect.get_center())

        self.play(
            FadeOut(self.brightness_rect),
            FadeIn(self.indicator)
        )

        # Here some digits of the indicator disappear...

        self.add_foreground_mobject(self.indicator.reading)


        self.unit_indicator_intensity = 1.0 # intensity at distance 1
                                            # (where we are about to move to)

        self.left_shift = (self.screen.get_center()[0] - self.spotlight.get_source_point()[0])/2

        self.play(
            self.screen.shift,[-self.left_shift,0,0],
            self.morty.shift,[-self.left_shift,0,0],
            self.indicator.shift,[-self.left_shift,0,0],
            self.indicator.set_intensity,self.unit_indicator_intensity,
        )
        


    def add_distance_arrow(self):

        # distance arrow (length 1)
        left_x = self.spotlight.get_source_point()[0]
        right_x = self.screen.get_center()[0]
        arrow_y = -2
        arrow1 = Arrow([left_x,arrow_y,0],[right_x,arrow_y,0])
        arrow2 = Arrow([right_x,arrow_y,0],[left_x,arrow_y,0])
        arrow1.set_fill(color = WHITE)
        arrow2.set_fill(color = WHITE)
        distance_decimal = Integer(1).next_to(arrow1,DOWN)
        self.arrow = VGroup(arrow1, arrow2,distance_decimal)
        self.add(self.arrow)


        # distance arrow (length 2)
        # will be morphed into
        self.distance_to_source = right_x - left_x
        new_right_x = left_x + 2 * self.distance_to_source
        new_arrow1 = Arrow([left_x,arrow_y,0],[new_right_x,arrow_y,0])
        new_arrow2 = Arrow([new_right_x,arrow_y,0],[left_x,arrow_y,0])
        new_arrow1.set_fill(color = WHITE)
        new_arrow2.set_fill(color = WHITE)
        new_distance_decimal = Integer(2).next_to(new_arrow1,DOWN)
        self.new_arrow = VGroup(new_arrow1, new_arrow2, new_distance_decimal)
        # don't add it yet


    def right_shift_screen_while_showing_light_indicator_and_distance_arrow(self):

        self.wait()

        self.play(
            ReplacementTransform(self.arrow,self.new_arrow),
            ApplyMethod(self.screen.shift,[self.distance_to_source,0,0]),
            ApplyMethod(self.indicator.shift,[self.left_shift,0,0]),
            
            ApplyMethod(self.indicator.set_intensity,self.indicator_intensity),
            # this should trigger ChangingDecimal, but it doesn't
            # maybe bc it's an anim within an anim?

            ApplyMethod(self.morty.shift,[self.distance_to_source,0,0]),
        )


    def left_shift_again(self):

        self.wait()

        self.play(
            ReplacementTransform(self.new_arrow,self.arrow),
            ApplyMethod(self.screen.shift,[-self.distance_to_source,0,0]),
            #ApplyMethod(self.indicator.shift,[-self.left_shift,0,0]),
            ApplyMethod(self.indicator.set_intensity,self.unit_indicator_intensity),
            ApplyMethod(self.morty.shift,[-self.distance_to_source,0,0]),
        )

    def morph_into_3d(self):


        self.play(FadeOut(self.morty))

        axes = ThreeDAxes()
        self.add(axes)

        phi0 = self.camera.get_phi() # default is 0 degs
        theta0 = self.camera.get_theta() # default is -90 degs
        distance0 = self.camera.get_distance()

        phi1 = 60 * DEGREES # angle from zenith (0 to 180)
        theta1 = -135 * DEGREES # azimuth (0 to 360)
        distance1 = distance0
        target_point = self.camera.get_spherical_coords(phi1, theta1, distance1)

        dphi = phi1 - phi0
        dtheta = theta1 - theta0

        camera_target_point = target_point # self.camera.get_spherical_coords(45 * DEGREES, -60 * DEGREES)
        projection_direction = self.camera.spherical_coords_to_point(phi1,theta1, 1)

        new_screen0 = Rectangle(height = self.screen_height,
            width = 0.1, stroke_color = RED, fill_color = RED, fill_opacity = 1)
        new_screen0.rotate(TAU/4,axis = DOWN)
        new_screen0.move_to(self.screen.get_center())
        self.add(new_screen0)
        self.remove(self.screen)
        self.light_source.set_screen(new_screen0)

        self.light_source.set_camera(self.camera)


        new_screen = Rectangle(height = self.screen_height,
            width = self.screen_height, stroke_color = RED, fill_color = RED, fill_opacity = 1)
        new_screen.rotate(TAU/4,axis = DOWN)
        new_screen.move_to(self.screen.get_center())

        self.add_foreground_mobject(self.ambient_light)
        self.add_foreground_mobject(self.spotlight)
        self.add_foreground_mobject(self.light_source.shadow)

        self.play(
             ApplyMethod(self.camera.rotation_mobject.move_to, camera_target_point),
             
        )
        self.remove(self.spotlight)

        self.play(Transform(new_screen0,new_screen))

        self.wait()

        self.unit_screen = new_screen0 # better name



    def prove_inverse_square_law(self):

        def orientate(mob):
            mob.move_to(self.unit_screen)
            mob.rotate(TAU/4, axis = LEFT)
            mob.rotate(TAU/4, axis = OUT)
            mob.rotate(TAU/2, axis = LEFT)
            return mob

        unit_screen_copy = self.unit_screen.copy()
        fourfold_screen = self.unit_screen.copy()
        fourfold_screen.scale(2,about_point = self.light_source.get_source_point())

        self.remove(self.spotlight)


        reading1 = OldTex("1")
        orientate(reading1)

        self.play(FadeIn(reading1))
        self.wait()
        self.play(FadeOut(reading1))
        

        self.play(
            Transform(self.unit_screen, fourfold_screen)
        )

        reading21 = OldTex("{1\over 4}").scale(0.8)
        orientate(reading21)
        reading22 = reading21.deepcopy()
        reading23 = reading21.deepcopy()
        reading24 = reading21.deepcopy()
        reading21.shift(0.5*OUT + 0.5*UP)
        reading22.shift(0.5*OUT + 0.5*DOWN)
        reading23.shift(0.5*IN + 0.5*UP)
        reading24.shift(0.5*IN + 0.5*DOWN)


        corners = fourfold_screen.get_anchors()
        midpoint1 = (corners[0] + corners[1])/2
        midpoint2 = (corners[1] + corners[2])/2
        midpoint3 = (corners[2] + corners[3])/2
        midpoint4 = (corners[3] + corners[0])/2
        midline1 = Line(midpoint1, midpoint3)
        midline2 = Line(midpoint2, midpoint4)

        self.play(
            ShowCreation(midline1),
            ShowCreation(midline2)
        )

        self.play(
            FadeIn(reading21),
            FadeIn(reading22),
            FadeIn(reading23),
            FadeIn(reading24),
        )

        self.wait()

        self.play(
            FadeOut(reading21),
            FadeOut(reading22),
            FadeOut(reading23),
            FadeOut(reading24),
            FadeOut(midline1),
            FadeOut(midline2)
        )

        ninefold_screen = unit_screen_copy.copy()
        ninefold_screen.scale(3,about_point = self.light_source.get_source_point())

        self.play(
            Transform(self.unit_screen, ninefold_screen)
        )

        reading31 = OldTex("{1\over 9}").scale(0.8)
        orientate(reading31)
        reading32 = reading31.deepcopy()
        reading33 = reading31.deepcopy()
        reading34 = reading31.deepcopy()
        reading35 = reading31.deepcopy()
        reading36 = reading31.deepcopy()
        reading37 = reading31.deepcopy()
        reading38 = reading31.deepcopy()
        reading39 = reading31.deepcopy()
        reading31.shift(IN + UP)
        reading32.shift(IN)
        reading33.shift(IN + DOWN)
        reading34.shift(UP)
        reading35.shift(ORIGIN)
        reading36.shift(DOWN)
        reading37.shift(OUT + UP)
        reading38.shift(OUT)
        reading39.shift(OUT + DOWN)

        corners = ninefold_screen.get_anchors()
        midpoint11 = (2*corners[0] + corners[1])/3
        midpoint12 = (corners[0] + 2*corners[1])/3
        midpoint21 = (2*corners[1] + corners[2])/3
        midpoint22 = (corners[1] + 2*corners[2])/3
        midpoint31 = (2*corners[2] + corners[3])/3
        midpoint32 = (corners[2] + 2*corners[3])/3
        midpoint41 = (2*corners[3] + corners[0])/3
        midpoint42 = (corners[3] + 2*corners[0])/3
        midline11 = Line(midpoint11, midpoint32)
        midline12 = Line(midpoint12, midpoint31)
        midline21 = Line(midpoint21, midpoint42)
        midline22 = Line(midpoint22, midpoint41)

        self.play(
            ShowCreation(midline11),
            ShowCreation(midline12),
            ShowCreation(midline21),
            ShowCreation(midline22),
        )

        self.play(
            FadeIn(reading31),
            FadeIn(reading32),
            FadeIn(reading33),
            FadeIn(reading34),
            FadeIn(reading35),
            FadeIn(reading36),
            FadeIn(reading37),
            FadeIn(reading38),
            FadeIn(reading39),
        )
