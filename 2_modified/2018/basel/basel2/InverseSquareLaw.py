# ==============================================================================
# Scene:      InverseSquareLaw
# Source:     videos/_2018/basel/basel2.py (lines 1589-1882)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InverseSquareLaw.py InverseSquareLaw -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - import the light helpers (LightSource, SwitchOn, ...): the original manim_imports_ext exported them, ours does not
#   - np.linspace needs an int number of points (numpy 2)
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


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


DEGREES = TAU/360


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


class InverseSquareLaw(ThreeDScene):
    CONFIG = {
        "screen_height" : 1.0,
        "source_point" : 5*LEFT,
        "unit_distance" : 4,
        "num_levels" : 100,
    }
    def construct(self):
        self.move_screen_farther_away()
        self.morph_into_3d()

    def move_screen_farther_away(self):
        source_point = self.source_point
        unit_distance = self.unit_distance

        # screen
        screen = self.screen = Line(self.screen_height*UP, ORIGIN)
        screen.get_reference_point = screen.get_center
        screen.shift(
            source_point + unit_distance*RIGHT -\
            screen.get_reference_point()
        )
        
        # light source
        light_source = self.light_source = LightSource(
            # opacity_function = inverse_quadratic(1,5,1),
            opacity_function = lambda r : 1./(r+1),
            num_levels = self.num_levels,
            radius = 10,
            max_opacity = 0.2
        )
        light_source.set_max_opacity_spotlight(0.2)

        light_source.set_screen(screen)
        light_source.move_source_to(source_point)

        # abbreviations
        ambient_light = light_source.ambient_light
        spotlight = light_source.spotlight
        lighthouse = light_source.lighthouse
        shadow = light_source.shadow

        # Morty
        morty = self.morty = Mortimer().scale(0.3)
        morty.next_to(screen, RIGHT, buff = MED_LARGE_BUFF)

        #Screen tracker
        def update_spotlight(spotlight):
            spotlight.update_sectors()

        spotlight_update = Mobject.add_updater(spotlight, update_spotlight)
        shadow_update = Mobject.add_updater(
            shadow, lambda m : light_source.update_shadow()
        )

        # Light indicator
        light_indicator = self.light_indicator = LightIndicator(
            opacity_for_unit_intensity = 0.5,
        )
        def update_light_indicator(light_indicator):
            distance = get_norm(screen.get_reference_point() - source_point)
            light_indicator.set_intensity(1.0/(distance/unit_distance)**2)
            light_indicator.next_to(morty, UP, MED_LARGE_BUFF)
        light_indicator_update = Mobject.add_updater(
            light_indicator, update_light_indicator
        )
        light_indicator_update.update(0)

        continual_updates = self.continual_updates = [
            spotlight_update, light_indicator_update, shadow_update
        ]

        # Distance indicators

        one_arrow = DoubleArrow(ORIGIN, unit_distance*RIGHT, buff = 0)
        two_arrow = DoubleArrow(ORIGIN, 2*unit_distance*RIGHT, buff = 0)
        arrows = VGroup(one_arrow, two_arrow)
        arrows.set_color(WHITE)
        one_arrow.move_to(source_point + DOWN, LEFT)
        two_arrow.move_to(source_point + 1.75*DOWN, LEFT)
        one = Integer(1).next_to(one_arrow, UP, SMALL_BUFF)
        two = Integer(2).next_to(two_arrow, DOWN, SMALL_BUFF)
        arrow_group = VGroup(one_arrow, one, two_arrow, two)

        # Animations

        self.add_foreground_mobjects(lighthouse, screen, morty)
        self.add(shadow_update)

        self.play(
            SwitchOn(ambient_light),
            morty.change, "pondering"
        )
        self.play(
            SwitchOn(spotlight),
            FadeIn(light_indicator)
        )
        # self.remove(spotlight)
        self.add(*continual_updates)
        self.wait()
        for distance in -0.5, 0.5:
            self.shift_by_distance(distance)
            self.wait()
        self.add_foreground_mobjects(one_arrow, one)
        self.play(GrowFromCenter(one_arrow), Write(one))
        self.wait()
        self.add_foreground_mobjects(two_arrow, two)
        self.shift_by_distance(1,
            GrowFromPoint(two_arrow, two_arrow.get_left()),
            Write(two, rate_func = squish_rate_func(smooth, 0.5, 1))
        )
        self.wait()

        q_marks = OldTexText("???")
        q_marks.next_to(light_indicator, UP)
        self.play(
            Write(q_marks),
            morty.change, "confused", q_marks
        )
        self.play(Blink(morty))
        self.play(FadeOut(q_marks), morty.change, "pondering")
        self.wait()
        self.shift_by_distance(-1, arrow_group.shift, DOWN)

        self.set_variables_as_attrs(
            ambient_light, spotlight, shadow, lighthouse,
            morty, arrow_group,
            *continual_updates
        )

    def morph_into_3d(self):
        # axes = ThreeDAxes()
        old_screen = self.screen
        spotlight = self.spotlight
        source_point = self.source_point
        ambient_light = self.ambient_light
        unit_distance = self.unit_distance
        light_indicator = self.light_indicator
        morty = self.morty

        new_screen = Square(
            side_length = self.screen_height,
            stroke_color = WHITE,
            stroke_width = 1,
            fill_color = WHITE,
            fill_opacity = 0.5
        )
        new_screen.rotate(TAU/4, UP)
        new_screen.move_to(old_screen, IN)
        old_screen.fade(1)

        cone = ThreeDSpotlight(
            new_screen, ambient_light,
            source_point_func = lambda : source_point
        )
        cone_update_anim = ContinualThreeDLightConeUpdate(cone)


        self.remove(self.spotlight_update, self.light_indicator_update)
        self.add(
            ContinualAnimation(new_screen),
            cone_update_anim
        )
        self.remove(spotlight)
        self.move_camera(
            phi = 60*DEGREES,
            theta = -145*DEGREES,
            added_anims = [
                # ApplyMethod(
                #     old_screen.scale, 1.8, {"about_edge" : DOWN},
                #     run_time = 2,
                # ),
                ApplyFunction(
                    lambda m : m.fade(1).shift(1.5*DOWN),
                    light_indicator,
                    remover = True
                ),
                FadeOut(morty)
            ],
            run_time = 2,
        )
        self.wait()

        ## Create screen copies
        def get_screen_copy_group(distance):
            n = int(distance)**2
            copies = VGroup(*[new_screen.copy() for x in range(n)])
            copies.rotate(-TAU/4, axis = UP)
            copies.arrange_in_grid(buff = 0)
            copies.rotate(TAU/4, axis = UP)
            copies.move_to(source_point, IN)
            copies.shift(distance*RIGHT*unit_distance)
            return copies
        screen_copy_groups = list(map(get_screen_copy_group, list(range(1, 8))))
        def get_screen_copy_group_anim(n):
            group = screen_copy_groups[n]
            prev_group = screen_copy_groups[n-1]
            group.save_state()
            group.fade(1)
            group.replace(prev_group, dim_to_match = 1)
            return ApplyMethod(group.restore)

        # corner_directions = [UP+OUT, DOWN+OUT, DOWN+IN, UP+IN]
        # edge_directions = [
        #     UP, UP+OUT, OUT, DOWN+OUT, DOWN, DOWN+IN, IN, UP+IN, ORIGIN
        # ]

        # four_copies = VGroup(*[new_screen.copy() for x in range(4)])
        # nine_copies = VGroup(*[new_screen.copy() for x in range(9)])
        # def update_four_copies(four_copies):
        #     for mob, corner_direction in zip(four_copies, corner_directions):
        #         mob.move_to(new_screen, corner_direction)
        # four_copies_update_anim = UpdateFromFunc(four_copies, update_four_copies)
        # def update_nine_copies(nine_copies):
        #     for mob, corner_direction in zip(nine_copies, edge_directions):
        #         mob.move_to(new_screen, corner_direction)
        # nine_copies_update_anim = UpdateFromFunc(nine_copies, update_nine_copies)

        three_arrow = DoubleArrow(
            source_point + 4*DOWN,
            source_point + 4*DOWN + 3*unit_distance*RIGHT,
            buff = 0,
            color = WHITE
        )
        three = Integer(3)
        three.next_to(three_arrow, DOWN)

        new_screen.fade(1)
        # self.add(
        #     ContinualAnimation(screen_copy),
        #     ContinualAnimation(four_copies),
        # )

        self.add(ContinualAnimation(screen_copy_groups[0]))
        self.add(ContinualAnimation(screen_copy_groups[1]))
        self.play(
            new_screen.scale, 2, {"about_edge" : IN},
            new_screen.shift, unit_distance*RIGHT,
            get_screen_copy_group_anim(1),
            run_time = 2,
        )
        self.wait()
        self.move_camera(
            phi = 75*DEGREES,
            theta = -155*DEGREES,
            distance = 7,
            run_time = 10,
        )
        self.begin_ambient_camera_rotation(rate = -0.01)
        self.add(ContinualAnimation(screen_copy_groups[2]))
        self.play(
            new_screen.scale, 3./2, {"about_edge" : IN},
            new_screen.shift, unit_distance*RIGHT,
            get_screen_copy_group_anim(2),
            GrowFromPoint(three_arrow, three_arrow.get_left()),
            Write(three, rate_func = squish_rate_func(smooth, 0.5, 1)),
            run_time = 2,
        )
        self.begin_ambient_camera_rotation(rate = -0.01)
        self.play(LaggedStartMap(
            ApplyMethod, screen_copy_groups[2],
            lambda m : (m.set_color, RED),
            run_time = 5,
            rate_func = there_and_back,
        ))
        self.wait(2)
        self.move_camera(distance = 18)
        self.play(*[
            ApplyMethod(mob.fade, 1)
            for mob in screen_copy_groups[:2]
        ])
        last_group = screen_copy_groups[2]
        for n in range(4, len(screen_copy_groups)+1):
            group = screen_copy_groups[n-1]
            self.add(ContinualAnimation(group))
            self.play(
                new_screen.scale, float(n)/(n-1), {"about_edge" : IN},
                new_screen.shift, unit_distance*RIGHT,
                get_screen_copy_group_anim(n-1),
                last_group.fade, 1,
            )
            last_group = group
            self.wait()

    ###

    def shift_by_distance(self, distance, *added_anims):
        anims = [
            self.screen.shift, self.unit_distance*distance*RIGHT,
        ]
        if self.morty in self.mobjects:
            anims.append(MaintainPositionRelativeTo(self.morty, self.screen))
        anims += added_anims
        self.play(*anims, run_time = 2)
