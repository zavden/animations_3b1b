# ==============================================================================
# Scene:      BoxCountingSierpinski
# Source:     videos/_2017/fractal_dimension.py (lines 1992-2038)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BoxCountingSierpinski.py BoxCountingSierpinski -w -m --fps 15
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


class BoxCountingSierpinski(BoxCountingScene):
    CONFIG = {
        "box_width" : 0.1,
        "sierpinski_order" : 7,
        "sierpinski_width" : 3,
        "num_boundary_check_points" : 6,
        "corner_rect_left_extension" : 2,
    }
    def construct(self):
        self.add(self.get_grid())
        sierp = Sierpinski(order = self.sierpinski_order)
        sierp.set_fill(opacity = 0)
        sierp.move_to(3*DOWN, DOWN+RIGHT)
        sierp.set_width(self.sierpinski_width)
        boxes = self.get_highlighted_boxes(sierp)

        corner_rect = self.get_corner_rect()
        counting_label = self.get_counting_label()

        self.play(ShowCreation(sierp))
        self.play(*list(map(FadeIn, [corner_rect, counting_label])))
        self.wait()
        counting_mob = self.count_boxes(boxes)
        self.wait()
        self.play(
            FadeOut(boxes),
            sierp.scale, 2, sierp.get_corner(DOWN+RIGHT),
        )
        self.play(counting_mob.next_to, counting_mob, DOWN)
        boxes = self.get_highlighted_boxes(sierp)
        new_counting_mob = self.count_boxes(boxes)
        self.wait()

        frac_line = OldTex("-")
        frac_line.set_color(YELLOW)
        frac_line.stretch_to_fit_width(new_counting_mob.get_width())
        frac_line.next_to(new_counting_mob, DOWN, buff = SMALL_BUFF)
        approx_three = OldTex("\\approx 3")
        approx_three.next_to(frac_line, RIGHT)
        equals_exp = OldTex("= 2^{1.585...}")
        equals_exp.next_to(approx_three, RIGHT, aligned_edge = DOWN)
        equals_exp.shift_onto_screen()

        self.play(*list(map(Write, [frac_line, approx_three])))
        self.wait()
        self.play(Write(equals_exp))
        self.wait()
