# ==============================================================================
# Scene:      GenericSymbolInformation
# Source:     videos/_2026/cross_entropy/entropy.py (lines 2374-2446)
# Category:   2 · Renders with modifications
# Includes code copied from: _2026/cross_entropy/distribution.py, _2026/cross_entropy/next_char.py
#
# Run from this folder:
#     manimgl GenericSymbolInformation.py GenericSymbolInformation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Replaced Grant's nanoGPT model (nonexistent checkpoint) with a synthetic character model (n-grams over text_data/ + English frequencies); the probabilities shown are plausible, not those of the real model.
#
# Placeholder assets (not Grant's originals):
#   - text_data/quotes.txt and training_data_examples.txt: original text and public-domain quotes (_lib/assets/generated/2026/cross_entropy/text_data/) instead of 3b1b's, which quoted copyrighted works
#
# Extra packages installed in the venv: torch
#
# Notes:
#   arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo.
# ==============================================================================

from __future__ import annotations
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


class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, width=0.5, *args, **kwargs):
        super().__init__("arrow.svg", *args, **kwargs)
        self.set_width(width)
        self.rotate(angle_of_vector(direction))
        self.direction = direction


class ArrowGroup(VGroup):
    def __init__(self):
        super().__init__(InstructionArrow(v) for v in [UP, DOWN, LEFT, RIGHT])


class ProbIcon(VGroup):
    def __init__(
        self,
        prob,
        radius=0.5,
        color=GREEN,
        label_font_size=24,
    ):
        super().__init__()
        self.sector_color = color
        self.label_font_size = label_font_size

        border = Circle(radius=radius).set_stroke(WHITE, 1)
        self.border = border
        self.add(border)

        self.sector = self.get_sector(prob)
        self.label = self.get_label(prob)

        self.add(self.border, self.sector, self.label)

    def set_value(self, value):
        self.label.set_value(100 * value)
        self.sector.become(self.get_sector(value))
        return self

    def get_sector(self, prob):
        radius = self.border.get_width() / 2
        sector = Sector(angle=-prob * TAU, start_angle=TAU / 4, radius=radius)
        sector.set_fill(self.sector_color, 1, border_width=1)
        sector.shift(self.border.get_center())
        return sector

    def get_label(self, prob):
        ndp = 0
        if prob < 0.01:
            ndp = 2
        elif (100 * prob) % 1 == 0.5:
            ndp = 1
        label = DecimalNumber(
            100 * prob,
            unit="%",
            font_size=self.label_font_size,
            num_decimal_places=ndp
        )
        label.next_to(self.border, DOWN, SMALL_BUFF)
        return label


class InformationOfLanguage(InteractiveScene):
    random_seed = 3
    # example_text = "information theory quiz"
    example_text = "compression is intelligence"
    final_shown_sample_index = -1

    def construct(self):
        # Set up ticker tape
        frame = self.frame
        arrow_dist = [0.5, 0.25, 0.125, 0.125]
        text = self.example_text
        n_syms = len(text)
        arrow_choice_indexes = random.choices(
            list(range(4)),
            weights=arrow_dist,
            k=n_syms
        )

        top_tape = Square().get_grid(1, n_syms, buff=0)
        top_tape.set_width(FRAME_WIDTH - 1)
        top_tape.to_edge(UP)
        top_tape.set_stroke(WHITE, 2)

        low_tape = top_tape.copy()
        low_tape.set_y(-1)

        top_probs = np.array([arrow_dist[i] for i in arrow_choice_indexes])
        top_prob_icons = self.get_prob_icons(top_tape, top_probs)

        low_probs = np.array([
            get_next_char_distribution(" " if n == 0 else text[:n])[CHAR_ALPHABET.index(char)]
            for n, char in enumerate(text.lower())
        ])
        low_probs[-1] = 0.3  # This just seems wrong to me

        low_prob_icons = self.get_prob_icons(low_tape, low_probs)

        # Show stream of symbols
        arrow_templates = VGroup(svg[0] for svg in ArrowGroup())
        arrow_templates.set_fill(opacity=1)
        arrow_templates.set_height(0.7 * top_tape[0].get_height())
        arrow_templates.set_submobject_colors_by_gradient(YELLOW_B, YELLOW_C, YELLOW_D)

        arrows = VGroup(
            arrow_templates[idx].copy().move_to(square)
            for square, idx in zip(top_tape, arrow_choice_indexes)
        )

        frame.set_height(2.0).move_to(top_tape[0], LEFT).shift(0.5 * DOWN)
        self.play(
            frame.animate.set_height(FRAME_HEIGHT).move_to(top_tape),
            ShowIncreasingSubsets(top_tape, rate_func=linear),
            ShowIncreasingSubsets(arrows, rate_func=linear),
            ShowIncreasingSubsets(top_prob_icons, rate_func=linear),
            run_time=5
        )
        self.wait()

        # Show scanning distribution
        next_arrow, arrow_distribution = self.get_prediction(top_tape[0], top_tape[1], arrow_dist, arrow_templates, dist_mob_width=5)
        dist_bar_labels = VGroup(
            Tex(Rf"1/{denom}", font_size=24).next_to(bar, UP, SMALL_BUFF)
            for bar, denom in zip(arrow_distribution.bars, [2, 4, 8, 8])
        )
        arrow_distribution.add(dist_bar_labels)
        arrow_distribution.center()
        arrow_distribution.set_width(8.0)
        arrow_distribution.next_to(frame.get_top(), DOWN, MED_LARGE_BUFF)

        top_groups = VGroup(
            VGroup(*mobs)
            for mobs in zip(top_tape, arrows, top_prob_icons)
        )
        top_groups.save_state()

        self.play(LaggedStart(
            FadeIn(arrow_distribution),
            lag_ratio=0.5
        ))
        self.wait(0.5)

        self.add(next_arrow)
        self.remove(arrows[1:], top_prob_icons[1:])
        shift_value = top_tape[1].get_center() - top_tape[0].get_center()
        next_arrow.shift(-shift_value)
        for n in range(1, len(arrows)):
            next_arrow.shift(shift_value)
            arrow_distribution.highlight(arrow_choice_indexes[n], fade_labels=False)
            self.add(arrows[n], top_prob_icons[n])
            self.wait(0.3)
        self.play(
            FadeOut(arrow_distribution),
            FadeOut(next_arrow),
        )
        self.wait()

        # Show bits
        codewords = VGroup(
            bit_string_mobject(s, font="CMU Serif")
            for s in ["0", "10", "110", "111"]
        )
        codewords.scale(0.85)
        all_bits = VGroup()
        for idx, square in zip(arrow_choice_indexes, top_tape):
            bits = codewords[idx].copy()
            bits.space_out_submobjects(0.85)
            bits.next_to(square, UP)
            all_bits.add(bits)

        self.play(LaggedStart(
            (TransformFromCopy(arrow, bits)
            for arrow, bits in zip(arrows, all_bits)),
            lag_ratio=0.1,
        ))
        self.wait()
        self.play(FadeOut(all_bits))

        # Show stream of words
        text_mob = self.get_text_in_tape(text, low_tape)

        self.play(
            frame.animate.set_y(1.0).set_anim_args(time_span=(0, 3)),
            TransformFromCopy(arrows, text_mob, lag_ratio=0.15),
            TransformFromCopy(top_tape, low_tape, lag_ratio=0.15),
            run_time=5
        )
        self.wait()
        self.play(LaggedStartMap(FadeIn, low_prob_icons, lag_ratio=0.5, run_time=4))
        self.wait()

        # Show generation of text by sampling
        char_pred = get_next_char_distribution(text[0])
        all_chars = Text(CHAR_ALPHABET.upper().replace(" ", "_"), font="Consolas")
        text_pred = self.get_prediction(low_tape[0], low_tape[1], char_pred, all_chars)

        self.play(
            frame.animate.move_to(4 * LEFT + DOWN).set_height(6).set_anim_args(run_time=2),
            Write(text_pred[0]),
            FadeIn(text_pred[1]),
            FadeOut(text_mob[1:]),
            FadeOut(low_prob_icons[1:]),
            FadeOut(next_arrow),
            FadeOut(arrow_distribution),
            FadeOut(top_groups),
        )
        self.wait()

        frame.clear_updaters()
        frame.add_updater(lambda m, dt: m.shift(0.3 * dt * RIGHT))
        end_offset = self.final_shown_sample_index

        for n in range(1, n_syms + end_offset):
            # Select
            text_pred[1].highlight(CHAR_ALPHABET.index(text[n].lower()), other_bar_opacity=0.1)
            self.add(text_mob[n])
            self.add(low_prob_icons[n])
            self.wait(0.5)

            # Next pred
            char_pred = get_next_char_distribution(text[:n + 1])
            next_text_pred = self.get_prediction(low_tape[n], low_tape[n + 1], char_pred, all_chars)

            self.play(
                ReplacementTransform(text_pred[1], next_text_pred[1]),
                FadeOut(text_pred[0]),
                GrowArrow(next_text_pred[0]),
                run_time=0.5
            )
            text_pred = next_text_pred
            self.wait(0.3)

        # Recenter
        frame.clear_updaters()
        self.play(
            frame.animate.to_default_state(),
            FadeOut(text_pred),
            FadeIn(text_mob[end_offset:]),
            FadeIn(low_prob_icons[end_offset:]),
            run_time=2,
        )
        self.add(text_mob, low_prob_icons)

        # Show information
        prob_to_info = Tex(R"p \rightarrow -\log_2(p)", font_size=60)
        prob_to_info["p"][0].set_color(GREEN)
        prob_to_info[R"-\log_2(p)"][0].set_color(BLUE)
        prob_to_info.next_to(low_tape, UP, buff=3.0)

        top_group = VGroup(top_tape, arrows, top_prob_icons)

        low_infos = -np.log2(low_probs)
        bit_height = 0.2
        low_info_bars = self.get_information_bars(low_tape, low_infos, bit_height=bit_height)
        low_info_bars.save_state()
        for bar in low_info_bars:
            bar.stretch(1e-6, 1, about_edge=DOWN)
            bar.set_stroke(width=0)

        self.play(
            FadeIn(prob_to_info, 2 * UP, run_time=2),
            Restore(low_info_bars, lag_ratio=0.1, run_time=3),
            frame.animate.center().set_anim_args(run_time=3),
        )
        self.wait()

        # Show bit lines
        n_bit_lines = 12
        bit_lines = Line(low_tape.get_left(), low_tape.get_right()).replicate(n_bit_lines)
        bit_lines.set_stroke(GREY, 1)
        bit_lines.arrange(UP, buff=bit_height)
        bit_lines.align_to(low_info_bars, DOWN)
        bit_line_labels = VGroup(
            Text(f"{n} bits", font_size=12).set_color(GREY).next_to(line, LEFT, SMALL_BUFF)
            for n, line in enumerate(bit_lines)
        )

        self.add(bit_lines, low_info_bars)
        self.play(
            ShowCreation(bit_lines, lag_ratio=0.03),
            LaggedStartMap(FadeIn, bit_line_labels),
            frame.animate.set_height(8.2, about_edge=RIGHT),
            run_time=2
        )
        self.wait()

        # Highlight a few examples
        fade_rects = FullScreenFadeRectangle().replicate(2)
        fade_rects.set_fill(opacity=0.7)
        fade_rects[0].align_to(low_tape[3], RIGHT)
        fade_rects[1].align_to(low_tape[12], LEFT)
        self.add(fade_rects, prob_to_info)

        self.play(FadeIn(fade_rects))
        self.wait()
        self.play(
            fade_rects[0].animate.align_to(low_tape[18], RIGHT),
            fade_rects[1].animate.align_to(low_tape[20], LEFT),
        )
        self.wait()
        self.play(FadeOut(fade_rects))
        self.wait()

        # Reference units of bits
        low_prob_icons.save_state()
        bit_names = VGroup(label["bits"][0] for label in bit_line_labels)
        bit_name_rects = VGroup(
            SurroundingRectangle(name, buff=0.025)
            for name in bit_names
        )
        bit_name_rects.set_stroke(YELLOW, 2)

        self.play(
            frame.animate.reorient(0, 0, 0, (-4.64, -0.65, 0.0), 3.57),
            FadeOut(prob_to_info),
            LaggedStart(
                (name.animate.set_color(YELLOW)
                for name in bit_names),
                lag_ratio=0.05,
            ),
            run_time=3,
        )
        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                bit_name_rects,
                time_width=1.5,
                lag_ratio=0.05,
            ),
            bit_line_labels.animate.set_color(GREY_B),
            run_time=3
        )
        self.wait()

        # Highlight I
        def get_info_label(index):
            bar = low_info_bars[index]
            info_label = DecimalNumber(low_infos[index])
            info_label.set_backstroke(BLACK, 5)
            info_label.set_width(1.5 * bar.get_width())
            info_label.next_to(bar, UP, buff=SMALL_BUFF)
            return info_label

        I_info_label = get_info_label(0)

        fractional_bits = bit_string_mobject("01100")
        frac_rect = BackgroundRectangle(fractional_bits[-1], buff=0)
        frac_rect.stretch(1 - (low_infos[0] % 1), 1, about_edge=DOWN)
        frac_rect.set_fill(BLACK, 0.9)
        fractional_bits.add(frac_rect)
        fractional_bits.next_to(text_mob[0], LEFT, buff=1.0)
        fractional_bits.match_y(I_info_label)
        fractional_bits.set_fill(border_width=0)

        bits_arrow = Arrow(
            text_mob[0],
            fractional_bits,
            SMALL_BUFF,
            path_arc=-60 * DEG,
            fill_color=TEAL,
        )

        self.play(
            Write(I_info_label),
            *(
                group[1:].animate.set_opacity(0.2)
                for group in [low_info_bars, text_mob, low_prob_icons]
            )
        )
        self.play(
            GrowArrow(bits_arrow),
            GrowFromPoint(fractional_bits, I_info_label.get_center()),
            frame.animate.reorient(0, 0, 0, (-5.72, -0.44, 0.0), 3.95),
        )
        self.wait()

        # Highlight the "o"
        o_index = 9
        o_info_label = get_info_label(o_index)

        fractional_bit = fractional_bits[-2:].copy()
        fractional_bit[1].stretch(1.1, 1, about_edge=DOWN).set_opacity(0.9)
        fractional_bit.next_to(o_info_label, UL, LARGE_BUFF)
        fractional_bit.add_to_back(
            BackgroundRectangle(fractional_bit, buff=0.1).set_fill(BLACK, 1).set_stroke(WHITE, 1, 0.5)
        )

        new_bit_arrow = Arrow(
            text_mob[o_index].get_left(),
            fractional_bit.get_bottom(),
            path_arc=-60 * DEG,
            fill_color=TEAL,
            buff=SMALL_BUFF,
        )

        self.play(
            frame.animate.reorient(0, 0, 0, (-3.23, -0.34, 0.0), 4.58).set_anim_args(run_time=2),
            FadeOut(fractional_bits),
            FadeOut(bits_arrow),
            FadeTransform(I_info_label, o_info_label, run_time=2),
            *(
                AnimationGroup(
                    group[o_index].animate.set_opacity(1),
                    group[0].animate.set_opacity(0.2),
                )
                for group in [low_info_bars, text_mob, low_prob_icons]
            )
        )
        self.wait()
        self.play(
            GrowArrow(new_bit_arrow),
            GrowFromPoint(fractional_bit, o_info_label.get_center())
        )
        self.wait()

        # Zoom out to full message
        short_text = "information theory"
        n_short = len(short_text)
        short_text_mob = text_mob[:n_short]
        low_prob_icons.saved_state[n_short:].set_opacity(0)
        p_labels = VGroup(Tex(Rf"p_{{{n}}}") for n in range(n_short))
        p_labels.scale(0.5)
        for icon, p_label in zip(low_prob_icons.saved_state, p_labels):
            p_label.move_to(icon[2])
            icon[2].set_opacity(0)

        self.remove(low_tape[n_short:])
        bit_lines.match_width(low_tape[:n_short], stretch=True, about_edge=LEFT)
        self.add(bit_lines, Point())
        self.play(
            frame.animate.set_height(8).match_x(short_text_mob).set_y(1),
            FadeOut(o_info_label),
            FadeOut(new_bit_arrow),
            FadeOut(fractional_bit),
            low_info_bars[:n_short].animate.set_opacity(1),
            low_info_bars[n_short:].animate.set_opacity(0),
            short_text_mob.animate.set_opacity(1),
            text_mob[n_short:].animate.set_opacity(0),
            Restore(low_prob_icons),
            FadeIn(p_labels, lag_ratio=0.1),
            run_time=2
        )

        # Encoding a phrase
        phrase = Text(f"“{short_text.upper()}”", font="Consolas")
        phrase.next_to(frame.get_top(), DOWN, buff=MED_LARGE_BUFF)
        encoding = int_to_bit_string(30)
        encoding.next_to(phrase, DOWN, LARGE_BUFF)
        arrow = Arrow(phrase, encoding, buff=SMALL_BUFF)

        self.play(
            FadeTransformPieces(text_mob["INFORMATION"][0].copy(), phrase["INFORMATION"][0]),
            FadeTransformPieces(text_mob["THEORY"][0].copy(), phrase["THEORY"][0]),
            Write(phrase[0], time_span=(0.5, 1.5)),
            Write(phrase[-1], time_span=(0.5, 1.5)),
        )
        self.play(
            GrowArrow(arrow),
            TransformFromCopy(phrase, encoding, lag_ratio=0.05, run_time=2),
        )
        self.wait()

        # Show probability factored out
        p_of = Tex(R"P()")
        p_of[:2].next_to(phrase, LEFT, SMALL_BUFF)
        p_of[2:].next_to(phrase, RIGHT, SMALL_BUFF)

        equals = Tex(R"=", font_size=72)
        equals.rotate(90 * DEG)
        equals.next_to(phrase, DOWN)

        factored_prob = Tex(R"p_0 \cdot p_1 \cdot p_2 \cdot p_3 \cdots p_n")
        factored_prob.next_to(equals, DOWN)

        encoding.save_state()

        self.play(
            encoding.animate.set_width(2.5).set_opacity(0.5).next_to(frame.get_corner(UR), DL),
            FadeOut(arrow, scale=0.5),
            Write(p_of),
        )
        self.play(
            Write(equals),
            *(
                TransformFromCopy(p_labels[n], factored_prob[f"p_{n}"][0])
                for n in [0, 1, 2, 3]
            ),
            TransformFromCopy(p_labels[-1], factored_prob["p_n"][0]),
            TransformFromCopy(p_labels[3:-1], factored_prob[R"\cdots"][0]),
            Write(factored_prob[R"\cdot"][:-1], time_span=(0.5, 2)),
            run_time=2
        )
        self.wait()

        # Cycle through probabilities
        icon_ghosts = low_prob_icons.copy().fade(0.75)

        self.add(icon_ghosts)
        self.play(LaggedStartMap(VFadeInThenOut, low_prob_icons, lag_ratio=0.25, run_time=5))
        self.play(FadeIn(low_prob_icons), FadeOut(icon_ghosts))
        self.wait()

        # Take logs
        log_of = Tex(R"-\log_2()").set_color(BLUE)
        log_of["()"].scale(1.1, about_edge=LEFT)
        log_ofs = log_of.replicate(2)

        for log, term in zip(log_ofs, [p_of, factored_prob]):
            log[:-1].next_to(term, LEFT, buff=SMALL_BUFF)
            log[-1:].next_to(term, RIGHT, buff=SMALL_BUFF)

        self.play(
            *map(Write, log_ofs)
        )
        self.wait()

        # Break up the log
        log_sum = Tex(
            R"-\log_2(p_0) -\log_2(p_1) -\log_2(p_2) - \cdots -\log_2(p_n)",
            t2c={R"\log_2": BLUE, "(": BLUE, ")": BLUE}
        )
        log_sum.next_to(equals, DOWN)

        stacked_bars = low_info_bars[:n_short].copy()
        stacked_bars.rotate(-90 * DEG)
        stacked_bars.arrange(RIGHT, buff=SMALL_BUFF)
        stacked_bars.match_width(log_sum)
        stacked_bars.next_to(log_sum, DOWN)

        self.remove(log_ofs[1])
        self.play(
            *(
                ReplacementTransform(factored_prob[f"p_{n}"], log_sum[f"p_{n}"])
                for n in [0, 1, 2, "n"]
            ),
            *(
                FadeOut(factored_prob[s])
                for s in ["p_3", R"\cdot"]
            ),
            ReplacementTransform(factored_prob[R"\cdots"], log_sum[R"\cdots"]),
            TransformFromCopy(log_ofs[1][R"-\log_2("], log_sum[R"-\log_2("]),
            TransformFromCopy(log_ofs[1][R")"], log_sum[R")"]),
            FadeIn(log_sum["-"][3]),
            run_time=2
        )
        self.wait()
        self.play(
            TransformFromCopy(low_info_bars[:n_short], stacked_bars)
        )
        self.play(stacked_bars.animate.arrange(RIGHT, buff=0).move_to(stacked_bars.get_center()))
        self.wait()

        # Relate encoding to information
        phrase.target = phrase.generate_target()
        phrase.target.shift(UP)

        arrow.next_to(phrase.target, DOWN, SMALL_BUFF)

        encoding.target = encoding.generate_target()
        encoding.target.set_opacity(1)
        encoding.target.match_width(stacked_bars)
        encoding.target.next_to(arrow, DOWN, SMALL_BUFF)

        self.play(
            frame.animate.set_height(9, about_edge=DOWN),
            FadeOut(log_ofs[0], UP),
            FadeOut(p_of, UP),
            MoveToTarget(phrase),
            FadeOut(equals),
            MoveToTarget(encoding),
            GrowArrow(arrow, time_span=(1, 2)),
            log_sum.animate.match_width(stacked_bars).next_to(stacked_bars, UP, SMALL_BUFF),
            run_time=2
        )

        # Add labels
        encoding_length = Text("Optimal \n Encoding length")
        encoding_length.next_to(encoding, LEFT, LARGE_BUFF, aligned_edge=DOWN)
        total_information = Text("Total information")
        total_information.next_to(VGroup(log_sum, stacked_bars), LEFT, LARGE_BUFF)
        total_information.set_color(BLUE_C)

        approx = Tex(R"\approx", font_size=72)
        approx.rotate(90 * DEG)
        approx.move_to(midpoint(encoding_length.get_bottom(), total_information.get_top()))

        equiv = VGroup(encoding_length, approx, total_information)

        self.play(
            FadeIn(equiv, LEFT),
            frame.animate.shift(1.5 * LEFT)
        )
        self.wait()

    def get_text_in_tape(self, text, tape):
        text_mob = Text(text.replace(" ", ".").upper(), font="Consolas")
        for char, char_mob, square in zip(text, text_mob, tape):
            char_mob.move_to(square)
            if char == " ":
                char_mob.scale(0)
            if char == "'":
                char_mob.shift(tape[0].get_height() * 0.25 * UP)
        return text_mob

    def get_prob_icons(self, tape, probs, width_ratio=0.7, max_height=2.0, color=GREEN, labeled=True):
        radius = tape[0].get_width() * 0.5 * width_ratio
        icons = VGroup(
            ProbIcon(
                p,
                radius=radius,
                label_font_size=16,
            ).next_to(box, DOWN, SMALL_BUFF)
            for p, box in zip(probs, tape)
        )
        return icons

        if labeled:
            for p, icon in zip(probs, icons):
                ndp = 0
                if p < 0.01:
                    ndp = 2
                elif (100 * p) % 1 == 0.5:
                    ndp = 1
                label = DecimalNumber(
                    100 * p,
                    unit="%",
                    font_size=16,
                    num_decimal_places=ndp
                )
                label.next_to(icon, DOWN, SMALL_BUFF)
                icon.add(label)
        return icons

    def get_information_bars(self, tape, info_values, width=0.25, bit_height=0.2, color=BLUE_D):
        rects = VGroup(
            Rectangle(width=width, height=bit_height * bits).next_to(box, UP, SMALL_BUFF)
            for box, bits in zip(tape, info_values)
        )
        rects.set_fill(color, 1)
        rects.set_stroke(WHITE, 1)
        return rects

    def get_prediction(self, box1, box2, dist, symbols, dist_mob_width=5, dist_mob_height=0.3):
        arrow = Arrow(
            LEFT, RIGHT,
            path_arc=-170 * DEG,
            thickness=5,
            buff=0.1
        )
        p1 = box1.get_top()
        p2 = box2.get_top()
        arrow.scale(0.5 * get_norm(p1 - p2))
        arrow.next_to(0.5 * (p1 + p2), UP, SMALL_BUFF)

        dist_mob = StackedProbDistribution(
            dist,
            width=dist_mob_width,
            height=dist_mob_height,
            labels=symbols.copy()
        )
        dist_mob.next_to(arrow, UP, SMALL_BUFF)
        return VGroup(arrow, dist_mob)

    def old(self):
        # Show generation of arrows by sampling (much copied from above)
        arrow_pred = self.get_prediction(top_tape[0], top_tape[1], arrow_dist, arrow_templates)

        for n in range(1, n_syms):
            # Select
            arrow_pred[1].highlight(arrow_choice_indexes[n], other_bar_opacity=0.1)
            self.add(arrows[n])
            self.wait(0.5)

            # Next pred
            next_arrow_pred = self.get_prediction(top_tape[n], top_tape[n + 1], arrow_dist, arrow_templates.copy())

            self.play(
                ReplacementTransform(arrow_pred[1], next_arrow_pred[1]),
                FadeOut(text_pred[0]),
                GrowArrow(next_text_pred[0]),
                run_time=0.2
            )
            text_pred = next_text_pred
            self.wait(0.5)

    def cycle_through_phrases(self):
        # Insert all this at the point of "Highlight a few examples"
        # Show average line
        avg_line = bit_lines[0].copy()
        avg_line.set_stroke(YELLOW, 2)
        avg_line.shift(bit_height * low_infos.mean() * UP)
        avg_word = Text("Average", font_size=48)
        avg_word.match_color(avg_line)
        avg_word.set_backstroke(BLACK, 5)
        avg_word.next_to(avg_line, UP, buff=-0.05)
        avg_word.match_x(low_tape[8])

        self.remove(prob_to_info)
        self.play(
            ShowCreation(avg_line),
            Write(avg_word),
        )
        self.wait()
        self.play(
            avg_line.animate.set_stroke(opacity=0.5),
            avg_word.animate.set_opacity(0.5),
        )

        # Cycle through alternate phrases
        phrases = [
            "great ideas are unexpected ",
            "general laws are are succinct, ",
            "once upon a time, there was",
            "3blue1brown is a weird name",
            "al-Khwarizmi was a mathematician",
            "prediction is compression, as shown",
            "a solemn fact to reflect upon, that every",
            "it is not the critic who counts, it is the",
            "cold and timid souls who know",
            "randy the pi creature, the blue one,",
        ]

        for phrase in phrases:
            new_text = phrase[:len(text)]
            new_text_mob = self.get_text_in_tape(new_text, low_tape)
            probs = np.array([
                get_next_char_distribution(" " if n == 0 else new_text[:n])[CHAR_ALPHABET.index(char)]
                for n, char in enumerate(new_text.lower())
            ])
            try:
                idx = new_text.index(",")
                new_text_mob[idx].align_to(low_tape, DOWN)
                probs[idx] = 0.3
            except ValueError:
                pass
            infos = -np.log2(probs)
            prob_icons = self.get_prob_icons(low_tape, probs)
            info_bars = self.get_information_bars(low_tape, -np.log2(probs), bit_height=bit_height)

            kw = dict(lag_ratio=0.05, run_time=2)
            self.play(
                FadeOut(text_mob, **kw),
                FadeIn(new_text_mob, **kw),
                FadeTransformPieces(text_mob, new_text_mob, **kw),
                ReplacementTransform(low_prob_icons, prob_icons, **kw),
                ReplacementTransform(low_info_bars, info_bars, **kw),
            )

            text_mob = new_text_mob
            low_prob_icons = prob_icons
            low_info_bars = info_bars

    def old_for_entropy(self):
        # Highlight all terms
        char_rects, prob_rects = all_rects = VGroup(
            VGroup(SurroundingRectangle(c, buff=0.05) for c in group)
            for group in [text_mob, low_prob_icons]
        )
        all_rects.set_stroke(YELLOW, 2)
        prob_to_info.set_width(2)
        prob_to_info.next_to(bits_group, UP, MED_SMALL_BUFF, LEFT).shift(0.5 * RIGHT)

        low_info_bars.save_state()
        for bar in low_info_bars:
            bar.stretch(0, 1, about_edge=DOWN)

        self.play(LaggedStartMap(ShowCreation, char_rects, run_time=1, lag_ratio=0.1))
        self.wait()
        self.play(ReplacementTransform(char_rects, prob_rects, lag_ratio=0.05))
        self.wait()
        self.add(bits_group, low_info_bars)
        self.play(
            FadeIn(bits_group),
            FadeIn(prob_to_info),
            FadeOut(prob_rects),
            Restore(low_info_bars, lag_ratio=0.05),
        )
        self.wait()

        # Show average line
        avg_line = bit_lines[0].copy()
        avg_line.set_stroke(YELLOW, 2)
        avg_line.shift(bit_height * low_infos.mean() * UP)
        avg_word = Text("Average", font_size=48)
        avg_word.match_color(avg_line)
        avg_word.set_backstroke(BLACK, 5)
        avg_word.next_to(avg_line, UP, buff=-0.05)
        avg_word.match_x(low_tape[8])

        self.play(ShowCreation(avg_line), Write(avg_word))
        self.wait()

        # Emphasize this is not well-defined
        eng_underline = Underline(entropy_question, buff=-0.07, stretch_factor=1)
        eng_underline.set_stroke(RED)
        morty = Mortimer(height=1.5)
        morty.next_to(eng_underline.get_right(), DOWN)
        q_marks = Text("???", font_size=72)
        q_marks.match_color(eng_underline)
        q_marks.next_to(morty, LEFT, aligned_edge=UP)

        for mob in eng_underline, morty, q_marks:
            mob.fix_in_frame()

        self.play(
            VFadeIn(morty),
            morty.change('confused').fix_in_frame(),
            ShowCreation(eng_underline),
            frame.animate.shift(1.0 * UP),
        )
        self.play(Write(q_marks))
        self.play(Blink(morty))
        self.play(
            morty.change("pondering", low_info_bars).fix_in_frame(),
            FadeOut(avg_word),
            FadeOut(avg_line),
        )
        self.wait()

        # Cycle through alternate phrases
        phrases = [
            "Mathematics is an art of logical abstractions",
            "Come on fhqwhgads I said come on fhqwhgads",
            "Oi, that's bollocks and you know it bruv",
            "yo that party last night was straight fire no cap fr fr",
            "omg lol i cant even rn this is sooo cursed lmaooo",
            "G'day mate, chuck us a tinnie from the esky",
            "ATP hydrolysis drives conformational changes in myosin",
            "tfw u finally git push --force and nobody notices",
            "It was the best of times it was the worst",
        ]

        for phrase in phrases:
            new_text = phrase[:len(text)]
            new_text_mob = self.get_text_in_tape(new_text, low_tape)
            probs = np.array([
                get_next_char_distribution(" " if n == 0 else new_text[:n])[CHAR_ALPHABET.index(char)]
                for n, char in enumerate(new_text.lower())
            ])
            if phrase in phrases[-1]:
                # Fudge a little to make predictable
                qs = 1 - probs
                qs *= np.linspace(1, 0, len(probs))**0.5
                probs = 1 - qs
            infos = -np.log2(probs)
            prob_icons = self.get_prob_icons(low_tape, probs)
            info_bars = self.get_information_bars(low_tape, -np.log2(probs), bit_height=bit_height)

            kw = dict(lag_ratio=0.05, run_time=2)
            self.play(
                FadeOut(text_mob, **kw),
                FadeIn(new_text_mob, **kw),
                FadeTransformPieces(text_mob, new_text_mob, **kw),
                ReplacementTransform(low_prob_icons, prob_icons, **kw),
                ReplacementTransform(low_info_bars, info_bars, **kw),
            )
            self.wait()

            text_mob = new_text_mob
            low_prob_icons = prob_icons
            low_info_bars = info_bars

        # Reference 1 bit estimate
        H_English = Tex(R"H[\text{English}]", t2c={"H": BLUE}, font_size=72)
        H_English.move_to(entropy_question)
        H_English.fix_in_frame()

        rhs = Tex(R"\approx 1 \; {\text{bit} \over \text{char}}")
        rhs[R"{\text{bit} \over \text{char}}"].scale(0.8)
        rhs.fix_in_frame()
        rhs.next_to(H_English, RIGHT)

        self.play(
            TransformMatchingTex(
                entropy_question,
                H_English,
                matched_keys={R"\text{Language}": R"\text{English}"},
                match_animation=FadeTransform,
            ),
            FadeOut(eng_underline),
            FadeOut(q_marks),
            morty.change("hesitant", H_English).fix_in_frame(),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("pondering", rhs).fix_in_frame(),
            Write(rhs),
        )
        self.wait()

        # Show bits
        bit_tape = low_tape.copy()
        bit_tape.shift(1.5 * DOWN)
        bits_text = "".join(random.choice(["0", "1"]) for m in text_mob)
        bits_mob = self.get_text_in_tape(bits_text, bit_tape)
        for bit, part in zip(bits_text, bits_mob):
            part.set_color([GREY_C, GREY_A][int(bit)])

        self.play(
            frame.animate.shift(1.5 * DOWN),
            FadeOut(prob_to_info),
            FadeOut(bit_lines[6:]),
            FadeOut(bit_line_labels[6:]),
            FadeOut(low_prob_icons),
            morty.change("thinking", low_tape).fix_in_frame()
        )

        self.play(
            TransformFromCopy(low_tape, bit_tape, lag_ratio=0.1),
            TransformFromCopy(text_mob, bits_mob, lag_ratio=0.1),
            morty.change("maybe", bits_mob).fix_in_frame().set_anim_args(time_span=(1, 2)),
            run_time=3
        )
        self.wait()


class GenericSymbolInformation(InformationOfLanguage):
    def construct(self):
        # Show tape with symbols and probabilities
        sym = Tex(R"S_1")
        var = sym.make_number_changeable("1", edge_to_fix=LEFT)
        var.scale(0.75, about_edge=LEFT)
        n_syms = 16

        tape = Square().get_grid(1, n_syms, buff=0)
        tape.set_width(FRAME_WIDTH - 1)

        symbols = VGroup()
        for n, square in enumerate(tape):
            var.set_value(n)
            new_sym = sym.copy()
            new_sym.move_to(square)
            symbols.add(new_sym)

        symbols.set_submobject_colors_by_gradient(YELLOW_B, RED)

        probs = np.random.random(n_syms)
        prob_icons = self.get_prob_icons(tape, probs)

        self.add(tape)
        self.play(
            ShowIncreasingSubsets(symbols),
            ShowIncreasingSubsets(prob_icons),
            rate_func=linear,
            run_time=2
        )
        self.wait()

        # Show average information information bars
        frame = self.frame
        info_values = -np.log2(probs)
        bit_height = 0.5
        info_bars = self.get_information_bars(tape, info_values, bit_height=bit_height)
        for bar in info_bars:
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)
            bar.set_stroke(opacity=0)

        avg_line = DashedLine(info_bars.get_left(), info_bars.get_right())
        avg_line.scale(1.05).align_to(tape, LEFT)
        avg_line.set_stroke(YELLOW, 3)
        avg_line.set_y(info_bars.get_y(DOWN) + bit_height * info_values.mean())
        avg_word = Text("Average\nInformation")
        avg_word.match_color(avg_line)
        avg_word.next_to(avg_line, RIGHT, SMALL_BUFF)

        self.play(
            frame.animate.reorient(0, 0, 0, (1.15, 0.56, 0.0), 9.71),
            LaggedStartMap(Restore, info_bars),
            ShowCreation(avg_line),
            FadeIn(avg_word, shift=3 * RIGHT, time_span=(0.5, 2)),
            run_time=2
        )
        self.wait()

        # Stack bars, put bits under
        stacked_bars = info_bars.copy()
        stacked_bars.rotate(-90 * DEG)
        stacked_bars.arrange(RIGHT, buff=0)
        stacked_bars.stretch(2, 1)
        stacked_bars.stretch(0.8, 0)
        stacked_bars.next_to(prob_icons, DOWN, LARGE_BUFF)
        stacked_bars.set_fill(BLUE_E)

        self.play(
            TransformFromCopy(info_bars, stacked_bars, lag_ratio=0.1),
            run_time=2
        )
        self.wait()
