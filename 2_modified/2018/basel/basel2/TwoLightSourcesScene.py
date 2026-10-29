# ==============================================================================
# Scene:      TwoLightSourcesScene
# Source:     videos/_2018/basel/basel2.py (lines 2041-2328)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TwoLightSourcesScene.py TwoLightSourcesScene -w -m --fps 15
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


INDICATOR_STROKE_WIDTH = 1


INDICATOR_STROKE_COLOR = WHITE


INDICATOR_TEXT_COLOR = WHITE


AMBIENT_FULL = 0.5


LIGHT_COLOR = YELLOW


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


class ManipulateLightsourceSetups(PiCreatureScene):
    CONFIG = {
        "num_levels" : 100,
        "radius" : 10,
        "pi_creature_point" : 2*LEFT + 2*DOWN,
    }
    def construct(self):
        unit_distance = 3

        # Morty
        morty = self.pi_creature
        observer_point = morty.eyes[1].get_center()

        bubble = ThoughtBubble(height = 3, width = 4, direction = RIGHT)
        bubble.set_fill(BLACK, 1)
        bubble.pin_to(morty)

        # Indicator
        light_indicator = LightIndicator(
            opacity_for_unit_intensity = 0.5,
            fill_color = YELLOW,
            radius = 0.4,
            reading_height = 0.2,
        )
        light_indicator.move_to(bubble.get_bubble_center())
        def update_light_indicator(light_indicator):
            distance = get_norm(light_source.get_source_point()-observer_point)
            light_indicator.set_intensity((unit_distance/distance)**2)

        #Light source
        light_source = LightSource(
            opacity_function = inverse_quadratic(1,2,1),
            num_levels = self.num_levels,
            radius = self.radius,
            max_opacity_ambient = AMBIENT_FULL,
        )
        light_source.move_to(observer_point + unit_distance*RIGHT)

        #Light source copies
        light_source_copies = VGroup(*[light_source.copy() for x in range(2)])
        for lsc, vect in zip(light_source_copies, [RIGHT, UP]):
            lsc.move_to(observer_point + np.sqrt(2)*unit_distance*vect)

        self.add(light_source)
        self.add_foreground_mobjects(morty, bubble, light_indicator)
        self.add(Mobject.add_updater(light_indicator, update_light_indicator))
        self.play(
            ApplyMethod(
                light_source.shift, 0.66*unit_distance*LEFT,
                rate_func = wiggle,
                run_time = 5,
            ),
            morty.change, "erm",
        )
        self.play(
            UpdateFromAlphaFunc(
                light_source, 
                lambda ls, a : ls.move_to(
                    observer_point + rotate_vector(
                        unit_distance*RIGHT, (1+1./8)*a*TAU
                    )
                ),
                run_time = 6,
                rate_func = bezier([0, 0, 1, 1])
            ),
            morty.change, "pondering",
            UpdateFromFunc(morty, lambda m : m.look_at(light_source))
        )
        self.wait()

        plus = OldTex("+")
        point = light_indicator.get_center()
        plus.move_to(point)
        light_indicator_copy = light_indicator.copy()
        self.add_foreground_mobjects(plus, light_indicator_copy)
        self.play(
            ReplacementTransform(
                light_source, light_source_copies[0]
            ),
            ReplacementTransform(
                light_source.copy().fade(1), 
                light_source_copies[1]
            ),
            FadeIn(plus),
            UpdateFromFunc(
                light_indicator_copy,
                lambda li : update_light_indicator(li),
            ),
            UpdateFromAlphaFunc(
                light_indicator, lambda m, a : m.move_to(
                    point + a*0.75*RIGHT,
                )
            ),
            UpdateFromAlphaFunc(
                light_indicator_copy, lambda m, a : m.move_to(
                    point + a*0.75*LEFT,
                )
            ),
            run_time = 2
        )
        self.play(morty.change, "hooray")
        self.wait(2)

    ##

    def create_pi_creature(self):
        morty = Mortimer()
        morty.flip()
        morty.scale(0.5)
        morty.move_to(self.pi_creature_point)
        return morty


class TwoLightSourcesScene(ManipulateLightsourceSetups):
    CONFIG = {
        "num_levels" : 200,
        "radius" : 15,
        "a" : 9,
        "b" : 5,
        "origin_point" : 5*LEFT + 2.5*DOWN
    }
    def construct(self):
        MAX_OPACITY = 0.4
        INDICATOR_RADIUS = 0.6
        OPACITY_FOR_UNIT_INTENSITY = 0.5
        origin_point = self.origin_point

        #Morty
        morty = self.pi_creature
        morty.change("hooray") # From last scen
        morty.generate_target()
        morty.target.change("plain")
        morty.target.scale(0.6)
        morty.target.next_to(
            origin_point, LEFT, buff = 0, 
            submobject_to_align = morty.target.eyes[1]
        )

        #Axes
        axes = Axes(
            x_min = -1, x_max = 10.5,
            y_min = -1, y_max = 6.5,
        )
        axes.shift(origin_point)

        #Important reference points
        A = axes.coords_to_point(self.a, 0)
        B = axes.coords_to_point(0, self.b)
        C = axes.coords_to_point(0, 0)
        xA = A[0]
        yA = A[1]
        xB = B[0]
        yB = B[1]
        xC = C[0]
        yC = C[1]
        # find the coords of the altitude point H
        # as the solution of a certain LSE
        prelim_matrix = np.array([
            [yA - yB, xB - xA], 
            [xA - xB, yA - yB]
        ]) # sic
        prelim_vector = np.array(
            [xB * yA - xA * yB, xC * (xA - xB) + yC * (yA - yB)]
        )
        H2 = np.linalg.solve(prelim_matrix, prelim_vector)
        H = np.append(H2, 0.)

        #Lightsources
        lsA = LightSource(
            radius = self.radius, 
            num_levels = self.num_levels,
            opacity_function = inverse_power_law(2, 1, 1, 1.5),
        )
        lsB = lsA.deepcopy()
        lsA.move_source_to(A)
        lsB.move_source_to(B)
        lsC = lsA.deepcopy()
        lsC.move_source_to(H)

        #Lighthouse labels
        A_label = OldTexText("A")
        A_label.next_to(lsA.lighthouse, RIGHT)
        B_label = OldTexText("B")
        B_label.next_to(lsB.lighthouse, LEFT)

        #Identical lighthouse labels
        identical_lighthouses_words = OldTexText("All identical \\\\ lighthouses")
        identical_lighthouses_words.to_corner(UP+RIGHT)
        identical_lighthouses_words.shift(LEFT)
        identical_lighthouses_arrows = VGroup(*[
            Arrow(
                identical_lighthouses_words.get_corner(DOWN+LEFT),
                ls.get_source_point(), 
                buff = SMALL_BUFF,
                color = WHITE,
            )
            for ls in (lsA, lsB, lsC)
        ])

        #Lines
        line_a = Line(C, A)
        line_a.set_color(BLUE)
        line_b = Line(C, B)
        line_b.set_color(RED)
        line_c = Line(A, B)
        line_h = Line(H, C)
        line_h.set_color(GREEN)

        label_a = OldTex("a")
        label_a.match_color(line_a)
        label_a.next_to(line_a, DOWN, buff = SMALL_BUFF)
        label_b = OldTex("b")
        label_b.match_color(line_b)
        label_b.next_to(line_b, LEFT, buff = SMALL_BUFF)
        label_h = OldTex("h")
        label_h.match_color(line_h)
        label_h.next_to(line_h.get_center(), RIGHT, buff = SMALL_BUFF)

        perp_mark = VMobject().set_points_as_corners([
            RIGHT, RIGHT+DOWN, DOWN
        ])
        perp_mark.scale(0.25, about_point = ORIGIN)
        perp_mark.rotate(line_c.get_angle() + TAU/4, about_point = ORIGIN)
        perp_mark.shift(H)
        # perp_mark.set_color(BLACK)

        #Indicators
        indicator = LightIndicator(
            color = LIGHT_COLOR,
            radius = INDICATOR_RADIUS,
            opacity_for_unit_intensity = OPACITY_FOR_UNIT_INTENSITY,
            show_reading = True,
            precision = 2,
        )
        indicator.next_to(origin_point, UP+LEFT)
        def update_indicator(indicator):
            intensity = 0
            for ls in lsA, lsB, lsC:
                if ls in self.mobjects:
                    distance = get_norm(ls.get_source_point() - origin_point)
                    d_indensity = fdiv(
                        3./(distance**2),
                        indicator.opacity_for_unit_intensity
                    )
                    d_indensity *= ls.ambient_light.submobjects[1].get_fill_opacity()
                    intensity += d_indensity
            indicator.set_intensity(intensity)
        indicator_update_anim = Mobject.add_updater(indicator, update_indicator)

        new_indicator = indicator.copy()
        new_indicator.light_source = lsC
        new_indicator.measurement_point = C

        #Note sure what this is...
        distance1 = get_norm(origin_point - lsA.get_source_point())
        intensity = lsA.ambient_light.opacity_function(distance1) / indicator.opacity_for_unit_intensity
        distance2 = get_norm(origin_point - lsB.get_source_point())
        intensity += lsB.ambient_light.opacity_function(distance2) / indicator.opacity_for_unit_intensity

        # IPT Theorem
        theorem = OldTex(
            "{1 \over ", "a^2}", "+", 
            "{1 \over", "b^2}", "=", "{1 \over","h^2}"
        )
        theorem.set_color_by_tex_to_color_map({
            "a" : line_a.get_color(),
            "b" : line_b.get_color(),
            "h" : line_h.get_color(),
        })
        theorem_name = OldTexText("Inverse Pythagorean Theorem")
        theorem_name.to_corner(UP+RIGHT)
        theorem.next_to(theorem_name, DOWN, buff = MED_LARGE_BUFF)
        theorem_box = SurroundingRectangle(theorem, color = WHITE)

        #Transition from last_scene
        self.play(
            ShowCreation(axes, run_time = 2),
            MoveToTarget(morty),
            FadeIn(indicator),
        )

        #Move lsC around
        self.add(lsC)
        indicator_update_anim.update(0)
        intensity = indicator.reading.number
        self.play(
            SwitchOn(lsC.ambient_light),
            FadeIn(lsC.lighthouse),
            UpdateFromAlphaFunc(
                indicator, lambda i, a : i.set_intensity(a*intensity)
            )
        )
        self.add(indicator_update_anim)
        self.play(Animation(lsC), run_time = 0) #Why is this needed?
        for point in axes.coords_to_point(5, 2), H:
            self.play(
                lsC.move_source_to, point,
                path_arc = TAU/4,
                run_time = 1.5,
            )
        self.wait()

        # Draw line
        self.play(
            ShowCreation(line_h),
            morty.change, "pondering"
        )
        self.wait()
        self.play(
            ShowCreation(line_c),
            ShowCreation(perp_mark)
        )
        self.wait()
        self.add_foreground_mobjects(line_c, line_h)

        #Add alternate light_sources
        for ls in lsA, lsB:
            ls.save_state()
            ls.move_to(lsC)
            ls.fade(1)
            self.add(ls)
            self.play(
                ls.restore, 
                run_time = 2
            )
        self.wait()
        A_label.save_state()
        A_label.center().fade(1)
        self.play(A_label.restore)
        self.wait()
        self.play(ReplacementTransform(
            A_label.copy().fade(1), B_label
        ))
        self.wait(2)

        #Compare combined of laA + lsB with lsC
        rect = SurroundingRectangle(indicator, color = RED)
        self.play(
            FadeOut(lsA),
            FadeOut(lsB),
        )
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.play(FadeOut(lsC))
        self.add(lsA, lsB)
        self.play(
            FadeIn(lsA),
            FadeIn(lsB),
        )
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.wait(2)

        # All standard lighthouses
        self.add(lsC)
        self.play(FadeIn(lsC))
        self.play(
            Write(identical_lighthouses_words),
            LaggedStartMap(GrowArrow, identical_lighthouses_arrows)
        )
        self.wait()
        self.play(*list(map(FadeOut, [
            identical_lighthouses_words,
            identical_lighthouses_arrows,
        ])))

        #Show labels of lengths
        self.play(ShowCreation(line_a), Write(label_a))
        self.wait()
        self.play(ShowCreation(line_b), Write(label_b))
        self.wait()
        self.play(Write(label_h))
        self.wait()

        #Write IPT
        a_part = theorem[:2]
        b_part = theorem[2:5]
        h_part = theorem[5:]
        for part in a_part, b_part, h_part:
            part.save_state()
            part.scale(3)
            part.fade(1)
        a_part.move_to(lsA)
        b_part.move_to(lsB)
        h_part.move_to(lsC)

        self.play(*list(map(FadeOut, [lsA, lsB, lsC, indicator])))
        for ls, part in (lsA, a_part), (lsB, b_part), (lsC, h_part):
            self.add(ls)
            self.play(
                SwitchOn(ls.ambient_light, run_time = 2),
                FadeIn(ls.lighthouse),
                part.restore
            )
        self.wait()
        self.play(
            Write(theorem_name),
            ShowCreation(theorem_box)
        )
        self.play(morty.change, "confused")
        self.wait(2)
