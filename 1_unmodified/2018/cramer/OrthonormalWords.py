# ==============================================================================
# Scene:      OrthonormalWords
# Source:     videos/_2018/cramer.py (lines 1218-1244)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OrthonormalWords.py OrthonormalWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OrthonormalWords(Scene):
    def construct(self):
        v_tex = "\\vec{\\textbf{v}}"
        w_tex = "\\vec{\\textbf{w}}"
        top_words = OldTex(
            "\\text{If }",
            "T(", v_tex, ")", "\\cdot",
            "T(", w_tex, ")", "=",
            v_tex, "\\cdot", w_tex,
            "\\text{ for all }", v_tex, "\\text{ and }", w_tex,
        )
        top_words.set_color_by_tex_to_color_map({
            v_tex: YELLOW,
            w_tex: MAROON_B,
        })
        bottom_words = OldTexText(
            "$T$", "is", "``Orthonormal''"
        )
        bottom_words.set_color_by_tex("Orthonormal", BLUE)
        words = VGroup(top_words, bottom_words)
        words.arrange(DOWN, buff=MED_LARGE_BUFF)
        for word in words:
            word.add_background_rectangle()
        words.to_edge(UP)

        self.play(Write(words))
        self.wait()
