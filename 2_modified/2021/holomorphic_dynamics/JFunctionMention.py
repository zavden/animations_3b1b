# ==============================================================================
# Scene:      JFunctionMention
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3412-3427)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl JFunctionMention.py JFunctionMention -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/j_invariant.png (placeholder; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class JFunctionMention(Scene):
    def construct(self):
        image = ImageMobject("j_invariant")
        image.set_height(5)
        name = OldTexText("Klein's $j$ function")
        name.next_to(image, UP)
        words = Text("A whole story...")
        words.next_to(image, RIGHT)

        self.play(
            FadeIn(image),
            Write(name)
        )
        self.wait()
        self.play(Write(words))
        self.wait()
