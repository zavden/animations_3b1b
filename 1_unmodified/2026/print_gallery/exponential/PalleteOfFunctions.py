# ==============================================================================
# Scene:      PalleteOfFunctions
# Source:     videos/_2026/print_gallery/exponential.py (lines 263-426)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PalleteOfFunctions.py PalleteOfFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def apply_func_between_planes(mob, func, src_plane, trg_plane):
    mob.shift(-src_plane.get_origin())
    mob.scale(1.0 / src_plane.get_unit_size(), about_point=ORIGIN)
    mob.apply_complex_function(func)
    mob.scale(trg_plane.get_unit_size(), about_point=ORIGIN)
    mob.shift(trg_plane.get_origin())
    return mob


def get_nested_square_grid(n_rows=8, n_recursions=6, height=4, stroke_color=WHITE, stroke_width=2, stroke_width_decay_factor=0.85, scale_factor=2):
    grid = Square().get_grid(n_rows, n_rows, buff=0)
    grid.center()
    grid.set_height(height)
    grid.set_stroke(stroke_color, stroke_width)
    grid.remove(*[
        square for square in grid
        if np.all(np.abs(square.get_center()) < (height / 2) / scale_factor)
    ])
    result = VGroup(grid)
    for n in range(n_recursions):
        result.add(result[-1].copy().scale((1 / scale_factor), about_point=ORIGIN))
        result[-1].set_stroke(width=stroke_width * stroke_width_decay_factor**(n + 1))

    return result


class PalleteOfFunctions(InteractiveScene):
    def construct(self):
        # Add example
        frame = self.frame
        frame.set_height(9)

        examples = VGroup(
            self.get_input_output_grid(R"{c} \cdot z", lambda z: (1.5 + 0.8j) * z),
            self.get_input_output_grid("z^2", lambda z: z**2),
            self.get_input_output_grid("z^3", lambda z: z**3),
            self.get_input_output_grid(
                "e^z", np.exp,
                in_x_range=(-7, 7),
                out_x_range=(-7, 7),
                in_grid_dims=(25, 16),
                in_grid_height=6.25,
                in_grid_z0=-2,
            ),
            log_example := self.get_input_output_grid(
                R"\ln(z)", np.log,
                in_x_range=(-2, 2),
                out_x_range=(-4, 4),
                in_grid_dims=(16, 16),
                in_grid_height=4,
                in_grid_z0=-2 - 2j,
            ),
            self.get_input_output_grid(
                R"\cos(z)", np.cos,
                in_grid_dims=(8, 16),
                in_grid_z0=-2,
            ),
            self.get_input_output_grid(
                R"\sin(z)", np.sin,
                in_grid_dims=(8, 16),
                in_grid_z0=-2,
            ),
            self.get_input_output_grid(R"\zeta(z)", lambda z: z),
            self.get_input_output_grid(R"\wp(z)", lambda z: z),
            self.get_input_output_grid(R"j(\tau)", lambda z: z),
        )
        for n, example in enumerate(examples):
            example.shift((3 - 3 * n) * UP - example[1].get_center())
        examples[5:].shift(15 * UP + 15 * RIGHT)

        self.add(examples)

        # Tweak log example
        in_plane = log_example[1]
        out_plane = log_example[3]
        log_grid = get_nested_square_grid(n_recursions=6)
        log_grid.replace(in_plane)
        log_grid.insert_n_curves(10)
        out_grid = log_grid.copy()
        for piece in out_grid.family_members_with_points():
            piece.scale(0.99)
        apply_func_between_planes(out_grid, np.log, in_plane, out_plane)
        for piece in out_grid.family_members_with_points():
            piece.scale(1.0 / 0.99)
        log_grid.set_stroke(BLUE, 1)
        out_grid.set_stroke(PINK, 1)

        log_example.replace_submobject(-2, log_grid)
        log_example.replace_submobject(-1, out_grid)

        # Cover up with question marks
        cover_rects = VGroup()
        all_q_marks = VGroup()
        for example in examples[3:]:
            planes = example[1:4]
            rect = BackgroundRectangle(planes, buff=MED_SMALL_BUFF)
            rect.set_fill(GREY_E, 1)
            q_marks = VGroup(
                Tex(R"?").set_height(0.5 * planes[0].get_height()).move_to(piece)
                for piece in planes
            )

            cover_rects.add(rect)
            all_q_marks.add(q_marks)

        self.add(cover_rects)
        self.add(all_q_marks)
        self.play(
            frame.animate.reorient(0, 0, 0, (7, -3, 0.0), 15.5),
            run_time=2
        )

        # Highlight exp and log
        exp_example, log_example = exp_log = examples[3:5]

        rect = SurroundingRectangle(exp_log, buff=0.5)

        self.play(
            ShowCreation(rect),
            FadeOut(cover_rects[:2]),
            FadeOut(all_q_marks[:2]),
        )
        self.play(
            frame.animate.reorient(0, 0, 0, (0.64, -7.71, 0.0), 7.26),
            examples[:3].animate.fade(0.8),
            FadeOut(examples[5:]),
            FadeOut(cover_rects[2:], time_span=(3, 4)),
            FadeOut(all_q_marks[2:], time_span=(3, 4)),
            rect.animate.set_stroke(width=1),
            run_time=4,
        )
        self.wait()

        # Emphasize the log
        self.remove(out_grid)
        self.play(
            FadeOut(out_grid.copy(), time_span=(0, 1)),
            TransformFromCopy(log_grid, out_grid),
            run_time=4,
        )
        self.wait()
        return

        # Focus on exp
        self.play(
            rect.animate.surround(exp_example, buff=0.5),
            log_example.animate.fade(0.8),
            frame.animate.match_y(exp_example).set_height(6.5),
            run_time=2
        )
        self.wait()

    def get_input_output_grid(
        self,
        tex_label,
        func,
        in_x_range=(-2, 2),
        out_x_range=(-4, 4),
        in_grid_dims=(8, 8),
        in_grid_height=2,
        in_grid_z0=0,
        plane_height=2,
        in_grid_color=BLUE,
        out_grid_color=PINK
    ):
        func_label = Tex(tex_label, font_size=72)
        in_plane, out_plane = planes = VGroup(
            ComplexPlane(in_x_range, in_x_range, faded_line_ratio=0),
            ComplexPlane(out_x_range, out_x_range, faded_line_ratio=0),
        )
        for plane in planes:
            plane.set_height(plane_height)
            plane.background_lines.set_stroke(BLUE, 1, 0.5)
            plane.add_coordinate_labels(font_size=16 / in_x_range[1], buff=0.1 / in_x_range[1])

        group = VGroup(func_label, in_plane, Vector(RIGHT), out_plane)
        group.arrange(RIGHT)
        func_label.shift(0.5 * LEFT)

        in_grid = Square().get_grid(*in_grid_dims, buff=0)
        in_grid.set_height(in_plane.get_unit_size() * in_grid_height)
        in_grid.move_to(in_plane.n2p(in_grid_z0), DL)
        in_grid.insert_n_curves(20)
        out_grid = apply_func_between_planes(in_grid.copy(), func, in_plane, out_plane)
        out_grid.always.clip_to_box(out_plane)
        in_grid.set_stroke(in_grid_color, 1)
        out_grid.set_stroke(out_grid_color, 1)

        group.add(in_grid, out_grid)
        return group
