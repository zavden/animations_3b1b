# ==============================================================================
# Scene:      IndependenceOpeningQuote
# Source:     videos/_2018/eop/independence.py (lines 106-122)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IndependenceOpeningQuote.py IndependenceOpeningQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - highlighted_quote_terms dict converted to a list of (term, color) pairs (GL OpeningQuote iterates pairs, Cairo took a dict)
# ==============================================================================

from manim_imports_ext import *

class IndependenceOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Far better an ", "approximate", 
            " answer to the ", " right question",
            ", which is often vague, than an ", "exact",
            " answer to the ", "wrong question", "."
        ],
        # CHANGE: GL OpeningQuote iterates highlighted_quote_terms as (term, color) pairs; Cairo took a dict
        "highlighted_quote_terms" : list({
            "approximate" : GREEN,
            "right" : GREEN,
            "exact" : RED,
            "wrong" : RED,
        }.items()),
        "author" : "John Tukey",
        "quote_arg_separator" : "",
    }
