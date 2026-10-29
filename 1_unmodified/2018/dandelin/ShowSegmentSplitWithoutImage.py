# ==============================================================================
# Scene:      ShowSegmentSplitWithoutImage
# Source:     videos/_2018/dandelin.py (lines 1041-1044)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSegmentSplitWithoutImage.py ShowSegmentSplitWithoutImage -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSegmentSplit(Scene):
    CONFIG = {
        "include_image": True,
    }

    def construct(self):
        if self.include_image:
            image = ImageMobject("ShowCircleToCircleLine")
            image.set_height(FRAME_HEIGHT)
            self.add(image)

        brace1 = Brace(Line(ORIGIN, 1.05 * UP), LEFT)
        brace2 = Brace(Line(1.7 * DOWN, ORIGIN), LEFT)
        braces = VGroup(brace1, brace2)
        braces.rotate(-14 * DEGREES)
        braces.move_to(0.85 * UP + 1.7 * LEFT)

        words = VGroup(
            OldTexText("Top segment"),
            OldTexText("Bottom segment")
        )
        for word, brace in zip(words, braces):
            word.next_to(
                brace.get_center(), LEFT,
                buff=0.35
            )
        words[0].set_color(PINK)
        words[1].set_color(GOLD)

        for mob in it.chain(braces, words):
            mob.add_to_back(mob.copy().set_stroke(BLACK, 5))

        for brace in braces:
            brace.save_state()
            brace.set_stroke(width=0)
            brace.scale(0)

        self.play(
            LaggedStartMap(
                Restore, braces,
                lag_ratio=0.7
            ),
        )
        for word in words:
            self.play(Write(word, run_time=1))
        self.wait()


class ShowSegmentSplitWithoutImage(ShowSegmentSplit):
    CONFIG = {
        "include_image": False,
    }
