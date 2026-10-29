# ==============================================================================
# Scene:      ProblemSolvingRule1
# Source:     videos/_2023/moser_reboot/main.py (lines 387-423)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProblemSolvingRule1.py ProblemSolvingRule1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProblemSolvingRule1(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        # Title
        title = Text(
            "Problem-solving rule #1",
            font_size=72
        )
        title.to_edge(UP)
        title.set_backstroke()
        underline = Underline(title, buff=-0.05)
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "thinking", "pondering", look_at=title),
            GrowFromPoint(title, morty.get_corner(UL))
        )
        self.add(title)
        self.add(underline, title)
        self.play(ShowCreation(underline))
        self.wait()

        # Words
        words = Text("""
            Try answering easier questions
            related to the problem at hand
        """, font_size=48)
        words.next_to(underline, DOWN, LARGE_BUFF)
        words.set_fill(YELLOW)

        self.play(
            FadeIn(words, lag_ratio=0.1, run_time=2),
            self.change_students("tease", "thinking", "well", look_at=words),
            morty.change("tease"),
        )
        self.wait(6)
