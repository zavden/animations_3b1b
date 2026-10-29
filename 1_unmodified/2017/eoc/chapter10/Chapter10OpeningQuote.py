# ==============================================================================
# Scene:      Chapter10OpeningQuote
# Source:     videos/_2017/eoc/chapter10.py (lines 26-44)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter10OpeningQuote.py Chapter10OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter10OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "For me, mathematics is a collection of ", 
            "examples", "; a ",
            "theorem", " is a statement about a collection of ",
            "examples", " and the purpose of proving ",
            "theorems", " is to classify and explain the ",
            "examples", "."
        ],
        "quote_arg_separator" : "",
        "highlighted_quote_terms" : {
            "examples" : BLUE,
        },
        "author" : "John B. Conway",
        "fade_in_kwargs" : {
            "run_time" : 7,
        }
    }
