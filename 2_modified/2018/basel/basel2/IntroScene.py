# ==============================================================================
# Scene:      IntroScene
# Source:     videos/_2018/basel/basel2.py (lines 286-619)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroScene.py IntroScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL animations create target_mobject in begin(); the last rect is the target of the last anim
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


LIGHT_COLOR = YELLOW


LIGHT_COLOR = YELLOW


class IntroScene(PiCreatureScene):
    CONFIG = {
        "rect_height" : 0.075,
        "duration" : 1.0,
        "eq_spacing" : 3 * MED_LARGE_BUFF,
        "n_rects_to_show" : 30,
    }

    def construct(self):
        randy = self.get_primary_pi_creature()
        randy.scale(0.7).to_corner(DOWN+RIGHT)

        self.build_up_euler_sum()
        self.show_history()
        # self.other_pi_formulas()
        # self.refocus_on_euler_sum()

    def build_up_euler_sum(self):
        morty = self.pi_creature
        euler_sum = self.euler_sum = OldTex(
           "1", "+", 
           "{1 \\over 4}", "+",
           "{1 \\over 9}", "+",
           "{1 \\over 16}", "+",
           "{1 \\over 25}", "+",
           "\\cdots", "=",
            arg_separator = " \\, "
        )
        equals_sign = euler_sum.get_part_by_tex("=")
        plusses = euler_sum.get_parts_by_tex("+")
        term_mobjects = euler_sum.get_parts_by_tex("1")

        self.euler_sum.to_edge(UP)
        self.euler_sum.shift(2*LEFT)
       
        max_n = self.n_rects_to_show
        terms = [1./(n**2) for n in range(1, max_n + 1)]
        series_terms = list(np.cumsum(terms))
        series_terms.append(np.pi**2/6) ##Just force this up there

        partial_sum_decimal = self.partial_sum_decimal = DecimalNumber(
            series_terms[1],
            num_decimal_places = 2
        )
        partial_sum_decimal.next_to(equals_sign, RIGHT)

        ## Number line

        number_line = self.number_line = NumberLine(
            x_min = 0,
            color = WHITE,
            number_at_center = 1,
            stroke_width = 1,
            big_tick_numbers = [0,1,2,3],
            numbers_to_show = np.arange(0,5),
            unit_size = 5,
            tick_frequency = 0.2,
            line_to_number_buff = MED_LARGE_BUFF
        )
        number_line.add_numbers()
        number_line.to_edge(LEFT)
        number_line.shift(MED_LARGE_BUFF*UP)

        # create slabs for series terms

        lines = VGroup()
        rects = self.rects = VGroup()
        rect_labels = VGroup()
        slab_colors = it.cycle([YELLOW, BLUE])
        rect_anims = []
        rect_label_anims = []

        for i, t1, t2 in zip(it.count(1), [0]+series_terms, series_terms):
            color = next(slab_colors)
            line = Line(*list(map(number_line.number_to_point, [t1, t2])))
            rect = Rectangle(
                stroke_width = 0,
                fill_opacity = 1,
                fill_color = color
            )
            rect.match_width(line)
            rect.stretch_to_fit_height(self.rect_height)
            rect.move_to(line)

            if i <= 5:
                if i == 1:
                    rect_label = OldTex("1")
                else:
                    rect_label = OldTex("\\frac{1}{%d}"%(i**2))
                    rect_label.scale(0.75)
                max_width = 0.7*rect.get_width()
                if rect_label.get_width() > max_width:
                    rect_label.set_width(max_width)
                rect_label.next_to(rect, UP, buff = MED_LARGE_BUFF/(i+1))

                term_mobject = term_mobjects[i-1]
                rect_anim = GrowFromPoint(rect, term_mobject.get_center())
                rect_label_anim = ReplacementTransform(
                    term_mobject.copy(), rect_label
                )
            else:
                rect_label = VectorizedPoint()
                rect_anim = GrowFromPoint(rect, rect.get_left())
                rect_label_anim = FadeIn(rect_label)

            rects.add(rect)
            rect_labels.add(rect_label)
            rect_anims.append(rect_anim)
            rect_label_anims.append(rect_label_anim)
            lines.add(line)
        dots = OldTex("\\dots").scale(0.5)
        # CHANGE: GL animations create target_mobject in begin(); the last rect is the target of the last anim
        last_rect = rects[-1]
        dots.set_width(0.9*last_rect.get_width())
        dots.move_to(last_rect, UP+RIGHT)
        rects.submobjects[-1] = dots
        rect_anims[-1] = FadeIn(dots)

        self.add(number_line)
        self.play(FadeIn(euler_sum[0]))
        self.play(
            rect_anims[0],
            rect_label_anims[0]
        )
        for i in range(4):
            self.play(
                FadeIn(term_mobjects[i+1]),
                FadeIn(plusses[i]),
            )
            anims = [
                rect_anims[i+1],
                rect_label_anims[i+1],
            ]
            if i == 0:
                anims += [
                    FadeIn(equals_sign),
                    FadeIn(partial_sum_decimal)
                ]
            elif i <= 5:
                anims += [
                    ChangeDecimalToValue(
                        partial_sum_decimal,
                        series_terms[i+1], 
                        run_time = 1,
                        num_decimal_places = 6,
                        position_update_func = lambda m: m.next_to(equals_sign, RIGHT)
                    )
                ]
            self.play(*anims)

        for i in range(4, len(series_terms)-2):
            anims = [
                rect_anims[i+1],
                ChangeDecimalToValue(
                    partial_sum_decimal,
                    series_terms[i+1],
                    num_decimal_places = 6,
                ),
            ]
            if i == 5:
                anims += [
                    FadeIn(euler_sum[-3]), # +
                    FadeIn(euler_sum[-2]), # ...
                ]
            self.play(*anims, run_time = 2./i)

        brace = self.brace = Brace(partial_sum_decimal, DOWN)
        q_marks = self.q_marks = OldTexText("???")
        q_marks.next_to(brace, DOWN)
        q_marks.set_color(LIGHT_COLOR)

        self.play(
            GrowFromCenter(brace),
            Write(q_marks),
            ChangeDecimalToValue(
                partial_sum_decimal,
                series_terms[-1],
                num_decimal_places = 6,
            ),
            morty.change, "confused",
        )
        self.wait()

        self.number_line_group = VGroup(
            number_line, rects, rect_labels
        )

    def show_history(self):
        # Pietro Mengoli in 1644
        morty = self.pi_creature
        pietro = ImageMobject("Pietro_Mengoli")
        euler = ImageMobject("Euler")

        pietro_words = OldTexText("Challenge posed by \\\\ Pietro Mengoli in 1644")
        pietro_words.scale(0.75)
        pietro_words.next_to(pietro, DOWN)
        pietro.add(pietro_words)

        euler_words = OldTexText("Solved by Leonard \\\\ Euler in 1735")
        euler_words.scale(0.75)
        euler_words.next_to(euler, DOWN)
        euler.add(euler_words)

        pietro.next_to(FRAME_X_RADIUS*LEFT, LEFT)
        euler.next_to(FRAME_X_RADIUS*RIGHT, RIGHT)

        pi_answer = self.pi_answer = OldTex("{\\pi^2 \\over 6}")
        pi_answer.set_color(YELLOW)
        pi_answer.move_to(self.partial_sum_decimal, LEFT)
        equals_sign = OldTex("=")
        equals_sign.next_to(pi_answer, RIGHT)
        pi_answer.shift(SMALL_BUFF*UP)
        self.partial_sum_decimal.generate_target()
        self.partial_sum_decimal.target.next_to(equals_sign, RIGHT)

        pi = pi_answer[0]
        pi_rect = SurroundingRectangle(pi, color = RED)
        pi_rect.save_state()
        pi_rect.set_height(FRAME_Y_RADIUS)
        pi_rect.center()
        pi_rect.set_stroke(width = 0)
        squared = pi_answer[1]
        squared_rect = SurroundingRectangle(squared, color = BLUE)

        brace = Brace(
            VGroup(self.euler_sum, self.partial_sum_decimal.target),
            DOWN, buff = SMALL_BUFF
        )
        basel_text = brace.get_text("Basel problem", buff = SMALL_BUFF)

        self.number_line_group.save_state()
        self.play(
            pietro.next_to, ORIGIN, LEFT, LARGE_BUFF,
            self.number_line_group.next_to, FRAME_Y_RADIUS*DOWN, DOWN,
            morty.change, "pondering",
        )
        self.wait(2)
        self.play(euler.next_to, ORIGIN, RIGHT, LARGE_BUFF)
        self.wait(2)
        self.play(
            ReplacementTransform(self.q_marks, pi_answer),
            FadeIn(equals_sign),
            FadeOut(self.brace),
            MoveToTarget(self.partial_sum_decimal)
        )
        self.wait()
        self.play(morty.change, "surprised")
        self.play(pi_rect.restore)
        self.wait()
        self.play(Transform(pi_rect, squared_rect))
        self.play(FadeOut(pi_rect))
        self.play(morty.change, "hesitant")
        self.wait(2)
        self.play(
            GrowFromCenter(brace),
            euler.to_edge, DOWN,
            pietro.to_edge, DOWN,
            self.number_line_group.restore,
            self.number_line_group.shift, LARGE_BUFF*RIGHT,
        )
        self.play(Write(basel_text))
        self.play(morty.change, "happy")
        self.wait(4)

    def other_pi_formulas(self):

        self.play(
            FadeOut(self.rects),
            FadeOut(self.number_line)
        )

        self.leibniz_sum = OldTex(
            "1-{1\\over 3}+{1\\over 5}-{1\\over 7}+{1\\over 9}-\\cdots",
            "=", "{\\pi \\over 4}")

        self.wallis_product = OldTex(
            "{2\\over 1} \\cdot {2\\over 3} \\cdot {4\\over 3} \\cdot {4\\over 5}" +
             "\\cdot {6\\over 5} \\cdot {6\\over 7} \\cdots",
             "=", "{\\pi \\over 2}")

        self.leibniz_sum.next_to(self.euler_sum.get_part_by_tex("="), DOWN,
            buff = self.eq_spacing,
            submobject_to_align = self.leibniz_sum.get_part_by_tex("=")
        )

        self.wallis_product.next_to(self.leibniz_sum.get_part_by_tex("="), DOWN,
            buff = self.eq_spacing,
            submobject_to_align = self.wallis_product.get_part_by_tex("=")
        )


        self.play(
            Write(self.leibniz_sum)
        )
        self.play(
            Write(self.wallis_product)
        )

    def refocus_on_euler_sum(self):

        self.euler_sum.add(self.pi_answer)

        self.play(
            FadeOut(self.leibniz_sum),
            FadeOut(self.wallis_product),
            ApplyMethod(self.euler_sum.shift,
                ORIGIN + 2*UP - self.euler_sum.get_center())
        )

        # focus on pi squared
        pi_squared = self.euler_sum.get_part_by_tex("\\pi")[-3]
        self.play(
            ScaleInPlace(pi_squared,2,rate_func = wiggle)
        )



        # Morty thinks of a circle

        q_circle = Circle(
            stroke_color = YELLOW,
            fill_color = YELLOW,
            fill_opacity = 0.5,
            radius = 0.4, 
            stroke_width = 10.0
        )
        q_mark = OldTex("?")
        q_mark.next_to(q_circle)

        thought = Group(q_circle, q_mark)
        q_mark.set_height(0.8 * q_circle.get_height())
        self.pi_creature_thinks(thought,target_mode = "confused",
            bubble_config = { "height" : 2, "width" : 3 })

        self.wait()
