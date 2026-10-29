# ==============================================================================
# Scene:      ParameterizeTheLoop
# Source:     videos/_2024/inscribed_rect/loops.py (lines 996-1721)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl ParameterizeTheLoop.py ParameterizeTheLoop -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The TorusTexture texture is missing (private): placeholder textures TorusTexture.png and MobiusStripTexture.png (grid with colored borders); the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2024/inscribed_rect/example_loop1.svg (placeholder, make_inscribed_rect_svgs.py)
#   - _lib/assets/generated/2024/inscribed_rect/scissors.svg (placeholder, make_inscribed_rect_svgs.py)
#   - _lib/assets/raster_images/TorusTexture.png (placeholder texture, make_inscribed_rect_images.py)
#   - _lib/assets/raster_images/MobiusStripTexture.png (placeholder texture, make_inscribed_rect_images.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/inscribed_rect/helpers.py -----

def get_example_loop(index=1, stroke_color=WHITE, stroke_width=3, width=5):
    result = SVGMobject(f"example_loop{index}").family_members_with_points()[0]
    result.set_width(width)
    result.set_stroke(stroke_color, stroke_width)
    return result


def get_special_dot(
    color=YELLOW,
    radius=0.05,
    glow_radius_multiple=3,
    glow_factor=1.5
):
    return Group(
        TrueDot(radius=radius).make_3d(),
        GlowDot(radius=radius * glow_radius_multiple, glow_factor=glow_factor)
    ).set_color(color)


# Surface functions
def square_func(u, v):
    return (u, v, 0)


def tube_func(u, v):
    return (-math.sin(TAU * u), v, math.cos(TAU * u))


def torus_func(u, v, outer_radius=1.5, inner_radius=0.5):
    theta = TAU * v
    phi = TAU * u
    p = math.cos(theta) * RIGHT + math.sin(theta) * UP
    q = -math.sin(phi) * p + math.cos(phi) * OUT
    return outer_radius * p + inner_radius * q


def mobius_strip_func(u, v, outer_radius=1.5, inner_radius=0.5):
    theta = TAU * v
    phi = theta / 2
    p = math.cos(theta) * RIGHT + math.sin(theta) * UP
    q = math.cos(phi) * p + math.sin(phi) * OUT
    return outer_radius * p + inner_radius * q * (2 * u - 1)


def torus_uv_to_mobius_uv(u, v):
    v2 = (u + v) % 1
    u2 = abs(u - v)
    if u + v >= 1.0:
        u2 = 1.0 - u2
    return u2, v2



# ----- From _2024/inscribed_rect/loops.py -----

class ParameterizeTheLoop(InteractiveScene):
    def construct(self):
        # Set up the loop
        loop = get_example_loop(width=5)
        loop.insert_n_curves(20)
        loop.to_edge(LEFT, buff=LARGE_BUFF)

        x_tracker = ValueTracker()
        get_x = x_tracker.get_value
        loop_x_group = self.get_loop_coord_group(loop, get_x)

        self.add(loop)
        self.add(loop_x_group)

        # Set up the unit interval
        interval = UnitInterval(width=6)
        interval.to_edge(RIGHT)
        interval.add_numbers()

        x_tip = ArrowTip(angle=-90 * DEG)
        x_tip.set_height(0.2)
        x_tip.set_color(YELLOW)
        x_tip.f_always.move_to(lambda: interval.n2p(get_x()), lambda: DOWN)
        int_x_label = DecimalNumber(font_size=24)
        int_x_label.set_color(YELLOW)
        int_x_label.always.next_to(x_tip, UP, buff=0.15)
        int_x_label.f_always.set_value(get_x)

        int_x_group = VGroup(x_tip, int_x_label)
        self.add(interval)
        self.add(int_x_group)

        # Animate changing x
        self.play(x_tracker.animate.set_value(1), run_time=12, rate_func=there_and_back)
        x_tracker.set_value(0)

        # Snip the loop
        snipped_loop = loop.copy()
        sl_points = np.array(loop.get_points())  # Snipped loop points
        sl_points[0] += 0.25 * LEFT
        sl_points[-1] += 0.25 * UP
        snipped_loop.set_points(sl_points)

        scissors = SVGMobject("scissors")
        scissors.set_color(GREY_B)
        scissors.rotate(45 * DEG)
        scissors.set_height(0.75)
        scissors_shift = np.array([0.7, -0.5, 0])
        scissors.move_to(loop.get_start() + scissors_shift)

        self.play(
            FadeOut(loop_x_group),
            FadeOut(int_x_group),
            FadeIn(scissors)
        )
        moving_loop = loop.copy()
        loop.set_stroke(opacity=0.25)
        self.play(
            Transform(moving_loop, snipped_loop, time_span=(0.5, 1.5)),
            scissors.animate.shift(-2 * scissors_shift),
            run_time=2
        )
        self.play(FadeOut(scissors))

        # Map it onto the unit interval
        line = Line(interval.n2p(0), interval.n2p(1))
        line.match_style(moving_loop)
        self.play(Transform(moving_loop, line, run_time=3, path_arc=-30 * DEG))
        self.wait()

        # Show coordinate moving around
        self.play(
            FadeIn(loop_x_group),
            FadeIn(int_x_group),
            loop.animate.set_stroke(opacity=1),
            FadeOut(moving_loop),
        )
        self.play(x_tracker.animate.set_value(1), run_time=5)
        self.wait()
        for value in [0, 1, 0]:
            x_tracker.set_value(value)
            self.wait()

        # Glue 0 to 1
        circular_interval = Circle(radius=TAU / interval.get_length())
        circular_interval.rotate(PI / 2)
        circular_interval.match_style(interval)
        circle_ticks = VGroup(
            Line(1.1 * point, 0.9 * point)
            for a in np.linspace(0, 1, 11)
            for point in [circular_interval.pfp(a)]
        )
        circle_numbers = interval.numbers.copy()
        for tick, number in zip(circle_ticks, circle_numbers):
            number.move_to(1.3 * tick.get_center())
        circle_numbers[-1].move_to(0.7 * circle_ticks[-1].get_center())

        circular_interval.add(circle_ticks, circle_numbers)
        circular_interval.move_to(interval)

        interval.save_state()
        self.play(
            FadeOut(int_x_group),
            Transform(interval, circular_interval, run_time=3),
        )
        self.play(FlashAround(VectorizedPoint(interval.get_start()), run_time=2))
        self.wait()
        self.play(Restore(interval, run_time=3))

        # Add a second point
        y_tracker = ValueTracker(0)
        get_y = y_tracker.get_value
        loop_y_group = self.get_loop_coord_group(loop, get_y, color=PINK, label_direction=UR)
        loop_y_group.update()

        self.add(loop_y_group)
        self.play(
            # FadeIn(loop_y_group, time_span=(0, 1)),
            x_tracker.animate.set_value(0.15),
            y_tracker.animate.set_value(0.25),
            run_time=2,
        )

        # Add a second axis
        x_axis = interval
        y_axis = UnitInterval()
        y_axis.set_width(interval.get_length())
        y_axis.rotate(90 * DEG)
        y_axis.add_numbers(direction=LEFT)

        y_axis.move_to(x_axis.n2p(0))
        y_axis.shift(0.25 * LEFT)

        int_y_group = int_x_group.copy()
        int_y_group.clear_updaters()
        int_y_group.set_color(PINK)
        y_tip, y_dec = int_y_group
        y_tip.rotate(-90 * DEG)
        y_tip.f_always.move_to(lambda: y_axis.n2p(get_y()), lambda: LEFT)
        y_dec.f_always.set_value(get_y)
        y_dec.always.next_to(y_tip, RIGHT, SMALL_BUFF)

        int_y_group.update()
        int_y_group.suspend_updating()
        self.play(
            FadeIn(y_axis),
            VFadeIn(int_x_group),
            x_axis.animate.shift(y_axis.n2p(0) - x_axis.n2p(0)),
            FadeTransformPieces(loop_y_group.copy(), int_y_group),
            run_time=2
        )
        int_y_group.resume_updating()
        self.wait()
        self.play(y_tracker.animate.set_value(0.84), run_time=3)
        self.play(x_tracker.animate.set_value(0.75), run_time=3)
        self.play(y_tracker.animate.set_value(0.65), run_time=3)

        # Show in the unit square
        axes = Axes((0, 1), (0, 1), width=x_axis.get_length(), height=y_axis.get_length())
        axes.shift(x_axis.n2p(0) - axes.c2p(0, 0))
        int_y_group.clear_updaters()
        int_x_group.clear_updaters()
        x_tip, x_dec = int_x_group

        square = Square()
        square.set_z_index(-1)
        square.set_stroke(GREY, 1)
        square.set_fill(GREY_E, 0.5)
        square.set_width(x_axis.get_length())
        square.move_to(x_axis.n2p(0), DL)

        square_point = get_special_dot(color=BLUE)
        square_point.f_always.move_to(lambda: axes.c2p(get_x(), get_y()))

        v_line = Line(DOWN, UP).set_stroke(WHITE, 1)
        h_line = Line(LEFT, RIGHT).set_stroke(WHITE, 1)
        v_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(get_x(), 0), axes.c2p(get_x(), get_y())
        ))
        h_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(0, get_y()), axes.c2p(get_x(), get_y())
        ))
        coord_lines = VGroup(v_line, h_line)

        coord_label = Tex(R"(0.00, 0.00)", font_size=24)
        coord_standins = coord_label.make_number_changeable("0.00", replace_all=True)
        coord_label.always.next_to(square_point, UR, buff=-0.1)
        coord_standins.set_opacity(0)

        coord_lines.update()
        coord_lines.suspend_updating()
        self.play(
            FadeIn(square),
            ShowCreation(v_line),
            ShowCreation(h_line),
            y_tip.animate.flip(UP, about_edge=LEFT),
            x_tip.animate.flip(RIGHT, about_edge=DOWN),
            x_dec.animate.move_to(coord_label[1]),
            y_dec.animate.move_to(coord_label[3]),
            FadeIn(coord_label),
            FadeIn(square_point, scale=0.5),
        )
        coord_lines.resume_updating()

        x_tip.f_always.match_x(lambda: x_axis.n2p(get_x()))
        y_tip.f_always.match_y(lambda: y_axis.n2p(get_y()))
        x_dec.f_always.set_value(get_x)
        y_dec.f_always.set_value(get_y)

        coord_label.replace_submobject(1, x_dec)
        coord_label.replace_submobject(3, y_dec)

        # Move coordinates
        xy_tracker = ValueTracker(np.array([get_x(), get_y()]))
        x_tracker.f_always.set_value(lambda: xy_tracker.get_value()[0])
        y_tracker.f_always.set_value(lambda: xy_tracker.get_value()[1])
        self.add(x_tracker, y_tracker)
        self.play(xy_tracker.animate.set_value([0.50, get_y()]), run_time=4)
        self.play(xy_tracker.animate.set_value([get_x(), 0.20]), run_time=4)
        self.play(xy_tracker.animate.set_value([0.05, get_y()]), run_time=4)
        np.random.seed(0)
        for _ in range(3):
            self.play(xy_tracker.animate.set_value(np.random.random(2)), run_time=4)

        # Highlight the x=0 and x=1 lines
        x_line_color = BLUE
        frame = self.frame
        left_edge = Line(DOWN, UP)
        left_edge.set_stroke(x_line_color, 5)
        left_edge.match_height(square)
        left_edge.move_to(square, LEFT)
        right_edge = left_edge.copy()
        right_edge.move_to(square, RIGHT)

        left_tips = ArrowTip(angle=90 * DEG).get_grid(3, 1, buff=1.0)
        left_tips.move_to(left_edge)
        left_tips.set_color(x_line_color)
        right_tips = left_tips.copy()
        right_tips.move_to(right_edge)

        self.play(xy_tracker.animate.set_value([0, 0]), run_time=2)
        self.play(
            frame.animate.set_height(9),
            ShowCreation(left_edge),
            xy_tracker.animate.set_value([0, 1]),
            run_time=12
        )
        xy_tracker.set_value([1, 0])
        self.play(
            ShowCreation(right_edge),
            xy_tracker.animate.set_value([1, 1]),
            run_time=8
        )
        self.wait()
        self.play(
            Write(left_tips),
            Write(right_tips),
        )

        v_arrows = VGroup(VGroup(left_edge, left_tips), VGroup(right_edge, right_tips))

        # Highlight y=0 and y=1 lines
        y_line_color = GREEN_SCREEN
        bottom_edge = Line(LEFT, RIGHT)
        bottom_edge.set_stroke(y_line_color, 5)
        bottom_edge.match_width(square)
        bottom_edge.move_to(square, DOWN)
        top_edge = bottom_edge.copy()
        top_edge.move_to(square, UP)

        bottom_tips = ArrowTip().get_grid(1, 3, buff=1.0)
        bottom_tips.move_to(bottom_edge)
        bottom_tips.set_color(y_line_color)
        top_tips = bottom_tips.copy()
        top_tips.move_to(top_edge)

        xy_tracker.set_value([0, 0])
        self.play(
            xy_tracker.animate.set_value([1, 0]),
            ShowCreation(bottom_edge),
            Write(bottom_tips, time_span=(2, 4)),
            run_time=4
        )
        xy_tracker.set_value([0, 1])
        self.play(
            xy_tracker.animate.set_value([1, 1]),
            ShowCreation(top_edge),
            Write(top_tips, time_span=(2, 4)),
            run_time=4
        )

        h_arrows = VGroup(VGroup(bottom_edge, bottom_tips), VGroup(top_edge, top_tips))

        # Fold into a torus
        def half_torus_func(u, v):
            return torus_func(u, 0.5 * v)

        surfaces = Group(
            TexturedSurface(ParametricSurface(func), "TorusTexture")
            for func in [square_func, tube_func, half_torus_func, torus_func]
        )
        for surface in surfaces:
            surface.set_shading(0.25, 0.25, 0)
            surface.set_opacity(0.75)

        target_z = 5
        square3d, tube, half_torus, torus = surfaces
        square3d.replace(square)

        surface = square3d.copy()
        surface.replace(square)
        surface.set_z(target_z)

        tube.set_width(surface.get_width() / PI)
        tube.match_height(surface, stretch=True)
        tube.move_to(surface, IN)

        torus.match_depth(tube)
        torus.move_to(tube)
        half_torus.match_width(torus)
        half_torus.move_to(torus, UP)

        cover_rect = SurroundingRectangle(Group(loop, loop_y_group))
        cover_rect.set_fill(BLACK, 1).set_stroke(width=0)

        self.add(surface)
        self.play(
            FadeIn(surface, shift=target_z * OUT),
            FadeIn(cover_rect),
            frame.animate.reorient(-13, 61, 0, (1.52, 1.67, 1.97), 15.41),
            run_time=3,
        )
        self.play(Transform(surface, tube), run_time=3)
        self.wait()
        self.play(Transform(surface, half_torus, path_arc=PI / 2), run_time=3)
        self.play(Transform(surface, torus, path_arc=PI / 2), run_time=3)
        self.wait()
        self.remove(surface)
        self.add(torus)

        # Put torus in position above the loop
        torus_point = TrueDot(color=BLUE)
        torus_point.f_always.move_to(lambda: torus.uv_to_point(get_x(), get_y()))
        torus_point.apply_depth_test()

        self.play(
            FadeOut(cover_rect),
            loop.animate.set_height(6).next_to(y_axis, LEFT, buff=1.5),
            frame.animate.reorient(0, 0, 0, (0.44, 1.84, 0.0), 13.21),
            torus.animate.set_height(7).rotate(50 * DEG, LEFT).move_to(6 * UP),
            torus.animate.set_height(7).rotate(50 * DEG, LEFT).move_to(6 * UP).match_x(square),
            v_arrows.animate.set_opacity(0.25),
            h_arrows.animate.set_opacity(0.25),
            coord_label.animate.scale(1.5),
            run_time=3
        )

        torus_mesh = SurfaceMesh(torus, resolution=(21, 21))
        torus_mesh.set_stroke(WHITE, 0.5, 0.5)
        self.add(torus_point, torus_mesh, torus)
        self.play(
            Write(torus_mesh, lag_ratio=0.01, stroke_width=0.5, run_time=1),
            FadeIn(torus_point),
        )

        target_xys = [
            [0.13, 0.25],
            [0.13, 0.65],
            [0.13, 0.35],
            [0.97, 0.35],
            [0.10, 0.35],
        ]
        for xy in target_xys:
            self.play(xy_tracker.animate.set_value(xy), run_time=4)

        # Wiggle the points
        for _ in range(3):
            self.play(
                xy_tracker.animate.increment_value(0.02 * np.random.uniform(-1, 1, 2)),
                run_time=2,
                rate_func=lambda t: wiggle(t, 7)
            )
            self.wait()

        # Fade back to square
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.57, 0.46, 0.0), 10),
            FadeOut(torus, UP),
            FadeOut(torus_mesh, UP),
            FadeOut(torus_point, UP),
            run_time=2
        )
        self.wait()

        # Show (x, y) -> (y, x) pairs
        coord_ghosts = Group()
        double_arrows = VGroup()

        def get_coord_ghost():
            result = Group(square_point, coord_label).copy()
            result.clear_updaters()
            result.fade(0.25)
            coord_ghosts.add(result)
            return result

        def get_double_arrow():
            point1 = axes.c2p(get_x(), get_y())
            point2 = axes.c2p(get_y(), get_x())
            vect = normalize(point2 - point1)
            result = VGroup(
                Arrow(point1, point2).shift(0.1 * vect),
                Arrow(point2, point1).shift(-0.1 * vect),
            )
            result.set_stroke(GREY_C)
            double_arrows.add(result)
            return result

        def show_reflection():
            x_dot = loop_x_group[0]
            y_dot = loop_y_group[0]
            loop_x_group.suspend_updating()
            loop_y_group.suspend_updating()

            self.add(get_coord_ghost())
            self.play(
                GrowFromPoint(get_double_arrow(), square_point.get_center()),
                xy_tracker.animate.set_value([get_y(), get_x()]),
                Swap(x_dot, y_dot),
                run_time=1
            )
            self.play(Swap(x_dot, y_dot))
            self.wait()
            self.add(get_coord_ghost())

            loop_x_group.resume_updating().update()
            loop_y_group.resume_updating().update()
            self.add(loop_x_group, loop_y_group)
            loop_x_group.update()
            loop_y_group.update()

        for xy in [[0.1, 0.9], [0.8, 0.95]]:
            show_reflection()
            self.play(xy_tracker.animate.set_value(xy))
        show_reflection()

        # Show fold line
        fold_line = Line(axes.c2p(0, 0), axes.c2p(1, 1))
        fold_line.set_stroke(Color("red"), 2)

        self.play(
            ShowCreation(fold_line),
            *map(FadeOut, [v_line, h_line, coord_label, square_point, x_tip, y_tip]),
        )
        self.wait()
        self.play(
            FadeOut(coord_ghosts),
            FadeOut(double_arrows),
            v_arrows.animate.set_opacity(1),
            h_arrows.animate.set_opacity(1),
        )

        # Fold the square
        ul_triangle = Polygon(DL, UL, UR)
        dr_triangle = Polygon(DL, DR, UR)
        for triangle in [ul_triangle, dr_triangle]:
            triangle.replace(square)
            triangle.match_style(square)
            triangle.set_z_index(-1)
            triangle.set_shading(0.25, 0, 0)
            self.add(triangle)
        self.remove(square)

        self.play(
            Rotate(ul_triangle, PI, about_point=square.get_center(), axis=UR),
            Rotate(v_arrows[0], PI, about_point=square.get_center(), axis=UR),
            Rotate(h_arrows[1], PI, about_point=square.get_center(), axis=UR),
            run_time=2
        )
        self.remove(v_arrows)
        self.play(h_arrows.animate.set_color(PURPLE))

        folded_square = Group(dr_triangle, h_arrows, fold_line).copy()

        # Note the diagonal line again
        self.play(
            FadeIn(square_point),
            FadeIn(coord_label),
        )
        self.play(xy_tracker.animate.set_value([0.9, 0.9]), run_time=2)
        self.play(xy_tracker.animate.set_value([0.1, 0.1]), run_time=8)
        self.wait()

        # Comment on the tricky points (Probably edit out the actual transitions)
        self.play(xy_tracker.animate.set_value([0.1, 0]), run_time=2)
        self.play(FlashAround(coord_label))
        self.wait()
        self.play(xy_tracker.animate.set_value([1, 0]), run_time=2)
        self.play(xy_tracker.animate.set_value([1, 0.1]))
        self.play(FlashAround(coord_label))
        self.wait()
        self.play(xy_tracker.animate.set_value([0.9, 0]))
        self.play(FlashAround(coord_label))
        self.wait()
        self.play(xy_tracker.animate.set_value([1, 0]))
        self.play(xy_tracker.animate.set_value([1, 0.9]), run_time=2)
        self.play(FlashAround(coord_label))

        # Fade out axes and such
        self.play(
            LaggedStartMap(FadeOut, Group(
                loop_x_group[1], loop_y_group[1], coord_label, square_point,
                x_axis, y_axis,
            ))
        )
        self.wait()

        # Show the new cut
        cut_line = Line(square.get_center(), square.get_corner(DR))
        cut_line.set_color(YELLOW)
        cut_tips = bottom_tips.copy().set_color(YELLOW)
        cut_tips.rotate(-45 * DEGREES)
        cut_tips.move_to(cut_line)
        cut_arrow1 = VGroup(cut_line, cut_tips)
        cut_arrow2 = cut_arrow1.copy()

        d_tri = Polygon(LEFT, UP, RIGHT)
        d_tri.match_width(square).move_to(square, DOWN)
        r_tri = Polygon(DOWN, LEFT, UP)
        r_tri.match_height(square).move_to(square, RIGHT)
        for tri in d_tri, r_tri:
            tri.set_fill(GREY_D, 0.75)
            tri.set_stroke(width=0)

        fold_line1, fold_line2 = fold_line.replicate(2)
        fold_line1.put_start_and_end_on(square.get_corner(DL), square.get_center())
        fold_line2.put_start_and_end_on(square.get_center(), square.get_corner(UR))

        piece1 = VGroup(d_tri, h_arrows[0], fold_line1).copy()
        piece2 = VGroup(r_tri, h_arrows[1], fold_line2).copy()
        pieces = VGroup(piece1, piece2)
        to_remove = VGroup(h_arrows, fold_line)
        old_tris = VGroup(ul_triangle, dr_triangle)

        self.add(pieces, old_tris, fold_line)
        self.play(
            ShowCreation(cut_line),
            Write(cut_tips, time_span=(0.5, 1.5)),
            FadeIn(pieces),
            FadeOut(old_tris),
            run_time=1.5,
        )
        self.remove(to_remove)
        piece1.add(cut_arrow1)
        piece2.add(cut_arrow2)
        self.add(pieces)
        self.play(VGroup(piece1, piece2).animate.space_out_submobjects(1.5).move_to(square))
        self.wait()

        # Rearrange pieces
        pieces.target = pieces.generate_target()
        pieces.target[0].rotate(90 * DEGREES)
        pieces.target[1].flip()
        pieces.target.arrange(RIGHT, buff=0.5)
        pieces.target.move_to(square)

        self.play(MoveToTarget(pieces), run_time=2)
        self.wait()
        self.play(
            piece1.animate.shift(square.get_center() - piece1[0].get_right()),
            piece2.animate.shift(square.get_center() - piece2[0].get_left()),
        )
        self.play(
            piece1[1].animate.set_opacity(0),
            piece2[1].animate.set_opacity(0),
        )
        self.wait()

        # Fold into a Mobius strip
        custom_squish = bezier([0, 0.05, 0.95, 1])

        def smoothed_mobius_func(u, v):
            return mobius_strip_func(u, custom_squish(v))

        def get_partial_strip(upper_theta=1.0):
            result = ParametricSurface(lambda u, v: mobius_strip_func(
                u, custom_squish(v) * upper_theta / TAU
            ))
            result.scale(2, about_point=ORIGIN)
            result.shift((0, 4, 4))
            return result

        surfaces = Group(
            TexturedSurface(plain_surface, "MobiusStripTexture")
            for plain_surface in [
                ParametricSurface(square_func),
                get_partial_strip(2.0),
            ]
        )
        for surface in surfaces:
            surface.set_shading(0.25, 0.25, 0)
            surface.set_opacity(0.75)

        target_z = 4
        square3d, partial_strip = surfaces
        square3d.rotate(45 * DEG)
        square3d.replace(pieces)
        square3d.set_z(target_z)
        surface = square3d.copy()

        cover_rect.surround(loop, buff=0.2)

        self.play(
            FadeIn(cover_rect),
            FadeIn(surface, shift=target_z * OUT),
            frame.animate.reorient(2, 51, 0, (-0.35, 3.04, 0.42), 15.36),
            run_time=3
        )
        self.play(
            Transform(surface, partial_strip, run_time=2),
        )
        self.play(
            UpdateFromAlphaFunc(surface, lambda m, a: m.set_points(
                get_partial_strip(interpolate(2, TAU, smooth(a))).get_points()
            )),
            run_time=5
        )
        self.play(
            frame.animate.reorient(0, 42, 0, (-0.11, 2.48, 0.87), 13.94),
            Rotate(surface, PI, axis=RIGHT),
            run_time=8
        )
        mobius_strip = surface

        # Reintroduce coordiante plane
        self.play(
            frame.animate.reorient(0, 0, 0, (-1.02, 3.21, 0.0), 14.55),
            mobius_strip.animate.rotate(40 * DEG, LEFT).move_to(7.5 * UP),
            loop.animate.scale(1.25, about_edge=RIGHT),
            FadeOut(pieces),
            FadeIn(x_axis),
            FadeIn(y_axis),
            FadeIn(folded_square),
            FadeIn(square_point),
            FadeIn(coord_label),
            FadeIn(loop_x_group[1]),
            FadeIn(loop_y_group[1]),
        )

        # Show a point on the mobius strip
        strip_dot = TrueDot(color=BLUE)

        def update_strip_dot(dot):
            u, v = torus_uv_to_mobius_uv(get_x(), get_y())
            strip_dot.move_to(mobius_strip.uv_to_point(u, v))

        strip_dot.add_updater(update_strip_dot)

        self.play(FadeIn(strip_dot))

        xy_values = [
            [0.5, 0.25],
            [0.9, 0.1],
            [0.8, 0.7],
            [0.53, 0.12],
            [0.0, 0.0],
        ]
        for xy in xy_values:
            self.play(xy_tracker.animate.set_value(xy), run_time=3)

        self.play(xy_tracker.animate.set_value([0.99, 0.99]), run_time=8)
        self.play(xy_tracker.animate.set_value([0, 0]), run_time=8)

        # Map from torus to strip
        torus_group = Group(torus_mesh, torus)
        torus_group.next_to(square, UP, buff=2)

        torus_fold_line = ParametricCurve(lambda t: torus.uv_to_point(t, t), t_range=(0, 1, 0.01))
        torus_fold_line.set_stroke(RED, 1, 1)

        self.play(
            mobius_strip.animate.shift(7 * LEFT),
            GrowFromCenter(torus_group),
            FadeIn(torus_point),
        )
        self.play(
            ShowCreation(torus_fold_line),
            xy_tracker.animate.set_value([0.99, 0.99]),
            run_time=5
        )
        self.wait()

        # Animate torus squish
        squished_torus = TexturedSurface(
            ParametricSurface(lambda u, v: mobius_strip_func(*torus_uv_to_mobius_uv(u, v))),
            "TorusTexture",
        )
        squished_torus.replace(torus)
        squished_torus.rotate(40 * DEG, LEFT)
        squished_torus.set_opacity(0)

        squished_torus_mesh = SurfaceMesh(squished_torus, resolution=(21, 21))
        squished_torus_mesh.match_style(torus_mesh)
        squished_torus_mesh.set_stroke(opacity=0.35)
        squished_torus_mesh.make_jagged()

        new_fold_line = ParametricCurve(lambda t: squished_torus.uv_to_point(t, t), t_range=(0, 0.99, 0.01))

        self.play(
            Transform(torus, squished_torus),
            Transform(torus_mesh, squished_torus_mesh),
            torus_fold_line.animate.set_points(new_fold_line.get_points()),
            run_time=5,
        )
        self.wait()

    def get_loop_coord_group(self, loop, get_x, color=YELLOW, font_size=36, dot_to_num_buff=0.075, label_direction=UL):
        loop_dot = get_special_dot(color=color)
        loop_dot.f_always.move_to(lambda: loop.pfp(get_x()))

        loop_x_label = DecimalNumber(font_size=font_size)
        loop_x_label.match_color(loop_dot[1])
        loop_x_label.set_backstroke(BLACK, 3)
        loop_x_label.always.next_to(loop_dot[0], label_direction, buff=dot_to_num_buff)
        loop_x_label.f_always.set_value(get_x)

        return Group(loop_dot, loop_x_label)
