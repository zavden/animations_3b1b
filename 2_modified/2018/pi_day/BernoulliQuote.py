# ==============================================================================
# Scene:      BernoulliQuote
# Source:     videos/_2018/pi_day.py (lines 178-200)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BernoulliQuote.py BernoulliQuote -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo indexed glyphs via text.submobjects[i]; GL keeps them nested, so index text[i] instead (single-string OldTexText indexes its glyphs)
# ==============================================================================

from manim_imports_ext import *

HIGHLIGHT_COLOR = YELLOW


class BernoulliQuote(Scene):

    def construct(self):

        text = OldTexText('``Your most profound investigation of the series \\\\'\
         '$1+{1\over 4}+{1\over 9}+{1\over 16} + $ etc., which I had found to be \\\\'\
          'one sixth of the square of $\pi$ itself\dots, not only\\\\'\
        ' gave me the greatest pleasure, but also renown \\\\'\
        'among the whole Academy of St.\ Petersburg."')
        # CHANGE: Cairo indexed the glyphs in text.submobjects; GL keeps them nested, but text[i] already indexes the glyphs of a single-string OldTexText (CL18-D shim)
        text[88].set_fill(HIGHLIGHT_COLOR)
        for char in text[41:60]:
            char.set_fill(HIGHLIGHT_COLOR)
        for char in text[79:107]:
            char.set_fill(HIGHLIGHT_COLOR)
        for char in text[127:143]:
            char.set_fill(HIGHLIGHT_COLOR)
        for char in text[151:157]:
            char.set_fill(HIGHLIGHT_COLOR)

        self.play(LaggedStartMap(FadeIn,text), run_time = 5)
        self.wait()
        self.play(FadeOut(text))
        self.wait
