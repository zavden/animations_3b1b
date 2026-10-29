# ==============================================================================
# Scene:      TheNaturalLog
# Source:     videos/_2026/print_gallery/exponential.py (lines 1253-2031)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TheNaturalLog.py TheNaturalLog -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_texture_folder() points to a 'textures' folder next to the file (the Dropbox path of Grant does not exist)
#   - The PrintGalleryLog/PiHouseLog(Small) textures are procedural placeholder images: periodic strips with picture frames / houses with pi creatures (_lib/assets/generated/2026/print_gallery/make_print_gallery_assets.py)
#   - Patch of TexturedSurface.pointwise_become_partial (the installed ManimGL uses an undefined `im_coords` and raises NameError in ShowCreation of textured surfaces)
#   - small_droste_randy[10] -> small_droste_randy[4]: the placeholder SVG of EscherPiCreature has only 6 parts
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/print_gallery/textures/PrintGalleryLog.png
#   - _lib/assets/generated/2026/print_gallery/textures/PiHouseLog.png
#   - _lib/assets/generated/2026/print_gallery/textures/PiHouseLogSmall.png
#   - _lib/assets/svg_images/EscherPiCreature.svg
#
# Notes:
#   The original images (the rectified 'Print Gallery' lithograph and the 'pi house') are private. Placeholder strips were generated with make_print_gallery_assets.py: they are periodic on both axes and have square cells in (log r, theta) space, with ln(scale):TAU proportion, so after exp or the Droste zoom the ring and sector structure is visible; it is not Escher's work. EscherPiCreature.svg (pi creature drawn by Grant in Escher's style) is not in the repo: PiCreatures_plain.svg is used as a substitute (copied to _lib/assets/svg_images/).
# ==============================================================================

from manim_imports_ext import *

# CHANGE: bug in the installed ManimGL: TexturedSurface.pointwise_become_partial uses the variable
# `im_coords` without defining it (NameError when doing ShowCreation of a textured surface). The
# method is replaced with a corrected version (it also trims the image coordinates).
def _textured_surface_become_partial(self, tsmobject, a, b, axis=None):
    if axis is None:
        axis = self.preferred_creation_axis
    Surface.pointwise_become_partial(self, tsmobject, a, b, axis)
    with self.data.being_written() as data:
        data["im_coords"][:] = tsmobject.data["im_coords"]
    if a <= 0 and b >= 1:
        return self
    nu, nv = tsmobject.get_resolution()
    with self.data.being_written() as data:
        data["im_coords"][:] = self.get_partial_points_array(
            data["im_coords"], a, b, (nu, nv, 2), axis
        )
    return self


TexturedSurface.pointwise_become_partial = _textured_surface_become_partial

def get_texture_folder():
    # CHANGE: the textures lived in Grant's Dropbox; now they are in the "textures" folder next to
    # this file (procedurally generated placeholder images).
    return Path(__file__).parent / "textures"


def get_pi_house_log_image_path(small=False):
    file_name = "PiHouseLogSmall.png" if small else "PiHouseLog.png"
    return Path(get_texture_folder(), file_name)


def get_log_image(log_image_path, scale_factor, resolution=(51, 101)):
    log_image = TexturedSurface(
        Square3D(resolution=resolution),
        log_image_path,
    )
    log_image.set_shading(0, 0, 0)
    log_image.deactivate_depth_test()
    log_image.set_shape(math.log(scale_factor), TAU)
    return log_image


def get_droste_from_log_image_path(log_image_path, scale_factor=256, n_iterations=5, height=7.5):
    log_image = get_log_image(log_image_path, scale_factor)
    log_images = log_image.get_grid(1, n_iterations, buff=0)
    log_images.move_to(ORIGIN, DR)
    log_images.apply_complex_function(np.exp)
    log_images.set_height(height)
    return log_images


def get_image_slice(image: TexturedSurface, delta_u: float, u_min: float):
    """
    Takes in a TexturedSurface for a rectangular image, returns a vertical slice.
    Think of 'u' as the coordinate for the horizontal direction.
    delta_u gives the width of the slice, u_min gives its position
    """
    nu, nv = image.get_resolution()
    image_slice = TexturedSurface(
        Square3D(resolution=(int(delta_u * nu) + 1, nv)),
        image.textures["LightTexture"].path
    )
    image_slice.set_shading(0, 0, 0)
    image_slice.deactivate_depth_test()
    image_slice.set_image_coords_by_uv_func(
        lambda u, v: (u_min + delta_u * u, v)
    )
    width, height, depth = image.get_shape()
    image_slice.set_shape(delta_u * width, height)
    image_slice.move_to(image, DL).shift(u_min * width * RIGHT)
    return image_slice


def apply_func_between_planes(mob, func, src_plane, trg_plane):
    mob.shift(-src_plane.get_origin())
    mob.scale(1.0 / src_plane.get_unit_size(), about_point=ORIGIN)
    mob.apply_complex_function(func)
    mob.scale(trg_plane.get_unit_size(), about_point=ORIGIN)
    mob.shift(trg_plane.get_origin())
    return mob


class TheNaturalLog(InteractiveScene):
    def construct(self):
        # Set up input and output planes
        plane_style = dict(
            background_line_style=dict(
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.5,
            ),
            faded_line_style=dict(
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.1
            )
        )
        z_plane = ComplexPlane((-3, 3), (-1, 7), unit_size=0.8, **plane_style)
        big_z_plane = ComplexPlane((-10, 3), (-20, 20), unit_size=0.8, **plane_style)
        w_plane = ComplexPlane((-3, 3), (-3, 3), unit_size=0.85, **plane_style)

        z_plane.to_edge(LEFT)
        big_z_plane.shift(z_plane.get_origin() - big_z_plane.get_origin())
        w_plane.to_edge(RIGHT)

        for plane in [z_plane, big_z_plane, w_plane]:
            plane.add_coordinate_labels(font_size=16, buff=0.05)

        self.add(z_plane, w_plane)

        # Set up example lines and circles
        v_lines = VGroup(
            Line(z_plane.n2p(x), z_plane.n2p(x + TAU * 1j))
            for x in np.linspace(1, -1, 9)
        )
        v_lines.set_stroke(WHITE, 1)
        v_lines.set_submobject_colors_by_gradient(YELLOW, RED)

        def apply_func_to_z_space(mob, func):
            return apply_func_between_planes(mob, func, z_plane, w_plane)

        circles = apply_func_to_z_space(v_lines.insert_n_curves(100).copy(), np.exp)

        # Add arrows
        right_arrow = Arrow(z_plane, w_plane, thickness=5, fill_color=GREY_B)
        right_arrow.set_y(1)
        left_arrow = right_arrow.copy().rotate(PI)
        left_arrow.set_y(-1)

        right_arrow_label = Tex(R"z \rightarrow e^z", t2c={"z": BLUE})
        left_arrow_label = Tex(R"\ln(w) \leftarrow w", t2c={"w": PINK})
        right_arrow_label.next_to(right_arrow, UP, SMALL_BUFF)
        left_arrow_label.next_to(left_arrow, DOWN, SMALL_BUFF)

        self.add(right_arrow)
        self.add(right_arrow_label)

        self.play(FadeIn(v_lines))
        self.play(TransformFromCopy(v_lines, circles, lag_ratio=0.1, run_time=10, path_arc=(0, 0.8 * PI)))
        self.wait()
        self.play(
            TransformFromCopy(right_arrow, left_arrow, path_arc=-PI / 2),
            FadeTransformPieces(VGroup(*reversed(right_arrow_label.copy())), left_arrow_label, path_arc=-PI / 2),
            FadeOut(v_lines),
        )
        self.play(
            TransformFromCopy(circles, v_lines, lag_ratio=0.1, run_time=3, path_arc=(0, -0.8 * PI)),
        )
        self.wait()

        # Add Droste image
        frame = self.frame
        log_image = get_log_image(get_pi_house_log_image_path(), 16)
        log_image.scale(z_plane.get_unit_size())
        log_image.move_to(z_plane.n2p(math.log(3)), DR)

        droste_image = get_droste_from_log_image_path(get_pi_house_log_image_path(), 16)
        droste_image.match_height(w_plane)
        droste_image.move_to(w_plane)

        w_plane.target = w_plane.generate_target()
        w_plane.target.x_axis.set_stroke(BLACK)
        w_plane.target.y_axis.set_stroke(BLACK)
        w_plane.target.background_lines.set_stroke(GREY_C)
        w_plane.target.faded_lines.set_stroke(GREY_C)
        w_plane.target.coordinate_labels.set_fill(BLACK)
        w_plane.target.coordinate_labels[2].set_opacity(0)

        w_plane.set_z_index(1)
        self.play(
            FadeOut(circles),
            FadeOut(v_lines),
            FadeIn(droste_image),
            MoveToTarget(w_plane),
        )
        self.wait()
        self.play(
            frame.animate.scale(1 / 16, about_point=w_plane.get_origin()),
            run_time=7,
            rate_func=lambda t: there_and_back_with_pause(t, 1.0 / 7),
        )

        # Create slices
        delta_u = 0.025
        n_log_slice_repetitions = 2
        log_image_slices = Group(
            get_image_slice(log_image, delta_u, u)
            for n in range(n_log_slice_repetitions)
            for u in np.arange(0, 1, delta_u)[::-1]
        )
        log_image_slices.arrange(LEFT, buff=0)
        log_image_slices.move_to(log_image, DR)
        droste_image_rings = apply_func_to_z_space(log_image_slices.copy(), np.exp)

        # Set up in dot and out dot
        z_tracker = ComplexValueTracker()

        def get_z():
            return z_tracker.get_value()

        def get_w():
            return np.exp(z_tracker.get_value())

        z_dot = Group(GlowDot(), TrueDot()).set_color(BLUE)
        w_dot = Group(GlowDot(), TrueDot()).set_color(PINK)
        z_dot.f_always.move_to(lambda: z_plane.n2p(get_z()))
        w_dot.f_always.move_to(lambda: w_plane.n2p(get_w()))

        traced_paths = self.get_traced_paths([z_dot, w_dot])

        # Draw circle
        z_tracker.set_value(z_plane.p2n(log_image_slices[0].get_bottom()))
        self.play(
            FadeIn(z_dot),
            FadeIn(w_dot),
            droste_image.animate.set_opacity(0.25)
        )
        self.add(traced_paths)
        self.play(z_tracker.animate.increment_value(TAU * 1j), run_time=2)
        traced_paths.suspend_updating()
        self.wait()

        # Show image ring
        droste_ring = droste_image_rings[0]
        log_slice = log_image_slices[0]
        path_func = path_along_arc(arc_angle=np.array([-0.35 * z_plane.y_axis.p2n(p) for p in log_slice.get_points()]))

        self.play(
            ShowCreation(droste_ring),
            FadeOut(traced_paths[1]),
        )
        self.wait()
        self.play(
            TransformFromCopy(droste_ring, log_slice, path_func=path_func),
            FadeOut(traced_paths[0], time_span=(0, 1)),
            FadeOut(z_dot),
            FadeOut(w_dot),
            run_time=3
        )
        self.wait()
        traced_paths.clear_points()

        # Circle e times smaller
        circle = Circle().replace(droste_ring)
        line = Line(DOWN, UP).match_height(log_slice).move_to(log_slice, DR)
        VGroup(circle, line).set_stroke(WHITE, 2)

        index = int(1 / math.log(16) / delta_u)
        small_ring = droste_image_rings[index].copy()
        small_log_slice = log_image_slices[index].copy()

        in_arrows = VGroup(
            Arrow(3 * v, np.exp(-1) * 3 * v, thickness=4, fill_color=WHITE)
            for v in compass_directions(8)
        )
        in_arrows.replace(circle).scale(0.9)
        in_arrows.set_z_index(2)
        one_over_e_label = Tex(R"\times 1 / e", font_size=36)
        one_over_e_label.next_to(in_arrows[0], UP, buff=0)

        traced_paths.set_stroke(WHITE, 2)
        self.play(
            line.animate.shift(z_plane.get_unit_size() * LEFT),
            circle.animate.scale(np.exp(-1), about_point=w_plane.get_origin()),
            Write(one_over_e_label),
            *map(GrowArrow, in_arrows),
        )
        self.play(ShowCreation(small_ring), FadeOut(circle))
        self.play(
            TransformFromCopy(small_ring, small_log_slice, path_func=path_func),
            FadeOut(line, time_span=(2, 3)),
            run_time=3
        )
        one_arrow = Arrow(log_slice.get_top(), line.get_top(), path_arc=120 * DEG, buff=0.1)
        one_arrow_label = Tex(R"-1", font_size=36).next_to(one_arrow, UP, SMALL_BUFF)
        self.play(
            GrowArrow(one_arrow),
            FadeIn(one_arrow_label, 0.1 * UP),
        )
        self.wait()
        self.play(FadeOut(VGroup(one_arrow, one_arrow_label, in_arrows, one_over_e_label)))

        # Show all the rings in between, and down towards the center
        droste_image_rings.set_opacity(1)
        v_lines = VGroup(
            Line(piece.get_corner(DL), piece.get_corner(UL)).set_stroke(BLACK, 1, 0.5)
            for piece in log_image_slices
        )
        black_circles = VGroup(
            Circle().replace(ring).set_stroke(BLACK, width=np.clip(circle.get_width(), 0, 1), opacity=0.5)
            for ring in droste_image_rings
        )
        log_image_row = log_image.get_grid(1, 4, buff=0)
        log_image_row.move_to(log_image, RIGHT)
        log_image_row.set_opacity(0.9)
        log_image_slices.set_opacity(0.9)

        self.play(
            LaggedStartMap(FadeIn, droste_image_rings, lag_ratio=0.5),
            LaggedStartMap(FadeIn, log_image_slices, lag_ratio=0.5),
            LaggedStartMap(FadeIn, v_lines, lag_ratio=0.5),
            LaggedStartMap(FadeIn, black_circles, lag_ratio=0.5),
            FadeOut(small_ring, time_span=(2, 4)),
            FadeOut(small_log_slice, time_span=(2, 4)),
            run_time=25
        )
        self.remove(log_image_slices, droste_image_rings)
        droste_image.set_opacity(1)
        self.add(log_image_row, droste_image, v_lines, black_circles)
        self.play(
            v_lines.animate.set_stroke(opacity=0.25),
            black_circles.animate.set_stroke(opacity=0.25),
        )
        self.wait()

        # Reference leftward repetition
        self.play(
            frame.animate.set_x(-4.8),
            v_lines.animate.set_opacity(0),
            run_time=7,
            rate_func=there_and_back_with_pause,
        )

        # Show a labeled z_value
        z_tracker.set_value(1.0)
        z_label = VGroup(Tex(R"z = "), DecimalNumber(complex(0)))
        z_label.scale(0.5)
        z_label.arrange(RIGHT, buff=SMALL_BUFF)
        z_label[1].shift(0.02 * UP)
        z_label[1].f_always.set_value(get_z)
        z_label.always.next_to(z_dot, UR, buff=-0.1)
        z_label.set_backstroke(BLACK, 5)
        exp_z_label = Tex(R"e^z")
        exp_z_label.set_z_index(3)
        exp_z_label.set_backstroke(BLACK, 4)
        exp_z_label.always.next_to(w_dot, UR, buff=-0.1)

        traced_paths = self.get_traced_paths([z_dot, w_dot], colors=[BLUE, PINK])
        traced_paths.set_z_index(2)

        brace = Brace(log_image, RIGHT, SMALL_BUFF)
        brace_label = brace.get_tex(R"2\pi")

        w_dot[0].set_color(PINK)
        w_dot[1].set_color(MAROON_E)
        z_dot[1].set_color(BLUE_E)

        self.play(
            FadeIn(z_dot),
            FadeIn(z_label),
        )
        self.play(
            TransformFromCopy(z_dot, w_dot, suspend_mobject_updating=True),
            TransformFromCopy(z_label[0], exp_z_label),
        )
        self.add(traced_paths)
        self.play(
            z_tracker.animate.increment_value(TAU * 1j),
            run_time=3
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_label, 0.25 * RIGHT),
        )
        self.wait()

        # Grow to 4πi
        log_image_slices.add(*log_image_slices.copy())
        log_image_slices.arrange(LEFT, buff=0)
        log_image_slices.move_to(log_image.get_corner(UR), DR)

        big_z_plane.set_z_index(-1)

        circle_points = log_image_slices[1].copy()
        circle_points.set_z_index(3)
        circle_points.save_state()
        apply_func_to_z_space(circle_points, np.exp)

        self.play(
            z_tracker.animate.increment_value(TAU * 1j),
            frame.animate.reorient(0, 0, 0, (0, 2, 0.0), 13),
            FadeOut(v_lines),
            FadeOut(black_circles),
            FadeOut(z_plane, time_span=(2, 4)),
            FadeIn(big_z_plane, time_span=(2, 4)),
            run_time=12
        )
        traced_paths[1].add_updater(lambda m: m.set_stroke(width=1.5))
        traced_paths.suspend_updating()
        self.play(
            ShowCreation(circle_points, lag_ratio=0),
            droste_image.animate.set_opacity(0.5),
        )
        self.play(
            Restore(circle_points, run_time=2),
            traced_paths[0].animate.set_stroke(width=0.5)
        )
        self.wait()
        self.play(
            ShowCreation(log_image_slices, lag_ratio=0.03, run_time=5),
            FadeOut(circle_points, time_span=(1, 2)),
            traced_paths[0].animate.set_stroke(width=2),
            droste_image.animate.set_opacity(1),
        )
        self.add(log_image_slices)
        self.wait()
        traced_paths.resume_updating()

        # Add more tiles below
        log_image_tiles = log_image.get_grid(7, 6, buff=0)
        log_image_tiles.move_to(log_image, RIGHT)
        log_image_tiles.set_opacity(0.8)

        self.remove(log_image_row, log_image_slices, droste_image)
        self.add(log_image_tiles, droste_image)
        self.wait()
        self.play(
            frame.animate.set_y(-1),
            z_tracker.animate.increment_value(-3 * TAU * 1j),
            run_time=12
        )
        self.wait()

        # Place point on the pi
        traced_paths.clear_updaters()
        v_line, pink_circle = traced_paths
        v_line.add_updater(lambda m: m.match_x(z_dot))
        pink_circle.add_updater(lambda m: m.set_width(2 * get_norm(w_dot.get_center() - w_plane.get_origin())).move_to(w_plane.get_origin()))

        self.add(log_image_tiles, z_label, z_dot)
        self.play(
            z_tracker.animate.set_value(complex(0.5, -2.3)),
            frame.animate.set_y(0),
            run_time=3
        )
        self.play(FlashAround(z_label[0]))
        self.play(
            w_plane.animate.scale(2, about_point=w_plane.get_left()),
            droste_image.animate.scale(2, about_point=w_plane.get_left()),
            run_time=2
        )
        self.wait()
        self.play(TransformFromCopy(z_dot, w_dot, suspend_mobject_updating=True))
        self.play(FlashAround(exp_z_label))
        self.wait()

        # Show the pi creatures
        droste_randy = SVGMobject("EscherPiCreature")
        droste_randy.set_z_index(3)
        droste_randy.set_fill(border_width=1)
        droste_randy.set_height(1.9)
        droste_randy.move_to(w_plane.c2p(-1.24, -1.34))

        log_randy = droste_randy.copy()
        log_randy.apply_points_function(lambda ps: np.array([
            z_plane.n2p(np.log(w_plane.p2n(p)))
            for p in ps
        ]), about_point=ORIGIN)
        z_unit = z_plane.get_unit_size()
        log_randys = VGroup(
            log_randy,
            log_randy.copy().shift(TAU * z_unit * UP),
            log_randy.copy().shift(2 * TAU * z_unit * UP),
        )
        brace_group = VGroup(brace, brace_label)

        log_randy_rect = SurroundingRectangle(log_randys[0]).set_stroke(YELLOW, 3)

        self.play(
            FadeOut(z_label),
            FadeOut(exp_z_label),
            FadeOut(z_dot),
            FadeOut(w_dot),
            v_line.animate.set_stroke(width=1),
            pink_circle.animate.set_stroke(width=1),
            log_image_tiles.animate.set_opacity(0.25),
            droste_image.animate.set_opacity(0.25),
            w_plane.axes.animate.set_stroke(WHITE),
            w_plane.coordinate_labels.animate.set_fill(WHITE),
            FadeIn(log_randy),
            FadeIn(droste_randy),
        )
        self.play(FadeIn(log_randy_rect, scale=0.25, run_time=1, rate_func=rush_into))
        self.play(FlashAround(log_randys[0], run_time=2, stroke_width=6))
        self.wait()
        self.play(
            TransformFromCopy(log_randy, log_randys[1]),
            log_randy_rect.animate.surround(log_randys[1]),
            brace_group.animate.set_y(log_randy.get_y(), DOWN),
        )
        self.play(FlashAround(log_randys[1], run_time=2, stroke_width=6))
        self.play(
            TransformFromCopy(log_randys[1], log_randys[2]),
            log_randy_rect.animate.surround(log_randys[2]),
        )
        self.play(FlashAround(log_randys[2], run_time=2, stroke_width=6))
        self.wait()
        self.play(FadeOut(log_randy_rect))
        self.play(
            LaggedStart(
                (TransformFromCopy(lr, droste_randy)
                for lr in reversed(log_randys)),
                lag_ratio=0.25,
                run_time=4
            )
        )
        self.wait()

        # Show a band of values
        log_image_row = log_image_tiles.copy()
        log_image_row.set_opacity(1)
        limit_box = Rectangle(20, TAU)
        z_unit = z_plane.get_unit_size()
        limit_box.scale(z_unit)
        limit_box.move_to(z_plane.n2p(3), DR)
        limit_box.set_stroke(width=0)
        log_image_row.always.clip_to_box(limit_box)

        self.play(FadeIn(log_image_row))
        self.wait()
        self.play(
            limit_box.animate.shift(z_unit * PI * DOWN),
            run_time=5,
            rate_func=there_and_back
        )
        self.play(limit_box.animate.scale(5), run_time=6)
        self.remove(limit_box)
        self.play(FadeOut(log_image_row))
        self.wait()

        # Droste randy to log randys
        long_log_randys = VGroup(
            *log_randys,
            log_randy.copy().shift(z_unit * TAU * DOWN),
            log_randy.copy().shift(2 * z_unit * TAU * DOWN),
        )
        long_log_randys.save_state()
        w_dot.set_z_index(3)
        z_dot.set_z_index(3)
        circle = Circle(radius=get_norm(w_dot.get_center() - w_plane.get_origin()))
        circle.move_to(w_plane.get_origin())
        circle.set_stroke(PINK, 2)
        circle.rotate(np.log(get_w()).imag)
        z_tracker.save_state()

        self.play(
            FadeIn(w_dot),
            FadeIn(z_dot),
            FlashAround(w_dot),
        )
        for n in range(2):
            added_anims = [ShowCreation(circle)] if n == 0 else []
            self.play(
                z_tracker.animate.increment_value(TAU * 1j),
                Rotate(droste_randy, TAU, about_point=w_plane.get_origin()),
                long_log_randys.animate.shift(z_unit * TAU * UP),
                *added_anims,
                run_time=3,
            )
            long_log_randys.restore()
        self.play(FadeOut(z_dot), FadeOut(w_dot), FadeOut(circle))
        z_tracker.restore()

        # Comment on repetition to the left
        left_rep_arrow = Vector(4 * LEFT, thickness=8, fill_color=RED)
        left_rep_arrow.next_to(log_randys[1], UL)

        self.play(
            droste_image.animate.set_opacity(0.75),
            log_image_tiles.animate.set_opacity(0.75),
        )
        self.play(GrowArrow(left_rep_arrow))
        self.wait()
        self.play(FadeOut(left_rep_arrow))

        # Shift left
        small_droste_randy = droste_randy.copy()
        z_dot.set_opacity(0)
        w_dot.set_opacity(0)
        self.add(z_dot, w_dot)
        self.remove(droste_randy)
        self.play(
            log_randys.animate.shift(math.log(16) * z_plane.get_unit_size() * LEFT),
            UpdateFromFunc(small_droste_randy, lambda m: m.become(apply_func_to_z_space(log_randy.copy(), np.exp))),
            z_tracker.animate.increment_value(-math.log(16)),
            FadeOut(brace_group, time_span=(0, 1)),
            frame.animate.reorient(0, 0, 0, (0, 0.75, 0.0), 11),
            run_time=10
        )
        self.wait()
        self.play(
            frame.animate.reorient(0, 0, 0, (6.59, -0.04, 0.0), 0.38).set_anim_args(
                rate_func=lambda t: there_and_back_with_pause(t, 1 / 7),
                run_time=7
            ),
            FadeOut(left_arrow)
        )
        self.play(
            droste_image.animate.set_opacity(0.25),
            log_image_tiles.animate.set_opacity(0.25),
        )

        # Show exp and log properties
        func_labels = VGroup(right_arrow_label, right_arrow, left_arrow, left_arrow_label)
        t2c = {"z_1": BLUE, "z_2": BLUE_D, "w_1": PINK, "w_2": MAROON_B}
        exp_rule = Tex(R"e^{z_1 + z_2} = e^{z_1} e^{z_2}", t2c=t2c)
        log_rule = Tex(R"\ln(w_1 w_2) = \ln(w_1) + \ln(w_2)", t2c=t2c, font_size=40)
        rules = VGroup(exp_rule, log_rule)
        rules.scale(1.25)
        rules.arrange(DOWN, buff=LARGE_BUFF)
        rules.set_x(-0.1).set_y(-1.2)

        rect = SurroundingRectangle(exp_rule["z_1 + z_2"], buff=0.1)
        rect.set_stroke(YELLOW, 2)

        self.play(
            func_labels.animate.arrange(DOWN).align_to(w_plane, UP),
            Write(exp_rule, time_span=(0.5, 1.5)),
            Write(log_rule, time_span=(1.0, 2.0)),
        )
        self.play(ShowCreation(rect))
        self.wait()
        self.play(rect.animate.surround(exp_rule[R"e^{z_1} e^{z_2}"]))
        self.wait()
        self.play(rect.animate.surround(log_rule[R"w_1 w_2"]))
        self.wait()
        self.play(rect.animate.surround(log_rule[R"\ln(w_1) + \ln(w_2)"]))
        self.wait()
        self.play(FadeOut(rect))
        self.wait()

        # Show example point w -> 16w
        w_dot = Dot()
        w_dot.set_z_index(4)
        w_dot.set_color(RED)
        # CHANGE: the placeholder EscherPiCreature SVG has only 6 parts (the body is the 4th); the original used part 10.
        w_dot.move_to(small_droste_randy[4].get_corner(DL))
        w = w_plane.p2n(w_dot.get_center())

        w16_dot = w_dot.copy()
        w16_dot.move_to(w_plane.n2p(16 * w))

        w_label = Tex(R"w")
        w_label.set_color(RED)
        w_label.set_backstroke(BLACK, 2)
        w_label.next_to(w_dot, DL, buff=0, aligned_edge=UP)

        w16_label = Tex(R"w \cdot 16")
        w16_label.match_style(w_label)
        w16_label.next_to(w16_dot, UL, buff=0)

        scale_arrow = Arrow(w_label, w16_label, buff=0.1, path_arc=45 * DEG, thickness=5)
        scale_arrow.set_fill(RED)
        times_16_label = Tex(R"\times 16")
        times_16_label.next_to(scale_arrow.pfp(0.8), UL, SMALL_BUFF)

        w_label.save_state()
        w_dot.save_state()
        w_dot.scale(1 / 8)
        w_label.scale(1 / 4)
        w_label.next_to(w_dot, DL, buff=0.01)

        self.play(FadeOut(pink_circle))
        self.play(
            frame.animate.reorient(0, 0, 0, (6.08, -0.13, 0.0), 1.37),
            FadeIn(w_dot, 0.1 * UR, time_span=(1, 2)),
            FadeIn(w_label, 0.1 * UR, time_span=(1, 2)),
            FadeOut(v_line),
            FadeOut(rules),
            run_time=2,
        )
        self.wait()
        w_plane.coordinate_labels[1].set_opacity(0)
        self.play(
            frame.animate.reorient(0, 0, 0, (0.7, 0.69, 0.0), 11.37),
            Restore(w_dot),
            Restore(w_label),
            TransformFromCopy(w_dot, w16_dot),
            TransformMatchingTex(w_label.copy(), w16_label),
            TransformFromCopy(small_droste_randy, droste_randy),
            GrowArrow(scale_arrow),
            FadeIn(times_16_label, time_span=(1, 2), shift=0.25 * scale_arrow.get_vector()),
            run_time=3,
        )
        self.wait()

        # Show corresponding log(w) -> log(w) + log(16)
        log_w_dot = Dot()
        log_w_dot.match_style(w_dot)
        log_w_dot.move_to(z_plane.n2p(np.log(w) + TAU * 1j))
        log_w_label = Tex(R"\ln(w)")
        log_w_label.next_to(log_w_dot, DOWN, SMALL_BUFF)
        log_w_label.shift(SMALL_BUFF * LEFT)
        log_w_label.match_style(w_label)

        shift_vect = math.log(16) * z_plane.get_unit_size() * RIGHT
        shifted_log_dot = log_w_dot.copy().shift(shift_vect)
        shifted_log_randys = log_randys.copy().shift(shift_vect)
        shift_log_label = Tex(R"\ln(w) + \ln(16)")
        shift_log_label[R"\ln(w)"].set_fill(RED)
        shift_log_label.set_backstroke(BLACK, 3)
        shift_log_label.move_to(log_w_label, LEFT).shift(shift_vect)

        shift_arrow = Vector(shift_vect, thickness=5)
        shift_arrow.next_to(VGroup(log_randys[1], shifted_log_randys[1]), UP, SMALL_BUFF)
        shift_arrow_label = Tex(R"+ \ln(16)")
        shift_arrow_label.next_to(shift_arrow, UP, buff=0)
        shift_arrow_label.shift(3 * SMALL_BUFF * LEFT)
        shift_arrow_label.set_backstroke(BLACK, 3)

        self.play(
            TransformFromCopy(w_dot, log_w_dot, path_arc=-15 * DEG),
            TransformMatchingTex(w_label.copy(), log_w_label, path_arc=-15 * DEG),
            run_time=2,
        )
        self.wait()
        self.play(
            TransformFromCopy(log_w_dot, shifted_log_dot),
            TransformFromCopy(log_randys, shifted_log_randys),
            FadeTransform(log_w_label.copy(), shift_log_label[R"\ln(w)"][0]),
            FadeIn(shift_log_label[R"+ \ln(16)"][0], shift=shift_vect),
            TransformFromCopy(small_droste_randy, droste_randy),
            TransformFromCopy(w_dot, w16_dot),
            GrowArrow(shift_arrow, time_span=(1, 2)),
            FadeIn(shift_arrow_label, shift=0.25 * RIGHT, time_span=(1, 2)),
            run_time=3
        )
        self.wait()

        # Show tile and annulus
        top_brace = Brace(log_image, UP, SMALL_BUFF)
        shift_arrow_label.target = shift_arrow_label.generate_target()
        shift_arrow_label.target[0].scale(0, about_point=shift_arrow_label[1].get_left())
        shift_arrow_label.target.next_to(log_image, UP)
        shift_arrow_label.target.set_backstroke(BLACK, 5)
        shift_arrow_label.target.next_to(top_brace, UP, SMALL_BUFF)
        log_image.set_opacity(1)
        brace_group.next_to(log_image, RIGHT, SMALL_BUFF)

        fundamental_rect = SurroundingRectangle(log_image, buff=0)
        fundamental_rect.set_stroke(WHITE, 1)

        annulus = apply_func_to_z_space(log_image.copy(), np.exp)
        annulus.save_state()
        log_image_group = Group(log_image, top_brace, brace_group, shift_arrow_label)

        self.play(
            FadeOut(VGroup(w_dot, w_label, w16_dot, w16_label, scale_arrow, times_16_label)),
            FadeOut(VGroup(log_w_dot, log_w_label, shifted_log_dot, shift_log_label, shift_arrow)),
            FadeOut(VGroup(small_droste_randy, droste_randy, log_randys, shifted_log_randys)),
            MoveToTarget(shift_arrow_label),
            GrowFromCenter(top_brace),
            FadeIn(brace_group),
            FadeOut(big_z_plane.coordinate_labels[-15:]),
            FadeIn(log_image),
            run_time=2
        )
        self.play(ShowCreation(fundamental_rect))
        self.wait()
        self.play(
            ShowCreation(log_image),
            ShowCreation(annulus),
            w_plane.coordinate_labels.animate.set_opacity(0),
            w_plane.axes.animate.set_stroke(WHITE, 1, 0.25),
            run_time=3
        )
        self.wait()
        log_image_group.save_state()
        for n in range(3):
            self.play(
                log_image_group.animate.shift(-shift_vect),
                annulus.animate.scale(1 / 16, about_point=w_plane.get_origin()),
                frame.animate.reorient(0, 0, 0, (0.67, 0.14, 0.0), 13.59),
                run_time=3,
            )
            self.wait()
        self.play(
            Restore(log_image_group),
            Restore(annulus),
            frame.animate.reorient(0, 0, 0, (1.72, 0.49, 0.0), 13.42),
            run_time=2
        )

        # Show the boundary
        colors = color_gradient([RED, YELLOW], 4)
        v_lines = VGroup(
            Line(
                log_image.get_corner(DR),
                log_image.get_corner(UR)
            ).shift(-0.25 * n * shift_vect)
            for n in range(20)
        )
        v_lines.set_stroke(WHITE, 3)
        v_lines.set_submobject_colors_by_gradient(RED, YELLOW, GREEN, BLUE, interp_by_hsl=True)

        circles = apply_func_to_z_space(v_lines.copy().insert_n_curves(100), np.exp)
        indic_arrow = Vector(DL, thickness=6).set_fill(RED)
        indic_arrow.next_to(v_lines.get_corner(DR), UR, buff=SMALL_BUFF)

        log_image_tiles.set_clip_plane(LEFT, 0)
        v_lines.set_clip_plane(LEFT, 0)
        droste_image.set_clip_plane(RIGHT, 0)
        circles.set_clip_plane(RIGHT, 0)

        func_labels.set_backstroke(BLACK, 5)
        func_labels.set_z_index(5)
        self.add(func_labels)

        self.play(
            FadeOut(VGroup(top_brace, shift_arrow_label, brace_group)),
            log_image_tiles.animate.set_opacity(0.9),
            droste_image.animate.set_opacity(0.9),
            FadeOut(Group(log_image, annulus), time_span=(0.9, 1)),
            FadeOut(fundamental_rect),
        )
        self.play(
            indic_arrow.animate.shift(v_lines[0].get_vector()),
            ShowCreation(v_lines[0]),
            ShowCreation(circles[0]),
            run_time=3
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, v_lines[1:], lag_ratio=0.1, run_time=2),
            LaggedStartMap(ShowCreation, circles[1:], lag_ratio=0.1, run_time=2),
        )
        self.wait()
        self.play(FadeOut(indic_arrow))

        # Expand
        def update_droste(mob):
            mob.set_width(2 * w_plane.get_unit_size() * np.exp(z_plane.p2n(log_image_tiles.get_right()).real))
            mob.move_to(w_plane.get_origin())
            return mob

        self.play(
            Group(log_image_tiles, v_lines).animate.shift(4 * RIGHT),
            UpdateFromFunc(Group(droste_image, circles), update_droste),
            run_time=10
        )
        self.play(FadeOut(v_lines), FadeOut(circles))
        self.wait()
        self.play(
            log_image_tiles.animate.shift(TAU * z_plane.get_unit_size() * UP),
            Rotate(droste_image, TAU, about_point=w_plane.get_origin()),
            run_time=6
        )
        log_image_tiles.shift(shift_vect * RIGHT)
        self.play(
            log_image_tiles.animate.shift(shift_vect * LEFT),
            UpdateFromFunc(droste_image, update_droste),
            run_time=6
        )
        self.wait()

    def get_traced_paths(self, dots, colors=None, stroke_width=3):
        if colors is None:
            colors = [dot.family_members_with_points()[0].get_color() for dot in dots]
        return VGroup(
            TracedPath(dot.get_center, stroke_color=color, stroke_width=stroke_width)
            for dot, color in zip(dots, colors)
        )
