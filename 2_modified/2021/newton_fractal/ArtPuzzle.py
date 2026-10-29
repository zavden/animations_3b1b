# ==============================================================================
# Scene:      ArtPuzzle
# Source:     videos/_2021/newton_fractal.py (lines 4219-4233)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ArtPuzzle.py ArtPuzzle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - White background (FullScreenRectangle): the text is black and it was not visible over the scene's black background (Grant composites it over a light image when editing)
# ==============================================================================

from manim_imports_ext import *

class ArtPuzzle(Scene):
    def construct(self):
        # CHANGE: the text is black (Grant composites it over a light image when editing) and it would
        # not be visible on the scene's black background; a white background is added
        self.add(FullScreenRectangle(fill_color=WHITE, fill_opacity=1))
        words = VGroup(
            Text("Art Puzzle:", font_size=60),
            OldTexText("- Use $\\ge 3$ colors"),
            OldTexText("- Boundary of one color = Boundary of all"),
        )
        words.set_color(BLACK)
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        words[1:].shift(0.5 * DOWN + 0.5 * RIGHT)
        words.to_corner(UL)

        for word in words:
            self.play(FadeIn(word, lag_ratio=0.1))
            self.wait()
