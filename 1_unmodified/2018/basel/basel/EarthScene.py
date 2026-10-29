# ==============================================================================
# Scene:      EarthScene
# Source:     videos/_2018/basel/basel.py (lines 1028-1139)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EarthScene.py EarthScene -w -m --fps 15
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


DEGREES = TAU/360


class EarthScene(Scene):

    def construct(self):

        SCREEN_THICKNESS = 10

        self.screen_height = 2.0
        self.brightness_rect_height = 1.0

        # screen
        self.screen = VMobject(stroke_color = WHITE, stroke_width = SCREEN_THICKNESS)
        self.screen.set_points_as_corners([
            [0,-self.screen_height/2,0],
            [0,self.screen_height/2,0]
        ])

        # Earth

        earth_center_x = 2
        earth_center = [earth_center_x,0,0]
        earth_radius = 3
        earth = Circle(radius = earth_radius)
        earth.add(self.screen)
        earth.move_to(earth_center)
        #self.remove(self.screen_tracker)

        theta0 = 70 * DEGREES
        dtheta = 10 * DEGREES
        theta1 = theta0 + dtheta
        theta = (theta0 + theta1)/2

        self.add_foreground_mobject(self.screen)

        # background Earth
        background_earth = SVGMobject(
            file_name = "earth",
            width = 2 * earth_radius,
            fill_color = BLUE,
        )
        background_earth.move_to(earth_center)
        # Morty

        morty = Mortimer().scale(0.5).next_to(self.screen, RIGHT, buff = 1.5)
        self.add_foreground_mobject(morty)


        # Light source (far-away Sun)

        sun_position = [-100,0,0]

        self.sun = LightSource(
            opacity_function = lambda r : 0.5,
            max_opacity_ambient = 0,
            max_opacity_spotlight = 0.5,
            num_levels = NUM_LEVELS,
            radius = 150,
            screen = self.screen
        )

        self.sun.move_source_to(sun_position)


        # Add elements to scene

        self.add(self.sun,self.screen)
        self.bring_to_back(self.sun.shadow)
        screen_tracker = ScreenTracker(self.sun)

        self.add(screen_tracker)
        
        self.wait()

        self.play(
            FadeIn(earth),
            FadeIn(background_earth)
        )
        self.add_foreground_mobject(earth)
        self.add_foreground_mobject(self.screen)


        # move screen onto Earth
        screen_on_earth = self.screen.deepcopy()
        screen_on_earth.rotate(-theta)
        screen_on_earth.scale(0.3)
        screen_on_earth.move_to(np.array([
            earth_center_x - earth_radius * np.cos(theta),
            earth_radius * np.sin(theta),
            0]))

        polar_morty = morty.copy().scale(0.5).next_to(screen_on_earth,DOWN,buff = 0.5)
        polar_morty.set_color(BLUE_C)

        self.play(
            Transform(self.screen, screen_on_earth),
            Transform(morty,polar_morty)
        )

        self.wait()


        tropical_morty = polar_morty.copy()
        tropical_morty.move_to(np.array([0,0,0]))
        tropical_morty.set_color(RED)

        morty.target = tropical_morty

        # move screen to equator

        self.play(
            Rotate(earth, theta0 + dtheta/2,run_time = 3),
            MoveToTarget(morty, path_arc = 70*DEGREES, run_time = 3),
        )
