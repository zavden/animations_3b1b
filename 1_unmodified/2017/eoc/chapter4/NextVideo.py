# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2017/eoc/chapter4.py (lines 2128-2197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        next_video = series[4]

        pre_expression = OldTex(
            "x", "^2", "+", "y", "^2", "=", "1"
        )
        d_expression = OldTex(
            "2", "x", "\\,dx", "+", "2", "y", "\\,dy", "=", "0"
        )
        expression_to_d_expression_indices = [
            1, 0, 0, 2, 4, 3, 3, 5, 6
        ]
        expression = VGroup()
        for i, j in enumerate(expression_to_d_expression_indices):
            submob = pre_expression[j].copy()
            if d_expression.expression_parts[i] == "2":
                two = OldTex("2")
                two.replace(submob)
                expression.add(two)
            else:
                expression.add(submob)

        for mob in expression, d_expression:
            mob.scale(1.2)
            mob.next_to(
                self.get_teacher().get_corner(UP+LEFT), UP,
                buff = MED_LARGE_BUFF
            )
            mob.shift_onto_screen()

        axes = Axes(x_min = -3, x_max = 3, color = GREY)
        axes.add(Circle(color = YELLOW))
        line = Line(np.sqrt(2)*UP, np.sqrt(2)*RIGHT)
        line.scale(1.5)
        axes.add(line)

        axes.scale(0.5)
        axes.next_to(d_expression, LEFT)

        self.add(series)        
        self.play(
            next_video.shift, 0.5*DOWN,
            next_video.set_color, YELLOW,
            self.get_teacher().change_mode, "raise_right_hand"
        )
        self.wait()
        self.play(
            Write(expression),
            *[
                ApplyMethod(pi.change_mode, "pondering")
                for pi in self.get_students()
            ]
        )
        self.play(FadeIn(axes))
        self.wait()
        self.remove(expression)
        self.play(Transform(expression, d_expression, path_arc = np.pi/2))
        self.wait()
        self.play(
            Rotate(
                line, np.pi/4, 
                about_point = axes.get_center(),
                rate_func = wiggle,
                run_time = 3
            )
        )
        self.wait(2)
