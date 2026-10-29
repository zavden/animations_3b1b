# ==============================================================================
# Scene:      AskQuestions
# Source:     videos/_2018/div_curl.py (lines 867-934)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskQuestions.py AskQuestions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def vec_tex(s):
    return "\\vec{\\textbf{%s}}" % s


class AskQuestions(TeacherStudentsScene):
    def construct(self):
        div_tex = OldTex("\\nabla \\cdot", vec_tex("v"))
        curl_tex = OldTex("\\nabla \\times", vec_tex("v"))
        div_name = OldTexText("Divergence")
        curl_name = OldTexText("Curl")
        div = VGroup(div_name, div_tex)
        curl = VGroup(curl_name, curl_tex)
        for group in div, curl:
            group[1].set_color_by_tex(vec_tex("v"), YELLOW)
            group.arrange(DOWN)
        topics = VGroup(div, curl)
        topics.arrange(DOWN, buff=LARGE_BUFF)
        topics.move_to(self.hold_up_spot, DOWN)
        div.save_state()
        div.move_to(self.hold_up_spot, DOWN)
        screen = self.screen

        self.student_says(
            "What does fluid flow have \\\\ to do with electricity?",
            added_anims=[self.teacher.change, "happy"]
        )
        self.wait()
        self.student_says(
            "And you mentioned \\\\ complex numbers?",
            index=0,
        )
        self.wait(3)
        self.play(
            FadeInFromDown(div),
            self.teacher.change, "raise_right_hand",
            FadeOut(self.students[0].bubble),
            FadeOut(self.students[0].bubble.content),
            self.change_students(*["pondering"] * 3)
        )
        self.play(
            FadeInFromDown(curl),
            div.restore
        )
        self.wait()
        self.look_at(self.screen)
        self.wait()
        self.play_all_student_changes("hooray", look_at=screen)
        self.wait(3)

        topics.generate_target()
        topics.target.to_edge(LEFT, buff=LARGE_BUFF)
        arrow = OldTex("\\leftrightarrow")
        arrow.scale(2)
        arrow.next_to(topics.target, RIGHT, buff=LARGE_BUFF)
        screen.next_to(arrow, RIGHT, LARGE_BUFF)
        complex_analysis = OldTexText("Complex analysis")
        complex_analysis.next_to(screen, UP)

        self.play(
            MoveToTarget(topics),
            self.change_students(
                "confused", "sassy", "erm",
                look_at=topics.target
            ),
            self.teacher.change, "pondering", screen
        )
        self.play(
            Write(arrow),
            FadeInFromDown(complex_analysis)
        )
        self.look_at(screen)
        self.wait(6)
