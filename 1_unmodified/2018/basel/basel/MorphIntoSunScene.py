# ==============================================================================
# Scene:      MorphIntoSunScene
# Source:     videos/_2018/basel/basel.py (lines 917-1008)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MorphIntoSunScene.py MorphIntoSunScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


NUM_LEVELS = 15


AMBIENT_FULL = 0.8


SPOTLIGHT_FULL = 0.8


SPOTLIGHT_SCALE = 1.0


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint,scale,cutoff: inverse_power_law(maxint,scale,cutoff,2)


class MorphIntoSunScene(PiCreatureScene):
    def construct(self):
        self.setup_elements()
        self.morph_lighthouse_into_sun()

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

        self.add(self.light_source.lighthouse,self.light_source.ambient_light)
        

        # Screen

        self.screen = Rectangle(
            width = 0.06,
            height = 2,
            mark_paths_closed = True,
            fill_color = WHITE,
            fill_opacity = 1.0,
            stroke_width = 0.0
        )

        self.screen.next_to(morty,LEFT)

        self.light_source.set_screen(self.screen)
        self.add(self.screen,self.light_source.shadow)
        
        self.add_foreground_mobject(self.light_source.shadow)
        self.add_foreground_mobject(morty)
        self.light_source.dim_ambient
        self.add(self.light_source.spotlight)
        self.screen_tracker = ScreenTracker(self.light_source)
        self.add(self.screen_tracker)

        self.wait()


    def morph_lighthouse_into_sun(self):

        sun_position = np.array([-100,0,0])




        # Why does none of this change the opacity function???

        self.sun = self.light_source.copy()

        self.sun.change_spotlight_opacity_function(lambda r: 0.1)
        # self.sun.spotlight.opacity_function = lambda r: 0.1
        # for submob in self.sun.spotlight.submobjects:
        #     submob.set_fill(opacity = 0.1)

        #self.sun.move_source_to(sun_position)
        #self.sun.set_radius(120)

        self.sun.spotlight.init_points()

        self.wait()

        self.play(
             Transform(self.light_source,self.sun)
        )

        self.wait()
