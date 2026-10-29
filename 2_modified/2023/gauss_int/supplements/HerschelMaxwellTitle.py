# ==============================================================================
# Scene:      HerschelMaxwellTitle
# Source:     videos/_2023/gauss_int/supplements.py (lines 701-728)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HerschelMaxwellTitle.py HerschelMaxwellTitle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - title.remove(*pre_name) -> title.remove(*pre_name[0]): title["Herschel"] is a VGroup holding a VGroup of glyphs, so remove removed nothing and FadeOut(title) and ReplacementTransform animated the same glyphs at once; with this manimgl's in-place blend that fails because of different sizes
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HerschelMaxwellTitle(InteractiveScene):
    def construct(self):
        title = Text("""
            The Herschel-Maxwell
            derivation for a Gaussian
        """, font_size=72)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_backstroke(width=5)
        self.play(Write(title))
        self.wait(3)

        # Transition to Herschel name
        name = Text("John Herschel", font_size=60)
        years = Text("1792 - 1871")
        bio = VGroup(name, years)
        bio.arrange(DOWN)
        bio.to_corner(UL)
        bio.shift(1.0 * RIGHT)

        pre_name = title["Herschel"]
        # CHANGE: pre_name is a VGroup with a VGroup of glyphs (one match), so remove(*pre_name) removed nothing and FadeOut(title) and ReplacementTransform animated the same glyphs at once; with the in-place blend of structured_array.py:227 that fails because of different sizes
        title.remove(*pre_name[0])
        self.play(
            FadeOut(title, lag_ratio=0.1),
            ReplacementTransform(pre_name, name["Herschel"]),
            FadeInFromPoint(name["John"], pre_name.get_left()),
        )
        self.play(Write(years))
        self.wait()
