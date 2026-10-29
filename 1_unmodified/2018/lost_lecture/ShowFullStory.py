# ==============================================================================
# Scene:      ShowFullStory
# Source:     videos/_2018/lost_lecture.py (lines 306-357)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFullStory.py ShowFullStory -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowFullStory(Scene):
    def construct(self):
        directory = os.path.join(
            MEDIA_DIR,
            "animations/active_projects/lost_lecture/images"
        )
        scene_names = [
            "ShowEmergingEllipse",
            "ShowFullStory",
            "FeynmanFameStart",
            "TheMotionOfPlanets",
            "FeynmanElementaryQuote",
            "DrawingEllipse",
            "ShowEllipseDefiningProperty",
            "ProveEllipse",
            "KeplersSecondLaw",
            "AngularMomentumArgument",
            "HistoryOfAngularMomentum",
            "FeynmanRecountingNewton",
            "IntroduceShapeOfVelocities",
            "ShowEqualAngleSlices",
            "PonderOverOffCenterDiagram",
            "UseVelocityDiagramToDeduceCurve",
        ]
        images = Group(*[
            ImageMobject(os.path.join(directory, name + ".png"))
            for name in scene_names
        ])
        for image in images:
            image.add(
                SurroundingRectangle(image, buff=0, color=WHITE)
            )
        images.arrange_in_grid(n_rows=4)

        images.scale(
            1.01 * FRAME_WIDTH / images[0].get_width()
        )
        images.shift(-images[0].get_center())

        self.play(
            images.set_width, FRAME_WIDTH - 1,
            images.center,
            run_time=3,
        )
        self.wait()
        self.play(
            images.shift, -images[2].get_center(),
            images.scale, FRAME_WIDTH / images[2].get_width(),
            {"about_point": ORIGIN},
            run_time=3,
        )
        self.wait()
