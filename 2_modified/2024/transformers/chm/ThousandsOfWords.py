# ==============================================================================
# Scene:      ThousandsOfWords
# Source:     videos/_2024/transformers/chm.py (lines 1257-1270)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ThousandsOfWords.py ThousandsOfWords -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's Dropbox path to tale_of_two_cities.txt points to _lib/data/2024/transformers/data/
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from pathlib import Path


# ----- From _2024/transformers/helpers.py -----

def get_paragraph(words, line_len=40, font_size=48):
    """
    Handle word wrapping
    """
    words = list(map(str.strip, words))
    word_lens = list(map(len, words))
    lines = []
    lh, rh = 0, 0
    while rh < len(words):
        rh += 1
        if sum(word_lens[lh:rh]) > line_len:
            rh -= 1
            lines.append(words[lh:rh])
            lh = rh
    lines.append(words[lh:])
    text = "\n".join([" ".join(line).strip() for line in lines])
    return Text(text, alignment="LEFT", font_size=font_size)



# ----- From _2024/transformers/chm.py -----

class ThousandsOfWords(InteractiveScene):
    def construct(self):
        # Find passage
        # CHANGE: the book lives in _lib/data (in the original, in Grant's Dropbox)
        file = Path(get_directories()["data"], "2024/transformers/data/tale_of_two_cities.txt")
        novel = file.read_text()
        start_index = novel.index("It was the best of times")
        end_index = novel.index("There were a king with a large jaw")

        # Add text
        passage = novel[start_index:start_index + 5000].replace("\n", " ")
        text = get_paragraph(passage.split(" "), line_len=150)
        text.set_width(14)
        text.to_edge(UP)
        self.add(text)
