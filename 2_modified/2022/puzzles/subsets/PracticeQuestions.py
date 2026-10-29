# ==============================================================================
# Scene:      PracticeQuestions
# Source:     videos/_2022/puzzles/subsets.py (lines 4217-4233)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PracticeQuestions.py PracticeQuestions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - load_mobject('Question1..4.mob') (files from Grant's Dropbox) -> four placeholder practice questions (Text), one per quadrant
# ==============================================================================

from manim_imports_ext import *

class PracticeQuestions(InteractiveScene):
    def construct(self):
        # Blah
        division = VGroup(Line().set_width(FRAME_WIDTH), Line(UP, DOWN).set_height(FRAME_HEIGHT))
        division.set_stroke(WHITE, 1)
        self.disable_interaction(division)
        self.add(division)

        # CHANGE: Question1..4.mob (mobjects saved in Grant's Dropbox, of unknown content) are replaced by four
        # placeholder practice questions, one per quadrant
        questions = VGroup(*(
            Text(q, font_size=30, alignment="LEFT").set_max_width(FRAME_WIDTH / 2 - 1.0)
            for q in [
                "1. Find the number of subsets of\n{1, 2, ..., 2000} whose sum is divisible by 7",
                "2. How many subsets of {1, ..., 100}\nhave a sum divisible by 4?",
                "3. Find the sum of the products of\nall pairs of 5th roots of unity",
                "4. What is the generating function for\nsubsets of the primes?",
            ]
        ))
        for q, vect in zip(questions, [UL, UR, DL, DR]):
            q.move_to(vect * np.array([FRAME_WIDTH / 4, FRAME_HEIGHT / 4, 0]))

        self.play(LaggedStartMap(FadeIn, questions, lag_ratio=0.25, run_time=2))
        self.wait()
