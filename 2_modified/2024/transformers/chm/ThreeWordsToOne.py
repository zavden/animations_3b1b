# ==============================================================================
# Scene:      ThreeWordsToOne
# Source:     videos/_2024/transformers/chm.py (lines 1855-1918)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThreeWordsToOne.py ThreeWordsToOne -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/CHMTopText.png (placeholder)
#   - raster_images/CHM_Exterior.jpeg (placeholder; Grant's Dropbox path, which _lib resolves by name)
#   - svg_images/GenericComputer.svg (original icon)
#   - svg_images/History.svg (original icon)
#   - svg_images/Museum.svg (original icon)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeWordsToOne(InteractiveScene):
    def construct(self):
        # Test
        image = ImageMobject("CHMTopText")
        image.set_height(FRAME_HEIGHT)
        # self.add(image)

        phrase = Text("Computer History Museum", font_size=61)
        words = VGroup(phrase[word][0] for word in phrase.get_text().split(" "))
        words.move_to([0, 2.627, 0])
        og_words = words.copy()
        og_words.shift(DOWN)
        words[0].shift(0.13 * LEFT)
        words[2].shift(0.4 * RIGHT)
        colors = ["#63DCF7", "#90C9FA", "#85D4FE"]
        for word, color in zip(words, colors):
            word.set_color(color)

        words.save_state()

        self.add(words)
        self.wait()

        # Back to unity
        rect = SurroundingRectangle(og_words)
        rect.set_color(RED)
        chm_image = ImageMobject("/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2024/transformers/chm/images/CHM_Exterior.jpeg")
        chm_image.match_width(rect)
        chm_image.next_to(rect, DOWN)

        self.play(Transform(words, og_words))
        self.play(
            ShowCreation(rect),
            FadeIn(chm_image, DOWN)
        )
        self.wait()

        # Three pieces
        rects = VGroup(
            SurroundingRectangle(word).set_fill(color, 0.2).set_stroke(color, 2)
            for word, color in zip(words.saved_state, colors)
        )
        words.set_z_index(1)

        icons = VGroup(
            SVGMobject("GenericComputer.svg"),
            SVGMobject("History.svg"),
            SVGMobject("Museum.svg"),
        )
        for word, icon in zip(words.saved_state, icons):
            icon.set_fill(word.get_color(), 1, border_width=1)
            icon.set_height(1)
            icon.next_to(word, DOWN)

        self.remove(chm_image)
        self.play(
            ReplacementTransform(VGroup(rect), rects),
            Restore(words),
            *(
                FadeTransform(chm_image.copy(), icon)
                for icon in icons
            )
        )
        self.wait()
