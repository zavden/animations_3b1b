# ==============================================================================
# Scene:      WantToLearnQM
# Source:     videos/_2017/waves.py (lines 445-486)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WantToLearnQM.py WantToLearnQM -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class WantToLearnQM(TeacherStudentsScene):
    def construct(self):
        question1 = OldTex(
            "\\text{What does }\\qquad \\\\", 
            "|\\!\\psi \\rangle", "=",
            "\\frac{1}{\\sqrt{2}}", "|\\!\\uparrow \\rangle", "+",
            "\\frac{1}{\\sqrt{2}}", "|\\!\\downarrow \\rangle \\\\",
            "\\text{mean?}\\qquad\\quad"
        )
        question1.set_color_by_tex_to_color_map({
            "psi" : BLUE,
            "uparrow" : GREEN,
            "downarrow" : RED,
        })
        question2 = OldTexText(
            "Why are complex \\\\ numbers involved?"
        )
        question3 = OldTexText(
            "How do you compute \\\\ quantum probabilities?"
        )
        questions = [question1, question2, question3]
        bubbles = VGroup()

        for i, question in zip([1, 2, 0], questions):
            self.student_says(
                question, 
                content_introduction_kwargs = {"run_time" : 2},
                index = i,
                bubble_config = {"fill_opacity" : 1},
                bubble_creation_class = FadeIn,
            )
            bubble = self.students[i].bubble
            bubble.add(bubble.content)
            bubbles.add(bubble)
            self.students
            self.students[i].bubble = None
        self.wait(2)
        self.teacher_says(
            "First, lots and lots \\\\ of linear algebra",
            added_anims = list(map(FadeOut, bubbles))
        )
        self.wait()
