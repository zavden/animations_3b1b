# ==============================================================================
# Scene:      CompressibilitOfText
# Source:     videos/_2026/cross_entropy/entropy.py (lines 91-242)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/next_char.py
#
# Run from this folder:
#     manimgl CompressibilitOfText.py CompressibilitOfText -w -m --fps 15
#
# Notes:
#   huffman_table.json (real wikitext counts) comes from the repo; with it the nanoGPT corpus is not needed.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import heapq
import json
import os
import pickle
import numpy as np
from collections import Counter
from functools import lru_cache


# ----- From _2026/cross_entropy/next_char.py -----

CHAR_ALPHABET = "abcdefghijklmnopqrstuvwxyz .,'!?"


NANOGPT_DIR = "/Users/grant/cs/nanoGPT"


HUFFMAN_TABLE_PATH = os.path.join(
    os.path.dirname(__file__), "huffman_table.json"
)


def _wiki_char_text() -> str:
    """Decode the nanoGPT wiki_char train.bin back into a string."""
    meta_path = f"{NANOGPT_DIR}/data/wiki_char/meta.pkl"
    bin_path = f"{NANOGPT_DIR}/data/wiki_char/train.bin"
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)
    itos = meta["itos"]
    ids = np.fromfile(bin_path, dtype=np.uint16)
    return "".join(itos[int(i)] for i in ids)


def build_huffman_table(
    alphabet: str = CHAR_ALPHABET,
    save_path: str | None = HUFFMAN_TABLE_PATH,
) -> dict[str, str]:
    """
    Build a Huffman code table for `alphabet` using character frequencies
    from the lowercased nanoGPT wiki_char training corpus. Characters not
    in `alphabet` are ignored. Returns a dict mapping char -> bitstring.
    If `save_path` is given, also writes the result as JSON (sorted by
    code length, then char).
    """
    text = _wiki_char_text().lower()
    counts = Counter(c for c in text if c in alphabet)
    # Ensure every alphabet char appears, so all are encodable
    for c in alphabet:
        counts.setdefault(c, 1)

    # Heap entries: (weight, tie_breaker, node). Node is either a
    # single-char string (leaf) or a (left, right) tuple.
    heap: list[tuple[int, int, object]] = []
    for i, (ch, w) in enumerate(counts.items()):
        heapq.heappush(heap, (w, i, ch))
    next_id = len(heap)
    while len(heap) > 1:
        w1, _, n1 = heapq.heappop(heap)
        w2, _, n2 = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next_id, (n1, n2)))
        next_id += 1
    root = heap[0][2]

    codes: dict[str, str] = {}

    def walk(node, prefix: str) -> None:
        if isinstance(node, str):
            codes[node] = prefix or "0"
            return
        left, right = node
        walk(left, prefix + "0")
        walk(right, prefix + "1")

    walk(root, "")

    if save_path is not None:
        ordered = dict(sorted(codes.items(), key=lambda kv: (len(kv[1]), kv[0])))
        payload = {
            "source": "nanoGPT/data/wiki_char/train.bin (lowercased)",
            "alphabet": alphabet,
            "total_chars_counted": sum(counts.values()),
            "counts": {c: counts[c] for c in ordered},
            "codes": ordered,
        }
        with open(save_path, "w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    return codes


@lru_cache(maxsize=1)
def load_huffman_table(alphabet: str = CHAR_ALPHABET) -> dict[str, str]:
    """
    Load the cached Huffman table from disk, building it if missing.
    Rebuilds if the cached alphabet doesn't match.
    """
    if os.path.exists(HUFFMAN_TABLE_PATH):
        with open(HUFFMAN_TABLE_PATH) as f:
            payload = json.load(f)
        if payload.get("alphabet") == alphabet:
            return payload["codes"]
    return build_huffman_table(alphabet)



# ----- From _2026/cross_entropy/entropy.py -----

def bit_string_mobject(
    bit_string: str,
    font: str = "Consolas",
    font_size: int = 48,
    colors: List[Colors] = [GREY_C, GREY_B]
):
    result = Text(bit_string, font=font, font_size=font_size)
    result["0"].set_color(colors[0])
    result["1"].set_color(colors[1])
    return result


def int_to_bit_string(n_bits, value=None, **kwargs):
    if value is None:
        value = np.random.randint(0, 2**n_bits)
    return bit_string_mobject(f"{value:0{n_bits}b}", **kwargs)


class CompressibilitOfText(InteractiveScene):
    def construct(self):
        # Set up
        rects = Rectangle().get_grid(6, 6, buff=0)
        rects.set_shape(FRAME_WIDTH - 1, 6)
        rects.to_edge(RIGHT, buff=0)
        rects.to_edge(DOWN, buff=MED_LARGE_BUFF)
        n_shown = len(rects)
        dots = Tex(R"\vdots")
        dots.to_edge(DOWN, buff=SMALL_BUFF)

        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
        huffman_table = load_huffman_table(alphabet)

        char_mobs = VGroup()
        ascii_mobs = VGroup()
        pre_encodings = VGroup()
        huffman_mobs = VGroup()
        for char, rect in zip(alphabet, rects):
            char_mob = Text(char.lower() + ":")
            char_mob.shift(rect.get_left() - char_mob[1].get_right())
            ascii_mob = bit_string_mobject(f"{ord(char):08b}")
            ascii_mob.set_height(0.2)
            ascii_mob.next_to(char_mob[1], RIGHT, SMALL_BUFF, DOWN)

            pre_encoding = VGroup(
                int_to_bit_string(int(a)).match_height(ascii_mob).move_to(ascii_mob, LEFT)
                for a in np.linspace(1, 8, 30)
            )
            pre_encoding.add(*ascii_mob.copy().replicate(3))

            huffman_mob = bit_string_mobject(huffman_table[char.lower()])
            huffman_mob.match_height(ascii_mob)
            huffman_mob.set_max_width(ascii_mob.get_width())
            huffman_mob.move_to(ascii_mob, LEFT)

            char_mobs.add(char_mob)
            ascii_mobs.add(ascii_mob)
            pre_encodings.add(pre_encoding)
            huffman_mobs.add(huffman_mob)

        # Set up titles and bpc labels
        right_arrow = Tex(R"\rightarrow")
        right_arrow.to_edge(UP, buff=MED_LARGE_BUFF)
        right_arrow.stretch(1.5, 0)

        bpc_label = Tex(R"\sim 8.0 \text{bits} / \text{ch}")
        squiggle = bpc_label[0]
        squiggle.set_opacity(0)
        bpc_dec = bpc_label.make_number_changeable("8.0")
        bpc_dec.shift(0.2 * LEFT)
        bpc_dec.set_color(BLUE)
        bpc_label.next_to(right_arrow, RIGHT, SMALL_BUFF)

        titles = VGroup(
            Text("ASCII"),
            Text("Huffman"),
            Text("Neural methods"),
        )
        for title in titles:
            title.next_to(right_arrow, LEFT)
            title.align_to(bpc_dec, DOWN)

        # Show ascii table
        self.add(char_mobs, right_arrow, dots, bpc_label)
        self.play(
            Write(titles[0]),
            LaggedStartMap(ShowSubmobjectsOneByOne, pre_encodings, run_time=2, lag_ratio=0.01),
        )
        self.remove(pre_encodings)
        self.add(ascii_mobs)
        self.wait()

        # Show Huffman table
        self.remove(ascii_mobs)
        self.play(
            LaggedStart(
                (TransformFromCopy(ascii_mob, huffman_mob)
                for ascii_mob, huffman_mob in zip(ascii_mobs, huffman_mobs)),
                lag_ratio=0.05,
                run_time=2,
            ),
            LaggedStart(
                FadeIn(titles[1], 0.35 * UP),
                FadeOut(titles[0], 0.35 * UP),
                lag_ratio=0.1,
                run_time=1,
            ),
            ChangeDecimalToValue(bpc_dec, 4.2),
            squiggle.animate.set_opacity(1).shift(SMALL_BUFF * LEFT),
            right_arrow.animate.shift(SMALL_BUFF * LEFT)
        )
        self.wait()

        # Collapse to an example phrase
        phrase = Text("""
            It was the best of times, it was the worst of times,
            it was the age of wisdom, it was the age of foolishness...
        """, alignment="LEFT")
        phrase.move_to(rects, UP).shift(DOWN)
        phrase.set_fill(GREY_A)
        arrow = Vector(1.25 * DOWN, fill_color=BLUE, thickness=5)
        arrow.next_to(phrase, DOWN, buff=SMALL_BUFF)
        bits = bit_string_mobject("".join([random.choice("01") for n in range(len(phrase))]))
        for n in range(30, len(phrase), 30):
            bits[n:].next_to(bits[n - 30], DOWN, SMALL_BUFF, LEFT)
        bits.refresh_bounding_box()
        bits.next_to(arrow, DOWN)
        bits.set_x(0)

        colons = VGroup()
        chars = VGroup()
        for char_mob in char_mobs:
            char, colon = char_mob
            colons.add(colon)
            chars.add(char)

            char.target = char.generate_target()
            ch = char_mob.get_text()[0]

            trg = phrase[ch]
            if len(trg) > 0:
                char.target.replace(trg[0])
                char.target.match_color(trg[0])
            else:
                char.target.set_opacity(0).move_to(phrase)

        self.play(
            FadeIn(phrase, lag_ratio=0.01, run_time=2),
            LaggedStart(
                FadeIn(titles[2], 0.35 * UP),
                FadeOut(titles[1], 0.35 * UP),
                lag_ratio=0.1,
                run_time=1,
            ),
            FadeOut(dots),
            FadeOut(huffman_mobs, scale=0.5, lag_ratio=0.01),
            FadeOut(colons, scale=0.5, lag_ratio=0.1),
            LaggedStartMap(MoveToTarget, chars, lag_ratio=0.001, run_time=2),
            ChangeDecimalToValue(bpc_dec, +1.1),
        )
        self.play(
            GrowArrow(arrow),
            LaggedStart(
                (FlashAround(c, buff=0.05, time_width=1.5, stroke_width=2)
                for c in phrase),
                lag_ratio=0.01,
                run_time=3
            ),
            ShowIncreasingSubsets(bits, run_time=3),
        )
        self.wait()
