# ==============================================================================
# Scene:      CrossingOneMillion
# Source:     videos/_2018/fc1.py (lines 5-106)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/efvgt.py
#
# Run from this folder:
#     manimgl CrossingOneMillion.py CrossingOneMillion -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - student_says() speaks with students[2] by default (index=2 in GL and student_index=2 in Cairo), so the bubble is on students[2], not students[1]
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/efvgt.py -----

class ConfettiSpiril(Animation):
    CONFIG = {
        "x_start" : 0,
        "spiril_radius" : 0.5,
        "num_spirils" : 4,
        "run_time" : 10,
        "rate_func" : None,
    }
    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        mobject.next_to(self.x_start*RIGHT + FRAME_Y_RADIUS*UP, UP)
        self.total_vert_shift = \
            FRAME_HEIGHT + mobject.get_height() + 2*MED_SMALL_BUFF
        
        Animation.__init__(self, mobject, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.set_points(starting_submobject.get_points())

    def interpolate_mobject(self, alpha):
        Animation.interpolate_mobject(self, alpha)
        angle = alpha*self.num_spirils*2*np.pi
        vert_shift = alpha*self.total_vert_shift

        start_center = self.mobject.get_center()
        self.mobject.shift(self.spiril_radius*OUT)
        self.mobject.rotate(angle, axis = UP, about_point = start_center)
        self.mobject.shift(vert_shift*DOWN)


def get_confetti_animations(num_confetti_squares):
    colors = [RED, YELLOW, GREEN, BLUE, PURPLE, RED]
    confetti_squares = [
        Square(
            side_length = 0.2,
            stroke_width = 0,
            fill_opacity = 0.75,
            fill_color = random.choice(colors),
        )
        for x in range(num_confetti_squares)
    ]
    confetti_spirils = [
        ConfettiSpiril(
            square,
            x_start = 2*random.random()*FRAME_X_RADIUS - FRAME_X_RADIUS,
            rate_func = squish_rate_func(rush_from, a, a+0.5)
        )
        for a, square in zip(
            np.linspace(0, 0.5, num_confetti_squares),
            confetti_squares
        )
    ]
    return confetti_spirils



# ----- From _2018/fc1.py -----

class CrossingOneMillion(TeacherStudentsScene):
    def construct(self):
        self.increment_count()
        self.comment_on_real_milestone()
        self.reflect()

    def increment_count(self):
        number = self.number = Integer(0)
        number.move_to(UP, LEFT)
        number.scale(3)
        self.look_at(number, run_time=0)

        confetti_spirils = self.confetti_spirils = list(map(
            turn_animation_into_updater,
            get_confetti_animations(50)
        ))
        self.add(*confetti_spirils)
        self.play(
            ChangeDecimalToValue(
                number, 10**6,
                position_update_func=lambda m: m.move_to(
                    UP, LEFT
                ),
                rate_func=bezier([0, 0, 0, 1, 1, 1]),
                run_time=5,
            ),
            LaggedStartMap(
                ApplyMethod, self.get_pi_creatures(),
                lambda m: (m.change, "hooray", number),
                rate_func=squish_rate_func(smooth, 0, 0.5),
                run_time=4,
            ),
        )
        self.wait()

    def comment_on_real_milestone(self):
        number = self.number
        remainder = Integer(2**20 - 10**6)
        words = OldTexText(
            "Just",
            "{:,}".format(remainder.number),
            "to go \\\\ before the real milestone",
        )
        self.student_says(
            words,
            added_anims=[
                ApplyMethod(self.teacher.change, "hesitant"),
                self.change_students(
                    "sassy", "speaking", "happy"
                ),
                number.scale, 0.5,
                number.center,
                number.to_edge, UP,
            ]
        )
        self.wait()
        self.remove(*self.confetti_spirils)
        remainder.replace(words[1])
        words.submobjects[1] = remainder
        self.play(
            ChangeDecimalToValue(number, 2**20, run_time=3),
            ChangeDecimalToValue(remainder, 0.1, run_time=3),
            self.teacher.change, "pondering", number,
            self.change_students(
                *["pondering"] * 3,
                look_at=number
            ),
        )
        self.play(
            # CHANGE: student_says() speaks with students[2] by default (index=2 in GL and student_index=2 in Cairo), so the bubble is on students[2], not students[1]
            FadeOut(self.students[2].bubble),
            FadeOut(self.students[2].bubble.content),
        )
        self.wait(2)

    def reflect(self):
        bubble = ThoughtBubble(
            direction=RIGHT,
            height=4,
            width=7,
        )
        bubble.pin_to(self.teacher)
        q_marks = OldTex("???")
        q_marks.scale(2)
        q_marks.set_color_by_gradient(BLUE_D, BLUE_B)
        q_marks.next_to(bubble[-1].get_top(), DOWN)
        arrow = Vector(0.5 * DOWN, color=WHITE)
        arrow.next_to(q_marks, DOWN)
        number = self.number
        number.generate_target()
        number.target.next_to(arrow, DOWN)

        self.play(
            ShowCreation(
                bubble,
                rate_func=squish_rate_func(smooth, 0, 0.3)
            ),
            Write(q_marks),
            GrowArrow(arrow),
            MoveToTarget(number),
            run_time=3
        )
        self.wait()
