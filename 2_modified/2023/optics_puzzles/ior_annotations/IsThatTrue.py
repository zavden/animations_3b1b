# ==============================================================================
# Scene:      IsThatTrue
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 664-728)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IsThatTrue.py IsThatTrue -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - self.change_students(look_at=label) (without modes) creates an empty LaggedStart and AnimationGroup() with no arguments fails in this manimgl (IndexError); the call was a no-op, it was removed
# ==============================================================================

from manim_imports_ext import *

EQUATION_T2C = {
    R"\vec{\textbf{x}}(t)": RED,
    R"\vec{\textbf{F}}(t)": YELLOW,
    R"\vec{\textbf{a}}(t)": YELLOW,
    R"\frac{d^2 \vec{\textbf{x}}}{dt^2}(t) ": YELLOW,
    R"\vec{\textbf{E}}_0": BLUE,
    R"\omega_r": PINK,
    R"\omega_l": TEAL,
}


class IsThatTrue(TeacherStudentsScene):
    def construct(self):
        # Ask
        stds = self.students
        morty = self.teacher
        law = Tex(R"\vec{\textbf{F}}(t) = -k \vec{\textbf{x}}(t)", t2c=EQUATION_T2C)
        law.move_to(self.hold_up_spot, DOWN)
        morty.change_mode("raise_right_hand")
        self.add(law)
        self.play(
            stds[0].change("pondering", self.screen),
            stds[1].says("Is that accurate?", mode="sassy", look_at=self.screen),
            stds[2].change("erm", self.screen),
        )
        self.wait(2)

        # Answer
        self.play(
            morty.says(TexText(
                R"For small $\vec{\textbf{x}}$, \\ accurate enough",
                t2c={R"$\vec{\textbf{x}}$": RED}
            )),
            self.change_students("thinking", "erm", "happy", look_at=morty.eyes),
            law.animate.to_edge(UP),
        )
        self.wait()

        # Name restoring force
        label = TexText("``Linear restoring force''")
        label.next_to(law, DOWN)
        self.play(
            FadeInFromPoint(label, morty.get_corner(UL)),
            # CHANGE: change_students without modes creates an empty LaggedStart and AnimationGroup() with no arguments fails with IndexError (composition.py:38, args[0]); in the original version it was an empty animation (it did nothing),
            # so self.change_students(look_at=label) is removed,
            morty.debubble("raise_right_hand", look_at=label),
            stds[1].debubble("pondering", look_at=label),
        )
        self.wait(2)

        # True law
        group = VGroup(law, label)
        true_law = Tex(
            R"""
            \text{True force: }
            F = -k x + c_2 x^2 + c_3 x^3 + c_4 x^4 + \cdots
            """,
            t2c={"F": YELLOW, "x": RED},
            font_size=60
        )
        true_law.move_to(UP)
        rect = SurroundingRectangle(true_law["F = -k x"], buff=0.25)
        rect.set_stroke(BLUE, 1)

        self.play(
            group.animate.set_height(1).to_corner(UR),
            FadeIn(true_law, lag_ratio=0.1, run_time=2),
            morty.change("hesitant"),
            self.change_students("pondering", "pondering", "pondering", look_at=true_law)
        )
        self.wait(2)
        self.play(
            ShowCreation(rect),
            true_law[R" + c_2 x^2 + c_3 x^3 + c_4 x^4 + \cdots"].animate.set_opacity(0.2),
            morty.change("tease"),
        )
        self.wait(2)
