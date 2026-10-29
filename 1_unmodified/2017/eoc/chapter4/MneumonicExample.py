# ==============================================================================
# Scene:      MneumonicExample
# Source:     videos/_2017/eoc/chapter4.py (lines 1367-1424)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MneumonicExample.py MneumonicExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MneumonicExample(TeacherStudentsScene):
    def construct(self):
        d, left, right, rp = deriv_q = OldTex(
            "\\frac{d}{dx}(", "\\sin(x)", "x^2", ")"
        )
        deriv_q.to_edge(UP)

        words = OldTexText(
            "Left ", "d(Right) ", "+", " Right ", "d(Left)",
            arg_separator = ""
        )
        deriv = OldTex("\\sin(x)", "2x", "+", "x^2", "\\cos(x)")
        for mob in words, deriv:
            VGroup(mob[1], mob[4]).set_color(GREEN)
            mob.next_to(deriv_q, DOWN, buff = MED_LARGE_BUFF)
        deriv.shift(words[2].get_center()-deriv[2].get_center())

        self.add(words)
        self.play(
            Write(deriv_q),
            self.get_teacher().change_mode, "raise_right_hand"
        )
        self.play_student_changes(*["pondering"]*3)

        left_words = VGroup(*words[:2])
        left_terms = VGroup(*deriv[:2])
        self.play(
            left_words.next_to, left_terms, DOWN,
            MED_LARGE_BUFF, RIGHT
        )
        self.play(ReplacementTransform(
            left_words.copy(), left_terms
        ))
        self.wait()
        self.play(*list(map(Indicate, [left, left_words[0], left_terms[0]])))
        self.wait()
        self.play(*list(map(Indicate, [right, left_words[1], left_terms[1]])))
        self.wait()

        right_words = VGroup(*words[2:])
        right_terms = VGroup(*deriv[2:])
        self.play(
            right_words.next_to, right_terms, DOWN,
            MED_LARGE_BUFF, LEFT
        )
        self.play(ReplacementTransform(
            right_words.copy(), right_terms
        ))
        self.wait()
        self.play(*list(map(Indicate, [right, right_words[1], right_terms[1]])))
        self.wait()
        self.play(*list(map(Indicate, [left, right_words[2], right_terms[2]])))
        self.wait(3)

        self.play(self.get_teacher().change_mode, "shruggie")
        self.wait()
        self.play_student_changes(*["confused"]*3)
        self.wait(3)
