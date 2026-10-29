# ==============================================================================
# Scene:      MapOfVideo
# Source:     videos/_2018/borsuk_addition.py (lines 142-198)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl MapOfVideo.py MapOfVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class MapOfVideo(MovingCameraScene):
    def construct(self):
        images = Group(
            ImageMobject("NecklaceThumbnail"),
            ImageMobject("BorsukUlamThumbnail"),
            ImageMobject("TopologyProofThumbnail"),
            ImageMobject("ContinuousNecklaceThumbnail"),
            ImageMobject("NecklaceSphereAssociationThumbnail")
        )
        for image in images:
            rect = SurroundingRectangle(image, buff=0)
            rect.set_stroke(WHITE, 3)
            image.add(rect)

        image_line = Group(*images[:2], *images[3:])
        image_line.arrange(RIGHT, buff=LARGE_BUFF)
        images[2].next_to(image_line, DOWN, buff=1.5)
        images.set_width(FRAME_WIDTH - 1)
        images.to_edge(UP, buff=LARGE_BUFF)

        arrows = VGroup(
            Arrow(images[0], images[1], buff=SMALL_BUFF),
            Arrow(
                images[1].get_corner(DR) + 0.5 * LEFT,
                images[2].get_top() + 0.5 * LEFT,
            ),
            Arrow(
                images[2].get_top() + 0.5 * RIGHT,
                images[3].get_corner(DL) + 0.5 * RIGHT,
            ),
            Arrow(images[3], images[4], buff=SMALL_BUFF),
        )

        self.play(LaggedStartMap(FadeInFromDown, images, run_time=4))
        self.play(LaggedStartMap(GrowArrow, arrows))
        self.wait()
        group = Group(images, arrows)
        for image in images:
            group.save_state()
            group.generate_target()
            group.target.shift(-image.get_center())
            group.target.scale(
                FRAME_WIDTH / image.get_width(),
                about_point=ORIGIN,
            )

            self.play(MoveToTarget(group, run_time=3))
            self.wait()
            self.play(Restore(group, run_time=3))

    def get_curved_arrow(self, *points):
        line = VMobject()
        line.set_points(points)
        tip = Arrow(points[-2], points[-1], buff=SMALL_BUFF).tip
        line.pointwise_become_partial(line, 0, 0.9)
        line.add(tip)
        return line
