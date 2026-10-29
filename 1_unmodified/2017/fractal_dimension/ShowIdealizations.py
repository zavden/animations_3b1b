# ==============================================================================
# Scene:      ShowIdealizations
# Source:     videos/_2017/fractal_dimension.py (lines 442-490)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowIdealizations.py ShowIdealizations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Britain(SVGMobject):
    CONFIG = {
        "file_name" : "Britain.svg",
        "stroke_width" : 0,
        "fill_color" : BLUE_D,
        "fill_opacity" : 1,
        "height" : 5,
        "mark_paths_closed" : True,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_points(self[0].get_points())
        self.submobjects = []
        self.set_height(self.height)
        self.center()


class ShowIdealizations(Scene):
    def construct(self):
        arrow = DoubleArrow(FRAME_X_RADIUS*LEFT, FRAME_X_RADIUS*RIGHT)
        arrow.shift(DOWN)
        left_words = OldTexText("Idealization \\\\ as smooth")
        middle_words = OldTexText("Nature")
        right_words = OldTexText("""
            Idealization
            as perfectly
            self-similar
        """)
        for words in left_words, middle_words, right_words:
            words.scale(0.8)
            words.next_to(arrow, DOWN)
        left_words.to_edge(LEFT)
        right_words.to_edge(RIGHT)
        self.add(arrow, left_words, middle_words, right_words)

        britain = Britain()[0]
        britain.set_height(4)
        britain.next_to(arrow, UP)

        anchors = britain.get_anchors()
        smooth_britain = VMobject()
        smooth_britain.set_points_smoothly(anchors[::10])
        smooth_britain.set_stroke(width = 0)
        smooth_britain.set_fill(BLUE_D, opacity = 1)
        smooth_britain.next_to(arrow, UP)
        smooth_britain.to_edge(LEFT)

        koch_snowflake = KochSnowFlake(order = 5, monochromatic = True)
        koch_snowflake.set_stroke(width = 0)
        koch_snowflake.set_fill(BLUE_D, opacity = 1)
        koch_snowflake.set_height(3)
        koch_snowflake.rotate(2*np.pi/3)
        koch_snowflake.next_to(arrow, UP)
        koch_snowflake.to_edge(RIGHT)

        VGroup(smooth_britain, britain, koch_snowflake).set_color_by_gradient(
            BLUE_B, BLUE_D
        )

        self.play(FadeIn(britain))
        self.wait()
        self.play(Transform(britain.copy(), smooth_britain))
        self.wait()
        self.play(Transform(britain.copy(), koch_snowflake))
        self.wait()
        self.wait(2)
