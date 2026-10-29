# ==============================================================================
# Scene:      BetterTranslation
# Source:     videos/_2018/uncertainty.py (lines 4205-4272)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BetterTranslation.py BetterTranslation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class BetterTranslation(TeacherStudentsScene):
    def construct(self):
        english_term = OldTexText("Uncertainty principle")
        german_word = OldTexText("Unschärferelation")
        translation = OldTexText("Unsharpness relation")

        to_german_words = OldTexText("In German")
        to_german_words.scale(0.5)
        to_german_arrow = Vector(DOWN, color = WHITE, buff = SMALL_BUFF)
        to_german_words.next_to(to_german_arrow, RIGHT, SMALL_BUFF)
        to_german_words.set_color(YELLOW)
        to_german_group = VGroup(to_german_arrow, to_german_words)

        translation_words = OldTexText("Literal translation")
        translation_words.scale(0.5)
        translation_arrow = Vector(DOWN, color = WHITE, buff = SMALL_BUFF)
        translation_words.next_to(translation_arrow, LEFT, SMALL_BUFF)
        translation_words.set_color(YELLOW)
        translation_group = VGroup(translation_arrow, translation_words)

        english_term.next_to(self.teacher, UP+LEFT)
        english_term.save_state()
        english_term.shift(DOWN)
        english_term.fade(1)
        self.play(
            english_term.restore,
            self.change_students(*["pondering"]*3)
        )
        self.wait()

        german_word.move_to(english_term)
        to_german_group.next_to(
            german_word, UP,
            submobject_to_align = to_german_arrow
        )
        self.play(
            self.teacher.change, "raise_right_hand", 
            english_term.next_to, to_german_arrow, UP
        )
        self.play(
            GrowArrow(to_german_arrow),
            FadeIn(to_german_words),
            ReplacementTransform(
                english_term.copy().fade(1),
                german_word
            )
        )
        self.wait(2)

        group = VGroup(english_term, to_german_group, german_word)
        translation.move_to(german_word)
        translation_group.next_to(
            german_word, UP,
            submobject_to_align = translation_arrow
        )
        self.play(
            group.next_to, translation_arrow, UP,
        )
        self.play(
            GrowArrow(translation_arrow),
            FadeIn(translation_words),
            ReplacementTransform(
                german_word.copy().fade(1),
                translation
            )
        )
        self.play_student_changes(*["happy"]*3)
        self.wait(2)
