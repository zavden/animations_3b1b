# ==============================================================================
# Scene:      WhatAreFractals
# Source:     videos/_2017/fractal_dimension.py (lines 130-159)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WhatAreFractals.py WhatAreFractals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - width is a bubble parameter, not an animation kwarg
# ==============================================================================

from manim_imports_ext import *

class WhatAreFractals(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But what \\emph{is} a fractal?",
            # CHANGE: width is a bubble parameter, not an animation kwarg
            index = 2,
            bubble_config = {"width": 6}
        )
        self.play_student_changes("thinking", "pondering", None)
        self.wait()

        name = OldTexText("Benoit Mandelbrot")
        name.to_corner(UP+LEFT)
        # picture = Rectangle(height = 4, width = 3)
        picture = ImageMobject("Mandelbrot")
        picture.set_height(4)
        picture.next_to(name, DOWN)
        self.play(
            Write(name, run_time = 2),
            FadeIn(picture),
            *[
                ApplyMethod(pi.look_at, name)
                for pi in self.get_pi_creatures()
            ]
        )
        self.wait(2)
        question = OldTexText("Aren't they", "self-similar", "shapes?")
        question.set_color_by_tex("self-similar", YELLOW)
        self.student_says(question)
        self.play(self.get_teacher().change_mode, "happy")
        self.wait(2)
