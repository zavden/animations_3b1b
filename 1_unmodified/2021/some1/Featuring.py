# ==============================================================================
# Scene:      Featuring
# Source:     videos/_2021/some1.py (lines 116-144)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Featuring.py Featuring -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_tripple_underline(mobject, buff=0.1):
    ul1 = Underline(mobject, buff=buff).set_stroke(BLUE_C, 3)
    ul2 = Underline(ul1).scale(0.9).set_stroke(BLUE_D, 2)
    ul3 = Underline(ul2).scale(0.9).set_stroke(BLUE_E, 1)
    return VGroup(ul1, ul2, ul3)


class Featuring(TeacherStudentsScene):
    def construct(self):
        screen = ScreenRectangle()
        screen.set_height(4)
        screen.to_corner(UL)
        screen.set_stroke(WHITE, 2)
        screen.set_fill(BLACK, 1)

        self.add(screen)

        words = OldTexText("Your work here")
        words.set_width(screen.get_width() - 1)
        words.move_to(screen)

        self.play(
            self.teacher.change("tease"),
            self.change_students(*3 * ["hooray"], look_at=screen),
            FadeIn(screen, UP)
        )
        self.play(Write(words))
        self.play(ShowCreation(get_tripple_underline(words)))
        self.wait(5)
        self.student_says(
            OldTexText("Anything\\\\else?"),
            target_mode="raise_left_hand",
            look_at=self.teacher,
        )
        self.play(self.teacher.change("sassy"))
        self.wait(2)
