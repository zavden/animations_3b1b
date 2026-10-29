# ==============================================================================
# Scene:      AskAboutAllTheGroups
# Source:     videos/_2020/monster.py (lines 2962-3079)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutAllTheGroups.py AskAboutAllTheGroups -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutAllTheGroups(TeacherStudentsScene):
    def construct(self):
        # Ask
        question = OldTexText("What are all the groups", "?")
        self.teacher_holds_up(question)
        self.play_student_changes("pondering", "thinking", "erm")
        self.wait(2)

        question.generate_target()
        question.target.to_corner(UL)
        self.teacher_says(
            "Now you can\\\\ask something\\\\more sophisticated.",
            target_mode="hooray",
            added_anims=[
                MoveToTarget(question, run_time=2),
                self.change_students(
                    "erm", "pondering", "pondering",
                    look_at=question.target
                )
            ]
        )
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(
                self.teacher, target_mode="tease",
                look_at=question.get_right(),
            ),
            question.set_x, 0,
        )

        # Add up to isomorphism
        caveat = OldTexText("up to \\emph{isomorphism}")
        caveat.next_to(question, DOWN)
        caveat.set_color(YELLOW)

        self.play(
            Write(caveat, run_time=1),
            question[1].next_to, caveat[0][-1], RIGHT, SMALL_BUFF, DOWN,
            question[1].match_color, caveat,
            self.change_students(*3 * ["thinking"], look_at=question)
        )
        question.add(caveat)
        self.wait(2)
        self.look_at(self.screen)
        self.wait(2)
        self.look_at(question)

        # Alt question
        sym_question = OldTexText("What are all the\\\\", "symmetric", " things", "?")
        self.teacher_holds_up(sym_question)

        cross = Cross(sym_question)
        self.look_at(
            cross,
            added_anims=[
                ShowCreation(cross),
                self.change_students("erm", "sassy", "hesitant")
            ]
        )
        self.wait()

        abs_question = OldTexText("What are all the", " \\emph{ways}\\\\", "things ", "can be ", "symmetric", "?")
        new_words = VGroup(abs_question[1], abs_question[3])
        new_words.match_color(caveat)
        abs_question.move_to(sym_question)
        abs_question.shift_onto_screen()
        self.play(
            *[
                ReplacementTransform(sym_question[i], abs_question[j], path_arc=10 * DEGREES)
                for i, j in [(0, 0), (1, 4), (2, 2), (3, 5)]
            ],
            FadeOut(cross),
            self.change_students("happy", "thinking", "tease"),
        )
        self.play(
            self.teacher.change, "speaking", abs_question,
            Write(new_words),
        )
        self.look_at(abs_question)
        self.wait(2)

        # Formula
        suggestions = VGroup(*[
            OldTexText("Some ", word, "?", tex_to_color_map={word: color})
            for word, color in [
                ("formula", RED),
                ("procedure", MAROON_B),
                ("algorithm", PINK),
            ]
        ])
        for words in suggestions:
            words.move_to(abs_question, UP)
            words.to_edge(LEFT, buff=LARGE_BUFF)

        self.play(
            FadeIn(suggestions[0], DOWN),
            self.change_students(*3 * ["pondering"], look_at=suggestions),
            self.teacher.change, "happy",
        )
        self.wait()
        for words1, words2 in zip(suggestions, suggestions[1:]):
            self.play(
                FadeOut(words1[1], UP),
                FadeIn(words2[1], DOWN),
                ReplacementTransform(words1[2], words2[2])
            )
            self.remove(words1)
            self.add(words2)
            self.wait()
        self.wait(3)
        self.play(
            FadeOut(
                VGroup(question, abs_question, suggestions[-1]),
                0.5 * DOWN,
                lag_ratio=0.02,
                run_time=2,
            )
        )
