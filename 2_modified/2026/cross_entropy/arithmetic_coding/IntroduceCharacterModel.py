# ==============================================================================
# Scene:      IntroduceCharacterModel
# Source:     videos/_2026/cross_entropy/arithmetic_coding.py (lines 188-393)
# Category:   2 · Renders with modifications
# Includes code copied from: _2026/cross_entropy/distribution.py, _2026/cross_entropy/next_char.py
#
# Run from this folder:
#     manimgl IntroduceCharacterModel.py IntroduceCharacterModel -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Replaced Grant's nanoGPT model (nonexistent checkpoint) with a synthetic character model (n-grams over text_data/ + English frequencies); the probabilities shown are plausible, not those of the real model.
#   - BigModel.png is looked up next to the file (before: Grant's output folder) and is a placeholder image; the path is passed to ImageMobject as a str.
#
# Placeholder assets (not Grant's originals):
#   - Paul Assets/BigModel.png (placeholder image: large neural network)
#   - text_data/quotes.txt and training_data_examples.txt: original text and public-domain quotes (_lib/assets/generated/2026/cross_entropy/text_data/) instead of 3b1b's, which quoted copyrighted works
#
# Extra packages installed in the venv: torch
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *
import pickle
import sys
import torch
import numpy as np
from functools import lru_cache


# ----- From _2026/cross_entropy/distribution.py -----

class StackedProbDistribution(VGroup):
    def __init__(
        self,
        distribution,
        width=12,
        height=0.5,
        fill_colors=(BLUE_E, TEAL_E),
        fill_opacity=1,
        stroke_width=1,
        stroke_color=WHITE,
        labels=None,
        label_height_ratio=0.5,
        label_width_ratio=0.8,
        fit_labels_to_height=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.distribution = distribution
        self.cdf = np.cumsum(distribution)
        self.bar_color_bounds = fill_colors
        self.label_height_ratio = label_height_ratio
        self.label_width_ratio = label_width_ratio

        # Set bars with dummy values
        self.bars = Rectangle().get_grid(1, len(distribution), buff=0)
        self.bars.set_shape(width, height)
        self.bars.set_fill(fill_colors, 1, gradient_direction=RIGHT)
        self.bars.set_stroke(stroke_color, stroke_width)

        # Initialize labels as empty
        self.labels = VGroup()

        self.add(self.bars, self.labels)

        self.set_distribution(distribution)
        self.fit_labels_to_height = fit_labels_to_height
        if labels is not None:
            self.set_labels(labels)

    def set_labels(self, labels: VMobject):
        self.labels.set_submobjects(labels)
        self.original_labels = labels.copy()
        self.reposition_labels()
        return self

    def reposition_labels(self):
        self.labels.become(self.original_labels)
        if self.fit_labels_to_height:
            self.labels.set_height(self.bars.get_height() * self.label_height_ratio)
        self.labels.move_to(self.bars)
        for label, bar in zip(self.labels, self.bars):
            label.match_x(bar)
            fill_opacity = float(label.get_width() < bar.get_width() * self.label_width_ratio)
            label.set_fill(opacity=fill_opacity)
        return self

    def set_distribution(self, distribution):
        center = self.bars.get_center().copy()
        width, height = self.bars.get_shape()[:2]
        n_bars = len(distribution)
        bar_style = self.bars[0].get_style()

        if len(self.bars) != n_bars:
            self.bars.set_submobjects(Rectangle().replicate(n_bars))

        for bar, prob in zip(self.bars, distribution):
            bar.set_shape(width * prob, height)
            bar.set_style(**bar_style)
        self.bars.arrange(RIGHT, buff=0)
        self.bars.move_to(center)
        self.bars.set_fill(self.bar_color_bounds, gradient_direction=RIGHT)

        if len(self.labels) > 0:
            self.reposition_labels()

        return self

    def highlight(self, index, color=None, other_bar_opacity=0.35, fade_labels=True):
        self.bars.set_fill(self.bar_color_bounds, opacity=other_bar_opacity, gradient_direction=RIGHT)
        self.bars[index].set_fill(color, opacity=1)
        if fade_labels:
            for idx, label in enumerate(self.labels):
                if label.get_fill_opacity() == 0:
                    op = 0
                elif idx == index:
                    op = 1
                else:
                    op = other_bar_opacity
                label.set_fill(opacity=op)
        return self

    def renormalize_around(self, index: int):
        width, height = self.get_shape()[:2]
        center = self.get_center().copy()
        bar_width = self.bars[index].get_width()
        self.bars.stretch(width / bar_width, 0)
        self.bars.shift(center - self.bars[index].get_center())
        self.reposition_labels()
        return self

    def stretch(self, factor, dim, **kwargs):
        super().stretch(factor, dim, **kwargs)
        if dim == 0:
            self.reposition_labels()
        return self

    def float_to_index(self, value: float):
        """
        Given a value in [0, 1], returns the index of the
        corresponding event from the distribution
        """
        for idx, upper_value in enumerate(self.cdf):
            if value < upper_value:
                return idx
        # Otherwise, last element
        return len(self.distribution) - 1


class DynamicInterval(UnitInterval):
    def __init__(
        self,
        x_range=(0, 1),
        width=12,
        subdivisions=10,
        include_numbers=True,
        include_endpoint_numbers=True,
        width_fade_range=(4, 6),
        number_font_size=24,
        **kwargs
    ):
        self.width_fade_range = width_fade_range

        x_min, x_max = x_range[0], x_range[1]
        step = (x_max - x_min) / subdivisions
        num_decimal_places = max(int(np.round(-np.log(step) / np.log(subdivisions))), 0)

        super().__init__(
            x_range=(x_min, x_max, step),
            width=width,
            big_tick_numbers=[x_min, x_max],
            **kwargs
        )
        label_values = [x_min + step * n for n in range(subdivisions + 1)]
        if not include_endpoint_numbers:
            label_values = label_values[1:-1]
        self.add_numbers(
            label_values,
            direction=UP,
            num_decimal_places=num_decimal_places,
            font_size=number_font_size,
        )
        self.original_numbers = self.numbers.copy()

    def reposition_labels(self):
        self.numbers.become(self.original_numbers)
        for label, original in zip(self.numbers, self.original_numbers):
            label.match_x(self.n2p(original.get_value()))
        return self

    def update_opacity_from_width(self):
        w_min, w_max = self.width_fade_range
        opacity = clip(inverse_interpolate(w_min, w_max, self.get_width()), 0, 1)
        self.set_stroke(opacity=opacity)
        self.numbers.set_fill(opacity=opacity)
        return self

    def stretch(self, factor, dim, **kwargs):
        super().stretch(factor, dim, **kwargs)
        if dim == 0:
            self.reposition_labels()
        self.update_opacity_from_width()
        return self



# ----- From _2026/cross_entropy/next_char.py -----

CHAR_ALPHABET = "abcdefghijklmnopqrstuvwxyz .,'!?"


NANOGPT_DIR = "/Users/grant/cs/nanoGPT"


NANOGPT_CKPT = "/Users/grant/cs/nanoGPT/out-wiki-char/ckpt.pt"


_nano_model = None


_nano_encode = None


_nano_vocab = None  # list of chars in order


# CHANGE: Grant's nanoGPT checkpoint (/Users/grant/cs/nanoGPT/...) and the GPT-2 / Qwen models (transformers,
# with weights) are not available. These SYNTHETIC models (character and token n-grams, computed over
# text_data/ + English frequency tables) have the same minimal interface that the functions below use, so the
# rest of the scene's code does not change. The probabilities shown are plausible, not those of the real
# models.
import re as _synth_re
from pathlib import Path as _SynthPath

_SYNTH_FALLBACK_TEXT = (
    "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness. "
    "The quick brown fox jumps over the lazy dog. Once upon a time, there was a little girl who lived in a village near the forest. "
    "I think, therefore I am. There is some good in this world, and it's worth fighting for. "
    "The only way out of the labyrinth of suffering is to forgive. All animals are equal, but some animals are more equal than others. "
) * 4

_SYNTH_CHARS = "abcdefghijklmnopqrstuvwxyz .,'!?0123456789-:;\"()"

# Approximate English frequencies (per thousand characters) used as the base distribution
_SYNTH_CHAR_PRIOR = {
    " ": 180, "e": 100, "t": 73, "a": 66, "o": 60, "i": 56, "n": 54, "s": 50, "h": 49, "r": 48, "d": 34, "l": 32,
    "u": 22, "c": 22, "m": 19, "w": 19, "f": 18, "g": 16, "y": 16, "p": 15, "b": 12, "v": 8, "k": 6, "j": 1.2,
    "x": 1.2, "q": 0.8, "z": 0.6, ",": 12, ".": 11, "'": 3, "!": 0.5, "?": 0.7, "-": 1.5, ":": 0.5, ";": 0.4,
    "\"": 1.0, "(": 0.4, ")": 0.4,
}


def _synth_corpus() -> str:
    folder = _SynthPath(__file__).parent / "text_data"
    pieces = []
    if folder.exists():
        for p in sorted(folder.glob("*.txt")):
            if p.name != "th_followers.txt":
                pieces.append(p.read_text(encoding="utf-8", errors="ignore"))
    text = "\n".join(pieces)
    return text if len(text) > 2000 else _SYNTH_FALLBACK_TEXT


def _synth_th_followers():
    """Real distribution of what follows 'th' in wikitext (text_data/th_followers.txt), if it exists."""
    path = _SynthPath(__file__).parent / "text_data" / "th_followers.txt"
    result = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = _synth_re.match(r"\s*'(.)'\s+(\d+)\s+([\d.]+)%", line)
            if m:
                result[m.group(1)] = float(m.group(3)) / 100
    return result


class _SynthCharGPT:
    """Synthetic character model (n-gram with Witten-Bell smoothing) with nanoGPT's minimal interface:
    model(idx, targets=None) -> (logits, loss) and model.config.block_size."""
    class _Config:
        block_size = 256

    def __init__(self, text, order=4):
        self.config = self._Config()
        self.vocab = list(_SYNTH_CHARS)
        self.stoi = {c: i for i, c in enumerate(self.vocab)}
        self.order = order
        V = len(self.vocab)
        prior = np.array([_SYNTH_CHAR_PRIOR.get(c, 0.3) for c in self.vocab], dtype=float)
        self.base = prior / prior.sum()
        clean = "".join(c if c in self.stoi else " " for c in text.lower())
        clean = _synth_re.sub(r" +", " ", clean)
        ids = [self.stoi[c] for c in clean]
        self.counts = [dict() for _ in range(order)]
        for i, c in enumerate(ids):
            for k in range(order):
                if i - k < 0:
                    break
                ctx = tuple(ids[i - k:i])
                self.counts[k].setdefault(ctx, np.zeros(V))[c] += 1
        self.th = np.zeros(V)
        for ch, p in _synth_th_followers().items():
            if ch in self.stoi:
                self.th[self.stoi[ch]] = p
        if self.th.sum() > 0:
            self.th /= self.th.sum()

    def probs(self, ctx_ids):
        p = self.base.copy()
        for k in range(min(self.order, len(ctx_ids) + 1)):
            ctx = tuple(ctx_ids[len(ctx_ids) - k:]) if k > 0 else ()
            c = self.counts[k].get(ctx)
            if c is None:
                break
            n, t = c.sum(), (c > 0).sum()
            p = (c + t * p) / (n + t)
        if self.th.sum() > 0 and len(ctx_ids) >= 2 and ctx_ids[-2:] == [self.stoi["t"], self.stoi["h"]]:
            p = 0.3 * p + 0.7 * self.th
        return np.clip(p, 1e-6, None) / np.clip(p, 1e-6, None).sum()

    def __call__(self, idx, targets=None):
        ids = idx[0].tolist()
        positions = range(len(ids)) if targets is not None else [len(ids) - 1]
        rows = [np.log(self.probs(ids[max(0, t + 1 - self.order + 1):t + 1])) for t in positions]
        logits = torch.tensor(np.array(rows), dtype=torch.float32)[None]
        return logits, None


class _SynthTokenizer:
    """GPT-2 BPE tokenizer (tiktoken) with the minimal interface of the transformers tokenizers."""
    def __init__(self):
        import tiktoken  # noqa: PLC0415
        self._enc = tiktoken.get_encoding("gpt2")
        self.n_vocab = self._enc.n_vocab
        self.pad_token_id = None
        self.eos_token_id = 50256

    def encode(self, text, add_special_tokens=False, return_tensors=None):
        ids = self._enc.encode(text, disallowed_special=())
        return torch.tensor([ids]) if return_tensors == "pt" else ids

    def decode(self, ids, skip_special_tokens=False):
        if hasattr(ids, "tolist"):
            ids = ids.tolist()
        return self._enc.decode(list(ids))


_SYNTH_PRIOR_WORDS = {
    " the": 50, ",": 46, ".": 40, " of": 28, " and": 27, " to": 26, " a": 23, " in": 20, " is": 12, " that": 11,
    " it": 10, " for": 10, " was": 9, " with": 8, " as": 8, " on": 8, " I": 7, " be": 6, " are": 6, " you": 6,
    " The": 6, " this": 5, " have": 5, " not": 5, " at": 5, " by": 5, " from": 5, " or": 4.5, " an": 4,
    " his": 4, " he": 4, " we": 4, " but": 4, " they": 3.5, " which": 3.5, " had": 3.5, "\n": 3, "'s": 3,
    " their": 3, " one": 3, " all": 2.5, " would": 2.5, " there": 2.5, " what": 2.5, " so": 2.5, " up": 2,
    " out": 2, " if": 2, " about": 2, " who": 2, " when": 2, " can": 2, " will": 2, "?": 2, "!": 1.5,
    " my": 1.5, "-": 1.5, ":": 1.5, " time": 1, " people": 1, " like": 1, " more": 1,
}

# "Author" predictions for the prefixes the scenes show (the rest comes from the n-gram). Each entry:
# prefix -> [(token, probability), ...]; the remaining mass is spread according to the n-gram.
_SYNTH_TOKEN_OVERRIDES = {
    "My name is": [(" Jack", .035), (" John", .03), (" Michael", .025), (" David", .02), (" Daniel", .02),
                   (" James", .018), (" Chris", .017), (" Alex", .015), (" Sarah", .014), (" Mike", .013)],
    "Once": [(",", .17), (" again", .09), (" upon", .07), (" the", .06), (" you", .05), (" a", .045), (" I", .03), (" they", .028)],
    "Once upon": [(" a", .93), (" the", .015), (" this", .008), (" my", .004), (" arriving", .003), (" reaching", .003), (" returning", .002), (" completion", .002)],
    "Once upon a": [(" time", .96), (" midnight", .004), (" day", .003), (" Time", .003), (" moment", .002), (" dream", .002), (" mountain", .001), (" hill", .001)],
    "Once upon a time": [(",", .83), (" in", .035), (" there", .02), (" the", .015), (".", .012), (" a", .01), (" I", .01), (" when", .008)],
    "Once upon a time,": [(" there", .41), (" in", .13), (" a", .09), (" the", .05), (" I", .04), (" when", .03), (" my", .02), (" long", .02)],
    "Once upon a time, there": [(" was", .78), (" lived", .05), (" were", .04), (" existed", .02), (" came", .01), (" is", .01), (" once", .01), (" stood", .006)],
    "Once upon a time, there was": [(" a", .50), (" an", .08), (" no", .05), (" once", .04), (" this", .03), (" the", .03), (" one", .025), (" only", .02)],
    "Once upon a time, there was a": [(" young", .09), (" little", .04), (" man", .04), (" boy", .03), (" girl", .03), (" time", .03), (" small", .025), (" woman", .02)],
    "Once upon a time, there was a tiny": [(" little", .06), (" village", .05), (" town", .03), (" bit", .03), (" bird", .03), (" fairy", .02), (" mouse", .02), (" boy", .02)],
    "Once upon a time, there was a tiny pi": [("g", .09), ("ne", .06), ("rate", .04), ("ll", .03), ("ck", .03), ("e", .03), ("nk", .02), ("zz", .02)],
    "Once upon a time, there was a tiny pi creature": [(" named", .12), (" that", .09), (" called", .07), (".", .07), (",", .06), (" who", .05), (" with", .04), (" in", .03)],
    "Once upon a time, there was a tiny pi creature who": [(" lived", .14), (" was", .12), (" had", .08), (" loved", .06), (" wanted", .05), (" could", .04), (" liked", .03), (" lives", .03)],
    "Once upon a time, there was a tiny pi creature who lived": [(" in", .55), (" on", .08), (" with", .06), (" alone", .04), (" at", .04), (" under", .03), (" inside", .03), (" near", .02)],
    "Once upon a time, there was a tiny pi creature who lived between": [(" the", .28), (" two", .10), (" a", .08), (" his", .04), (" them", .03), (" her", .03), (" three", .025), (" worlds", .02)],
    "Once upon a time, there was a tiny pi creature who lived between 3": [("rd", .22), (" and", .15), ("0", .08), ("-", .05), (" months", .03), (" weeks", .03), ("5", .03), (",", .03)],
    "Once upon a time, there was a tiny pi creature who lived between 3rd": [(" and", .35), (" Street", .12), (" of", .05), (",", .05), (" St", .04), (" Avenue", .035), (" century", .03), (" Ave", .03)],
    "Once upon a time, there was a tiny pi creature who lived between 3rd and": [(" 4", .22), (" 5", .10), (" 2", .08), (" 6", .05), (" the", .05), (" 7", .04), (" 10", .035), (" 1", .03)],
    "Once upon a time, there was a tiny pi creature who lived between 3rd and 4": [("th", .72), (".", .03), ("0", .03), (" and", .02), (",", .02), ("rd", .02), ("-", .01), (")", .01)],
    "Once upon a time, there was a tiny pi creature who lived between 3rd and 4th": [(" Street", .35), (" street", .10), (" Ave", .05), (" Avenue", .05), (" and", .045), (" St", .04), (" floor", .03), (",", .03)],
    "Once upon a time, there was a tiny pi creature who lived between 3rd and 4th street": [(".", .30), (",", .20), (" in", .05), (" and", .04), (" was", .03), ("\n", .03), (" near", .02), (" corner", .02)],
    "It": [(" is", .17), (" was", .12), ("'s", .09), (" has", .05), (" would", .04), (" will", .04), (" seems", .03), (" looks", .03)],
    "It is": [(" a", .12), (" not", .09), (" the", .07), (" also", .05), (" important", .04), (" true", .03), (" difficult", .02), (" possible", .02)],
    "It is not": [(" the", .08), (" a", .07), (" clear", .06), (" known", .05), (" possible", .04), (" necessary", .04), (" surprising", .035), (" an", .03)],
    "It is not the": [(" first", .06), (" case", .05), (" only", .05), (" same", .04), (" end", .03), (" intention", .02), (" fault", .02), (" job", .02)],
    "It is not the critic": [(" who", .62), (" that", .05), (",", .04), (" of", .03), (".", .03), (" in", .02), (" but", .02), (" is", .02)],
    "It is not the critic who": [(" counts", .55), (" matters", .08), (" is", .06), (" should", .04), (" has", .03), (" will", .03), (" can", .02), (" makes", .02)],
    "You": [(" are", .13), (" can", .10), (" may", .06), (" will", .05), (" have", .05), (" should", .04), (" might", .03), (" need", .03), (" must", .03), (" know", .02)],
    "You can": [(" use", .09), (" find", .06), (" also", .06), (" see", .05), (" get", .05), (" do", .04), (" have", .04), (" make", .03), (" try", .03), (" check", .03)],
    "You can ref": [("ine", .30), ("actor", .14), ("er", .12), ("res", .09), ("lect", .06), ("ill", .04), ("rain", .03), ("rig", .02), ("ere", .02), ("rame", .004)],
    "You can reframe": [(" the", .35), (" your", .20), (" it", .06), (" this", .04), (" a", .04), (" these", .03), (" any", .02), (" how", .02), (" them", .02), (" what", .02)],
    "You can reframe the": [(" way", .10), (" problem", .07), (" situation", .06), (" question", .04), (" issue", .04), (" narrative", .03), (" conversation", .03), (" discussion", .03), (" debate", .025), (" challenge", .025)],
    "You can reframe the way": [(" you", .30), (" we", .12), (" they", .05), (" people", .05), (" your", .04), (" in", .04), (" that", .03), (" to", .03), (" the", .03), (" it", .02)],
    "You can reframe the way you": [(" think", .12), (" see", .06), (" approach", .05), (" look", .05), (" view", .04), (" perceive", .03), (" feel", .03), (" are", .03), (" talk", .03), (" handle", .02)],
    "You can reframe the way you think": [(" about", .60), (" of", .20), (" and", .02), (",", .02), (" in", .02), (" through", .015), (" is", .01), (" the", .01), (" or", .01), (" differently", .01)],
    "You can reframe the way you think about": [(" it", .20), (" your", .10), (" the", .10), (" money", .04), (" yourself", .04), (" life", .03), (" problems", .03), (" things", .03), (" what", .03), (" a", .02)],
    "You can reframe the way you think about training": [(" your", .10), (" and", .06), (" for", .05), (" is", .03), (" in", .03), (" programs", .03), (" a", .03), (" as", .02), (" the", .02), (" to", .02)],
    "You can reframe the way you think about training large": [(" language", .10), (" models", .06), (" amounts", .05), (" datasets", .05), (" scale", .04), (" neural", .04), (" batch", .03), (" data", .03), (" deep", .02), (" numbers", .02)],
    "You can reframe the way you think about training large language": [(" models", .75), (" model", .08), (" data", .02), (",", .015), (" understanding", .01), (" processing", .01), (" tasks", .01), (".", .01), (" learning", .008), (" generation", .006)],
    "You can reframe the way you think about training large language models": [(" (", .22), (" is", .10), (",", .10), (" to", .08), (" in", .06), (".", .05), (" as", .03), (" and", .03), (" with", .03), (" like", .02)],
    "You can reframe the way you think about training large language models to": [(" be", .10), (" produce", .04), (" do", .04), (" perform", .03), (" generate", .03), (" achieve", .03), (" make", .03), (" solve", .03), (" improve", .03), (" better", .02)],
    "You can reframe the way you think about training large language models to not": [(" be", .30), (" just", .05), (" only", .04), (" have", .04), (" rely", .03), (" use", .03), (" depend", .02), (" require", .02), (" fall", .02), (" over", .015)],
    "You can reframe the way you think about training large language models to not be": [(" about", .12), (" so", .06), (" just", .05), (" a", .05), (" too", .04), (" overly", .03), (" focused", .03), (" limited", .03), (" the", .03), (" afraid", .02)],
    "You can reframe the way you think about training large language models to not be about": [(" the", .20), (" predicting", .06), (" training", .05), (" learning", .05), (" generating", .04), (" optimizing", .04), (" finding", .03), (" solving", .03), (" getting", .02), (" making", .02)],
    "You can reframe the way you think about training large language models to not be about next": [(" steps", .15), (" generation", .08), (" year", .06), (" week", .05), (" level", .05), (" token", .04), (" word", .04), (" time", .04), (" step", .03), (" move", .03)],
    "You can reframe the way you think about training large language models to not be about next token": [(" prediction", .25), (" generation", .18), ("s", .10), (" sequence", .05), (" sampling", .04), (" is", .03), (" in", .02), (" probabilities", .02), (" level", .02), (" classification", .02)],
    "You can reframe the way you think about training large language models to not be about next token prediction": [(",", .22), (" and", .10), (".", .10), (" but", .08), (" to", .06), (" or", .05), (" in", .04), (" as", .03), (" accuracy", .02), (" alone", .02)],
    "You can reframe the way you think about training large language models to not be about next token prediction,": [(" but", .24), (" and", .12), (" which", .08), (" or", .05), (" as", .04), (" rather", .04), (" so", .03), (" is", .02), (" with", .02), (" the", .02)],
}


class _SynthTokenLM:
    """Synthetic language model over GPT-2's BPE vocabulary: token n-gram (Witten-Bell) computed over
    text_data/ + English unigrams + author predictions for the scenes' prefixes.
    Minimal interface: lm(input_ids).logits[0, -1, :]"""
    def __init__(self, tokenizer):
        self.tok = tokenizer
        V = tokenizer.n_vocab
        self.V = V
        prior = np.full(V, 1e-4)
        for word, w in _SYNTH_PRIOR_WORDS.items():
            ids = tokenizer.encode(word)
            if len(ids) == 1:
                prior[ids[0]] += w
        corpus_ids = tokenizer.encode(_synth_corpus())
        uni = np.zeros(V)
        self.bi, self.tri = {}, {}
        for i, t in enumerate(corpus_ids):
            uni[t] += 1
            if i >= 1:
                self.bi.setdefault((corpus_ids[i - 1],), {}).setdefault(t, 0)
                self.bi[(corpus_ids[i - 1],)][t] += 1
            if i >= 2:
                self.tri.setdefault((corpus_ids[i - 2], corpus_ids[i - 1]), {}).setdefault(t, 0)
                self.tri[(corpus_ids[i - 2], corpus_ids[i - 1])][t] += 1
        base = prior / prior.sum()
        self.base = 0.7 * base + 0.3 * (uni + 1e-3) / (uni + 1e-3).sum()
        self.base /= self.base.sum()
        self.overrides = {}
        for prefix, items in _SYNTH_TOKEN_OVERRIDES.items():
            pairs = []
            for tok, p in items:
                ids = tokenizer.encode(tok)
                if len(ids) == 1:
                    pairs.append((ids[0], p))
            self.overrides[prefix] = pairs

    def next_probs(self, ids):
        p = self.base.copy()
        for k, table in ((1, self.bi), (2, self.tri)):
            if len(ids) < k:
                break
            counts = table.get(tuple(ids[-k:]))
            if not counts:
                break
            q = np.zeros(self.V)
            for t, c in counts.items():
                q[t] = c
            n, t_types = q.sum(), len(counts)
            p = (q + t_types * p) / (n + t_types)
        over = self.overrides.get(self.tok.decode(ids))
        if over:
            idx = [i for i, _ in over]
            mass = sum(pr for _, pr in over)
            cap = 0.8 * min(pr for _, pr in over)
            p[idx] = 0
            for _ in range(4):  # the rest of the tokens do not exceed the author ones
                p = np.minimum(p, cap)
                p *= (1 - mass) / p.sum()
            for i, pr in over:
                p[i] = pr
        return p / p.sum()

    def __call__(self, input_ids):
        ids = input_ids[0].tolist()
        row = torch.tensor(np.log(np.clip(self.next_probs(ids), 1e-12, None)), dtype=torch.float32)
        class _Out:
            pass
        out = _Out()
        out.logits = row.expand(1, len(ids), self.V)
        return out

    def eval(self):
        return self


_SYNTH_TOKEN_STACK = {}


def _synth_token_stack():
    if "tok" not in _SYNTH_TOKEN_STACK:
        tok = _SynthTokenizer()
        _SYNTH_TOKEN_STACK["tok"] = tok
        _SYNTH_TOKEN_STACK["lm"] = _SynthTokenLM(tok)
    return _SYNTH_TOKEN_STACK["tok"], _SYNTH_TOKEN_STACK["lm"]


def _ensure_nano_loaded():
    global _nano_model, _nano_encode, _nano_decode, _nano_vocab
    if _nano_model is not None:
        return
    # CHANGE: synthetic character model instead of Grant's nanoGPT checkpoint (not available)
    model = _SynthCharGPT(_synth_corpus())
    _nano_model = model
    stoi, itos = model.stoi, model.vocab
    def _nano_encode(s): return [stoi[c.lower()] for c in s if c.lower() in stoi]
    def _nano_decode(ids): return "".join(itos[i] for i in ids)
    _nano_vocab = list(itos)


@lru_cache()
def get_next_char_distribution(prefix: str, alphabet: str = CHAR_ALPHABET) -> np.ndarray:
    """
    Return a probability distribution over `alphabet` using the nanoGPT
    wiki_char model. Because this model was trained character-by-character
    (each token = one character), the logits directly give P(next character).
    """
    _ensure_nano_loaded()

    alpha_lower = alphabet.lower()

    ids = _nano_encode(prefix)[-_nano_model.config.block_size:]
    if ids:
        input_ids = torch.tensor([ids])
        with torch.no_grad():
            logits = _nano_model(input_ids)[0][0, -1]  # (vocab_size,)
        probs = torch.softmax(logits, dim=-1).numpy()
    else:
        probs = np.ones(len(_nano_vocab)) / len(_nano_vocab)

    char_probs = np.zeros(len(alphabet))
    for vocab_idx, char in enumerate(_nano_vocab):
        idx = alpha_lower.find(char.lower())
        if idx != -1:
            char_probs[idx] += probs[vocab_idx]

    total = char_probs.sum()
    if total > 0:
        char_probs /= total

    return char_probs



# ----- From _2026/cross_entropy/arithmetic_coding.py -----

class ArithmeticCodingDiagram(Group):
    def __init__(
        self,
        width=12,
        buff_to_bars=0.25,
        show_decimal_labels=True,
        interval_subdivisions=10,
        char_alphabet=CHAR_ALPHABET,
        highlight_colors=(GREEN_E, GREEN_D),
        label_to_bar_height_ratio=0.5,
        context=" ",
    ):
        self.layers = VGroup()
        self.intervals = VGroup()
        self.full_width = width
        self.show_decimal_labels = show_decimal_labels
        self.interval_subdivisions = interval_subdivisions
        self.char_alphabet = char_alphabet
        self.label_to_bar_height_ratio = label_to_bar_height_ratio
        self.context = context

        self.highlight_color_iter = it.cycle(highlight_colors)

        self.unit_interval = DynamicInterval(width=width)
        self.intervals.add(self.unit_interval)
        self.interval_keys = {(1, 0)}  # Of the form (step_size, lower_bound_int)

        self.curr_text = ""  # Start with a neutral context
        self.char_labels_template = Text(char_alphabet)
        self.layers.add(self.get_new_layer(buff=SMALL_BUFF))

        super().__init__(self.intervals, Point(), self.layers)

    def get_new_layer(self, buff=0.1):
        if len(self.layers) == 0:
            mob_above = self.unit_interval[0]
        else:
            mob_above = self.get_letter_bar(self.curr_text[-1])

        full_context = self.context + self.curr_text
        distribution = get_next_char_distribution(full_context)
        # if len(full_context.strip()) == 0:
        #     # Artificially suppress punctuation
        #     distribution[26:] *= 1e-3
        #     distribution /= sum(distribution)

        layer = StackedProbDistribution(
            distribution,
            labels=self.char_labels_template.copy(),
            width=mob_above.get_width(),
            label_height_ratio=self.label_to_bar_height_ratio
        )
        layer.next_to(mob_above, DOWN, buff=buff)
        return layer

    def get_letter_bar(self, char, layer_index=-1):
        index = self.char_alphabet.index(char)
        return self.layers[layer_index].bars[index]

    def get_letter_label(self, char, layer_index=-1):
        index = self.char_alphabet.index(char)
        return self.layers[layer_index].labels[index]

    def populate_intervals(self, x_min, x_max):
        log_val = np.log(x_max - x_min) / np.log(self.interval_subdivisions)
        min_scale = int(np.ceil(np.round(log_val, 1)))

        for scale in range(-1, min_scale - 1, -1):
            step = self.interval_subdivisions**(scale)
            for lower_bound_int in range(int(x_min / step) - 1, int(x_max / step) + 1):
                interval_key = (step, lower_bound_int)
                if interval_key in self.interval_keys:
                    continue
                low = lower_bound_int * step
                high = (lower_bound_int + 1) * step
                interval = DynamicInterval(
                    x_range=(low, high),
                    width=get_norm(self.unit_interval.n2p(high) - self.unit_interval.n2p(low)),
                    subdivisions=self.interval_subdivisions,
                    include_numbers=self.show_decimal_labels,
                    include_endpoint_numbers=False,
                    number_font_size=24 + scale * 2,
                )
                interval.shift(self.unit_interval.n2p(low) - interval.n2p(low))
                self.intervals.add(interval)
                self.interval_keys.add(interval_key)
        return self

    def get_conditional_probability(self, char, layer_index=-1):
        idx = self.char_alphabet.index(char)
        return self.layers[layer_index].distribution[idx]

    def get_absolute_information(self, text):
        result = 0
        for layer, char in zip(self.layers, text):
            result += -math.log2(layer.distribution[self.char_alphabet.index(char)])
        return result

    # Animations
    def renormalize_animation(
        self,
        x_min,
        x_max,
        run_time=3,
        center=ORIGIN,
        center_curr_text=False,
        **kwargs
    ):
        big_interval = self.intervals[0]
        x_mid = (x_min + x_max) / 2
        p_left, p_mid, p_right = [big_interval.n2p(x) for x in (x_min, x_mid, x_max)]

        stretch_factor = self.full_width / get_norm(p_right - p_left)
        x_shift = (center - p_mid)[0] * RIGHT

        self.populate_intervals(x_min, x_max)
        for interval in self.intervals:
            interval.update_opacity_from_width()

        target = self.copy()

        for interval in target.intervals:
            interval.shift(x_shift)
            interval.stretch(stretch_factor, 0, about_point=ORIGIN)
        for layer in target.layers:
            layer.shift(x_shift)
            layer.stretch(stretch_factor, 0, about_point=ORIGIN)
            layer.reposition_labels()
        if center_curr_text:
            for layer, char in zip(target.layers, self.curr_text):
                label = layer[1][self.char_alphabet.index(char)]
                label.match_x(center)

        return Transform(self, target, run_time=run_time, **kwargs)

    def highlight_letter(
        self,
        char,
        color=None,
        layer_index=-1,
        other_bar_opacity=0.35,
        add_to_text=False
    ):
        if color is None:
            color = next(self.highlight_color_iter)
        index = self.char_alphabet.index(char)
        animation = self.layers[layer_index].animate.highlight(
            index,
            color,
            other_bar_opacity=other_bar_opacity
        )

        if add_to_text:
            self.curr_text += char

        return animation

    def zoom_in_on_letter(self, char, layer_index=-1, add_to_text=True, **kwargs):
        bar = self.get_letter_bar(char, layer_index)
        x_min = self.unit_interval.p2n(bar.get_left())
        x_max = self.unit_interval.p2n(bar.get_right())
        if add_to_text:
            self.curr_text += char
        return self.renormalize_animation(x_min, x_max, center_curr_text=True, **kwargs)

    def fade_in_new_layer(self, char=None, buff=0):
        layer = self.get_new_layer()
        self.layers.add(layer)
        return FadeIn(layer)


class IntroduceCharacterModel(InteractiveScene):

    def construct(self):
        # Show a few example distributions
        frame = self.frame
        input_phrase = "compression is "
        n_initial_letters = 1
        char_labels = CHAR_ALPHABET.replace(" ", "_")
        distribution = get_next_char_distribution(input_phrase[:n_initial_letters])
        bar_chart = self.get_bar_chart(distribution, char_labels)

        out_arrow = Line(3 * UP, 3 * RIGHT, path_arc=-90 * DEG, stroke_width=8, buff=0)
        out_arrow.add_tip(width=0.5, length=0.5)
        out_arrow.set_color(GREY_B)
        out_arrow.shift(bar_chart.get_bottom() - out_arrow.get_end() + 5 * UP)
        # CHANGE: BigModel.png lived in "Paul Assets" next to Grant's video output (private image); now there is a
        # placeholder image next to this file. ImageMobject requires str (not Path) in this version of manimgl.
        model = ImageMobject(str(Path(__file__).parent / "Paul Assets" / "BigModel.png"))
        model.set_height(5)
        model.rotate(-2 * DEG)
        model.next_to(out_arrow.get_start(), LEFT)
        in_arrow = Vector(RIGHT, thickness=5)
        in_arrow.next_to(model, LEFT)
        in_arrow.scale(1.5, about_edge=LEFT)

        def get_in_text(s, font_size=72):
            result = Text(f"“{s}”", font_size=font_size)
            result.next_to(in_arrow, LEFT, buff=0.15)
            result.shift(0.05 * UP)
            return result

        def get_bar_chart(in_text):
            return self.get_bar_chart(
                distribution=get_next_char_distribution(in_text),
                labels=char_labels
            )

        in_text_mob = get_in_text(input_phrase[:n_initial_letters])

        frame.reorient(0, 0, 0, (-4.50, 2.56, 0.00), 12.89)
        self.add(model, in_text_mob, in_arrow, out_arrow, bar_chart)
        self.wait(0.5)
        for n in range(n_initial_letters + 1, len(input_phrase) + 1):
            in_text_mob.set_submobjects(get_in_text(input_phrase[:n]))
            new_chart = get_bar_chart(input_phrase[:n])
            self.play(ReplacementTransform(bar_chart, new_chart), run_time=0.25)
            bar_chart = new_chart
            self.wait(0.5)

        # Highlight distribution and limited vocabulary
        wide_char_rect = SurroundingRectangle(bar_chart.labels, buff=0.05)
        wide_char_rect.set_stroke(YELLOW, 2)
        char_rects = VGroup(
            wide_char_rect.copy().set_width(label.get_width() + 0.1, stretch=True).match_x(label)
            for label in bar_chart.labels
        )
        alphabet_rects = char_rects[:26]
        punc_rects = char_rects[26:]

        in_rect = SurroundingRectangle(in_text_mob)
        out_rect = SurroundingRectangle(bar_chart)
        in_rect.set_stroke(TEAL, 3)
        out_rect.set_stroke(TEAL, 3)
        out_arrow.set_z_index(1)

        self.play(ShowCreation(in_rect))
        self.wait()
        self.play(
            frame.animate(time_span=(0.5, 2.5)).to_default_state().set_y(-1),
            ReplacementTransform(in_rect, out_rect, run_time=1)
        )
        self.wait()
        self.play(
            FadeOut(out_rect),
            ShowCreation(alphabet_rects, lag_ratio=0.05, run_time=2),
        )
        self.wait()
        self.play(
            FadeOut(alphabet_rects, lag_ratio=0.01),
            ShowCreation(punc_rects, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            frame.animate(run_time=3).reorient(0, 0, 0, (-4.50, 2.56, 0.00), 12.89),
            FadeOut(punc_rects, time_span=(1, 2)),
        )

        # Show blank space input
        for n in range(len(input_phrase), -1, -1):
            in_text_mob.set_submobjects(get_in_text(input_phrase[:n]))
            new_chart = get_bar_chart(input_phrase[:n] or " ")
            self.play(ReplacementTransform(bar_chart, new_chart), run_time=0.1)
            bar_chart = new_chart
            self.wait(0.1)
        self.wait()

        self.play(
            frame.animate.reorient(0, 0, 0, (-1.69, 1.39, 0.00), 9.99),
            LaggedStart(*(
                bar.animate(rate_func=there_and_back).set_fill(YELLOW)
                for bar in bar_chart.bars
            ), lag_ratio=0.25),
            LaggedStart(*(
                FadeIn(rect, rate_func=there_and_back)
                for rect in char_rects
            ), lag_ratio=0.25),
            run_time=7
        )

        # Transition to horizontal stack
        diagram = ArithmeticCodingDiagram()
        layer = diagram.layers[0]
        new_dec_labels = self.get_stacked_distribution_dec_labels(layer)

        for bar in bar_chart.bars:
            og = bar.copy()
            bar.rotate(90 * DEG)
            bar.replace(og, stretch=True)

        kw = dict(run_time=3, lag_ratio=0.05)
        self.play(
            LaggedStart(
                (FadeTransform(dec1, dec2)
                for dec1, dec2 in zip(bar_chart.dec_labels, new_dec_labels)),
                group_type=Group,
                **kw
            ),
            ReplacementTransform(bar_chart.bars, layer.bars, **kw),
            ReplacementTransform(bar_chart.labels, layer.labels, **kw),
            LaggedStartMap(FadeOut, Group(in_text_mob, in_arrow, model, out_arrow), shift=UP, time_span=(1, 3)),
            frame.animate(run_time=3).to_default_state().set_y(-1),
        )
        self.add(layer)
        self.wait()

    def get_bar_chart(
        self,
        distribution,
        labels,
        bar_colors=(BLUE_E, TEAL),
        spacing=0.15,
        bar_width=0.25,
        unit_height=15,
        max_height=5,
        label_font_size=36,
        dec_font_size=16,
        bottom=2 * DOWN
    ):
        bars = VGroup(
            Rectangle(width=bar_width, height=prob * unit_height)
            for prob in distribution
        )
        bars.arrange(RIGHT, buff=spacing, aligned_edge=DOWN)
        bars.set_fill(bar_colors, 1, gradient_direction=RIGHT)
        bars.set_stroke(WHITE, 1)
        bars.set_max_height(max_height, stretch=True)
        bars.center()

        dec_labels = VGroup(
            DecimalNumber(100 * prob, font_size=dec_font_size, unit="%", num_decimal_places=1)
            for prob in distribution
        )
        dec_labels.set_fill(GREY_B)
        char_labels = Text(labels, font_size=label_font_size)
        char_labels.next_to(bars, DOWN, SMALL_BUFF)

        for bar, char, dec in zip(bars, char_labels, dec_labels):
            char.match_x(bar)
            dec.next_to(bar, UP, SMALL_BUFF)

        result = VGroup(bars, char_labels, dec_labels)
        result.labels = char_labels
        result.dec_labels = dec_labels
        result.bars = bars
        result.move_to(bottom, DOWN)
        return result

    def get_stacked_distribution_dec_labels(self, layer, font_size=12, num_decimal_places=2):
        dec_labels = VGroup(
            DecimalNumber(x, font_size=font_size, num_decimal_places=num_decimal_places)
            for x in layer.distribution
        )
        dec_labels.set_fill(GREY_B)
        for dec, bar in zip(dec_labels, layer.bars):
            dec.next_to(bar, DOWN, buff=SMALL_BUFF)
            if dec.get_width() > bar.get_width():
                dec.set_opacity(0)
        return dec_labels

    def old_animations(self):
        for group in bar_chart:
            for mob in group:
                mob.save_state()
                mob.scale(0)
                mob.set_opacity(0)
                mob.move_to(model.get_right())

        frame.reorient(0, 0, 0, (-3.64, 2.97, 0.00), 11.64)
        self.add(model, in_text, in_arrow, out_arrow)
        kw = dict(lag_ratio=0.02, path_arc=-45 * DEG, run_time=2)
        self.play(*(
            LaggedStartMap(Restore, group, **kw)
            for group in bar_chart
        ))
        self.wait()
