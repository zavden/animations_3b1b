# ==============================================================================
# Scene:      PreviewTwoMethods
# Source:     videos/_2018/sphere_area.py (lines 338-370)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewTwoMethods.py PreviewTwoMethods -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewTwoMethods(MovingCameraScene):
    def construct(self):
        thumbnails = Group(
            ImageMobject("SphereSurfaceProof1"),
            ImageMobject("SphereSurfaceProof2"),
        )
        for thumbnail in thumbnails:
            thumbnail.set_width(FRAME_WIDTH / 2 - 1)
            thumbnail.add_to_back(SurroundingRectangle(
                thumbnail, buff=0,
                stroke_color=WHITE,
                stroke_width=5
            ))
        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)

        title = OldTexText("Two proofs")
        title.scale(2)
        title.to_edge(UP)

        frame = self.camera.frame

        self.add(title)
        for thumbnail in thumbnails:
            self.play(FadeInFromDown(thumbnail))
        self.wait()
        for thumbnail in thumbnails:
            frame.save_state()
            self.play(
                frame.replace, thumbnail,
                run_time=2
            )
            self.wait()
            self.play(Restore(frame, run_time=2))
