# ==============================================================================
# Scene:      AskWhyAreTheyTheSame
# Source:     videos/_2018/dandelin.py (lines 730-804)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhyAreTheyTheSame.py AskWhyAreTheyTheSame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhyAreTheyTheSame(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.student_says(
            "Why on earth \\\\ are these the same?",
            index=2,
            target_mode="sassy",
            bubble_config={"direction": LEFT}
        )
        bubble = self.students[2].bubble
        self.play(
            morty.change, "awe",
            self.change_students("confused", "confused", "sassy")
        )
        self.look_at(self.screen)
        self.wait(3)
        self.play(morty.change, "thinking", self.screen)
        self.play_student_changes("maybe", "erm", "confused")
        self.look_at(self.screen)
        self.wait(3)

        baby_morty = BabyPiCreature()
        baby_morty.match_style(morty)
        baby_morty.to_corner(DL)

        self.play(
            FadeOut(bubble),
            FadeOut(bubble.content),
            LaggedStartMap(
                FadeOutAndShift, self.students,
                lambda m: (m, 3 * DOWN),
            ),
            ReplacementTransform(
                morty, baby_morty,
                path_arc=30 * DEGREES,
                run_time=2,
            )
        )
        self.pi_creatures = VGroup(baby_morty)
        bubble = ThoughtBubble(height=6, width=7)
        bubble.set_fill(GREY_D, 0.5)
        bubble.pin_to(baby_morty)

        egg = Circle(radius=0.4)
        egg.stretch(0.75, 1)
        egg.move_to(RIGHT)
        egg.apply_function(
            lambda p: np.array([
                p[0], p[0] * p[1], p[2]
            ])
        )
        egg.flip()
        egg.set_width(3)
        egg.set_stroke(RED, 5)
        egg.move_to(bubble.get_bubble_center())

        self.play(baby_morty.change, "confused", 2 * DOWN)
        self.wait(2)
        self.play(
            baby_morty.change, "thinking",
            LaggedStartMap(DrawBorderThenFill, bubble)
        )
        self.play(ShowCreation(egg))
        self.wait(3)

        bubble_group = VGroup(bubble, egg)
        self.play(
            ApplyMethod(
                bubble_group.shift, FRAME_WIDTH * LEFT,
                rate_func=running_start,
            ),
            baby_morty.change, "awe"
        )
        self.play(Blink(baby_morty))
        self.wait()
