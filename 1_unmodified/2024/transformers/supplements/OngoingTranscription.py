# ==============================================================================
# Scene:      OngoingTranscription
# Source:     videos/_2024/transformers/supplements.py (lines 1133-1140)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py
#
# Run from this folder:
#     manimgl OngoingTranscription.py OngoingTranscription -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/embedding.py -----

def break_into_pieces(phrase_mob: Text, offsets: list[int]):
    phrase = phrase_mob.get_string()
    lhs = offsets
    rhs = [*offsets[1:], len(phrase)]
    result = []
    for lh, rh in zip(lhs, rhs):
        substr = phrase[lh:rh]
        start = phrase_mob.substr_to_path_count(phrase[:lh])
        end = start + phrase_mob.substr_to_path_count(substr)
        result.append(phrase_mob[start:end])
    return VGroup(*result)


def break_into_words(phrase_mob):
    offsets = [m.start() for m in re.finditer(" ", phrase_mob.get_string())]
    return break_into_pieces(phrase_mob, [0, *offsets])



# ----- From _2024/transformers/supplements.py -----

class OngoingTranscription(InteractiveScene):
    def construct(self):
        phrase = Text("or maybe audio input of speech, and an ongoing transcription")
        words = break_into_words(phrase)
        for word in words:
            self.add(word)
            self.wait(0.1 * len(word))
        self.wait()
