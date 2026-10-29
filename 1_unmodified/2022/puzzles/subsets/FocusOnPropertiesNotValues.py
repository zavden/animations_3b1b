# ==============================================================================
# Scene:      FocusOnPropertiesNotValues
# Source:     videos/_2022/puzzles/subsets.py (lines 5036-5060)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FocusOnPropertiesNotValues.py FocusOnPropertiesNotValues -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FocusOnPropertiesNotValues(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        kw = dict(
            tex_to_color_map={"\\zeta": YELLOW}
        )
        words = VGroup(
            Tex("\\text{Don't worry about the}\\\\ \\text{numerical value of } \\zeta", **kw),
            Tex("\\text{Focus on properties}\\\\ \\text{of } \\{\\zeta^1, \\zeta^2, \\zeta^3, \\zeta^4\\, \\zeta^5\\}", **kw),
        )
        words.move_to(self.hold_up_spot, DOWN).shift_onto_screen()

        self.play(
            morty.change('raise_right_hand'),
            self.change_students("erm", "confused", "hesitant", look_at=words[0]),
            FadeIn(words[0], UP)
        )
        self.wait(3)
        self.play(
            morty.change("hooray", words[1]),
            FadeIn(words[1], UP),
            words[0].animate.shift(2.5 * UP),
            self.change_students("tease", "happy", "tease")
        )
        self.wait(4)
