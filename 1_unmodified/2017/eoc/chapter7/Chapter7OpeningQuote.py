# ==============================================================================
# Scene:      Chapter7OpeningQuote
# Source:     videos/_2017/eoc/chapter7.py (lines 4-23)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter7OpeningQuote.py Chapter7OpeningQuote -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class Chapter7OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            " Calculus required ",
            "continuity",
            ", and ",
            "continuity ",
            "was supposed to require the ",
            "infinitely little",
            "; but nobody could discover what the ",
            "infinitely little",
            " might be. ",
        ],
        "quote_arg_separator" : "",
        "highlighted_quote_terms" : {
            "continuity" : BLUE,
            "infinitely" : GREEN,
        },
        "author" : "Bertrand Russell",
    }
