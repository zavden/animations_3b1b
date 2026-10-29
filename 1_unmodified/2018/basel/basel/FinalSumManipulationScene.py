# ==============================================================================
# Scene:      FinalSumManipulationScene
# Source:     videos/_2018/basel/basel.py (lines 3930-4246)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalSumManipulationScene.py FinalSumManipulationScene -w -m --fps 15
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


LIGHT_COLOR = YELLOW


inverse_power_law = lambda maxint,scale,cutoff,exponent: \
    (lambda r: maxint * (cutoff/(r/scale+cutoff))**exponent)


inverse_quadratic = lambda maxint,scale,cutoff: inverse_power_law(maxint,scale,cutoff,2)


class FinalSumManipulationScene(PiCreatureScene):

    def construct(self):

        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8

        LIGHT_COLOR2 = RED
        LIGHT_COLOR3 = BLUE

        unit_length = 1.5
        vertical_spacing = 2.5 * DOWN
        switch_on_time = 0.2

        sum_vertical_spacing = 1.5

        randy = self.get_primary_pi_creature()
        randy.set_color(MAROON_D)
        randy.color = MAROON_D
        randy.scale(0.7).flip().to_edge(DOWN + LEFT)
        self.wait()

        ls_template = LightSource(
            radius = 1,
            num_levels = 10,
            max_opacity_ambient = 0.5,
            opacity_function = inverse_quadratic(1,0.75,1)
        )


        odd_range = np.arange(1,9,2)
        even_range = np.arange(2,16,2)
        full_range = np.arange(1,8,1)

        self.number_line1 = NumberLine(
            x_min = 0,
            x_max = 11,
            color = LAKE_STROKE_COLOR,
            number_at_center = 0,
            stroke_width = LAKE_STROKE_WIDTH,
            stroke_color = LAKE_STROKE_COLOR,
            #numbers_to_show = full_range,
            number_scale_val = 0.5,
            big_tick_numbers = [],
            unit_size = unit_length,
            tick_frequency = 1,
            line_to_number_buff = MED_SMALL_BUFF,
            include_tip = True,
            label_direction = UP,
        )

        self.number_line1.next_to(2.5 * UP + 3 * LEFT, RIGHT, buff = 0.3)
        self.number_line1.add_numbers()

        odd_lights = VMobject()
        for i in odd_range:
            pos = self.number_line1.number_to_point(i)
            ls = ls_template.copy()
            ls.move_source_to(pos)
            odd_lights.add(ls)

        self.play(
            ShowCreation(self.number_line1, run_time = 5),
        )
        self.wait()


        odd_terms = VMobject()
        for i in odd_range:
            if i == 1:
                term = OldTex("\phantom{+\,\,\,}{1\over " + str(i) + "^2}",
                    fill_color = LIGHT_COLOR, stroke_color = LIGHT_COLOR)
            else:
                term = OldTex("+\,\,\, {1\over " + str(i) + "^2}",
                    fill_color = LIGHT_COLOR, stroke_color = LIGHT_COLOR)

            term.next_to(self.number_line1.number_to_point(i), DOWN, buff = 1.5)
            odd_terms.add(term)


        for (ls, term) in zip(odd_lights.submobjects, odd_terms.submobjects):
            self.play(
                FadeIn(ls.lighthouse, run_time = switch_on_time),
                SwitchOn(ls.ambient_light, run_time = switch_on_time),
                Write(term, run_time = switch_on_time)
            )

        result1 = OldTex("{\pi^2\over 8} =", fill_color = LIGHT_COLOR,
            stroke_color = LIGHT_COLOR)
        result1.next_to(self.number_line1, LEFT, buff = 0.5)
        result1.shift(0.87 * vertical_spacing)
        self.play(Write(result1))




        self.number_line2 = self.number_line1.copy()
        self.number_line2.numbers_to_show = full_range
        self.number_line2.shift(2 * vertical_spacing)
        self.number_line2.add_numbers()

        full_lights = VMobject()

        for i in full_range:
            pos = self.number_line2.number_to_point(i)
            ls = ls_template.copy()
            ls.color = LIGHT_COLOR3
            ls.move_source_to(pos)
            full_lights.add(ls)

        self.play(
            ShowCreation(self.number_line2, run_time = 5),
        )
        self.wait()


        full_lighthouses = VMobject()
        full_ambient_lights = VMobject()
        for ls in full_lights:
            full_lighthouses.add(ls.lighthouse)
            full_ambient_lights.add(ls.ambient_light)

        self.play(
            LaggedStartMap(FadeIn, full_lighthouses, lag_ratio = 0.2, run_time = 3),
        )

        self.play(
            LaggedStartMap(SwitchOn, full_ambient_lights, lag_ratio = 0.2, run_time = 3)
        )

        # for ls in full_lights.submobjects:
        #     self.play(
        #         FadeIn(ls.lighthouse, run_time = 0.1),#5 * switch_on_time),
        #         SwitchOn(ls.ambient_light, run_time = 0.1)#5 * switch_on_time),
        #     )



        even_terms = VMobject()
        for i in even_range:
            term = OldTex("+\,\,\, {1\over " + str(i) + "^2}", fill_color = LIGHT_COLOR2, stroke_color = LIGHT_COLOR)
            term.next_to(self.number_line1.number_to_point(i), DOWN, buff = sum_vertical_spacing)
            even_terms.add(term)


        even_lights = VMobject()

        for i in even_range:
            pos = self.number_line1.number_to_point(i)
            ls = ls_template.copy()
            ls.color = LIGHT_COLOR2
            ls.move_source_to(pos)
            even_lights.add(ls)

        for (ls, term) in zip(even_lights.submobjects, even_terms.submobjects):
            self.play(
                SwitchOn(ls.ambient_light, run_time = switch_on_time),
                Write(term)
            )
        self.wait()



        # now morph the even lights into the full lights
        full_lights_copy = full_lights.copy()
        even_lights_copy = even_lights.copy()


        self.play(
            Transform(even_lights,full_lights, run_time = 2)
        )


        self.wait()

        for i in range(6):
            self.play(
                Transform(even_lights[i], even_lights_copy[i])
            )
            self.wait()

        # draw arrows
        P1 = self.number_line2.number_to_point(1)
        P2 = even_terms.submobjects[0].get_center()
        Q1 = interpolate(P1, P2, 0.2)
        Q2 = interpolate(P1, P2, 0.8)
        quarter_arrow = Arrow(Q1, Q2,
            color = LIGHT_COLOR2)
        quarter_label = OldTex("\\times {1\over 4}", fill_color = LIGHT_COLOR2, stroke_color = LIGHT_COLOR2)
        quarter_label.scale(0.7)
        quarter_label.next_to(quarter_arrow.get_center(), RIGHT)

        self.play(
            ShowCreation(quarter_arrow),
            Write(quarter_label),
        )
        self.wait()

        P3 = odd_terms.submobjects[0].get_center()
        R1 = interpolate(P1, P3, 0.2)
        R2 = interpolate(P1, P3, 0.8)
        three_quarters_arrow = Arrow(R1, R2,
            color = LIGHT_COLOR)
        three_quarters_label = OldTex("\\times {3\over 4}", fill_color = LIGHT_COLOR, stroke_color = LIGHT_COLOR)
        three_quarters_label.scale(0.7)
        three_quarters_label.next_to(three_quarters_arrow.get_center(), LEFT)

        self.play(
            ShowCreation(three_quarters_arrow),
            Write(three_quarters_label)
        )
        self.wait()

        four_thirds_arrow = Arrow(R2, R1, color = LIGHT_COLOR)
        four_thirds_label = OldTex("\\times {4\over 3}", fill_color = LIGHT_COLOR, stroke_color = LIGHT_COLOR)
        four_thirds_label.scale(0.7)
        four_thirds_label.next_to(four_thirds_arrow.get_center(), LEFT)


        self.play(
            FadeOut(quarter_label),
            FadeOut(quarter_arrow),
            FadeOut(even_lights),
            FadeOut(even_terms)

        )
        self.wait()

        self.play(
            ReplacementTransform(three_quarters_arrow, four_thirds_arrow),
            ReplacementTransform(three_quarters_label, four_thirds_label)
        )
        self.wait()

        full_terms = VMobject()
        for i in range(1,8): #full_range:
            if i == 1:
                term = OldTex("\phantom{+\,\,\,}{1\over " + str(i) + "^2}", fill_color = LIGHT_COLOR3, stroke_color = LIGHT_COLOR3)
            elif i == 7:
                term = OldTex("+\,\,\,\dots", fill_color = LIGHT_COLOR3, stroke_color = LIGHT_COLOR3)
            else:
                term = OldTex("+\,\,\, {1\over " + str(i) + "^2}", fill_color = LIGHT_COLOR3, stroke_color = LIGHT_COLOR3)

            term.move_to(self.number_line2.number_to_point(i))
            full_terms.add(term)

        #return

        self.play(
            FadeOut(self.number_line1),
            FadeOut(odd_lights),
            FadeOut(self.number_line2),
            FadeOut(full_lights),
            FadeIn(full_terms)
        )
        self.wait()

        v = (sum_vertical_spacing + 0.5) * UP
        self.play(
            odd_terms.shift, v,
            result1.shift, v,
            four_thirds_arrow.shift, v,
            four_thirds_label.shift, v,
            odd_terms.shift, v,
            full_terms.shift, v
        )

        arrow_copy = four_thirds_arrow.copy()
        label_copy = four_thirds_label.copy()
        arrow_copy.shift(2.5 * LEFT)
        label_copy.shift(2.5 * LEFT)

        self.play(
            FadeIn(arrow_copy),
            FadeIn(label_copy)
        )
        self.wait()

        final_result = OldTex("{\pi^2 \over 6}=", fill_color = LIGHT_COLOR3, stroke_color = LIGHT_COLOR3)
        final_result.next_to(arrow_copy, DOWN)

        self.play(
            Write(final_result),
            randy.change_mode,"hooray"
        )
        self.wait()

        equation = VMobject()
        equation.add(final_result)
        equation.add(full_terms)


        self.play(
            FadeOut(result1),
            FadeOut(odd_terms),
            FadeOut(arrow_copy),
            FadeOut(label_copy),
            FadeOut(four_thirds_arrow),
            FadeOut(four_thirds_label),
            full_terms.shift,LEFT,
        )
        self.wait()

        self.play(equation.shift, -equation.get_center()[1] * UP + UP + 1.5 * LEFT)

        result_box = Rectangle(width = 1.1 * equation.get_width(),
            height = 2 * equation.get_height(), color = LIGHT_COLOR3)
        result_box.move_to(equation)


        self.play(
            ShowCreation(result_box)
        )
        self.wait()
