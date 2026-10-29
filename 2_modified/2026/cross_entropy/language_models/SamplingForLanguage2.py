# ==============================================================================
# Scene:      SamplingForLanguage2
# Source:     videos/_2026/cross_entropy/language_models.py (lines 515-550)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SamplingForLanguage2.py SamplingForLanguage2 -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - text_data/quotes.txt and training_data_examples.txt: original text and public-domain quotes (_lib/assets/generated/2026/cross_entropy/text_data/) instead of 3b1b's, which quoted copyrighted works
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from pathlib import Path

def get_training_text_examples(file_name="training_data_examples.txt"):
    data_file = Path(__file__).parent / "text_data" / file_name
    return data_file.read_text().splitlines()


class SamplingForLanguage2(InteractiveScene):
    def construct(self):
        # Test
        text = get_training_text_examples("rights_of_man.txt")[0][:500]
        text_mob = Text(text, font="Consolas")

        a_to_z = "".join([chr(n) for n in range(ord("a"), ord("z") + 1)])
        chars = sorted(list(set(text.lower() + a_to_z)))
        char_blocks = Square().get_grid(1, len(chars), buff=0)
        char_blocks.set_stroke(WHITE, 1)
        char_blocks.set_width(FRAME_WIDTH - 1)
        char_blocks.move_to(UP)
        char_syms = Text("_" + "".join(chars[1:]), font="Consolas", font_size=30)
        char_syms.move_to(char_blocks)
        for sym, block in zip(char_syms, char_blocks):
            sym.match_x(block)
            char_syms.add(sym)

        self.add(char_blocks, char_syms)
        self.add(text_mob)

        # Generate
        time_per_char = 1 / 15
        space_free_text = text.replace(" ", "").lower()
        for n in range(1, len(text_mob)):
            text_mob.set_fill(WHITE)
            text_mob[n].set_color(YELLOW)
            text_mob[:n + 1].set_opacity(1)
            text_mob[n + 1:].set_opacity(0)
            text_mob.shift(-text_mob[n].get_x() * RIGHT)
            char_indx = chars.index(space_free_text[n])
            char_blocks.set_fill(opacity=0)
            char_syms.set_fill(opacity=0.5)
            char_blocks[char_indx].set_fill(YELLOW, 0.5)
            char_syms[char_indx].set_fill(WHITE, 1)
            self.wait(time_per_char)
