# ==============================================================================
# Scene:      Chapter8OpeningQuote
# Source:     videos/_2017/eoc/chapter8.py (lines 21-81)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter8OpeningQuote.py Chapter8OpeningQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter8OpeningQuote(OpeningQuote, PiCreatureScene):
    CONFIG = {
        "quote" : [
            " One should never try to prove anything that \\\\ is not ",
            "almost obvious", ". "
        ],
        "quote_arg_separator" : "",
        "highlighted_quote_terms" : {
            "almost obvious" : BLUE,
        },
        "author" : "Alexander Grothendieck"
    }
    def construct(self):
        self.remove(self.pi_creature)
        OpeningQuote.construct(self)

        words_copy = self.quote.get_part_by_tex("obvious").copy()
        author = self.author
        author.save_state()
        formula = self.get_formula()
        formula.next_to(author, DOWN, MED_LARGE_BUFF)
        formula.to_edge(LEFT)

        self.revert_to_original_skipping_status()
        self.play(FadeIn(self.pi_creature))
        self.play(
            author.next_to, self.pi_creature.get_corner(UP+LEFT), UP,
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(3)
        self.play(
            author.restore,
            self.pi_creature.change_mode, "plain"
        )
        self.play(
            words_copy.next_to, self.pi_creature, 
                LEFT, MED_SMALL_BUFF, UP,
            self.pi_creature.change_mode, "thinking"
        )
        self.wait(2)
        self.play(
            Write(formula),
            self.pi_creature.change_mode, "confused"
        )
        self.wait()

    def get_formula(self):
        result = OldTex(
            "{d(\\sin(\\theta)) \\over \\,", "d\\theta}", "=",
            "\\lim_{", "h", " \\to 0}", 
            "{\\sin(\\theta+", "h", ") - \\sin(\\theta) \\over", " h}", "=",
            "\\lim_{", "h", " \\to 0}", 
            "{\\big[ \\sin(\\theta)\\cos(", "h", ") + ",
            "\\sin(", "h", ")\\cos(\\theta)\\big] - \\sin(\\theta) \\over", "h}",
            "= \\dots"
        )
        result.set_color_by_tex("h", GREEN, substring = False)
        result.set_color_by_tex("d\\theta", GREEN)

        result.set_width(FRAME_WIDTH - 2*MED_SMALL_BUFF)
        return result
