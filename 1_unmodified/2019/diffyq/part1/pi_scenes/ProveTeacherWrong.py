# ==============================================================================
# Scene:      ProveTeacherWrong
# Source:     videos/_2019/diffyq/part1/pi_scenes.py (lines 134-230)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ProveTeacherWrong.py ProveTeacherWrong -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/pi_scenes.py -----

class ProveTeacherWrong(TeacherStudentsScene):
    def construct(self):
        tex_config = {
            "tex_to_color_map": {
                "{\\theta}": BLUE,
                "{\\dot\\theta}": YELLOW,
                "{\\ddot\\theta}": RED,
            }
        }
        func = OldTex(
            "{\\theta}(t)", "=",
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)",
            **tex_config,
        )
        d_func = OldTex(
            "{\\dot\\theta}(t)", "=",
            "-\\left(\\sqrt{g / L}\\right)",
            "\\theta_0", "\\sin(\\sqrt{g / L} \\cdot t)",
            **tex_config,
        )
        dd_func = OldTex(
            "{\\ddot\\theta}(t)", "=",
            "-\\left(g / L\\right)",
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)",
            **tex_config,
        )
        # ode = OldTex(
        #     "\\ddot {\\theta}({t})", "=",
        #     "-\\mu \\dot {\\theta}({t})",
        #     "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        #     **tex_config,
        # )
        ode = get_ode()
        arrows = [Tex("\\Downarrow") for x in range(2)]

        VGroup(func, d_func, dd_func, ode, *arrows).scale(0.7)

        teacher = self.teacher
        you = self.students[2]

        self.student_thinks(ode)
        you.add_updater(lambda m: m.look_at(func))
        self.teacher_holds_up(func)
        self.wait()

        group = VGroup(arrows[0], d_func, arrows[1], dd_func)
        group.arrange(DOWN)
        group.move_to(func, DOWN)

        arrow = Arrow(
            group.get_corner(UL),
            ode.get_top(),
            path_arc=PI / 2,
        )
        q_marks = VGroup(*[
            OldTex("?").scale(1.5).next_to(
                arrow.point_from_proportion(a),
                UP
            )
            for a in np.linspace(0.2, 0.8, 5)
        ])
        cycle_animation(VFadeInThenOut(
            q_marks,
            lag_ratio=0.2,
            run_time=4,
            rate_func=squish_rate_func(smooth, 0, 0.5)
        ))

        self.play(
            func.next_to, group, UP,
            LaggedStartMap(
                FadeInFrom, group,
                lambda m: (m, UP)
            ),
            teacher.change, "guilty",
            you.change, "sassy",
        )

        rect = SurroundingRectangle(
            VGroup(group, func)
        )
        dashed_rect = DashedVMobject(rect, num_dashes=75)
        animated_rect = AnimatedBoundary(dashed_rect, cycle_rate=1)

        self.wait()
        self.add(animated_rect, q_marks)
        self.play(
            ShowCreation(arrow),
            # FadeInFromDown(q_mark),
            self.change_students("confused", "confused")
        )
        self.wait(4)
        self.play_student_changes(
            *3 * ["pondering"],
            self.teacher.change, "maybe"
        )
        self.wait(8)
