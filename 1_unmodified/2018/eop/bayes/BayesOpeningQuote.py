# ==============================================================================
# Scene:      BayesOpeningQuote
# Source:     videos/_2018/eop/bayes.py (lines 7-13)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BayesOpeningQuote.py BayesOpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BayesOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "Inside every non-Bayesian there \\\\ is a Bayesian struggling to get out."
        ],
        "author" : "Dennis V. Lindley",
    }
