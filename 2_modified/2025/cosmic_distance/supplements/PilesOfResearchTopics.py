# ==============================================================================
# Scene:      PilesOfResearchTopics
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 64-82)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PilesOfResearchTopics.py PilesOfResearchTopics -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The paper pages are read from TerenceTaoPapers/ next to this file (before: Grant's Dropbox) and are placeholder pages.
#
# Placeholder assets (not Grant's originals):
#   - TerenceTaoPapers/paper_01..12.png (placeholder paper pages, made with placeholder.py)
# ==============================================================================

from manim_imports_ext import *

class PilesOfResearchTopics(InteractiveScene):
    def construct(self):
        # CHANGE: the paper pages lived in Grant's Dropbox; now there are placeholder pages in TerenceTaoPapers/ next to this file.
        folder = str(Path(__file__).parent / 'TerenceTaoPapers')
        images = Group()
        for n, filename in enumerate(os.listdir(folder)):
            image = ImageMobject(os.path.join(folder, filename))
            image.set_opacity(1.0)
            image.set_height(6)
            image.move_to((3 * n % 10) * 1.0 * RIGHT + n * 0.1 * DOWN)
            border = SurroundingRectangle(image, buff=0)
            border.set_stroke(GREY_C, 3)
            border.set_anti_alias_width(5)
            group = Group(image, border)

            images.add(group)

        images.center().to_edge(UP, buff=0.25)

        self.play(LaggedStartMap(FadeIn, images, shift=0.2 * UP, lag_ratio=0.5, run_time=12))
