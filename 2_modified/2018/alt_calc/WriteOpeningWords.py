# ==============================================================================
# Scene:      WriteOpeningWords
# Source:     videos/_2018/alt_calc.py (lines 446-471)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteOpeningWords.py WriteOpeningWords -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the empty "\\Large" part has no glyphs in GL (Cairo gave it a VectorizedPoint), so len(word) was 0 and lag_ratio divided by zero
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class WriteOpeningWords(Scene):
    def construct(self):
        raw_string1 = "Dear calculus student,"
        raw_string2 = "You're about to go through your first course. Like " + \
                      "any new topic, it will take some hard work to understand,"
        words1, words2 = [
            OldTexText("\\Large", *rs.split(" "))
            for rs in (raw_string1, raw_string2)
        ]
        words1.next_to(words2, UP, aligned_edge=LEFT, buff=LARGE_BUFF)
        # CHANGE: the empty "\\Large" part has no glyphs in GL (Cairo gave it a VectorizedPoint), so len(word) was 0 and lag_ratio divided by zero
        words = VGroup(*[word for word in it.chain(words1, words2) if len(word) > 0])
        words.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)
        words.to_edge(UP)

        letter_wait = 0.05
        word_wait = 2 * letter_wait
        comma_wait = 5 * letter_wait
        for word in words:
            self.play(LaggedStartMap(
                FadeIn, word,
                run_time=len(word) * letter_wait,
                lag_ratio=1.5 / len(word)
            ))
            self.wait(word_wait)
            if word.get_tex()[-1] == ",":
                self.wait(comma_wait)
