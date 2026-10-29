# ==============================================================================
# Scene:      NameTheFundamentalTheorem
# Source:     videos/_2017/eoc/old_chapter1.py (lines 2394-2424)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameTheFundamentalTheorem.py NameTheFundamentalTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NameTheFundamentalTheorem(TeacherStudentsScene):
    def construct(self):
        symbols = OldTex(
            "\\frac{d}{dx} \\int_0^x f(t)dt = f(x)",
        )
        symbols.to_corner(UP+LEFT)
        brace = Brace(symbols)
        abstract = brace.get_text("Abstract version")
        self.add(symbols)
        self.play(
            GrowFromCenter(brace),
            Write(abstract),
            *[
                ApplyMethod(pi.look_at, symbols)
                for pi in self.get_pi_creatures()
            ]
        )
        self.play_student_changes("pondering", "confused", "erm")
        self.random_blink()
        self.teacher_says("""
            This is known as
            the ``fundamental 
            theorem of calculus''
        """, width = 5, height = 5, target_mode = "hooray")
        self.random_blink(3)
        self.teacher_says("""
            We'll get here
            in due time.
        """)
        self.play_student_changes(*["happy"]*3)
        self.wait(2)
