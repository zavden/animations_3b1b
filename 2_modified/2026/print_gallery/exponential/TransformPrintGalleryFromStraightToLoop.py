# ==============================================================================
# Scene:      TransformPrintGalleryFromStraightToLoop
# Source:     videos/_2026/print_gallery/exponential.py (lines 3088-3126)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TransformPrintGalleryFromStraightToLoop.py TransformPrintGalleryFromStraightToLoop -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_texture_folder() points to a 'textures' folder next to the file (the Dropbox path of Grant does not exist)
#   - The PrintGalleryLog/PiHouseLog(Small) textures are procedural placeholder images: periodic strips with picture frames / houses with pi creatures (_lib/assets/generated/2026/print_gallery/make_print_gallery_assets.py)
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

def get_texture_folder():
    # CHANGE: the textures lived in Grant's Dropbox; now they are in the "textures" folder next to
    # this file (procedurally generated placeholder images).
    return Path(__file__).parent / "textures"


def get_print_gallery_log_image_path():
    return Path(get_texture_folder(), "PrintGalleryLog.png")


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


def apply_func_between_planes(mob, func, src_plane, trg_plane):
    mob.shift(-src_plane.get_origin())
    mob.scale(1.0 / src_plane.get_unit_size(), about_point=ORIGIN)
    mob.apply_complex_function(func)
    mob.scale(trg_plane.get_unit_size(), about_point=ORIGIN)
    mob.shift(trg_plane.get_origin())
    return mob


class CreatingTheSpiral(InteractiveScene):
    # log_image_resolution = (51, 101)
    log_image_resolution = (21, 41)
    droste_scale_adjustment = 1.5
    droste_scale_factor = 16
    fixed_point = 4.0j
    droste_plane_x_range = (-1, 1)
    log_plane_x_range = (-5, 5)

    def setup(self):
        super().setup()

        # Planes
        self.planes = self.get_four_planes()
        self.dark_planes = self.get_four_dark_planes()
        a_plane, b_plane, c_plane, d_plane = self.planes

        # Arrows
        self.log_arrow_group, self.exp_arrow_group = self.get_log_exp_arrow_groups()

        # Droste image
        droste_image = get_droste_from_log_image_path(self.get_log_image_path(), self.droste_scale_factor)
        droste_image.set_height(2 * a_plane.get_unit_size() * self.droste_scale_adjustment)
        droste_image.move_to(a_plane)
        droste_image.clip_to_box(a_plane)
        self.droste_image = droste_image

        # Log image
        self.const = complex(0, TAU) / complex(math.log(self.droste_scale_factor), TAU)

        self.log_image_tiles = self.get_log_image_tiles(b_plane, 9, 9, resolution=(2, 2))
        self.pre_transform_log = self.get_log_image_tiles(b_plane, 3, 3, resolution=self.log_image_resolution)
        # self.pre_transform_log = self.get_log_image_tiles(b_plane, 5, 5, resolution=self.log_image_resolution)

        self.var_const = ComplexValueTracker(self.const)
        self.var_fixed_point = ComplexValueTracker(self.fixed_point)

        # Blank spot
        blank_dot = Dot()
        blank_dot.set_width(0.4)
        blank_dot.set_color(WHITE)
        blank_spot = Group(GlowDot(color=WHITE, radius=2 * blank_dot.get_width()), blank_dot)
        blank_spot.move_to(d_plane.get_center())
        self.blank_spot = blank_spot

    def construct(self):
        # Load up local variables
        planes = self.planes
        dark_planes = self.dark_planes
        a_plane, b_plane, c_plane, d_plane = planes
        dark_a_plane, dark_b_plane, dark_c_plane, dark_d_plane = dark_planes

        log_arrow_group = self.log_arrow_group
        exp_arrow_group = self.exp_arrow_group
        log_arrow, log_label = log_arrow_group
        exp_arrow, exp_label = exp_arrow_group

        droste_image = self.droste_image
        log_image_tiles = self.log_image_tiles
        blank_spot = self.blank_spot

        const = self.const
        fixed_point = self.fixed_point
        var_const = self.var_const
        var_fixed_point = self.var_fixed_point

        rot_func = self.rot_func
        get_rot_tiles = self.get_rot_tiles
        get_final_image = self.get_final_image

        # Show start and end goal
        frame = self.frame
        frame.set_field_of_view(1 * DEG)
        frame.match_x(a_plane)

        func_arrow = Arrow(a_plane.get_right(), d_plane.get_right(), path_arc=-120 * DEG, thickness=5)
        fz, eq, q_marks = question = VGroup(Tex(R"f(z)"), Tex(R"="), Tex(R"???"))
        question.arrange(RIGHT, SMALL_BUFF)
        question.next_to(func_arrow, RIGHT)

        var_const.set_value(1)
        final_image = get_final_image()
        droste_image.save_state()

        self.add(func_arrow, question)
        self.add(a_plane, d_plane)
        self.play(
            FadeIn(droste_image),
            FadeIn(dark_a_plane),
            FadeOut(a_plane),
        )
        self.play(droste_image.animate.scale(16), run_time=4)
        droste_image.restore()
        self.play(
            FadeIn(final_image),
            FadeIn(dark_d_plane),
            FadeOut(d_plane),
            FadeIn(blank_spot),
        )
        self.play(
            UpdateFromFunc(final_image, lambda m: m.become(get_final_image())),
            var_const.animate.set_value(const),
            run_time=5
        )
        self.wait()

        # Show the four steps
        var_const.set_value(1)
        rot_log_tiles = get_rot_tiles()

        mult_arrow = Arrow(b_plane.get_left(), c_plane.get_left(), path_arc=90 * DEG, thickness=5)
        kw = dict(t2c={"{z}": BLUE})
        rot_label = Text("Rotate \n & Scale", font_size=36)
        rot_label.next_to(mult_arrow, LEFT, SMALL_BUFF)
        mult_arrow_group = VGroup(mult_arrow, rot_label)

        self.play(
            ReplacementTransform(func_arrow, log_arrow, time_span=(0, 1)),
            Write(log_label),
            FadeIn(b_plane),
            frame.animate.reorient(0, 0, 0, (0.01, 1.96, 0.0), 5.04),
            FadeOut(question, time_span=(1, 2)),
            run_time=2,
        )
        self.play(
            FadeOut(droste_image.copy()),
            ShowCreation(droste_image, lag_ratio=0),
            ShowCreation(log_image_tiles, lag_ratio=0),
            FadeOut(b_plane),
            FadeIn(dark_b_plane),
            run_time=3
        )
        self.wait()
        self.play(
            FadeIn(rot_log_tiles),
            FadeIn(dark_c_plane),
            Write(mult_arrow),
            FadeIn(rot_label, 0.25 * DOWN),
            frame.animate.to_default_state(),
            run_time=2,
        )
        self.play(
            var_const.animate.set_value(const),
            UpdateFromFunc(rot_log_tiles, lambda m: m.become(get_rot_tiles())),
            run_time=4,
        )
        self.wait()

        # Final exp
        exp_mover = self.get_log_image_tiles(c_plane, 3, 3)
        exp_mover.set_opacity(0.5)
        apply_func_between_planes(exp_mover, rot_func, c_plane, c_plane)
        box = SurroundingRectangle(c_plane, buff=0)
        box.set_stroke(width=0)
        exp_mover.add_updater(lambda m: m.clip_to_box(box))
        self.play(
            GrowArrow(exp_arrow, time_span=(0, 1)),
            Write(exp_label, time_span=(0, 1)),
            Transform(
                exp_mover,
                apply_func_between_planes(exp_mover.copy(), np.exp, c_plane, d_plane),
                time_span=(1, 3)
            ),
            box.animate.move_to(d_plane).set_anim_args(time_span=(1, 3)),
            run_time=3,
        )
        self.remove(exp_mover)
        self.wait()

        # Show the line from big to small
        plane_covers = VGroup(
            BackgroundRectangle(plane, buff=0.05).set_fill(BLACK, 0.9)
            for plane in planes
        )

        randy = SVGMobject("EscherPiCreature")
        randy.set_backstroke(BLACK, 3)
        randy.set_height(0.9)
        randy.move_to(a_plane.c2p(-0.62, -0.95), DOWN)
        randy.set_z_index(2)

        randy_box = SurroundingRectangle(randy, buff=0.05)
        randy_box.set_stroke(YELLOW, 2)

        randy_group = VGroup(randy, randy_box)
        small_randy, small_box = small_group = randy_group.copy().scale(1 / 16, about_point=a_plane.get_origin())
        box_lines = VGroup(
            Line(
                randy_box.get_corner(corner),
                small_box.get_corner(corner)
            ).match_style(small_box)
            for corner in [UL, DR]
        )

        randy_line = Line(randy.get_center(), small_randy.get_center())
        randy_line.set_stroke([RED, RED_E], width=[10, 3])
        randy_line_dots = VGroup(
            Dot(randy_line.get_start(), radius=0.05).set_fill(RED),
            Dot(randy_line.get_end(), radius=0.01).set_fill(RED_E),
        )

        self.play(
            frame.animate.reorient(0, 0, 0, (2.52, 1.16, 0.0), 1.74),
            run_time=3,
        )
        self.play(
            FadeIn(randy),
            ShowCreation(randy_box),
            droste_image.animate.set_opacity(0.5),
        )
        self.wait()
        self.play(
            TransformFromCopy(randy_group, small_group),
            ShowCreation(box_lines, lag_ratio=0),
            run_time=2
        )
        self.wait()
        self.play(GrowFromCenter(randy_line_dots[0]))
        self.play(
            FadeOut(randy_box),
            FadeOut(small_box),
            FadeOut(box_lines),
            TransformFromCopy(*randy_line_dots),
            ShowCreation(randy_line),
        )
        self.wait()

        # Show the corresponding loop
        self.add(plane_covers[1:3])
        log_arrow_group.set_fill(opacity=0.2)
        exp_arrow_group.set_fill(opacity=0.2)
        mult_arrow_group.set_fill(opacity=0.2)

        final_randy = apply_func_between_planes(
            randy.copy(), lambda z: np.exp(rot_func(np.log(z) + TAU * 1j)), a_plane, d_plane,
        )
        loop = Circle(radius=0.9 * d_plane.get_unit_size())
        loop.flip(RIGHT).rotate(225 * DEG)
        loop.move_to(d_plane)
        loop.set_stroke([RED, RED_E], 8)

        self.remove(randy_line, randy_line_dots)
        self.play(
            frame.animate.reorient(0, 0, 0, (4.43, -0.86, 0.0), 6.44),
            final_image.animate.set_opacity(0.1),
            TransformFromCopy(randy, final_randy),
            Animation(randy_line),
            Animation(randy_line_dots),
            run_time=2
        )
        self.play(
            TransformFromCopy(randy_line, loop, run_time=3, path_arc=[0, -0.5 * PI]),
            TransformFromCopy(small_randy, final_randy, run_time=3, path_arc=-0.5 * PI)
        )
        self.wait()
        self.play(
            ShowCreation(loop),
            ShowCreation(randy_line),
            run_time=2
        )
        self.wait()
        self.play(
            TransformFromCopy(loop, randy_line),
            TransformFromCopy(final_randy, randy),
            TransformFromCopy(final_randy, small_randy),
            rate_func=there_and_back_with_pause,
            run_time=6
        )
        self.add(randy_line)
        self.wait()

        # Show randy in log image
        b_unit = b_plane.get_unit_size()
        log_randy = apply_func_between_planes(randy.copy(), np.log, a_plane, b_plane)
        log_randys = VGroup(
            log_randy.copy().shift(n * b_unit * TAU * UP)
            for n in range(5)
        )
        log_randys.set_backstroke(BLACK, 2)
        small_log_randys = log_randys.copy().shift(b_unit * math.log(16) * LEFT)

        big_box = SurroundingRectangle(log_randys[:2])
        small_box = SurroundingRectangle(small_log_randys[:2])
        VGroup(big_box, small_box).set_stroke(BLUE_B, 2)
        big_box_label = Text("Big", font_size=24).next_to(big_box, UP, SMALL_BUFF)
        small_box_label = Text("Small", font_size=24).next_to(small_box, UP, SMALL_BUFF)
        big_box_label.align_to(small_box_label, UP)

        self.play(
            frame.animate.reorient(0, 0, 0, (-0.32, 1.82, 0.0), 4.54),
            log_arrow_group.animate.set_opacity(1),
            FadeOut(plane_covers[1]),
            log_image_tiles.animate.set_opacity(0.5),
            run_time=2,
        )
        self.play(
            TransformFromCopy(randy.replicate(len(log_randys)), log_randys),
            log_image_tiles.animate.set_opacity(0.25),
            run_time=2
        )
        self.play(
            ShowCreation(big_box),
            Write(big_box_label)
        )
        self.wait()
        self.play(
            TransformFromCopy(randy, small_randy),
            TransformFromCopy(log_randys, small_log_randys),
            TransformFromCopy(big_box, small_box),
            run_time=2
        )
        self.play(
            Write(small_box_label),
        )
        self.wait()

        log_randys = log_randys[:3]
        small_log_randys = small_log_randys[:3]
        old_randy_line = randy_line
        self.remove(*log_randys[2:])
        self.remove(*small_log_randys[2:])

        # Show the log lines
        log_lines = VGroup(
            Line(br.get_center(), sr.get_center()).set_stroke(RED, 3)
            for br, sr in zip(log_randys, small_log_randys)
        )
        old_log_lines = log_lines.copy()
        randy_line_style = randy_line.get_style()

        def get_true_randy_line():
            result = log_lines[1].copy()
            if result.get_num_points() < 100:
                result.insert_n_curves(100)
            apply_func_between_planes(result, np.exp, b_plane, a_plane)
            result.set_style(**randy_line_style)
            return result

        self.remove(old_randy_line, randy_line_dots)
        randy_line = get_true_randy_line()

        randy_line_indicator = GlowDot(randy_line.get_start(), color=RED, radius=0.25)
        log_indicators = Group(
            GlowDot(color=RED).move_to(lr) for lr in log_randys
        )
        line_indicators = Group(randy_line_indicator, log_indicators)

        self.play(
            UpdateFromFunc(randy_line_indicator, lambda m: m.move_to(randy_line.get_end())),
            log_indicators.animate.move_to(log_lines, LEFT),
            ShowCreation(log_lines, lag_ratio=0),
            ShowCreation(randy_line, lag_ratio=0),
            run_time=2
        )
        self.play(
            FadeOut(line_indicators),
        )
        self.wait()

        # Diagonal line
        diag_line = Line(log_randys[1].get_center(), small_log_randys[0].get_center())
        diag_line.match_style(log_lines[0])
        v_shift = b_unit * TAU * UP
        diag_lines = VGroup(
            diag_line.copy().shift(-v_shift),
            diag_line,
            diag_line.copy().shift(v_shift)
        )
        for lines in log_lines, diag_lines:
            lines.insert_n_curves(100)
            lines.clip_to_box(b_plane)

        test_line = apply_func_between_planes(log_lines[1].copy(), np.exp, b_plane, a_plane)

        self.play(
            ReplacementTransform(log_lines, diag_lines, run_time=3),
            UpdateFromFunc(randy_line, lambda m: m.match_points(get_true_randy_line())),
        )
        self.wait()
        self.play(big_box.animate.surround(log_randys[1]))
        self.wait()
        self.play(
            small_box.animate.surround(small_log_randys[0]),
            small_box_label.animate.next_to(small_log_randys[0], DOWN, buff=0.2),
        )
        self.wait()

        # Move along curled line
        log_randy = log_randys[1].copy()

        def get_exp_log_randy():
            return apply_func_between_planes(log_randy.copy(), np.exp, b_plane, a_plane)

        exp_log_randy = get_exp_log_randy()

        self.play(FadeIn(log_randy), FadeIn(exp_log_randy))
        self.play(
            log_randy.animate.move_to(small_log_randys[0]),
            UpdateFromFunc(exp_log_randy, lambda m: m.become(get_exp_log_randy())),
            run_time=3
        )
        self.play(FadeOut(log_randy), FadeOut(exp_log_randy))
        self.wait()

        # Zoom out to describe the goal
        plane_rect = SurroundingRectangle(d_plane)
        plane_rect.set_stroke(YELLOW, 4)

        v_line = apply_func_between_planes(diag_line.copy(), rot_func, b_plane, c_plane)
        v_line.deactivate_clip_plane()
        v_line.set_stroke(RED, 5)

        v_line_brace = Brace(v_line, RIGHT, SMALL_BUFF)
        v_line_label = v_line_brace.get_tex(R"2\pi")
        v_line_brace_group = VGroup(v_line_brace, v_line_label)
        v_line_brace_group.set_backstroke(BLACK, 5)

        rot_log_randys = VGroup(log_randys[1].copy(), small_log_randys[0].copy())
        apply_func_between_planes(rot_log_randys, rot_func, b_plane, c_plane)

        diag_arrow, down_arrow = red_arrows = VGroup(
            Arrow(line.get_start(), line.get_end(), buff=0, thickness=4, fill_color=RED)
            for line in [diag_line, v_line]
        )

        self.play(frame.animate.to_default_state(), run_time=2)
        self.play(ShowCreation(plane_rect))
        self.wait()
        self.play(
            plane_rect.animate.surround(c_plane),
            TransformFromCopy(loop, v_line),
            TransformFromCopy(final_randy.replicate(2), rot_log_randys),
            exp_arrow_group.animate.set_fill(opacity=1),
            FadeOut(plane_covers[2]),
            rot_log_tiles.animate.set_opacity(0.5),
            run_time=2
        )
        self.play(
            GrowFromCenter(v_line_brace),
            Write(v_line_label, stroke_color=WHITE),
        )
        self.wait()
        self.play(
            plane_rect.animate.surround(b_plane).stretch(1.05, 1, about_edge=DOWN),
            FadeOut(diag_lines),
            FadeIn(diag_arrow),
            FadeOut(VGroup(log_randys[0], small_log_randys[1])),
            log_image_tiles.animate.set_opacity(0.5),
        )
        self.wait()
        self.play(
            plane_rect.animate.surround(VGroup(b_plane, c_plane)).stretch(1.02, 1, about_edge=DOWN),
            TransformFromCopy(diag_arrow, down_arrow),
            mult_arrow_group.animate.set_fill(opacity=1),
            run_time=2,
        )
        self.wait()

        # Talk about complex constant
        kw = dict(t2c={"{z}": BLUE, "{c}": YELLOW})
        func_label = VGroup(
            Tex(R"{z}", **kw),
            Tex(R"\downarrow"),
            Tex(R"{c} \cdot {z}", **kw),
        )
        func_label.arrange(DOWN)
        func_label.next_to(mult_arrow, LEFT)
        true_output = Tex(R"{c} \cdot ({z} - z_0) + z_0", **kw)
        true_output.move_to(func_label[2], RIGHT)

        pivot_dot = Dot(b_plane.n2p(fixed_point)).set_color(TEAL)
        pivot_dot.set_stroke(WHITE, 1)
        pivot_dot_label = Tex(R"z_0")
        pivot_dot_label.set_backstroke(BLACK, 3)
        pivot_dot_label.next_to(pivot_dot, RIGHT, SMALL_BUFF)

        self.play(
            frame.animate.set_x(-2),
            FadeOut(rot_label, 0.5 * DOWN),
            FadeIn(func_label, 0.5 * DOWN),
        )
        self.wait()
        self.play(plane_rect.animate.surround(randy))
        self.wait()
        self.play(plane_rect.animate.surround(log_randys[1]))
        self.wait()
        self.play(
            FadeOut(VGroup(log_randys[1], small_log_randys[0], big_box, big_box_label, small_box, small_box_label, plane_rect)),
            diag_arrow.animate.put_start_and_end_on(pivot_dot.get_center(), diag_arrow.get_end()),
            FadeIn(pivot_dot),
        )
        self.play(
            log_image_tiles.animate.rotate(70 * DEG, about_point=diag_arrow.get_start()),
            diag_arrow.animate.rotate(70 * DEG, about_point=diag_arrow.get_start()),
            rate_func=there_and_back,
            run_time=4
        )
        self.play(Write(pivot_dot_label, stroke_color=WHITE))
        self.wait()
        self.play(
            TransformMatchingTex(func_label[2], true_output),
            TransformFromCopy(pivot_dot_label.replicate(2), true_output["z_0"]),
            func_label[:2].animate.match_x(true_output),
        )
        self.wait()

        func_label = VGroup(*func_label[:2], true_output)
        self.add(func_label)

        # Write the value for c
        c_value = Tex(R"{c} = \frac{2\pi i}{\ln(16) + 2 \pi i}", **kw)
        c_value.next_to(func_label, DOWN)

        log16_line = DashedLine(small_log_randys[0].get_center(), log_randys[0].get_center())
        two_pi_i_line = DashedLine(log_randys[0].get_center(), log_randys[1].get_center())
        two_pi_i_line.shift(pivot_dot.get_center() - log_randys[1].get_center())
        two_pi_i_line.set_z_index(3)

        log_16_label = Tex(R"\ln(16)", font_size=24)
        log_16_label.next_to(log16_line, DOWN, SMALL_BUFF)
        two_pi_i_label = Tex(R"2\pi i", font_size=24)
        two_pi_i_label.next_to(two_pi_i_line, RIGHT, SMALL_BUFF)
        VGroup(two_pi_i_label, log_16_label).set_backstroke(BLACK, 3)

        self.play(
            ShowCreation(log16_line),
            FadeIn(log_16_label),
        )
        self.play(
            ShowCreation(two_pi_i_line),
            FadeIn(two_pi_i_label),
        )
        self.wait()
        self.play(
            func_label.animate.shift(0.7 * UP),
            FadeIn(c_value, 0.5 * DOWN),
        )
        self.wait()

        # Clear the board
        faders = VGroup(
            randy, small_randy, randy_line, # pivot_dot, pivot_dot_label,
            log16_line, two_pi_i_line, log_16_label, two_pi_i_label,
            rot_log_randys,
            plane_rect, diag_arrow, v_line, down_arrow, v_line_brace_group,
            loop, final_randy,
        )

        self.remove(blank_spot)
        self.play(
            LaggedStartMap(FadeOut, faders, lag_ratio=0.1),
            droste_image.animate.set_opacity(1).set_anim_args(time_span=(0, 1)),
            log_image_tiles.animate.set_opacity(1).set_anim_args(time_span=(0.25, 1.25)),
            rot_log_tiles.animate.set_opacity(1).set_anim_args(time_span=(0.5, 1.5)),
            final_image.animate.set_opacity(1).set_anim_args(time_span=(0.75, 1.75)),
            FadeIn(blank_spot),
            run_time=2,
        )
        self.wait()

        # Show the factor c on its own plane
        mult_plane, c_group = self.get_mult_plane(c_plane)
        mult_plane.match_x(func_label)
        c_dot, c_vect, c_label = c_group

        self.play(
            FadeOut(c_value, DOWN),
            FadeIn(mult_plane, DOWN),
            FadeIn(c_group, DOWN),
            func_label.animate.shift(0.25 * UP)
        )

        # Play
        var_const.clear_updaters().add_updater(lambda m: m.set_value(mult_plane.p2n(c_dot.get_center())))
        rot_log_tiles.clear_updaters().add_updater(lambda m: m.become(get_rot_tiles()))
        final_image.clear_updaters().add_updater(lambda m: m.become(get_final_image()))
        value = complex(0, 2 * PI) / complex(np.log(16), 2 * PI)
        for mob in self.mobjects:
            self.disable_interaction(mob)
        self.enable_interaction(c_dot)
        self.add(c_dot)
        c_dot.move_to(mult_plane.n2p(value))

        self.play(Rotating(c_dot, about_point=c_dot.get_center() + 0.25 * DOWN, run_time=10))
        self.wait()  # Set longer to interact with in a recording
        self.play(c_dot.animate.move_to(mult_plane.n2p(const)), run_time=2)

        rot_log_tiles.clear_updaters()
        final_image.clear_updaters()

        # Comment on the center dot
        plane_rect.surround(d_plane)
        plane_covers.set_fill(opacity=0.5)

        self.pre_transform_log.save_state()
        final_image.save_state()
        rot_log_tiles.save_state()

        self.pre_transform_log.become(self.get_log_image_tiles(b_plane, 9, 9, resolution=self.log_image_resolution))
        self.log_image_tiles.become(self.get_log_image_tiles(b_plane, 15, 15, resolution=(2, 2)))
        rot_log_tiles.become(self.get_rot_tiles())
        final_image.become(get_final_image())

        self.play(
            ShowCreation(plane_rect),
            droste_image.animate.set_opacity(0.5),
            FadeIn(plane_covers[:3]),
        )
        self.wait()
        self.play(
            plane_rect.animate.surround(blank_spot[1]),
            frame.animate.reorient(0, 0, 0, (2.21, -1.99, 0.0), 3.48).set_anim_args(run_time=2),
        )
        self.wait()
        self.play(FadeOut(blank_spot))
        self.wait()
        self.play(
            FadeOut(plane_rect),
            FadeOut(plane_covers[2]),
            frame.animate.reorient(0, 0, 0, (-0.07, -1.85, 0.0), 4.89),
        )
        self.wait()
        self.play(
            rot_log_tiles.animate.shift(c_plane.n2p(4 * const * math.log(16)) - c_plane.get_origin()),
            self.pre_transform_log.animate.shift(4 * b_unit * math.log(16) * RIGHT),
            UpdateFromFunc(
                final_image,
                lambda m: m.become(get_final_image())
            ),
            run_time=12,
        )
        self.wait()

        self.pre_transform_log.restore()
        final_image.restore()
        rot_log_tiles.restore()

        # Zoom back out
        self.play(
            droste_image.animate.set_opacity(1),
            FadeOut(plane_covers[:2]),
            frame.animate.to_default_state().set_x(-2),
            run_time=2
        )
        self.wait()

        # Trying to use horizontal line
        self.play(
            ShowCreation(old_randy_line),
            ShowCreation(old_log_lines),
        )
        self.wait()

        var_const.clear_updaters().add_updater(lambda m: m.set_value(mult_plane.p2n(c_dot.get_center())))
        rot_log_tiles.clear_updaters().add_updater(lambda m: m.become(get_rot_tiles()))
        final_image.clear_updaters().add_updater(lambda m: m.become(get_final_image()))

        self.play(
            c_dot.animate.move_to(mult_plane.n2p(complex(0, TAU / math.log(16)))),
            run_time=3
        )
        rot_log_tiles.clear_updaters()
        final_image.clear_updaters()
        for factor, time in [(0.5, 2), (5e-7, 8)]:
            self.play(
                final_image.animate.scale(factor, about_point=d_plane.get_origin()),
                rot_log_tiles.animate.shift(b_unit * math.log(factor) * RIGHT),
                run_time=time
            )
        self.wait()

    def get_log_image_path(self):
        return get_pi_house_log_image_path()

    def get_four_planes(
        self,
        axes_color=WHITE,
        line_color=BLUE,
        line_width=1,
        line_opacity=1,
        faded_line_ratio=4,
        faded_line_opacity=0.25,
        h_buff=2.0,
        v_buff=0.75,
        include_coordinates=True
    ):
        kw = dict(faded_line_ratio=faded_line_ratio)
        planes = VGroup(
            ComplexPlane(self.droste_plane_x_range, self.droste_plane_x_range, **kw),
            ComplexPlane(self.log_plane_x_range, self.log_plane_x_range, **kw),
            ComplexPlane(self.log_plane_x_range, self.log_plane_x_range, **kw),
            ComplexPlane(self.droste_plane_x_range, self.droste_plane_x_range, **kw),
        )
        for plane in planes:
            plane.set_height(3.25)
            plane.axes.set_stroke(axes_color)
            plane.background_lines.set_stroke(line_color, line_width, line_opacity)
            plane.faded_lines.set_stroke(line_color, line_width, faded_line_opacity)
        planes.arrange_in_grid(2, 2, h_buff=h_buff, v_buff=v_buff)
        planes[0].match_x(planes[3])
        planes[1].match_x(planes[2])

        if include_coordinates:
            for plane in planes:
                plane.add_coordinate_labels(font_size=12, buff=0.05)

        return planes

    def get_four_dark_planes(self):
        result = self.get_four_planes(
            axes_color=BLACK,
            line_color=BLACK,
            line_opacity=0.25,
            faded_line_ratio=0,
            include_coordinates=False
        )
        result.set_z_index(1)
        return result

    def get_log_exp_arrow_groups(self):
        a_plane, b_plane, c_plane, d_plane = self.planes
        arrow_kw = dict(thickness=5, fill_color=GREY_B)
        tex_kw = dict(font_size=36, t2c={"z": BLUE, "w": PINK})
        log_arrow = Arrow(a_plane, b_plane, **arrow_kw)
        exp_arrow = Arrow(c_plane, d_plane, **arrow_kw)
        log_label = Tex(R"\ln(w) \leftarrow w", **tex_kw)
        log_label.next_to(log_arrow, UP, buff=SMALL_BUFF)
        exp_label = Tex(R"z \to e^z", **tex_kw)
        exp_label.next_to(exp_arrow, UP, buff=SMALL_BUFF)

        log_arrow_group = VGroup(log_arrow, log_label)
        exp_arrow_group = VGroup(exp_arrow, exp_label)

        return log_arrow_group, exp_arrow_group

    def get_log_image_tiles(self, plane, n_rows=None, n_cols=None, resolution=(21, 51)):
        log_image = get_log_image(self.get_log_image_path(), self.droste_scale_factor, resolution)
        log_image.scale(plane.get_unit_size())

        if n_cols is None:
            n_cols = int(np.ceil(plane.get_width() / log_image.get_width())) + 2
        if n_rows is None:
            n_rows = int(np.ceil(plane.get_height() / log_image.get_height())) + 2

        log_image_tiles = log_image.get_grid(n_rows, n_cols, buff=0)
        log_image_tiles.center()
        log_image_tiles.sort(lambda p: p[1])
        log_image_tiles.move_to(plane.n2p(math.log(self.droste_scale_adjustment)), DR)
        log_image_tiles.shift((n_rows // 2 + 1) * log_image.get_height() * DOWN)
        log_image_tiles.shift((n_cols // 2) * log_image.get_width() * RIGHT)
        log_image_tiles.clip_to_box(plane)
        return log_image_tiles

    def rot_func(self, z):
        z0 = self.var_fixed_point.get_value()
        c = self.var_const.get_value()
        return c * (z - z0) + z0

    def get_rot_tiles(self):
        b_plane, c_plane = self.planes[1:3]
        result = apply_func_between_planes(
            self.log_image_tiles.copy(), self.rot_func, b_plane, c_plane
        )
        result.clip_to_box(c_plane)
        return result

    def get_final_image(self):
        b_plane = self.planes[1]
        d_plane = self.planes[3]
        result = apply_func_between_planes(
            self.pre_transform_log.copy(), lambda z: np.exp(self.rot_func(z)), b_plane, d_plane
        )
        result.clip_to_box(d_plane)
        return result

    def get_mult_arrow_group(self):
        b_plane, c_plane = self.planes[1:3]
        mult_arrow = Arrow(
            b_plane.get_left(),
            c_plane.get_left(),
            path_arc=90 * DEG,
            thickness=5
        )
        kw = dict(t2c={"{z}": BLUE, "c": YELLOW})
        mult_label = VGroup(
            Tex(R"{z}", **kw),
            Tex(R"\downarrow", **kw),
            Tex(R"{c} \cdot ({z} - z_0) + z_0", **kw),
        )
        mult_label.arrange(DOWN)
        mult_label.next_to(mult_arrow, LEFT)

        return VGroup(mult_arrow, mult_label)

    def get_mult_plane(self, ref_plane, x_range=(-2, 2)):
        mult_plane = ComplexPlane(x_range, x_range)
        mult_plane.match_width(ref_plane)
        mult_plane.next_to(ref_plane, LEFT)

        c_dot = Group(GlowDot(), TrueDot()).set_color(YELLOW)
        c_dot.move_to(mult_plane.n2p(self.var_const.get_value()))
        c_vect = Vector(fill_color=YELLOW)
        c_label = Tex(R"c").set_color(YELLOW)
        c_label.always.next_to(c_dot, RIGHT, buff=0)
        c_vect.f_always.put_start_and_end_on(mult_plane.get_origin, c_dot.get_center)
        c_group = Group(c_dot, c_vect, c_label)

        return Group(mult_plane, c_group)


class FourPannelsWithPrintGallery(CreatingTheSpiral):
    log_image_resolution = (41, 101)
    droste_scale_factor = 256
    droste_scale_adjustment = 120
    fixed_point = 0.2 + 3.8j
    log_plane_x_range = (-7, 7)

    def construct(self):
        # Load up local variables
        planes = self.planes
        dark_planes = self.dark_planes
        a_plane, b_plane, c_plane, d_plane = planes
        dark_a_plane, dark_b_plane, dark_c_plane, dark_d_plane = dark_planes

        log_arrow_group = self.log_arrow_group
        exp_arrow_group = self.exp_arrow_group
        log_arrow, log_label = log_arrow_group
        exp_arrow, exp_label = exp_arrow_group

        droste_image = self.droste_image
        log_image_tiles = self.log_image_tiles
        blank_spot = self.blank_spot

        const = self.const
        fixed_point = self.fixed_point
        var_const = self.var_const
        var_fixed_point = self.var_fixed_point

        rot_func = self.rot_func
        get_rot_tiles = self.get_rot_tiles
        get_final_image = self.get_final_image

        # Edit dark planes
        for dark_plane in dark_planes:
            dark_plane.background_lines.set_stroke(BLUE_D, 2)
            dark_plane.axes.set_stroke(BLUE_D, 3)

        # Introduce droste_image
        frame = self.frame
        full_screen = FullScreenRectangle()
        droste_image.add(droste_image[-1].copy().scale(self.droste_scale_factor))
        droste_image.set_opacity(0.5)
        droste_image.save_state()
        droste_image.set_opacity(1)
        droste_image.clip_to_box(full_screen)
        droste_image.center()

        start_width = 1.5 * FRAME_WIDTH
        droste_image.set_width(self.droste_scale_factor * start_width)

        self.add(droste_image)
        self.play(
            UpdateFromAlphaFunc(
                droste_image,
                lambda m, a: m.set_width(start_width * np.exp(a * math.log(50)))
            ),
            droste_image.animate.scale(50),
            run_time=5
        )
        self.play(
            Restore(droste_image),
            FadeIn(a_plane),
            frame.animate.set_height(4).move_to(a_plane),
            run_time=2
        )
        self.add(planes)
        self.play(
            droste_image.animate.scale(1.0 / self.droste_scale_factor, about_point=a_plane.get_origin()),
            rate_func=lambda t: np.log(np.exp(smooth(t))),
            run_time=5
        )
        droste_image.restore()
        self.play(
            droste_image.animate.set_opacity(1),
            FadeOut(a_plane),
            FadeIn(dark_a_plane),
        )
        self.wait()

        # Show log
        frame = self.frame
        self.play(
            GrowArrow(log_arrow),
            FadeIn(log_label, LEFT),
            FadeIn(log_image_tiles),
            FadeIn(dark_b_plane),
            FadeOut(b_plane),
            frame.animate.reorient(0, 0, 0, (-0.09, 2.03, 0.0), 4.90).set_anim_args(run_time=2),
        )
        self.play(
            ShowCreation(droste_image, lag_ratio=0),
            ShowCreation(log_image_tiles, lag_ratio=0),
            FadeOut(droste_image.copy(), rate_func=rush_from),
            FadeOut(log_image_tiles.copy(), rate_func=rush_from),
            run_time=5
        )
        self.wait()

        # Show tile size
        b_unit = b_plane.get_unit_size()
        tile_box = Rectangle(math.log(self.droste_scale_factor), TAU)
        tile_box.scale(b_unit)
        tile_box.move_to(b_plane.get_origin(), DL)
        tile_box.set_stroke(YELLOW, 3)
        tile_box.set_z_index(2)

        tile_box_labels = VGroup(
            Tex(R"2\pi", font_size=24).next_to(tile_box, LEFT, SMALL_BUFF),
            Tex(R"\ln(256)", font_size=24).next_to(tile_box, UP, SMALL_BUFF),
        )
        tile_box_labels.set_backstroke(BLACK, 3)

        highlighted_tiles = log_image_tiles.copy()
        highlighted_tiles.always.clip_to_box(tile_box)

        self.add(highlighted_tiles, tile_box)
        self.play(
            ShowCreation(tile_box),
            log_image_tiles.animate.set_opacity(0.2),
            Write(tile_box_labels)
        )
        self.wait()
        self.play(
            VGroup(tile_box, tile_box_labels).animate.shift(tile_box.get_width() * LEFT)
        )
        self.wait()
        self.play(
            FadeOut(tile_box),
            FadeOut(tile_box_labels),
            FadeOut(highlighted_tiles),
            log_image_tiles.animate.set_opacity(1),
        )
        self.wait()

        # Show rotation
        mult_arrow, mult_label = self.get_mult_arrow_group()

        mult_plane, c_group = self.get_mult_plane(c_plane)
        mult_plane.match_x(mult_label)
        c_dot, c_vect, c_label = c_group
        c_dot.add_updater(lambda m: m.move_to(mult_plane.n2p(var_const.get_value())))

        rot_log_tiles = self.get_rot_tiles()

        self.play(
            frame.animate.set_height(FRAME_HEIGHT).move_to(2 * LEFT),
            LaggedStart(
                FadeIn(mult_arrow),
                FadeIn(mult_label),
                FadeIn(rot_log_tiles),
                FadeOut(c_plane),
                FadeIn(dark_c_plane),
                lag_ratio=0.1,
            ),
            run_time=2,
        )
        self.wait()
        self.play(
            FadeIn(mult_plane, 0.5 * DOWN),
            FadeIn(c_group, 0.5 * DOWN),
            mult_label.animate.next_to(mult_plane, UP),
        )
        self.play(
            var_const.animate.set_value(1),
            UpdateFromFunc(rot_log_tiles, lambda m: m.become(self.get_rot_tiles())),
            run_time=7,
            rate_func=lambda t: there_and_back_with_pause(t, 1 / 7),
        )
        self.wait()

        # Show final image
        self.pre_transform_log = self.get_log_image_tiles(b_plane, 5, 5, resolution=self.log_image_resolution)
        final_image = self.get_final_image()

        self.play(
            GrowArrow(exp_arrow),
            FadeIn(exp_label, 0.5 * RIGHT),
            ShowCreation(final_image, lag_ratio=0, run_time=5),
            ShowCreation(rot_log_tiles, lag_ratio=0, run_time=5),
            FadeOut(rot_log_tiles.copy()),
            FadeOut(d_plane),
            FadeIn(dark_d_plane),
        )
        self.wait()
        self.play(
            var_const.animate.set_value(1),
            UpdateFromFunc(rot_log_tiles, lambda m: m.become(self.get_rot_tiles())),
            UpdateFromFunc(final_image, lambda m: m.become(self.get_final_image())),
            run_time=7,
            rate_func=lambda t: there_and_back_with_pause(t, 1 / 7),
        )

        # Zoom in on the final image
        self.play(
            frame.animate.set_height(3.5).move_to(d_plane),
            dark_d_plane.animate.set_stroke(opacity=0.25),
            run_time=2,
        )
        self.wait()

        # Show the twisted Droste zoom
        rot_log_tiles.become(self.get_rot_tiles())
        final_image.become(get_final_image())
        b_unit = b_plane.get_unit_size()
        const = var_const.get_value()

        self.play(
            frame.animate.set_height(4.9).move_to(VGroup(c_plane, d_plane)),
            dark_d_plane.animate.set_stroke(opacity=0.25),
            run_time=2,
        )
        self.wait()
        self.play(
            rot_log_tiles.animate.shift(c_plane.n2p(1 * const * math.log(256)) - c_plane.get_origin()),
            self.pre_transform_log.animate.shift(1 * b_unit * math.log(256) * RIGHT),
            UpdateFromFunc(
                final_image,
                lambda m: m.become(get_final_image())
            ),
            run_time=5,
            rate_func=linear,
        )
        return

        # Change the final image based on constant

        # Zoom in on final image (Old)
        self.pre_transform_log = self.get_log_image_tiles(b_plane, 7, 7, resolution=self.log_image_resolution)
        final_image.become(self.get_final_image())


        exp_tracker = ValueTracker(0)
        ref_height = frame.get_height()
        frame.add_updater(lambda m: m.set_height(ref_height * np.exp(exp_tracker.get_value())).move_to(d_plane))

        self.play(
            exp_tracker.animate.set_value(-9.5),
            run_time=15
        )

    def get_log_image_path(self):
        return get_print_gallery_log_image_path()


class TransformPrintGalleryFromStraightToLoop(FourPannelsWithPrintGallery):
    droste_scale_adjustment = 150 / 256
    fixed_point = (3.8 + TAU) * 1j

    def construct(self):
        # Load up local variables
        planes = self.planes
        dark_planes = self.dark_planes
        a_plane, b_plane, c_plane, d_plane = planes
        dark_a_plane, dark_b_plane, dark_c_plane, dark_d_plane = dark_planes

        droste_image = self.droste_image
        blank_spot = self.blank_spot

        const = self.const
        var_const = self.var_const

        # Edit dark planes
        for dark_plane in dark_planes:
            dark_plane.background_lines.set_stroke(BLUE_D, 2)
            dark_plane.axes.set_stroke(BLUE_D, 3)

        self.add(dark_a_plane, dark_d_plane)

        # Change
        frame = self.frame
        frame.replace(d_plane, 1)

        self.var_fixed_point.set_value(3.8j + TAU * 1j)
        self.pre_transform_log = always_redraw(lambda: self.get_log_image_tiles(b_plane, 5, 5, resolution=self.log_image_resolution))
        final_image = always_redraw(self.get_final_image)

        self.add(final_image)
        self.add(self.pre_transform_log)
        self.var_const.set_value(1)
        self.play(
            self.var_const.animate.set_value(const),
            run_time=8,
        )
