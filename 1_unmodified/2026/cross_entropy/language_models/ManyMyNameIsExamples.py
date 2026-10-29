# ==============================================================================
# Scene:      ManyMyNameIsExamples
# Source:     videos/_2026/cross_entropy/language_models.py (lines 1962-1999)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py, _2026/cross_entropy/next_char.py
#
# Run from this folder:
#     manimgl ManyMyNameIsExamples.py ManyMyNameIsExamples -w -m --fps 15
#
# Extra packages installed in the venv: torch, tiktoken
#
# Notes:
#   Uses the real cache of Qwen2.5-0.5B completions (qwen_completions_713b01ef65.json, from the repo): the model is not needed.
#   tiktoken downloads the GPT-2 BPE vocabulary (not model weights) the first time and caches it; internet is needed that one time.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import hashlib
import json
import os
import torch
import tiktoken


# ----- From _2026/cross_entropy/next_char.py -----

_qwen_tokenizer = None


_qwen_model = None


# Modern (2024) open-source stand-in for GPT-2. At ~0.5B params it is a few
# times larger than GPT-2 base (124M), but still small enough to run on CPU,
# and it uses a byte-level BPE tokenizer analogous to GPT-2's. This is the
# *base* model (raw next-token prediction over natural text), matching how the
# gpt2_* functions above behave.
QWEN_MODEL_NAME = "Qwen/Qwen2.5-0.5B"


def _ensure_qwen_loaded():
    global _qwen_tokenizer, _qwen_model
    if _qwen_model is not None:
        return
    from transformers import AutoTokenizer, AutoModelForCausalLM  # noqa: PLC0415
    _qwen_tokenizer = AutoTokenizer.from_pretrained(QWEN_MODEL_NAME)
    _qwen_model = AutoModelForCausalLM.from_pretrained(
        QWEN_MODEL_NAME, dtype=torch.float32
    )
    _qwen_model.eval()


def qwen_sample_completions(
    prefix: str,
    n: int = 200,
    max_new_tokens: int = 8,
    temperature: float = 0.9,
    top_p: float = 0.95,
    seed: int = 0,
    stop_at_newline: bool = True,
    use_cache: bool = True,
) -> list[str]:
    """
    Sample `n` completions of `prefix` from Qwen2.5-0.5B, each returned as the
    full string (prefix included) continued by up to `max_new_tokens` sampled
    tokens.

    Results are deterministic given `seed` and cached to a JSON file next to
    this module (keyed by all sampling parameters), so repeated scene renders
    don't re-run the model. Pass use_cache=False to force regeneration.
    """
    key = (prefix, n, max_new_tokens, temperature, top_p, seed, stop_at_newline)
    digest = hashlib.md5(repr(key).encode()).hexdigest()[:10]
    cache_path = os.path.join(
        os.path.dirname(__file__), f"qwen_completions_{digest}.json"
    )
    if use_cache and os.path.exists(cache_path):
        with open(cache_path) as f:
            return json.load(f)["completions"]

    _ensure_qwen_loaded()
    torch.manual_seed(seed)

    input_ids = _qwen_tokenizer.encode(
        prefix, add_special_tokens=False, return_tensors="pt"
    )
    pad_id = _qwen_tokenizer.pad_token_id
    if pad_id is None:
        pad_id = _qwen_tokenizer.eos_token_id

    completions: list[str] = []
    batch_size = 50
    with torch.no_grad():
        while len(completions) < n:
            k = min(batch_size, n - len(completions))
            batch_ids = input_ids.repeat(k, 1)
            outputs = _qwen_model.generate(
                batch_ids,
                attention_mask=torch.ones_like(batch_ids),
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                pad_token_id=pad_id,
            )
            for row in outputs:
                text = _qwen_tokenizer.decode(row, skip_special_tokens=True)
                if stop_at_newline:
                    text = text.split("\n")[0]
                completions.append(text.rstrip())

    completions = completions[:n]

    if use_cache:
        payload = {
            "model": QWEN_MODEL_NAME,
            "prefix": prefix,
            "params": {
                "n": n, "max_new_tokens": max_new_tokens,
                "temperature": temperature, "top_p": top_p, "seed": seed,
                "stop_at_newline": stop_at_newline,
            },
            "completions": completions,
        }
        with open(cache_path, "w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    return completions



# ----- From _2024/transformers/embedding.py -----

def get_token_encoding():
    return tiktoken.encoding_for_model("davinci")


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


def break_into_tokens(phrase_mob):
    tokenizer = get_token_encoding()
    tokens = tokenizer.encode(phrase_mob.get_string())
    _, offsets = tokenizer.decode_with_offsets(tokens)
    return break_into_pieces(phrase_mob, offsets)


def get_piece_rectangles(
    phrase_pieces,
    h_buff=0.05,
    v_buff=0.1,
    fill_opacity=0.15,
    fill_color=None,
    stroke_width=1,
    stroke_color=None,
    hue_range=(0.5, 0.6),
    leading_spaces=False,
):
    rects = VGroup()
    height = phrase_pieces.get_height() + 2 * v_buff
    last_right_x = phrase_pieces.get_x(LEFT)
    for piece in phrase_pieces:
        left_x = last_right_x if leading_spaces else piece.get_x(LEFT)
        right_x = piece.get_x(RIGHT)
        fill = random_bright_color(hue_range) if fill_color is None else fill_color
        stroke = fill if stroke_color is None else stroke_color
        rect = Rectangle(
            width=right_x - left_x + 2 * h_buff,
            height=height,
            fill_color=fill,
            fill_opacity=fill_opacity,
            stroke_color=stroke,
            stroke_width=stroke_width
        )
        if leading_spaces:
            rect.set_x(left_x, LEFT)
        else:
            rect.move_to(piece)
        rect.set_y(0)
        rects.add(rect)

        last_right_x = right_x

    rects.match_y(phrase_pieces)
    return rects



# ----- From _2026/cross_entropy/language_models.py -----

def get_token_groups(text):
    text_mob = Text(text)
    tokens = break_into_tokens(text_mob)
    rects = get_piece_rectangles(tokens, h_buff=0, leading_spaces=True)
    return VGroup(VGroup(*pair) for pair in zip(rects, tokens))


def get_tokens(text):
    tokenizer = get_token_encoding()
    token_indices = tokenizer.encode(text)
    _, offsets = tokenizer.decode_with_offsets(token_indices)
    offsets.append(len(text))
    return [text[o1:o2] for o1, o2 in zip(offsets, offsets[1:])]


class ManyMyNameIsExamples(InteractiveScene):
    def construct(self):
        prefix = "My name is"
        n_examples = 200
        # Each string is `prefix` continued by tokens sampled from Qwen2.5-0.5B.
        # Generated once and cached to disk, so this is cheap on re-render.
        examples = qwen_sample_completions(prefix, n=n_examples)
        token_groups = VGroup(map(get_token_groups, examples))
        for group in token_groups:
            group.shift(-group[2].get_right())

        prefix_len = len(get_tokens(prefix))
        prefix = token_groups[0][:prefix_len]
        prefix.save_state()
        prefix_rects = VGroup(mob[0] for mob in prefix)
        prefix_rects.set_opacity(0)

        underline = Line(LEFT, RIGHT)
        underline.next_to(prefix[-1][-1], RIGHT, aligned_edge=DOWN)

        self.add(prefix, underline)
        self.wait()

        # Show all completions
        suffixes = VGroup(group[prefix_len:] for group in token_groups)
        suffixes.arrange(UP, buff=0.5, aligned_edge=LEFT)
        suffixes.save_state()

        prefix.restore()
        self.remove(underline)

        for n in range(len(suffixes) - 1):
            suffixes.restore()
            suffixes[:n].fade(0.9)
            suffixes[n + 1:].fade(0.9)
            suffixes.shift(-suffixes[n].get_left())
            self.add(suffixes)
            self.wait(0.1)
