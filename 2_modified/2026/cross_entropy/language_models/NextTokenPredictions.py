# ==============================================================================
# Scene:      NextTokenPredictions
# Source:     videos/_2026/cross_entropy/language_models.py (lines 107-310)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/embedding.py, _2026/cross_entropy/next_char.py
#
# Run from this folder:
#     manimgl NextTokenPredictions.py NextTokenPredictions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Replaced the transformers GPT-2/Qwen models (no weights) with a synthetic token model (tiktoken's GPT-2 tokenizer, n-grams over text_data/ and author predictions for the scene's prefixes); the probabilities are plausible, not those of the real models.
#
# Placeholder assets (not Grant's originals):
#   - text_data/quotes.txt and training_data_examples.txt: original text and public-domain quotes (_lib/assets/generated/2026/cross_entropy/text_data/) instead of 3b1b's, which quoted copyrighted works
#
# Extra packages installed in the venv: torch, tiktoken
#
# Notes:
#   tiktoken downloads the GPT-2 BPE vocabulary (not model weights) the first time and caches it; internet is needed that one time.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import torch
import numpy as np
import tiktoken


# ----- From _2026/cross_entropy/next_char.py -----

_gpt2_tokenizer = None


_gpt2_model = None


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


def _ensure_gpt2_loaded():
    global _gpt2_tokenizer, _gpt2_model
    if _gpt2_model is not None:
        return
    # CHANGE: GPT-2 tokenizer (tiktoken) + synthetic model instead of transformers' GPT-2 (no weights)
    _gpt2_tokenizer, _gpt2_model = _synth_token_stack()


def gpt2_predict_next_token(text: str, n_shown: int = 7):
    """
    Top-`n_shown` next-token predictions from a local GPT-2 instance.
    Returns (tokens, probs) where tokens is a list of decoded strings and
    probs is a numpy array of their probabilities.
    """
    _ensure_gpt2_loaded()

    input_ids = _gpt2_tokenizer.encode(
        text, add_special_tokens=False, return_tensors="pt"
    )
    with torch.no_grad():
        logits = _gpt2_model(input_ids).logits[0, -1, :]
    probs = torch.softmax(logits, dim=-1)
    top_probs, top_indices = torch.topk(probs, n_shown)
    tokens = [_gpt2_tokenizer.decode([i]) for i in top_indices.tolist()]
    return tokens, top_probs.numpy()



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

class NextTokenPredictions(InteractiveScene):
    def construct(self):
        # Set up tokens
        text = "Once upon a time, there was a tiny pi creature who lived between 3rd and 4th"
        text_mob = Text(text)
        text_mob.to_edge(LEFT, buff=MED_LARGE_BUFF)

        tokens = break_into_tokens(text_mob)
        rects = get_piece_rectangles(tokens, h_buff=0, leading_spaces=True)

        tokenizer = get_token_encoding()
        token_indices = tokenizer.encode(text)
        _, offsets = tokenizer.decode_with_offsets(token_indices)
        prefixes = [text[:offset] for offset in offsets[1:]]
        text_tokens = [text[o1:o2] for o1, o2 in zip(offsets, offsets[1:])]

        # Predictions
        frame = self.frame
        arrows = VGroup(
            Vector(2.5 * RIGHT, fill_color=TEAL, thickness=7).next_to(rect, RIGHT, SMALL_BUFF)
            for rect in rects
        )
        pred_mobs = VGroup(
            self.prediction_mob_from_text(prefix)
            for prefix in prefixes
        )
        for pred_mob, arrow in zip(pred_mobs, arrows):
            pred_mob.next_to(arrow, RIGHT)

        moving_arrow = arrows[0].copy()

        token_ghosts = VGroup(tokens.copy(), rects.copy()).fade(0.8)
        arrow_ghosts = arrows.copy().set_fill(opacity=0.25)

        frame.add_updater(lambda m: m.move_to(moving_arrow))

        last_pm = VGroup()
        for pm, arrow, token, rect, next_token in zip(pred_mobs, arrows, tokens, rects, tokens[1:]):
            pre_pm = pm.copy()
            for part in pre_pm:
                part.scale(1e-4).fade(1).move_to(arrow.get_top() + SMALL_BUFF * UP)
            self.play(
                FadeIn(token),
                FadeIn(rect),
                moving_arrow.animate.move_to(arrow),
                FadeOut(last_pm, shift=(token.get_width() + 1) * RIGHT),
            )
            self.play(
                TransformFromCopy(pre_pm, pm, lag_ratio=0.002, path_arc=-25 * DEG)
            )
            self.wait(0.5)
            last_pm = pm
        self.play(
            FadeOut(last_pm),
        )

        # Step back to highlight model
        frame.clear_updaters()
        model_placeholder = Square(side_length=0.4 * rects.get_width())
        model_placeholder.next_to(moving_arrow, UP, MED_LARGE_BUFF, RIGHT)
        token_rects_copy = VGroup(*tokens[:-2], *rects[:-2]).copy()
        token_rects_copy.sort(lambda p: p[0])
        token_rects_copy.target = token_rects_copy.generate_target()
        pred_mob = last_pm
        pred_mob.scale(2, about_edge=LEFT)
        pred_mob.save_state()

        for mob in [*token_rects_copy.target, *pred_mob]:
            mob.move_to(model_placeholder).fade(1)

        self.play(frame.animate.reorient(0, 0, 0, (5.53, 1.67, 0.0), 14.22))
        self.wait()
        self.play(LaggedStart(
            MoveToTarget(token_rects_copy, path_arc=-90 * DEG, lag_ratio=0.01),
            Restore(pred_mob, lag_ratio=0.005),
            lag_ratio=0.7,
            run_time=2
        ))
        self.wait()

    def prediction_mob_from_text(self, text, n_shown=8, *args, **kwargs):
        tokens, probs = gpt2_predict_next_token(text, n_shown=n_shown)
        return self.get_prediction_distribution(tokens, probs, *args, **kwargs)

    def get_prediction_distribution(
        self, tokens, probs,
        bar_buff=0.3,
        font_size=40,
        n_shown=8,
        prob_1_width=3.0,
        prob_bar_height=0.4,
        prob_bar_colors=(BLUE_D, TEAL_D),
    ):
        prob_bars = VGroup(
            Rectangle(prob * prob_1_width, prob_bar_height)
            for prob in probs
        )
        prob_bars.arrange(DOWN, buff=bar_buff, aligned_edge=LEFT)
        prob_bars.set_fill(WHITE, 1)
        prob_bars.set_submobject_colors_by_gradient(*prob_bar_colors)
        prob_bars.set_stroke(WHITE, 1)

        token_mobs = VGroup(
            Text(token, font_size=font_size).next_to(bar, LEFT, SMALL_BUFF)
            for bar, token in zip(prob_bars, tokens)
        )
        dots = Tex(R"\vdots")
        dots.next_to(token_mobs[-1], DR)

        percentages = VGroup(
            DecimalNumber(
                100 * p,
                unit="%",
                font_size=font_size,
                num_decimal_places=(1 if p > 0.01 else 2),
                fill_color=GREY_B
            ).next_to(prob_bar, RIGHT, SMALL_BUFF)
            for p, prob_bar in zip(probs, prob_bars)
        )

        rows = VGroup(
            VGroup(*trio)
            for trio in zip(token_mobs, prob_bars, percentages)
        )
        rows.add(dots)

        return rows

    def get_pred_mob_row(self, prediction_mob, token):
        for row in prediction_mob[:-1]:
            if row[0].get_text() == token:
                return row
        return prediction_mob[-1]

    def old_animations(self):
        # Predictions
        frame = self.frame
        arrows = VGroup(
            Arrow(
                r1.get_top(),
                r2.get_top(),
                buff=0.2,
                path_arc=-180 * DEG,
                thickness=5,
                fill_color=YELLOW
            )
            for r1, r2 in zip(rects, rects[1:])
        )
        pred_mobs = VGroup(
            self.prediction_mob_from_text(prefix).next_to(VGroup(arrow), UP, index_of_submobject_to_align=-1)
            for prefix, arrow in zip(prefixes, arrows)
        )
        for pred_mob in pred_mobs:
            pred_mob.match_y(pred_mobs[0])

        token_ghosts = VGroup(tokens.copy(), rects.copy()).fade(0.8)
        arrow_ghosts = arrows.copy().set_fill(opacity=0.25)
        self.add(token_ghosts)
        self.add(tokens[0], rects[0])

        frame.add_updater(lambda m, dt: m.scale(1 + 0.02 * dt, about_edge=LEFT))
        self.play(
            frame.animate.set_y(1.5).set_anim_args(time_span=(0, 1)),
            ShowSubmobjectsOneByOne(VGroup(*pred_mobs), rate_func=linear, int_func=np.ceil),
            ShowSubmobjectsOneByOne(VGroup(*arrows), rate_func=linear, int_func=np.ceil),
            ShowIncreasingSubsets(arrow_ghosts, rate_func=linear, int_func=np.ceil),
            *(
                LaggedStartMap(FadeIn, group[1:], lag_ratio=0.4)
                for group in [tokens, rects]
            ),
            run_time=20
        )
        frame.clear_updaters()

        # Highlight one prediction
        example_index = 5
        arrow = arrows[example_index]
        pred_mob = pred_mobs[example_index]

        true_pred = pred_mob[0].copy().set_fill(opacity=1).set_stroke(opacity=1)
        true_pred_rect = SurroundingRectangle(true_pred[2])
        true_pred_rect.set_stroke(YELLOW, 2)
        next_rect = rects[example_index + 1]
        next_token = tokens[example_index + 1]

        prob_label = Tex(R"p = P(\text{true next token})")
        prob_label.next_to(true_pred_rect, RIGHT)

        self.play(
            frame.animate.to_default_state().set_y(1.5),
            VFadeIn(arrow),
            FadeIn(pred_mob),
            FadeOut(tokens[example_index + 1:]),
            FadeOut(rects[example_index + 1:]),
        )
        self.wait()
        self.play(
            pred_mob.animate.set_fill(opacity=0.25).set_stroke(opacity=0.25),
            FadeIn(true_pred),
            ShowCreation(true_pred_rect),
            next_rect.animate.set_fill(YELLOW, 0.25).set_stroke(YELLOW, 2, 1),
            next_token.animate.set_fill(WHITE, 1),
        )
        self.wait()
