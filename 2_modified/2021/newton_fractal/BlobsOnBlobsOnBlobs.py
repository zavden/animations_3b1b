# ==============================================================================
# Scene:      BlobsOnBlobsOnBlobs
# Source:     videos/_2021/newton_fractal.py (lines 4263-4278)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BlobsOnBlobsOnBlobs.py BlobsOnBlobsOnBlobs -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - White background (FullScreenRectangle): the text is black and it was not visible over the scene's black background (Grant composites it over a light image when editing)
# ==============================================================================

from manim_imports_ext import *

class BlobsOnBlobsOnBlobs(Scene):
    def construct(self):
        # CHANGE: the text is black (Grant composites it over a light image when editing) and it would
        # not be visible on the scene's black background; a white background is added
        self.add(FullScreenRectangle(fill_color=WHITE, fill_opacity=1))
        words = OldTexText(
            "Blobs", *(
                " on blobs " + ("\\\\" if n == 2 else "")
                for n in range(6)
            ),
            "..."
        )
        words.set_width(FRAME_WIDTH - 2)
        words.to_edge(UP)
        words.set_color(BLACK)
        self.add(words[0])
        for word in words[1:]:
            self.play(FadeIn(word, 0.25 * UP))
        self.wait()
