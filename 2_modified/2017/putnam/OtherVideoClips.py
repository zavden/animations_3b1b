# ==============================================================================
# Scene:      OtherVideoClips
# Source:     videos/_2017/putnam.py (lines 177-198)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OtherVideoClips.py OtherVideoClips -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
# ==============================================================================

from manim_imports_ext import *

class OtherVideoClips(Scene):
    def construct(self):
        rect = ScreenRectangle()
        rect.set_height(6.5)
        rect.center()
        rect.to_edge(DOWN)
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
        titles = list(map(OldTexText, [
            "Essence of calculus, chapter 1",
            "Pi hiding in prime regularities",
            "How do cryptocurrencies work?"
        ]))

        self.add(rect)
        last_title = None
        for title in titles:
            title.to_edge(UP, buff = MED_SMALL_BUFF)
            if last_title:
                self.play(ReplacementTransform(last_title, title))
            else:
                self.play(FadeIn(title))
            self.wait(3)
            last_title = title
