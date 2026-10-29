# ==============================================================================
# Scene:      SingleLighthouseScene
# Source:     videos/_2018/basel/basel.py (lines 749-911)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SingleLighthouseScene.py SingleLighthouseScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the helper lambda takes a dummy argument that the call omitted
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


ARC_TIP_LENGTH = 0.2


NUM_LEVELS = 15


AMBIENT_FULL = 0.8


AMBIENT_DIMMED = 0.5


SPOTLIGHT_FULL = 0.8


SPOTLIGHT_SCALE = 1.0


DEGREES = TAU/360


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint,scale,cutoff: inverse_power_law(maxint,scale,cutoff,2)


class AngleUpdater(ContinualAnimation):
    def __init__(self, angle_arc, spotlight, **kwargs):
        self.angle_arc = angle_arc

        self.spotlight = spotlight
        ContinualAnimation.__init__(self, self.angle_arc, **kwargs)

    def update_mobject(self, dt):
        new_arc = self.angle_arc.copy().set_bound_angles(
            start = self.spotlight.start_angle(),
            stop = self.spotlight.stop_angle()
        )
        new_arc.init_points()
        new_arc.move_arc_center_to(self.spotlight.get_source_point())
        self.angle_arc.set_points(new_arc.get_points())
        self.angle_arc.add_tip(tip_length = ARC_TIP_LENGTH,
            at_start = True, at_end = True)


class SingleLighthouseScene(PiCreatureScene):

    def construct(self):

        self.setup_elements()
        self.setup_angle() # spotlight and angle msmt change when screen rotates
        self.rotate_screen()
        #self.morph_lighthouse_into_sun()


    def setup_elements(self):

        self.remove(self.get_primary_pi_creature())

        SCREEN_SIZE = 3.0
        DISTANCE_FROM_LIGHTHOUSE = 10.0
        source_point = [-DISTANCE_FROM_LIGHTHOUSE/2,0,0]
        observer_point = [DISTANCE_FROM_LIGHTHOUSE/2,0,0]

        # Light source

        self.light_source = LightSource(
            opacity_function = inverse_quadratic(1,SPOTLIGHT_SCALE,1),
            num_levels = NUM_LEVELS,
            radius = 10,
            max_opacity_ambient = AMBIENT_FULL,
            max_opacity_spotlight = SPOTLIGHT_FULL,

        )

        self.light_source.move_source_to(source_point)


        # Pi Creature

        morty = self.get_primary_pi_creature()
        morty.scale(0.5)
        morty.move_to(observer_point)
        morty.shift(2*OUT)
        self.add_foreground_mobject(morty)

        self.add(self.light_source.lighthouse)

        self.play(
            SwitchOn(self.light_source.ambient_light)
        )

        # Screen

        self.screen = Rectangle(
            width = 0.06,
            height = 2,
            mark_paths_closed = True,
            fill_color = WHITE,
            fill_opacity = 1.0,
            stroke_width = 0.0
        )

        self.screen.rotate(-TAU/6)
        self.screen.next_to(morty,LEFT)

        self.light_source.set_screen(self.screen)

        # Animations

        self.play(FadeIn(self.screen))

        #self.light_source.set_max_opacity_spotlight(0.001)
        #self.play(SwitchOn(self.light_source.spotlight))


        self.wait()




        # just calling .dim_ambient via ApplyMethod does not work, why?
        dimmed_ambient_light = self.light_source.ambient_light.deepcopy()
        dimmed_ambient_light.dimming(AMBIENT_DIMMED)
        self.light_source.update_shadow()

        self.play(
            FadeIn(self.light_source.shadow),
        )
        self.add_foreground_mobject(self.light_source.shadow)
        self.add_foreground_mobject(morty)

        self.play(
            self.light_source.dim_ambient,
            #Transform(self.light_source.ambient_light,dimmed_ambient_light),
            #self.light_source.set_max_opacity_spotlight,1.0,
        )
        self.play(
            FadeIn(self.light_source.spotlight)
        )

        self.screen_tracker = ScreenTracker(self.light_source)
        self.add(self.screen_tracker)

        self.wait()




    def setup_angle(self):

        self.wait()

        
        pointing_screen_at_source = Rotate(self.screen,TAU/6)
        self.play(pointing_screen_at_source)

        # angle msmt (arc)

        arc_angle = self.light_source.spotlight.opening_angle()
        # draw arc arrows to show the opening angle
        self.angle_arc = Arc(radius = 5, start_angle = self.light_source.spotlight.start_angle(),
            angle = self.light_source.spotlight.opening_angle(), tip_length = ARC_TIP_LENGTH)
        #angle_arc.add_tip(at_start = True, at_end = True)
        self.angle_arc.move_arc_center_to(self.light_source.get_source_point())
        

        # angle msmt (decimal number)

        self.angle_indicator = DecimalNumber(arc_angle / DEGREES,
            num_decimal_places = 0,
            unit = "^\\circ",
            fill_opacity = 1.0,
            fill_color = WHITE)
        self.angle_indicator.next_to(self.angle_arc,RIGHT)

        angle_update_func = lambda x: self.light_source.spotlight.opening_angle() / DEGREES
        self.angle_indicator.add_updater(
            # CHANGE: the helper lambda takes a dummy argument that the call omitted
            lambda d: d.set_value(angle_update_func(0))
        )
        self.add(self.angle_indicator)

        ca2 = AngleUpdater(self.angle_arc, self.light_source.spotlight)
        self.add(ca2)

        self.play(
            ShowCreation(self.angle_arc),
            ShowCreation(self.angle_indicator)
        )

        self.wait()

    def rotate_screen(self):



        self.play(Rotate(self.light_source.spotlight.screen, TAU/8))
        self.play(Rotate(self.light_source.spotlight.screen, -TAU/4))

        self.play(Rotate(self.light_source.spotlight.screen, TAU/8))

        self.wait()

        self.play(Rotate(self.light_source.spotlight.screen, -TAU/4))

        self.wait()

        self.play(Rotate(self.light_source.spotlight.screen, TAU/4))
