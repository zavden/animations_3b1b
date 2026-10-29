# ==============================================================================
# Scene:      SelfSimilarFractalsAsSubset
# Source:     videos/_2017/fractal_dimension.py (lines 263-337)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SelfSimilarFractalsAsSubset.py SelfSimilarFractalsAsSubset -w -m --fps 15
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


class SelfSimilarFractalsAsSubset(Scene):
    CONFIG = {
        "fractal_width" : 1.5
    }
    def construct(self):
        self.add_self_similar_fractals()
        self.add_general_fractals()

    def add_self_similar_fractals(self):
        fractals = VGroup(
            DiamondFractal(order = 5),
            KochSnowFlake(order = 3),
            Sierpinski(order = 5),
        )
        for submob in fractals:
            submob.set_width(self.fractal_width)
        fractals.arrange(RIGHT)
        fractals[-1].next_to(VGroup(*fractals[:-1]), DOWN)

        title = OldTexText("Self-similar fractals")
        title.next_to(fractals, UP)

        small_rect = Rectangle()
        small_rect.replace(VGroup(fractals, title), stretch = True)
        small_rect.scale(1.2)
        self.small_rect = small_rect

        group = VGroup(fractals, title, small_rect)
        group.to_corner(UP+LEFT, buff = MED_LARGE_BUFF)

        self.play(
            Write(title),
            ShowCreation(fractals),
            run_time = 3
        )
        self.play(ShowCreation(small_rect))
        self.wait()

    def add_general_fractals(self):
        big_rectangle = Rectangle(
            width = FRAME_WIDTH - MED_LARGE_BUFF,
            height = FRAME_HEIGHT - MED_LARGE_BUFF,
        )
        title = OldTexText("Fractals")
        title.scale(1.5)
        title.next_to(ORIGIN, RIGHT, buff = LARGE_BUFF)
        title.to_edge(UP, buff = MED_LARGE_BUFF)

        britain = Britain(
            fill_opacity = 0,
            stroke_width = 2,
            stroke_color = WHITE,
        )
        britain.next_to(self.small_rect, RIGHT)
        britain.shift(2*DOWN)

        randy = Randolph().flip().scale(1.4)
        randy.next_to(britain, buff = SMALL_BUFF)
        randy.generate_target()
        randy.target.change_mode("pleading")
        fractalify(randy.target, order = 2)

        self.play(
            ShowCreation(big_rectangle),
            Write(title),
        )
        self.play(ShowCreation(britain), run_time = 5)
        self.play(
            britain.set_fill, BLUE, 1,
            britain.set_stroke, None, 0,
            run_time = 2
        )
        self.play(FadeIn(randy))
        self.play(MoveToTarget(randy, run_time = 2))
        self.wait(2)
