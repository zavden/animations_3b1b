# ==============================================================================
# Scene:      LastVideo
# Source:     videos/_2017/eoc/chapter5.py (lines 17-62)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LastVideo.py LastVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *

class LastVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        last_video = series[2]
        last_video.save_state()
        this_video = series[3]

        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        known_formulas = VGroup(*list(map(OldTex, [
            "\\frac{d(x^n)}{dx} = nx^{n-1}",
            "\\frac{d(\\sin(x))}{dx} = \\cos(x)",
        ])))
        known_formulas.arrange(
            DOWN, buff = MED_LARGE_BUFF,
        )
        known_formulas.set_height(2.5)
        exp_question = OldTex("2^x", ", 7^x, ", "e^x", " ???")

        last_video_brace = Brace(last_video)
        known_formulas.next_to(last_video_brace, DOWN)
        known_formulas.shift(MED_LARGE_BUFF*LEFT)
        last_video_brace.save_state()
        last_video_brace.shift(3*LEFT)
        last_video_brace.set_fill(opacity = 0)

        self.add(series)
        self.play(
            last_video_brace.restore,
            last_video.set_color, YELLOW,
            self.get_teacher().change_mode, "raise_right_hand",
        )
        self.play(Write(known_formulas))
        self.wait()
        self.student_says(
            exp_question, index = 1,
            added_anims = [self.get_teacher().change_mode, "pondering"]
        )
        self.wait(3)
        e_to_x = exp_question.get_part_by_tex("e^x")
        self.play(
            self.teacher.change_mode, "raise_right_hand",
            e_to_x.scale, 1.5,
            e_to_x.set_color, YELLOW,
            e_to_x.next_to, self.teacher.get_corner(UP+LEFT), UP
        )
        self.wait(2)
