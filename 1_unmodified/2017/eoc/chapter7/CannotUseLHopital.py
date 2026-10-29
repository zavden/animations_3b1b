# ==============================================================================
# Scene:      CannotUseLHopital
# Source:     videos/_2017/eoc/chapter7.py (lines 2794-2834)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CannotUseLHopital.py CannotUseLHopital -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class CannotUseLHopital(TeacherStudentsScene):
    def construct(self):
        deriv = OldTex(
            "{d(e^x)", "\\over \\,", "dx}", "(", "x", ")", "=",
            "\\lim", "_{h", "\\to 0}",
            "{e^{", "x", "+", "h}", 
            "-", "e^", "x",
            "\\over \\,", "h}"
        )
        deriv.to_edge(UP)
        deriv.set_color_by_tex("x", RED)
        deriv.set_color_by_tex("dx", GREEN)
        deriv.set_color_by_tex("h", GREEN)
        deriv.set_color_by_tex("e^", YELLOW)

        self.play(
            Write(deriv),
            *it.chain(*[
                [pi.change_mode, "pondering", pi.look_at, deriv]
                for pi in self.get_pi_creatures()
            ])
        )
        self.wait()
        self.student_says(
            "Use L'Hôpital's rule!", 
            target_mode = "hooray"
        )
        self.wait()
        answer = OldTex(
            "\\text{That requires knowing }",
            "{d(e^x)", "\\over \\,", "dx}"
        )
        answer.set_color_by_tex("e^", YELLOW)
        answer.set_color_by_tex("dx", GREEN)
        self.teacher_says(
            answer,
            bubble_config = {"height" : 2.5},
            target_mode = "hesitant"
        )
        self.play_student_changes(*["confused"]*3)
        self.wait(3)
