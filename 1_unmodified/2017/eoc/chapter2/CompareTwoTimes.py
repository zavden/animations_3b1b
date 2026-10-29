# ==============================================================================
# Scene:      CompareTwoTimes
# Source:     videos/_2017/eoc/chapter2.py (lines 676-786)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareTwoTimes.py CompareTwoTimes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

DISTANCE_COLOR = BLUE


TIME_COLOR = YELLOW


class CompareTwoTimes(Scene):
    CONFIG = {
        "start_distance" : 30,
        "start_time" : 4,
        "end_distance" : 50,
        "end_time" : 5,
        "fade_at_the_end" : True,
    }
    def construct(self):
        self.introduce_states()
        self.show_equation()
        if self.fade_at_the_end:
            self.fade_all_but_one_moment()

    def introduce_states(self):
        state1 = self.get_car_state(self.start_distance, self.start_time)
        state2 = self.get_car_state(self.end_distance, self.end_time)

        state1.to_corner(UP+LEFT)
        state2.to_corner(DOWN+LEFT)

        dividers = VGroup(
            Line(FRAME_X_RADIUS*LEFT, RIGHT),
            Line(RIGHT+FRAME_Y_RADIUS*UP, RIGHT+FRAME_Y_RADIUS*DOWN),
        )
        dividers.set_color(GREY)

        self.add(dividers, state1)
        self.wait()
        copied_state = state1.copy()
        self.play(copied_state.move_to, state2)
        self.play(Transform(copied_state, state2))
        self.wait(2)
        self.keeper = state1

    def show_equation(self):
        velocity = OldTexText("Velocity")
        change_over_change = OldTex(
            "\\frac{\\text{Change in distance}}{\\text{Change in time}}"
        )
        formula = OldTex(
            "\\frac{(%s - %s) \\text{ meters}}{(%s - %s) \\text{ seconds}}"%(
                str(self.end_distance), str(self.start_distance),
                str(self.end_time), str(self.start_time),
            )
        )
        ed_len = len(str(self.end_distance))
        sd_len = len(str(self.start_distance))
        et_len = len(str(self.end_time))
        st_len = len(str(self.start_time))
        seconds_len = len("seconds")
        VGroup(
            VGroup(*formula[1:1+ed_len]),
            VGroup(*formula[2+ed_len:2+ed_len+sd_len])
        ).set_color(DISTANCE_COLOR)
        VGroup(
            VGroup(*formula[-2-seconds_len-et_len-st_len:-2-seconds_len-st_len]),
            VGroup(*formula[-1-seconds_len-st_len:-1-seconds_len]),
        ).set_color(TIME_COLOR)

        down_arrow1 = OldTex("\\Downarrow")
        down_arrow2 = OldTex("\\Downarrow")
        group = VGroup(
            velocity, down_arrow1, 
            change_over_change, down_arrow2,
            formula,
        )
        group.arrange(DOWN)
        group.to_corner(UP+RIGHT)

        self.play(FadeIn(
            group, lag_ratio = 0.5,
            run_time = 3
        ))
        self.wait(3)
        self.formula = formula

    def fade_all_but_one_moment(self):
        anims = [
            ApplyMethod(mob.fade, 0.5)
            for mob in self.get_mobjects()
        ]
        anims.append(Animation(self.keeper.copy()))
        self.play(*anims)
        self.wait()

    def get_car_state(self, distance, time):
        line = Line(3*LEFT, 3*RIGHT)
        dots = list(map(Dot, line.get_start_and_end()))
        line.add(*dots)
        car = Car()
        car.move_to(line.get_start())
        car.shift((distance/10)*RIGHT)
        front_line = car.get_front_line()

        brace = Brace(VGroup(dots[0], front_line), DOWN)
        distance_label = brace.get_text(
            str(distance), " meters"
        )
        distance_label.set_color_by_tex(str(distance), DISTANCE_COLOR)
        brace.add(distance_label)
        time_label = OldTexText(
            "Time:", str(time), "seconds"
        )
        time_label.set_color_by_tex(str(time), TIME_COLOR)
        time_label.next_to(
            VGroup(line, car), UP,
            aligned_edge = LEFT
        )

        return VGroup(line, car, front_line, brace, time_label)
