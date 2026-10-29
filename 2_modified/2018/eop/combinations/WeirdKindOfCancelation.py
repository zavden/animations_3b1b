# ==============================================================================
# Scene:      WeirdKindOfCancelation
# Source:     videos/_2018/eop/combinations.py (lines 3158-3247)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WeirdKindOfCancelation.py WeirdKindOfCancelation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL OldTex/OldTexText keep "\\{ \\}" as one piece: build the two braces from separate strings so "lb, rb = braces" unpacks (Cairo split glyphs)
# ==============================================================================

from manim_imports_ext import *

class WeirdKindOfCancelation(TeacherStudentsScene):
    def construct(self):
        fraction = OldTex(
            "{5 \\cdot 4 \\cdot 3", 
            "\\text{ ordered}", "\\text{ triplets}",
            "\\over",
            "1 \\cdot 2 \\cdot 3", "\\text{ orderings \\;\\qquad}}"
        )
        top_numbers, ordered, triplets, frac_line, bottom_numbers, orderings = fraction
        for mob in top_numbers, bottom_numbers:
            mob.set_color_by_gradient(GREEN, YELLOW)
        fraction.next_to(self.teacher, UP+LEFT)

        names = VGroup(*list(map(TexText, [
            "Ali", "Ben", "Cam", "Denis", "Evan"
        ])))
        names.arrange(RIGHT)
        names.to_edge(UP, buff = LARGE_BUFF)
        names.save_state()
        # CHANGE: GL keeps "\{ \}" as a single piece; build the two braces from separate strings so lb, rb unpack as in Cairo
        lb, rb = braces = OldTex("\\{", "\\}")
        braces.scale(2)
        lb.next_to(names, LEFT, SMALL_BUFF)
        rb.next_to(names, RIGHT, SMALL_BUFF)

        chosen_names = VGroup(*random.sample(names, 3))
        chosen_names.generate_target()
        chosen_names.target.arrange(RIGHT)
        chosen_names.target.next_to(top_numbers, UP, MED_LARGE_BUFF)
        for name, name_target in zip(chosen_names, chosen_names.target):
            name.target = name_target

        self.teacher_says("It's like unit cancellation.")
        self.play_student_changes(*["confused"]*3)
        self.play(
            RemovePiCreatureBubble(
                self.teacher, target_mode = "raise_right_hand"
            ),
            LaggedStartMap(FadeIn, fraction, run_time = 1),
            FadeIn(braces),
            LaggedStartMap(FadeIn, names)
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = fraction
        )

        #Go through numerators
        for num, name in zip(top_numbers[::2], chosen_names):
            rect = SurroundingRectangle(num)
            name.target.set_color(num.get_color())
            self.play(
                ShowCreationThenDestruction(rect),
                MoveToTarget(name),
            )
        self.wait(2)

        #Go through denominators
        permutations = list(it.permutations(list(range(3))))[1:]

        self.shuffle(chosen_names, permutations[:2])
        self.play(LaggedStartMap(
            ShowCreationThenDestruction,
            VGroup(*list(map(SurroundingRectangle, bottom_numbers[::2])))
        ))
        self.shuffle(chosen_names, permutations[2:])
        self.wait()

        #Show cancelation
        top_cross = Cross(ordered)
        bottom_cross = Cross(orderings)

        self.play(
            ShowCreation(top_cross),
            self.teacher.change, "maybe",
        )
        self.play(ShowCreation(bottom_cross))
        self.play_student_changes(*["happy"]*3)
        self.wait(3)

    ###

    def shuffle(self, mobject, permutations):
        for permutation in permutations:
            self.play(*[
                ApplyMethod(
                    m.move_to, mobject[i].get_center(),
                    path_arc = np.pi,
                )
                for i, m in zip(permutation, mobject)
            ])
