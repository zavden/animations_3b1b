# ==============================================================================
# Scene:      WhereDidThatPictureComeFrom
# Source:     videos/_2026/print_gallery/supplements.py (lines 126-164)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhereDidThatPictureComeFrom.py WhereDidThatPictureComeFrom -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhereDidThatPictureComeFrom(TeacherStudentsScene):
    def construct(self):
        # Ask
        self.remove(self.background)
        morty = self.teacher
        stds = self.students

        self.play(
            stds[2].says("Where does that\n come from?", "raise_left_hand", bubble_direction=LEFT, look_at=self.screen),
            stds[0].change("thinking", self.screen),
            stds[1].change("hesitant", self.screen),
        )
        self.play(morty.change("tease"))
        self.wait(3)

        # Show the mathematicians
        frame = self.frame
        mathematicians = VGroup(
            PiCreature(color=GREY_C).flip(),
            PiCreature(color=GREY_D).flip(),
        )
        for pi in mathematicians:
            pi.body.insert_n_curves(100)
        mathematicians.arrange(RIGHT)
        mathematicians.next_to(morty, RIGHT, buff=4.0, aligned_edge=DOWN)

        self.play(
            frame.animate.set_x(10),
            stds[2].debubble(),
            morty.change("gracious", look_at=mathematicians.get_top()),
            mathematicians[0].change("hooray"),
            mathematicians[1].change("tease"),
            run_time=2
        )
        self.play(mathematicians[0].change("raise_right_hand"))
        self.play(Blink(mathematicians[0]))
        self.play(Blink(mathematicians[1]))
        self.wait()
        pass
