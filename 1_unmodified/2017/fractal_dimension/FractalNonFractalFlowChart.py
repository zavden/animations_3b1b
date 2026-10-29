# ==============================================================================
# Scene:      FractalNonFractalFlowChart
# Source:     videos/_2017/fractal_dimension.py (lines 2767-2819)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FractalNonFractalFlowChart.py FractalNonFractalFlowChart -w -m --fps 15
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


class FractalNonFractalFlowChart(Scene):
    def construct(self):
        is_fractal = OldTexText("Is it a \\\\ fractal?")
        nature = OldTexText("Probably from \\\\ nature")
        man_made = OldTexText("Probably \\\\ man-made")

        is_fractal.to_edge(UP)
        nature.shift(FRAME_X_RADIUS*LEFT/2)
        man_made.shift(FRAME_X_RADIUS*RIGHT/2)

        yes_arrow = Arrow(
            is_fractal.get_bottom(),
            nature.get_top()
        )
        no_arrow = Arrow(
            is_fractal.get_bottom(),
            man_made.get_top()
        )

        yes = OldTexText("Yes")
        no = OldTexText("No")
        yes.set_color(GREEN)
        no.set_color(RED)

        for word, arrow in (yes, yes_arrow), (no, no_arrow):
            word.next_to(ORIGIN, UP)
            word.rotate(arrow.get_angle())
            if word is yes:
                word.rotate(np.pi)
            word.shift(arrow.get_center())

        britain = Britain()
        britain.set_height(3)
        britain.to_corner(UP+LEFT)
        self.add(britain)

        randy = Randolph()
        randy.set_height(3)
        randy.to_corner(UP+RIGHT)
        self.add(randy)

        self.add(is_fractal)
        self.wait()
        for word, arrow, answer in (yes, yes_arrow, nature), (no, no_arrow, man_made):
            self.play(
                ShowCreation(arrow),
                Write(word, run_time = 1)
            )
            self.play(Write(answer, run_time = 1))
            if word is yes:
                self.wait()
            else:
                self.play(Blink(randy))
