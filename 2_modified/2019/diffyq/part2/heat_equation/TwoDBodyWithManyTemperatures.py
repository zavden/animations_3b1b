# ==============================================================================
# Scene:      TwoDBodyWithManyTemperatures
# Source:     videos/_2019/diffyq/part2/heat_equation.py (lines 5-143)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part2/shared_constructs.py
#
# Run from this folder:
#     manimgl TwoDBodyWithManyTemperatures.py TwoDBodyWithManyTemperatures -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL's arrow is a single filled shape without .tip (AttributeError); its black outline was already set on the previous line
#   - with the view from above (phi=0, as in Cairo) the plate and the cells are in the same plane z=0 and, with the depth test, the plate covers the cells; it is moved 0.01 behind them
#   - ThreeDScene.add sets a perpendicular (3D) stroke and the black outline of the arrow covered its yellow fill; the scene is flat, so it goes back to a flat stroke
#   - GL's filled arrow is much thinner than Cairo's yellow stroke (6): with a black outline of 8 the yellow was not visible; it is lowered to 3
#   - the fill of GL's arrow came out white; it is set to yellow as in the original
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part2/shared_constructs.py -----

def temperature_to_color(temp, min_temp=-1, max_temp=1):
    colors = [BLUE, TEAL, GREEN, YELLOW, "#ff0000"]

    alpha = inverse_interpolate(min_temp, max_temp, temp)
    index, sub_alpha = integer_interpolate(
        0, len(colors) - 1, alpha
    )
    return interpolate_color(
        colors[index], colors[index + 1], sub_alpha
    )


def two_d_temp_func(x, y, t):
    return np.sum([
        c * np.sin(f * var) * np.exp(-(f**2) * t)
        for c, f, var in [
            (0.2, 1, x),
            (0.3, 3, x),
            (0.02, 5, x),
            (0.01, 7, x),
            (0.5, 2, y),
            (0.1, 10, y),
            (0.01, 20, y),
        ]
    ])



# ----- From _2019/diffyq/part2/heat_equation.py -----

class TwoDBodyWithManyTemperatures(ThreeDScene):
    CONFIG = {
        "cells_per_side": 20,
        "body_height": 6,
    }

    def construct(self):
        self.introduce_body()
        self.show_temperature_at_all_points()

    def introduce_body(self):
        height = self.body_height
        buff = 0.025
        rows = VGroup(*[
            VGroup(*[
                Dot(
                    # stroke_width=0.5,
                    stroke_width=0,
                    fill_opacity=1,
                )
                for x in range(self.cells_per_side)
            ]).arrange(RIGHT, buff=buff)
            for y in range(self.cells_per_side)
        ]).arrange(DOWN, buff=buff)
        for row in rows[1::2]:
            row.submobjects.reverse()

        body = self.body = VGroup(*it.chain(*rows))
        body.set_height(height)
        body.center()
        body.to_edge(LEFT)

        axes = self.axes = Axes(
            x_min=-5, x_max=5,
            y_min=-5, y_max=5,
        )
        axes.match_height(body)
        axes.move_to(body)

        for cell in body:
            self.color_cell(cell)
        # body.set_stroke(WHITE, 0.5)  # Do this?

        plate = Square(
            stroke_width=0,
            fill_color=GREY_D,
            sheen_direction=UL,
            sheen_factor=1,
            fill_opacity=1,
        )
        # CHANGE: with the view from above (phi=0, as in Cairo) the plate and the cells are in the same plane z=0 and, with the depth test, the plate covers the cells; it is moved 0.01 behind them
        plate.replace(body)
        plate.shift(0.01 * IN)

        plate_words = OldTexText("Piece of \\\\ metal")
        plate_words.scale(2)
        plate_words.set_stroke(BLACK, 2, background=True)
        plate_words.set_color(BLACK)
        plate_words.move_to(plate)

        self.play(
            DrawBorderThenFill(plate),
            Write(
                plate_words,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.5, 1)
            )
        )
        self.wait()

        self.remove(plate_words)

    def show_temperature_at_all_points(self):
        body = self.body
        start_corner = body[0].get_center()

        dot = Dot(radius=0.01, color=WHITE)
        dot.move_to(start_corner)

        get_point = dot.get_center

        lhs = OldTex("T = ")
        lhs.next_to(body, RIGHT, LARGE_BUFF)

        decimal = DecimalNumber(
            num_decimal_places=1,
            unit="^\\circ"
        )
        decimal.next_to(lhs, RIGHT, MED_SMALL_BUFF, DOWN)
        decimal.add_updater(
            lambda d: d.set_value(
                40 + 50 * self.point_to_temp(get_point())
            )
        )

        # CHANGE: the fill of GL's arrow came out white; it is set to yellow as in the original
        arrow = Arrow(color=YELLOW).set_fill(YELLOW, 1)
        # CHANGE: GL's filled arrow is much thinner than Cairo's yellow stroke (6): with a black outline of 8 the yellow was not visible; it is lowered to 3
        arrow.set_stroke(BLACK, 3, background=True)
        # CHANGE: GL's arrow is a single filled shape without .tip (AttributeError); its black outline was already set on the previous line
        pass  # GL's filled arrow has no .tip; it already carries the black outline from above
        # arrow.add_to_back(arrow.copy().set_stroke(BLACK, 5))
        arrow.add_updater(lambda a: a.put_start_and_end_on(
            lhs.get_left() + MED_SMALL_BUFF * LEFT,
            get_point(),
        ))

        dot.add_updater(lambda p: p.move_to(
            body[-1] if (1 < len(body)) else start_corner
        ))
        # CHANGE: ThreeDScene.add sets a perpendicular (3D) stroke and the black outline of the arrow covered its yellow fill; the scene is flat, so it goes back to a flat stroke
        self.add(body, dot, lhs, decimal, arrow)
        arrow.set_flat_stroke(True)
        self.play(
            ShowIncreasingSubsets(
                body,
                run_time=10,
                rate_func=linear,
            )
        )
        self.wait()
        self.remove(dot)
        self.play(
            FadeOut(arrow),
            FadeOut(lhs),
            FadeOut(decimal),
        )

    #
    def point_to_temp(self, point, time=0):
        x, y = self.axes.point_to_coords(point)
        return two_d_temp_func(
            0.3 * x, 0.3 * y, t=time
        )

    def color_cell(self, cell, vect=RIGHT):
        p0 = cell.get_corner(-vect)
        p1 = cell.get_corner(vect)
        colors = []
        for point in p0, p1:
            temp = self.point_to_temp(point)
            color = temperature_to_color(temp)
            colors.append(color)
        cell.set_color(color=colors)
        cell.set_sheen_direction(vect)
        return cell
