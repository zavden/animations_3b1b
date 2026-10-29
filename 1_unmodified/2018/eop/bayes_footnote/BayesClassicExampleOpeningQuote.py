# ==============================================================================
# Scene:      BayesClassicExampleOpeningQuote
# Source:     videos/_2018/eop/bayes_footnote.py (lines 8-16)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BayesClassicExampleOpeningQuote.py BayesClassicExampleOpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BayesClassicExampleOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "When faced with a difficult question, we often " \
            "answer an easier one instead, usually without " \
            "noticing the substitution.",
        ],
        "author" : "Daniel Kahneman",
    }
