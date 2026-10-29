# ==============================================================================
# Scene:      AdditiveGroupOfReals
# Source:     videos/_2017/efvgt.py (lines 1230-1430)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AdditiveGroupOfReals.py AdditiveGroupOfReals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

ADDER_COLOR = GREEN


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
