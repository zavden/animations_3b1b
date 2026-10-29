# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2017/eoc/chapter5.py (lines 1881-1940)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter4.py
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter4.py -----

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



# ----- From _2017/eoc/chapter5.py -----

class NextVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        this_video = series[3]
        next_video = series[4]
        brace = Brace(this_video, DOWN)
        this_video.save_state()
        this_video.set_color(YELLOW)

        this_tex = OldTex(
            "{d(", "a^t", ") \\over dt} = ", "a^t", "\\ln(a)"
        )
        this_tex[1][1].set_color(YELLOW)
        this_tex[3][1].set_color(YELLOW)
        this_tex.next_to(brace, DOWN)

        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
        next_tex = VGroup(*list(map(OldTexText, [
            "Chain rule", "Product rule", "$\\vdots$"
        ])))
        next_tex.arrange(DOWN)
        next_tex.next_to(brace, DOWN)
        next_tex.shift(
            next_video.get_center()[0]*RIGHT\
            -next_tex.get_center()[0]*RIGHT
        )

        self.add(series, brace, *this_tex[:3])
        self.play_student_changes(
            "confused", "pondering", "erm",
            look_at = this_tex
        )
        self.play(ReplacementTransform(
            this_tex[1].copy(), this_tex[3]
        ))
        self.wait()
        self.play(
            Write(this_tex[4]),
            ReplacementTransform(
                this_tex[3][0].copy(),
                this_tex[4][3],
                path_arc = np.pi,
                remover = True
            )
        )
        self.wait(2)
        self.play(this_tex.replace, this_video)
        self.play(
            brace.next_to, next_video, DOWN,
            this_video.restore,
            Animation(this_tex),
            next_video.set_color, YELLOW,
            Write(next_tex),
            self.get_teacher().change_mode, "raise_right_hand"
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = next_tex
        )
        self.wait(3)
