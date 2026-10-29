# ==============================================================================
# Scene:      StacksApproachBellCurve
# Source:     videos/_2018/eop/combinations.py (lines 2012-2126)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StacksApproachBellCurve.py StacksApproachBellCurve -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StacksApproachBellCurve(Scene):
    CONFIG = {
        "n_iterations" : 30,
    }
    def construct(self):
        bar = Square(side_length = 1)
        bar.set_fill(BLUE)
        bar.set_stroke(width = 0)
        bars = VGroup(bar)

        numbers = VGroup(Integer(1))
        numbers.next_to(bars, UP, SMALL_BUFF)

        max_width = FRAME_WIDTH - 2
        max_height = FRAME_Y_RADIUS - 1.5

        for x in range(self.n_iterations):
            if x == 0:
                distance = 1.5
            else:
                distance = bars[1].get_center()[0] - bars[0].get_center()[0]

            bars_copy = bars.copy()

            #Copy and shift
            for mob, vect in (bars, DOWN), (bars_copy, UP):
                mob.generate_target()
                if mob.target.get_height() > max_height:
                    mob.target.stretch_to_fit_height(max_height)
                if mob.target.get_width() > max_width:
                    mob.target.stretch_to_fit_width(max_width)
                mob.target.next_to(ORIGIN, vect, MED_LARGE_BUFF)
            colors = color_gradient([BLUE, YELLOW], len(bars)+1)
            for color, bar in zip(colors, bars.target):
                bar.set_fill(color)
            for color, bar in zip(colors[1:], bars_copy.target):
                bar.set_fill(color)
            bars_copy.set_fill(opacity = 0)

            numbers_copy = numbers.copy()
            for bs, ns in (bars, numbers), (bars_copy, numbers_copy):
                ns.generate_target()
                for bar, number in zip(bs.target, ns.target):
                    # if number.get_width() > bar.get_width():
                    #     number.set_width(bar.get_width())
                    number.next_to(bar, UP, SMALL_BUFF)

            self.play(*list(map(MoveToTarget, [
                bars, bars_copy,
                numbers, numbers_copy
            ])))
            self.play(
                bars.shift, distance*LEFT/2,
                numbers.shift, distance*LEFT/2,
                bars_copy.shift, distance*RIGHT/2,
                numbers_copy.shift, distance*RIGHT/2,
            )

            #Stack
            bars_copy.generate_target()
            numbers.generate_target()
            numbers_copy.generate_target()
            new_numbers = VGroup()
            min_scale_val = 1
            for i in range(len(bars)-1):
                top_bar = bars_copy.target[i]
                low_bar = bars[i+1]
                top_num = numbers_copy.target[i]
                low_num = numbers.target[i+1]
                new_num = Integer(top_num.number + low_num.number)
                if new_num.get_width() > top_bar.get_width():
                    min_scale_val = min(
                        min_scale_val, 
                        top_bar.get_width() / new_num.get_width()
                    )
                new_numbers.add(new_num)

                top_bar.move_to(low_bar.get_top(), DOWN)
                new_num.next_to(top_bar, UP, SMALL_BUFF)
                Transform(low_num, new_num).update(1)
                Transform(top_num, new_num).update(1)
            for group in new_numbers, numbers.target[1:], numbers_copy.target[:-1]:
                for num in group:
                    num.scale(min_scale_val, about_point = num.get_bottom())
            if x > 1:
                height = numbers.target[1].get_height()
                for mob in numbers.target[0], numbers_copy.target[-1]:
                    mob.set_height(height)

            bars_copy.target[-1].align_to(bars, DOWN)
            numbers_copy.target[-1].next_to(bars_copy.target[-1], UP, SMALL_BUFF)

            self.play(*[
                MoveToTarget(mob, lag_ratio = 0.5)
                for mob in (bars_copy, numbers, numbers_copy)
            ])
            self.remove(numbers, numbers_copy)
            numbers = VGroup(numbers[0])
            numbers.add(*new_numbers)
            numbers.add(numbers_copy[-1])

            #Resize lower bars
            for top_bar, low_bar in zip(bars_copy[:-1], bars[1:]):
                bottom = low_bar.get_bottom()
                low_bar.replace(
                    VGroup(low_bar, top_bar),
                    stretch = True
                )
                low_bar.move_to(bottom, DOWN)
            bars.add(bars_copy[-1])
            self.remove(bars_copy)
            self.add(bars)

        self.add(numbers)
        self.wait()
