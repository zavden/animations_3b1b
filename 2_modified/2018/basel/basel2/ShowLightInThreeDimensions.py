# ==============================================================================
# Scene:      ShowLightInThreeDimensions
# Source:     videos/_2018/basel/basel2.py (lines 1522-1578)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowLightInThreeDimensions.py ShowLightInThreeDimensions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
#   - np.linspace needs an int number of points (numpy 2)
#   - the helper lambda takes a dummy argument that the call omitted
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


ARC_TIP_LENGTH = 0.2


AMBIENT_FULL = 0.5


DEGREES = TAU/360


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint, scale, cutoff: inverse_power_law(maxint,scale,cutoff,2)


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
        self.angle_arc.add_tip(
            tip_length = ARC_TIP_LENGTH,
            at_start = True, at_end = True
        )


class ThreeDSpotlight(VGroup):
    CONFIG = { 
        "fill_color" : YELLOW,
    }
    def __init__(self, screen, ambient_light, source_point_func, **kwargs):
        self.screen = screen
        self.ambient_light = ambient_light
        self.source_point_func = source_point_func
        self.dr = ambient_light.radius/ambient_light.num_levels
        VGroup.__init__(self, **kwargs)

    def update(self):
        screen = self.screen
        source_point = self.source_point_func()
        dr = self.dr
        corners = screen.get_anchors()
        self.submobjects = [VGroup() for a in screen.get_anchors()]

        distance = get_norm(
            screen.get_center() - source_point
        )
        # CHANGE: np.linspace needs an int number of points (numpy 2)
        n_parts = int(np.ceil(distance/dr))
        alphas = np.linspace(0, 1, n_parts+1)
        for face, (c1, c2) in zip(self, adjacent_pairs(corners)):
            face.submobjects = []
            for a1, a2 in zip(alphas, alphas[1:]):
                face.add(Polygon(
                    interpolate(source_point, c1, a1),
                    interpolate(source_point, c1, a2),
                    interpolate(source_point, c2, a2),
                    interpolate(source_point, c2, a1),
                    fill_color = self.fill_color,
                    fill_opacity = self.ambient_light.opacity_function(a1*distance),
                    stroke_width = 0
                ))


class ContinualThreeDLightConeUpdate(ContinualAnimation):
    def update(self, dt):
        self.mobject.update()


class IntroduceScreen(Scene):
    CONFIG = {
        "num_levels" : 100,
        "radius" : 10,
        "num_rays" : 250,
        "min_ray_angle" : 0,
        "max_ray_angle" : TAU,
        "source_point" : 2.5*LEFT,
        "observer_point" : 3.5*RIGHT,
        "screen_height" : 2,
    }
    def construct(self):
        self.setup_elements()
        self.setup_angle() # spotlight and angle msmt change when screen rotates
        self.rotate_screen()
        # self.morph_lighthouse_into_sun()

    def setup_elements(self):
        SCREEN_SIZE = 3.0
        source_point = self.source_point
        observer_point = self.observer_point,

        # Light source
        light_source = self.light_source = self.get_light_source()

        # Screen

        screen = self.screen = Rectangle(
            width = 0.05,
            height = self.screen_height,
            mark_paths_closed = True,
            fill_color = WHITE,
            fill_opacity = 1.0,
            stroke_width = 0.0
        )

        screen.next_to(observer_point, LEFT)

        screen_label = OldTexText("Screen")
        screen_label.next_to(screen, UP+LEFT)
        screen_arrow = Arrow(
            screen_label.get_bottom(),
            screen.get_center(),
        )

        # Pi creature
        morty = Mortimer()
        morty.shift(screen.get_center() - morty.eyes.get_left())
        morty.look_at(source_point)

        # Camera
        camera = SVGMobject(file_name = "camera")
        camera.rotate(TAU/4)
        camera.set_height(1.5)
        camera.move_to(morty.eyes, LEFT)

        # Animations
        light_source.set_max_opacity_spotlight(0.001)
        screen_tracker = self.screen_tracker = ScreenTracker(light_source)

        self.add(light_source.lighthouse)
        self.play(SwitchOn(light_source.ambient_light))
        self.play(
            Write(screen_label),
            GrowArrow(screen_arrow),
            FadeIn(screen)
        )
        self.wait()
        self.play(*list(map(FadeOut, [screen_label, screen_arrow])))
        screen.save_state()
        self.play(
            FadeIn(morty),
            screen.match_height, morty.eyes,
            screen.next_to, morty.eyes, LEFT, SMALL_BUFF
        )
        self.play(Blink(morty))
        self.play(
            FadeOut(morty),
            FadeIn(camera),
            screen.scale, 2, {"about_edge" : UP},
        )
        self.wait()
        self.play(
            FadeOut(camera),
            screen.restore,
        )

        light_source.set_screen(screen)
        light_source.spotlight.opacity_function = lambda r : 0.2/(r+1)
        screen_tracker.update(0)

        ## Ask about proportion
        self.add_foreground_mobjects(light_source.shadow, screen)
        self.shoot_rays()

        ##
        self.play(SwitchOn(light_source.spotlight))

    def setup_angle(self):

        self.wait()

        # angle msmt (arc)
        arc_angle = self.light_source.spotlight.opening_angle()
        # draw arc arrows to show the opening angle
        self.angle_arc = Arc(
            radius = 3, 
            start_angle = self.light_source.spotlight.start_angle(),
            angle = self.light_source.spotlight.opening_angle(),
            tip_length = ARC_TIP_LENGTH
        )
        #angle_arc.add_tip(at_start = True, at_end = True)
        self.angle_arc.move_arc_center_to(self.light_source.get_source_point())
        

        # angle msmt (decimal number)

        self.angle_indicator = DecimalNumber(
            arc_angle / DEGREES,
            num_decimal_places = 0,
            unit = "^\\circ"
        )
        self.angle_indicator.next_to(self.angle_arc, RIGHT)

        angle_update_func = lambda x: self.light_source.spotlight.opening_angle() / DEGREES
        self.angle_indicator.add_updater(
            # CHANGE: the helper lambda takes a dummy argument that the call omitted
            lambda d: d.set_value(angle_update_func(0))
        )
        self.add(self.angle_indicator)

        arc_tracker = AngleUpdater(
            self.angle_arc,
            self.light_source.spotlight
        )
        self.add(arc_tracker)

        self.play(
            ShowCreation(self.angle_arc),
            ShowCreation(self.angle_indicator)
        )

        self.wait()

    def rotate_screen(self):
        self.add(
            Mobject.add_updater(
                self.light_source,
                lambda m : m.update()
            ),
        )
        self.add(
            Mobject.add_updater(
                self.angle_indicator,
                lambda m : m.set_stroke(width = 0).set_fill(opacity = 1)
            )
        )
        self.remove(self.light_source.ambient_light)
        def rotate_screen(angle):
            self.play(
                Rotate(self.light_source.spotlight.screen, angle),
                Animation(self.angle_arc),
                run_time = 2,
            )
        for angle in TAU/8, -TAU/4, TAU/8, -TAU/6:
            rotate_screen(angle)
            self.wait()
        self.shoot_rays()
        rotate_screen(TAU/6)

    ##

    def get_light_source(self):
        light_source = LightSource(
            opacity_function = inverse_quadratic(1,2,1),
            num_levels = self.num_levels,
            radius = self.radius,
            max_opacity_ambient = AMBIENT_FULL,
        )
        light_source.move_source_to(self.source_point)
        return light_source

    def shoot_rays(self, show_creation_kwargs = None):
        if show_creation_kwargs is None:
            show_creation_kwargs = {}
        source_point = self.source_point
        screen = self.screen

        # Rays 
        step_size = (self.max_ray_angle - self.min_ray_angle)/self.num_rays
        rays = VGroup(*[
            Line(ORIGIN, self.radius*rotate_vector(RIGHT, angle))
            for angle in np.arange(
                self.min_ray_angle,
                self.max_ray_angle,
                step_size
            )
        ])
        rays.shift(source_point)
        rays.set_stroke(YELLOW, 1)
        max_angle = np.max([
            angle_of_vector(point - source_point)
            for point in screen.get_points()
        ])
        min_angle = np.min([
            angle_of_vector(point - source_point)
            for point in screen.get_points()
        ])
        for ray in rays:
            if min_angle <= ray.get_angle() <= max_angle:
                ray.target_color = GREEN
            else:
                ray.target_color = RED

        self.play(*[
            ShowCreation(ray, run_time = 3, **show_creation_kwargs)
            for ray in rays
        ])
        self.play(*[
            ApplyMethod(ray.set_color, ray.target_color)
            for ray in rays
        ])
        self.wait()
        self.play(FadeOut(rays))


class ShowLightInThreeDimensions(IntroduceScreen, ThreeDScene):
    CONFIG = {
        "num_levels" : 200,
    }
    def construct(self):
        light_source = self.get_light_source()
        screens = VGroup(
            Square(),
            RegularPolygon(8),
            Circle().insert_n_curves(25),
        )
        for screen in screens:
            screen.set_height(self.screen_height)
        screens.rotate(TAU/4, UP)
        screens.next_to(self.observer_point, LEFT)
        screens.set_stroke(WHITE, 2)
        screens.set_fill(WHITE, 0.5)
        screen = screens[0]

        cone = ThreeDSpotlight(
            screen, light_source.ambient_light,
            light_source.get_source_point
        )
        cone_update_anim = ContinualThreeDLightConeUpdate(cone)

        self.add(light_source, screen, cone)
        self.add(cone_update_anim)
        self.move_camera(
            phi = 60*DEGREES,
            theta = -155*DEGREES,
            run_time = 3,
        )
        self.begin_ambient_camera_rotation()
        kwargs = {"run_time" : 2}
        self.play(screen.stretch, 0.5, 1, **kwargs)
        self.play(screen.stretch, 2, 2, **kwargs)
        self.play(Rotate(
            screen, TAU/4, 
            axis = UP+OUT, 
            rate_func = there_and_back, 
            run_time = 3,
        ))
        self.play(Transform(screen, screens[1], **kwargs))
        self.play(screen.stretch, 0.5, 2, **kwargs)
        self.play(Transform(screen, screens[2], **kwargs))
        self.wait(2)
        self.play(
            screen.stretch, 0.5, 1, 
            screen.stretch, 2, 2, 
            **kwargs
        )
        self.play(
            screen.stretch, 3, 1, 
            screen.stretch, 0.7, 2, 
            **kwargs
        )
        self.wait(2)
