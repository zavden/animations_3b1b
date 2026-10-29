# ==============================================================================
# Scene:      ConstrastSmoothAndFractal
# Source:     videos/_2017/fractal_dimension.py (lines 339-413)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConstrastSmoothAndFractal.py ConstrastSmoothAndFractal -w -m --fps 15
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


class ConstrastSmoothAndFractal(Scene):
    CONFIG = {
        "britain_zoom_point_proportion" : 0.45,
        "scale_factor" : 50,
        "fractalification_order" : 2,
        "fractal_dimension" : 1.21,
    }
    def construct(self):
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        smooth = OldTexText("Smooth")
        smooth.shift(FRAME_X_RADIUS*LEFT/2)
        fractal = OldTexText("Fractal")
        fractal.shift(FRAME_X_RADIUS*RIGHT/2)
        VGroup(smooth, fractal).to_edge(UP)
        background_rectangle = Rectangle(
            height = FRAME_HEIGHT,
            width = FRAME_X_RADIUS,
        )
        background_rectangle.to_edge(RIGHT, buff = 0)
        background_rectangle.set_fill(BLACK, 1)
        background_rectangle.set_stroke(width = 0)
        self.add(v_line, background_rectangle, smooth, fractal)

        britain = Britain(
            fill_opacity = 0,
            stroke_width = 2,
            stroke_color = WHITE,
        )[0]
        anchors = britain.get_anchors()
        smooth_britain = VMobject()
        smooth_britain.set_points_smoothly(anchors[::10])
        smooth_britain.center().shift(FRAME_X_RADIUS*LEFT/2)
        index = np.argmax(smooth_britain.get_anchors()[:,0])
        smooth_britain.zoom_point = smooth_britain.point_from_proportion(
            self.britain_zoom_point_proportion
        )

        britain.shift(FRAME_X_RADIUS*RIGHT/2)
        britain.zoom_point = britain.point_from_proportion(
            self.britain_zoom_point_proportion
        )
        fractalify(
            britain,
            order = self.fractalification_order,
            dimension = self.fractal_dimension,
        )

        britains = VGroup(britain, smooth_britain)
        self.play(*[
            ShowCreation(mob, run_time = 3)
            for mob in britains
        ])
        self.play(
            britains.set_fill, BLUE, 1,
            britains.set_stroke, None, 0,
        )
        self.wait()
        self.play(
            ApplyMethod(
                smooth_britain.scale,
                self.scale_factor,
                smooth_britain.zoom_point
            ),
            Animation(v_line),
            Animation(background_rectangle),
            ApplyMethod(
                britain.scale,
                self.scale_factor,
                britain.zoom_point
            ),
            Animation(smooth),
            Animation(fractal),
            run_time = 10,
        )
        self.wait(2)
