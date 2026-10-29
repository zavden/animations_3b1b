# ==============================================================================
# Scene:      FlashThroughTextData2
# Source:     videos/_2024/transformers/ml_basics.py (lines 330-356)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl FlashThroughTextData2.py FlashThroughTextData2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR now points to _lib/data (get_directories()["data"]) instead of Grant's output folder (GloVe, placeholder texts)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from pathlib import Path


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")


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


def read_in_book(name="tale_of_two_cities"):
    return Path(DATA_DIR, name).with_suffix(".txt").read_text()



# ----- From _2024/transformers/ml_basics.py -----

class FlashThroughTextData2(InteractiveScene):
    n_examples = 200
    time_per_example = 0.1
    window_size = 50
    line_len = 35
    ul_point = 5 * LEFT + 3 * UP

    def construct(self):
        # Test
        totc = read_in_book(name="tale_of_two_cities")
        words = re.split(r"\s", totc)
        words = list(filter(lambda s: s, words))

        for n in range(self.n_examples):
            index = random.randint(0, len(words) - self.window_size)
            window = words[index:index + self.window_size]
            phrase = get_paragraph(window, line_len=self.line_len)
            phrase.move_to(self.ul_point, UL)

            word = phrase[window[-1]][-1]
            rect = SurroundingRectangle(word, buff=0.1)
            rect.set_stroke(YELLOW, 2)
            rect.set_fill(YELLOW, 0.5)

            self.add(phrase)
            self.wait(self.time_per_example)
            self.remove(phrase)
