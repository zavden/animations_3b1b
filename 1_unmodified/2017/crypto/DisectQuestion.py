# ==============================================================================
# Scene:      DisectQuestion
# Source:     videos/_2017/crypto.py (lines 182-245)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DisectQuestion.py DisectQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DisectQuestion(TeacherStudentsScene):
    def construct(self):
        self.hold_up_question()
        self.list_topics()
        self.isolate_you()

    def hold_up_question(self):
        question = OldTexText(
            "What does it mean to", "have", "a", "Bitcoin?"
        )
        question.set_color_by_tex("have", YELLOW)
        question.next_to(self.teacher, UP)
        question.to_edge(RIGHT, buff = LARGE_BUFF)
        question.save_state()
        question.shift(DOWN)
        question.set_fill(opacity = 0)

        self.play(
            self.teacher.change, "raise_right_hand",
            question.restore
        )
        self.play_student_changes(*["pondering"]*3)
        self.wait()

        self.bitcoin_word = question.get_part_by_tex("Bitcoin")

    def list_topics(self):
        topics = OldTexText(
            "Digital signatures, ",
            "Proof of work, ",
            "Cryptographic hash functions, \\dots"
        )
        topics.set_width(FRAME_WIDTH - LARGE_BUFF)
        topics.to_edge(UP)
        topics.set_color_by_tex("Digital", BLUE)
        topics.set_color_by_tex("Proof", GREEN)
        topics.set_color_by_tex("hash", YELLOW)

        for word in topics:
            anims = [Write(word, run_time = 1)]
            self.play_student_changes(
                *["confused"]*3,
                added_anims = anims,
                look_at = word
            )

    def isolate_you(self):
        self.pi_creatures = VGroup()
        you = self.students[1]
        rect = FullScreenFadeRectangle()
        words = OldTexText("Invent your own")
        arrow = Arrow(UP, DOWN)
        arrow.next_to(you, UP)
        words.next_to(arrow, UP)

        self.revert_to_original_skipping_status()
        self.play(FadeIn(rect), Animation(you))
        self.play(
            Write(words),
            ShowCreation(arrow),
            you.change, "erm", words
        )
        self.play(Blink(you))
        self.wait()
