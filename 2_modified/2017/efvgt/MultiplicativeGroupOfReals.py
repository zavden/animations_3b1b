# ==============================================================================
# Scene:      MultiplicativeGroupOfReals
# Source:     videos/_2017/efvgt.py (lines 1771-2028)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MultiplicativeGroupOfReals.py MultiplicativeGroupOfReals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation needs a Mobject, not a list: wrap the foreground list in a Group
#   - Cairo animations absorbed unknown kwargs (added_anims); GL raises TypeError: do not forward it
# ==============================================================================

from manim_imports_ext import *

ADDER_COLOR = GREEN


MULTIPLIER_COLOR = YELLOW


class AdditiveGroupOfReals(Scene):
    CONFIG = {
        "number_line_center" : UP,
        "shadow_line_center" : DOWN,
        "zero_color" : GREEN_B,
        "x_min" : -FRAME_WIDTH,
        "x_max" : FRAME_WIDTH,
    }
    def construct(self):
        self.add_number_line()
        self.show_example_slides(3, -7)
        self.write_group_of_slides()
        self.show_example_slides(2, 6, -1, -3)
        self.mark_zero()
        self.show_example_slides_labeled(3, -2)
        self.comment_on_zero_as_identity()
        self.show_example_slides_labeled(
            5.5, added_anims = [self.get_write_name_of_group_anim()]
        )
        self.show_example_additions((3, 2), (2, -5), (-4, 4))

    def add_number_line(self):
        number_line = NumberLine(
            x_min = self.x_min,
            x_max = self.x_max,
        )

        number_line.shift(self.number_line_center)
        shadow_line = NumberLine(color = GREY, stroke_width = 2)
        shadow_line.shift(self.shadow_line_center)
        for line in number_line, shadow_line:
            line.add_numbers()
        shadow_line.numbers.fade(0.25)
        shadow_line.save_state()
        shadow_line.set_color(BLACK)
        shadow_line.move_to(number_line)


        self.play(*list(map(Write, number_line)), run_time = 1)
        self.play(shadow_line.restore, Animation(number_line))
        self.wait()

        self.number_line = number_line
        self.shadow_line = shadow_line

    def show_example_slides(self, *nums):
        for num in nums:
            zero_point = self.number_line.number_to_point(0)            
            num_point = self.number_line.number_to_point(num)
            arrow = Arrow(zero_point, num_point, buff = 0)
            arrow.set_color(ADDER_COLOR)
            arrow.shift(MED_LARGE_BUFF*UP)

            self.play(ShowCreation(arrow))
            self.play(
                self.number_line.shift,
                num_point - zero_point,
                run_time = 2
            )
            self.play(FadeOut(arrow))

    def write_group_of_slides(self):
        title = OldTexText("Group of line symmetries")
        title.to_edge(UP)
        self.play(Write(title))
        self.title = title

    def mark_zero(self):
        dot = Dot(
            self.number_line.number_to_point(0),
            color = self.zero_color
        )
        arrow = Arrow(dot, color = self.zero_color)
        words = OldTexText("Follow zero")
        words.next_to(arrow.get_start(), UP)
        words.set_color(self.zero_color)

        self.play(
            ShowCreation(arrow),
            DrawBorderThenFill(dot),
            Write(words),
        )
        self.wait()
        self.play(*list(map(FadeOut, [arrow, words])))

        self.number_line.add(dot)

    def show_example_slides_labeled(self, *nums, **kwargs):
        for num in nums:
            line = DashedLine(
                self.number_line.number_to_point(num)+MED_LARGE_BUFF*UP,
                self.shadow_line.number_to_point(num)+MED_LARGE_BUFF*DOWN,
            )
            vect = self.number_line.number_to_point(num) - \
                   self.number_line.number_to_point(0)
            self.play(ShowCreation(line))
            self.wait()
            self.play(self.number_line.shift, vect, run_time = 2)
            self.wait()
            if "added_anims" in kwargs:
                self.play(*kwargs["added_anims"])
                self.wait()
            self.play(
                self.number_line.shift, -vect,
                FadeOut(line)
            )

    def comment_on_zero_as_identity(self):
        line = DashedLine(
            self.number_line.number_to_point(0)+MED_LARGE_BUFF*UP,
            self.shadow_line.number_to_point(0)+MED_LARGE_BUFF*DOWN,
        )
        words = OldTex("0 \\leftrightarrow \\text{Do nothing}")
        words.shift(line.get_top()+MED_SMALL_BUFF*UP - words[0].get_bottom())

        self.play(
            ShowCreation(line),
            Write(words)
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [line, words])))

    def get_write_name_of_group_anim(self):
        new_title = OldTexText("Additive group of real numbers")
        VGroup(*new_title[-len("realnumbers"):]).set_color(BLUE)
        VGroup(*new_title[:len("Additive")]).set_color(ADDER_COLOR)
        new_title.to_edge(UP)
        return Transform(self.title, new_title)

    def show_example_additions(self, *num_pairs):
        for num_pair in num_pairs:
            num_mobs = VGroup()
            arrows = VGroup()
            self.number_line.save_state()
            for num in num_pair:
                zero_point, num_point, arrow, num_mob = \
                    self.get_adder_mobs(num)
                if len(num_mobs) > 0:
                    last_num_mob = num_mobs[0]
                    x = num_mob.get_center()[0]
                    if x < last_num_mob.get_right()[0] and x > last_num_mob.get_left()[0]:
                        num_mob.next_to(last_num_mob, RIGHT)
                num_mobs.add(num_mob)
                arrows.add(arrow)

                self.play(
                    ShowCreation(arrow),
                    Write(num_mob, run_time = 1)
                )
                self.play(
                    self.number_line.shift, 
                    num_point - zero_point
                )
                self.wait()
            #Reset
            self.play(
                FadeOut(num_mobs),
                FadeOut(self.number_line)
            )
            ApplyMethod(self.number_line.restore).update(1)
            self.play(FadeIn(self.number_line))

            #Sum arrow
            num = sum(num_pair)
            zero_point, sum_point, arrow, sum_mob = \
                self.get_adder_mobs(sum(num_pair))
            VGroup(arrow, sum_mob).shift(MED_LARGE_BUFF*UP)
            arrows.add(arrow)
            self.play(
                ShowCreation(arrow),
                Write(sum_mob, run_time = 1)
            )
            self.wait()
            self.play(
                self.number_line.shift, 
                num_point - zero_point,
                run_time = 2
            )
            self.wait()
            self.play(
                self.number_line.restore,
                *list(map(FadeOut, [arrows, sum_mob]))
            )

    def get_adder_mobs(self, num):
        zero_point = self.number_line.number_to_point(0)            
        num_point = self.number_line.number_to_point(num)
        arrow = Arrow(zero_point, num_point, buff = 0)
        arrow.set_color(ADDER_COLOR)
        arrow.shift(MED_SMALL_BUFF*UP)
        if num == 0:
            arrow = DashedLine(UP, ORIGIN)
            arrow.move_to(zero_point)
        elif num < 0:
            arrow.set_color(RED)
            arrow.shift(SMALL_BUFF*UP)
        sign = "+" if num >= 0 else ""
        num_mob = OldTex(sign + str(num))
        num_mob.next_to(arrow, UP)
        num_mob.set_color(arrow.get_color())
        return zero_point, num_point, arrow, num_mob


class MultiplicativeGroupOfReals(AdditiveGroupOfReals):
    CONFIG = {
        "number_line_center" : 0.5*UP,
        "shadow_line_center" : 1.5*DOWN,
        "x_min" : -3*FRAME_X_RADIUS,
        "x_max" : 3*FRAME_X_RADIUS,
        "positive_reals_color" : MAROON_B,
    }
    def setup(self):
        self.foreground_mobjects = VGroup()

    def construct(self):
        self.add_title()
        self.add_number_line()
        self.introduce_stretch_and_squish()
        self.show_zero_fixed_in_place()
        self.follow_one()
        self.every_positive_number_association()
        self.compose_actions(3, 2)
        self.compose_actions(4, 0.5)
        self.write_group_name()
        self.compose_actions(1.5, 1.5)

    def add_title(self):
        self.title = OldTexText("Group of stretching/squishing actions")
        self.title.to_edge(UP)
        self.add(self.title)

    def add_number_line(self):
        AdditiveGroupOfReals.add_number_line(self)
        self.zero_point = self.number_line.number_to_point(0)
        self.one = [m for m in self.number_line.numbers if m.get_tex() is "1"][0]
        self.one.add_background_rectangle()
        self.one.background_rectangle.scale(1.3)
        self.number_line.save_state()        

    def introduce_stretch_and_squish(self):
        for num in [3, 0.25]:
            self.stretch(num)
            self.wait()
        self.play(self.number_line.restore)
        self.wait()

    def show_zero_fixed_in_place(self):
        arrow = Arrow(self.zero_point + UP, self.zero_point, buff = 0)
        arrow.set_color(ADDER_COLOR)
        words = OldTexText("Fix zero")
        words.set_color(ADDER_COLOR)
        words.next_to(arrow, UP)

        self.play(
            ShowCreation(arrow),
            Write(words)
        )
        self.foreground_mobjects.add(arrow)
        self.stretch(4)
        self.stretch(0.1)
        self.wait()
        self.play(self.number_line.restore)
        self.play(FadeOut(words))
        self.wait()

        self.zero_arrow = arrow

    def follow_one(self):
        dot = Dot(self.number_line.number_to_point(1))
        arrow = Arrow(dot.get_center()+UP+RIGHT, dot)
        words = OldTexText("Follow one")
        words.next_to(arrow.get_start(), UP)
        for mob in dot, arrow, words:
            mob.set_color(MULTIPLIER_COLOR)

        three_line, half_line = [
            DashedLine(
                self.number_line.number_to_point(num),
                self.shadow_line.number_to_point(num)
            )
            for num in (3, 0.5)
        ]
        three_mob = [m for m in self.shadow_line.numbers if m.get_tex() == "3"][0]
        half_point = self.shadow_line.number_to_point(0.5)
        half_arrow = Arrow(
            half_point+UP+LEFT, half_point, buff = SMALL_BUFF,
            tip_length = 0.15,
        )
        half_label = OldTex("1/2")
        half_label.scale(0.7)
        half_label.set_color(MULTIPLIER_COLOR)
        half_label.next_to(half_arrow.get_start(), LEFT, buff = SMALL_BUFF)
        
        self.play(
            ShowCreation(arrow),
            DrawBorderThenFill(dot),
            Write(words)
        )
        self.number_line.add(dot)
        self.number_line.numbers.add(dot)
        self.number_line.save_state()
        self.wait()
        self.play(*list(map(FadeOut, [arrow, words])))

        self.stretch(3)
        self.play(
            ShowCreation(three_line),
            Animation(self.one)
        )
        dot_copy = dot.copy()
        self.play(
            dot_copy.move_to, three_line.get_bottom()
        )
        self.play(Indicate(three_mob, run_time = 2))
        self.wait()
        self.play(
            self.number_line.restore,
            *list(map(FadeOut, [three_line, dot_copy]))
        )
        self.wait()
        self.stretch(0.5)
        self.play(
            ShowCreation(half_line),
            Animation(self.one)
        )
        dot_copy = dot.copy()
        self.play(
            dot_copy.move_to, half_line.get_bottom()
        )
        self.play(
            Write(half_label),
            ShowCreation(half_arrow)
        )
        self.wait()
        self.play(
            self.number_line.restore,
            *list(map(FadeOut, [
                half_label, half_arrow, 
                half_line, dot_copy
            ]))
        )
        self.wait()

        self.one_dot = dot

    def every_positive_number_association(self):
        positive_reals_line = Line(
            self.shadow_line.number_to_point(0),
            self.shadow_line.number_to_point(FRAME_X_RADIUS),
            color = self.positive_reals_color
        )
        positive_reals_words = OldTexText("All positive reals")
        positive_reals_words.set_color(self.positive_reals_color)
        positive_reals_words.next_to(positive_reals_line, UP)
        positive_reals_words.add_background_rectangle()

        third_line, one_line = [
            DashedLine(
                self.number_line.number_to_point(num),
                self.shadow_line.number_to_point(num)
            )
            for num in (0.33, 1)
        ]

        self.play(
            self.zero_arrow.shift, 0.5*UP,
            rate_func = there_and_back
        )
        self.wait()
        self.play(
            self.one_dot.shift, 0.25*UP,
            rate_func = wiggle
        )
        self.stretch(3)
        self.stretch(0.33/3, run_time = 3)
        self.wait()
        self.play(ShowCreation(third_line), Animation(self.one))
        self.play(
            ShowCreation(positive_reals_line),
            Write(positive_reals_words),
        )
        self.wait()
        self.play(
            ReplacementTransform(third_line, one_line),
            self.number_line.restore,
            Animation(positive_reals_words),
            run_time = 2
        )
        self.number_line.add_to_back(one_line)
        self.number_line.save_state()
        self.stretch(
            7, run_time = 10, rate_func = there_and_back,
            added_anims = [Animation(positive_reals_words)]
        )
        self.wait()

    def compose_actions(self, num1, num2):
        words = VGroup(*[
            OldTexText("(%s by %s)"%(word, str(num)))
            for num in (num1, num2, num1*num2)
            for word in ["Stretch" if num > 1 else "Squish"]
        ])
        words.submobjects.insert(2, OldTex("="))
        words.arrange(RIGHT)
        top_words = VGroup(*words[:2])
        top_words.set_color(MULTIPLIER_COLOR)
        bottom_words = VGroup(*words[2:])
        bottom_words.next_to(top_words, DOWN)
        words.scale(0.8)
        words.next_to(self.number_line, UP)
        words.to_edge(RIGHT)

        for num, word in zip([num1, num2], top_words):
            self.stretch(
                num, 
                added_anims = [FadeIn(word)],
                run_time = 3
            )
            self.wait()
        self.play(Write(bottom_words, run_time = 2))
        self.wait(2)
        self.play(
            ApplyMethod(self.number_line.restore, run_time = 2),
            FadeOut(words),
        )
        self.wait()

    def write_group_name(self):
        new_title = OldTexText(
            "Multiplicative group of positive real numbers"
        )
        new_title.to_edge(UP)
        VGroup(
            *new_title[:len("Multiplicative")]
        ).set_color(MULTIPLIER_COLOR)
        VGroup(
            *new_title[-len("positiverealnumbers"):]
        ).set_color(self.positive_reals_color)

        self.play(Transform(self.title, new_title))
        self.wait()

    ###

    def stretch(self, factor, run_time = 2, **kwargs):
        kwargs["run_time"] = run_time
        target = self.number_line.copy()
        target.stretch_about_point(factor, 0, self.zero_point)
        total_factor = (target.number_to_point(1)-self.zero_point)[0]
        for number in target.numbers:
            number.stretch_in_place(1./factor, dim = 0)
            if total_factor < 0.7:
                number.stretch_in_place(total_factor, dim = 0)
        self.play(
            # CHANGE: Cairo animations absorbed unknown kwargs (added_anims); GL raises TypeError: do not forward it
            Transform(self.number_line, target, **{k: v for k, v in kwargs.items() if k != "added_anims"}),
            *kwargs.get("added_anims", [])
        )

    def play(self, *anims, **kwargs):
        # CHANGE: Animation needs a Mobject, not a list: wrap the foreground list in a Group
        anims = list(anims) + [Animation(Group(*self.foreground_mobjects))]
        Scene.play(self, *anims, **kwargs)
