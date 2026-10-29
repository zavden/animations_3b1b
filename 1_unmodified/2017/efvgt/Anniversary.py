# ==============================================================================
# Scene:      Anniversary
# Source:     videos/_2017/efvgt.py (lines 90-186)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Anniversary.py Anniversary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class Anniversary(TeacherStudentsScene):
    CONFIG = {
        "num_confetti_squares" : 50,
        "message": "2 year Anniversary!",
    }
    def construct(self):
        self.celebrate()
        self.complain()

    def celebrate(self):
        title = OldTexText(self.message)
        title.scale(1.5)
        title.to_edge(UP)

        first_video = Rectangle(
            height = 2, width = 2*(16.0/9),
            stroke_color = WHITE,
            fill_color = "#111111",
            fill_opacity = 0.75,
        )
        first_video.next_to(self.get_teacher(), UP+LEFT)
        first_video.shift(RIGHT)
        formula = OldTex("e^{\\pi i} = -1")
        formula.move_to(first_video)
        first_video.add(formula)
        first_video.fade(1)

        hats = self.get_party_hats()
        confetti_spirils = get_confetti_animations(
            self.num_confetti_squares
        )
        self.play(
            Write(title, run_time = 2),
            *[
                ApplyMethod(pi.change_mode, "hooray")
                for pi in self.get_pi_creatures()
            ]
        )
        self.play(
            DrawBorderThenFill(
                hats,
                lag_ratio = 0.5,
                rate_func=linear,
                run_time = 2,
            ),
            *confetti_spirils + [
                Succession(
                    Animation(pi, run_time = 2),
                    ApplyMethod(pi.look, UP+LEFT),
                    ApplyMethod(pi.look, UP+RIGHT),
                    Animation(pi),
                    ApplyMethod(pi.look_at, first_video),
                    rate_func=linear
                )
                for pi in self.get_students()
            ] + [
                Succession(
                    Animation(self.get_teacher(), run_time = 2),
                    Blink(self.get_teacher()),
                    Animation(self.get_teacher(), run_time = 2),
                    ApplyMethod(self.get_teacher().change_mode, "raise_right_hand"),
                    rate_func=linear
                ),
                DrawBorderThenFill(
                    first_video, 
                    run_time = 10,
                    rate_func = squish_rate_func(smooth, 0.5, 0.7)
                )
            ]
        )
        self.play_student_changes(*["confused"]*3)

    def complain(self):
        self.student_says(
            "Why were you \\\\ talking so fast?",
            index = 0,
            target_mode = "sassy",
        )
        self.play_student_changes(*["sassy"]*3)
        self.play(self.get_teacher().change_mode, "shruggie")
        self.wait(2)

    def get_party_hats(self):
        hats = VGroup(*[
            PartyHat(
                pi_creature = pi,
                height = 0.5*pi.get_height()
            )
            for pi in self.get_pi_creatures()
        ])
        max_angle = np.pi/6
        for hat in hats:
            hat.rotate(
                random.random()*2*max_angle - max_angle,
                about_point = hat.get_bottom()
            )
        return hats
