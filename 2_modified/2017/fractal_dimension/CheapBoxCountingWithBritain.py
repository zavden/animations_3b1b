# ==============================================================================
# Scene:      CheapBoxCountingWithBritain
# Source:     videos/_2017/fractal_dimension.py (lines 2184-2189)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CheapBoxCountingWithBritain.py CheapBoxCountingWithBritain -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division in range()
#   - Cairo read a low-res pixel array of the mobject; rasterise the filled shapes with cairo_filled_mask (PIL) instead
#   - GL keeps the constructor stroke_width attribute; read the current stroke width instead
#   - GL keeps the constructor fill_opacity attribute; read the current fill opacity instead
#   - numpy 2: np.vstack needs a sequence, not a set
# ==============================================================================

from manim_imports_ext import *
from functools import reduce

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


class BoxCountingScene(Scene):
    CONFIG = {
        "box_width" : 0.25,
        "box_color" : YELLOW,
        "box_opacity" : 0.5,
        "num_boundary_check_points" : 200,
        "corner_rect_left_extension" : 0,
    }
    def setup(self):
        self.num_rows = 2*int(FRAME_Y_RADIUS/self.box_width)+1
        self.num_cols = 2*int(FRAME_X_RADIUS/self.box_width)+1

    def get_grid(self):
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        v_lines = VGroup(*[
            v_line.copy().shift(u*x*self.box_width*RIGHT)
            # CHANGE: Python 2 integer division in range()
            for x in range(self.num_cols//2+1)
            for u in [-1, 1]
        ])
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_lines = VGroup(*[
            h_line.copy().shift(u*y*self.box_width*UP)
            # CHANGE: Python 2 integer division in range()
            for y in range(self.num_rows//2+1)
            for u in [-1, 1]
        ])

        grid = VGroup(v_lines, h_lines)
        if self.box_width > 0.2:
            grid.set_stroke(width = 1)
        else:
            grid.set_stroke(width = 0.5)
        return grid

    def get_highlighted_boxes(self, vmobject):
        points = []
        # CHANGE: GL keeps the constructor stroke_width attribute; read the current stroke width instead
        if vmobject.get_stroke_width() > 0:
            for submob in vmobject.family_members_with_points():
                alphas = np.linspace(0, 1, self.num_boundary_check_points)
                points += [
                    submob.point_from_proportion(alpha)
                    for alpha in alphas
                ]
        # CHANGE: GL keeps the constructor fill_opacity attribute; read the current fill opacity instead
        if vmobject.get_fill_opacity() > 0:
            # CHANGE: Cairo read a low-res pixel array of the mobject; rasterise the filled shapes with cairo_filled_mask (PIL) instead
            box_centers = self.get_box_centers()
            inside = cairo_filled_mask(vmobject, box_centers)
            points += [center for center, hit in zip(box_centers, inside) if hit]
        return self.get_boxes(points)

    def get_box_centers(self):
        bottom_left = reduce(op.add, [
            self.box_width*(self.num_cols/2)*LEFT,
            self.box_width*(self.num_rows/2)*DOWN,
            self.box_width*RIGHT/2,
            self.box_width*UP/2,
        ])
        return np.array([
            bottom_left + (x*RIGHT+y*UP)*self.box_width
            for x in range(self.num_cols)
            for y in range(self.num_rows)
        ])

    def get_boxes(self, points):
        points = np.array(points)
        rounded_points = np.floor(points/self.box_width)*self.box_width
        # CHANGE: numpy 2: np.vstack needs a sequence, not a set
        unique_rounded_points = np.vstack(list({
            tuple(row) for
            row in rounded_points
        }))

        return VGroup(*[
            Square(
                side_length = self.box_width,
                stroke_width = 0,
                fill_color = self.box_color,
                fill_opacity = self.box_opacity,
            ).move_to(point, DOWN+LEFT)
            for point in unique_rounded_points
        ])

    def get_corner_rect(self):
        rect = Rectangle(
            height = FRAME_Y_RADIUS/2,
            width = FRAME_X_RADIUS+self.corner_rect_left_extension,
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.8
        )
        rect.to_corner(UP+RIGHT, buff = 0)
        return rect

    def get_counting_label(self):
        label = OldTexText("Boxes touched:")
        label.next_to(ORIGIN, RIGHT)
        label.to_edge(UP)
        label.shift(self.corner_rect_left_extension*LEFT)
        self.counting_num_reference = label[-1]
        rect = BackgroundRectangle(label)
        rect.stretch(1.3, 0)
        rect.move_to(label, LEFT)
        label.add_to_back(rect)
        return label

    def count_boxes(self, boxes):
        num = DecimalNumber(len(boxes), num_decimal_places = 0)
        num.next_to(boxes, RIGHT)
        num.add_to_back(BackgroundRectangle(num))

        self.play(ShowCreation(boxes, run_time = 3))
        self.play(Write(num))
        self.play(
            num.next_to, self.counting_num_reference, RIGHT, MED_SMALL_BUFF, DOWN,
            num.set_color, YELLOW
        )
        return num


class BoxCountingWithBritain(BoxCountingScene):
    CONFIG = {
        "box_width" : 0.1,
        "num_boundary_check_points" : 5000,
        "corner_rect_left_extension" : 1,
    }
    def construct(self):
        self.show_box_counting()
        self.show_formula()

    def show_box_counting(self):
        self.add(self.get_grid())
        britain = Britain(
            stroke_width = 2,
            fill_opacity = 0
        )
        britain = fractalify(britain, order = 1, dimension = 1.21)
        britain.shift(DOWN+LEFT)
        boxes = self.get_highlighted_boxes(britain)

        self.play(ShowCreation(britain, run_time = 3))
        self.wait()
        self.play(ShowCreation(boxes, run_time = 3))
        self.wait()
        self.play(FadeOut(boxes))
        self.play(britain.scale, 2.5, britain.get_corner(DOWN+RIGHT))
        boxes = self.get_highlighted_boxes(britain)
        self.play(ShowCreation(boxes, run_time = 2))
        self.wait()

    def show_formula(self):
        corner_rect = self.get_corner_rect()
        equation = OldTexText("""
            Number of boxes $\\approx$
            \\quad $c(\\text{scaling factor})^{1.21}$
        """)
        equation.next_to(
            corner_rect.get_corner(UP+LEFT), DOWN+RIGHT
        )

        N = equation[0].copy()
        word_len = len("Numberofboxes")
        approx = equation[word_len].copy()
        c = equation[word_len+1].copy()
        s = equation[word_len+3].copy()
        dim = VGroup(*equation[-len("1.21"):]).copy()

        N.set_color(YELLOW)
        s.set_color(BLUE)
        dim.set_color(GREEN)

        simpler_eq = VGroup(N, approx, c, s, dim)
        simpler_eq.generate_target()
        simpler_eq.target.arrange(buff = SMALL_BUFF)
        simpler_eq.target.move_to(N, LEFT)
        simpler_eq.target[-1].next_to(
            simpler_eq.target[-2].get_corner(UP+RIGHT),
            RIGHT,
            buff = SMALL_BUFF
        )

        self.play(
            FadeIn(corner_rect),
            Write(equation)
        )
        self.wait(2)
        self.play(FadeIn(simpler_eq))
        self.wait()
        self.play(
            FadeOut(equation),
            Animation(simpler_eq)
        )
        self.play(MoveToTarget(simpler_eq))
        self.wait(2)

        log_expression1 = OldTex(
            "\\log(", "N", ")", "=",
            "\\log(", "c", "s", "^{1.21}", ")"
        )
        log_expression2 = OldTex(
            "\\log(", "N", ")", "=",
            "\\log(", "c", ")", "+",
            "1.21", "\\log(", "s", ")"
        )
        for log_expression in log_expression1, log_expression2:
            log_expression.next_to(simpler_eq, DOWN, aligned_edge = LEFT)
            log_expression.set_color_by_tex("N", N.get_color())
            log_expression.set_color_by_tex("s", s.get_color())
            log_expression.set_color_by_tex("^{1.21}", dim.get_color())
            log_expression.set_color_by_tex("1.21", dim.get_color())
        rewired_log_expression1 = VGroup(*[
            log_expression1[index].copy()
            for index in [
                0, 1, 2, 3, #match with log_expression2
                4, 5, 8, 8,
                7, 4, 6, 8
            ]
        ])

        self.play(Write(log_expression1))
        self.remove(log_expression1)
        self.add(rewired_log_expression1)
        self.wait()
        self.play(Transform(
            rewired_log_expression1,
            log_expression2,
            run_time = 2
        ))
        self.wait(2)

        self.final_expression = VGroup(
            simpler_eq, rewired_log_expression1
        )


class CheapBoxCountingWithBritain(BoxCountingWithBritain):
    CONFIG = {
        "skip_animations" : True,
    }
    def construct(self):
        self.show_formula()
