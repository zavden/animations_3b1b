# ==============================================================================
# Scene:      MentionCommutativity
# Source:     videos/_2018/quaternions.py (lines 5867-5918)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionCommutativity.py MentionCommutativity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionCommutativity(TeacherStudentsScene):
    def construct(self):
        kwargs = {
            "tex_to_color_map": {
                "q": MAROON_B,
                "p": YELLOW,
                "i": GREEN,
                "j": RED,
                "k": BLUE,
            }
        }
        general_eq = OldTex("q \\cdot p \\ne p \\cdot q", **kwargs)
        general_eq.get_part_by_tex("\\ne").submobjects.reverse()
        ij_eq = OldTex("i \\cdot j = k", **kwargs)
        ji_eq = OldTex("j \\cdot i = -k", **kwargs)

        for mob in [general_eq, ij_eq, ji_eq]:
            mob.move_to(self.hold_up_spot, DOWN)

        words = OldTexText("Multiplication doesn't \\\\ commute")
        words.next_to(general_eq, UP, MED_LARGE_BUFF)
        words.shift_onto_screen()

        joke = OldTexText("Quaternions work from home")
        joke.scale(0.75)
        joke.to_corner(UL, MED_SMALL_BUFF)

        self.play(
            FadeInFromDown(general_eq),
            self.teacher.change, "raise_right_hand",
            self.change_students("erm", "confused", "sassy")
        )
        self.play(FadeIn(words, RIGHT))
        self.wait(2)
        self.play(
            ReplacementTransform(words, joke),
            general_eq.shift, UP,
            FadeInFromDown(ij_eq),
            self.change_students(*["pondering"] * 3)
        )
        self.look_at(self.screen)
        self.wait(3)
        self.play(
            FadeIn(ji_eq),
            LaggedStartMap(
                ApplyMethod, VGroup(ij_eq, general_eq),
                lambda m: (m.shift, UP),
                lag_ratio=0.8,
            )
        )
        self.look_at(self.screen)
        self.wait(5)
