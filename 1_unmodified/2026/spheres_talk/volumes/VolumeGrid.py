# ==============================================================================
# Scene:      VolumeGrid
# Source:     videos/_2026/spheres_talk/volumes.py (lines 113-717)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VolumeGrid.py VolumeGrid -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_boundary_volume_texs():
    return [
        R"0",
        R"2",
        R"2\pi r",
        R"4\pi r^2",
        R"2\pi^2 r^3",
        R"{8 \over 3}\pi^2 r^4",
        R"\pi^3 r^5",
        R"{16 \pi^3 \over 15} r^6",
        R"{\pi^4 \over 3} r^7",
        R"{32 \pi^4 \over 105} r^8",
    ]


def get_volume_texs():
    return [
        R"1",
        R"2 r",
        R"\pi r^2",
        R"{4 \over 3} \pi r^3",
        R"{\pi^2 \over 2} r^4",
        R"{8 \over 15} \pi^2 r^5",
        R"{\pi^3 \over 6} r^6",
        R"{16 \pi^3 \over 105} r^7",
        R"{\pi^4 \over 24} r^8",
        R"{32 \pi^4 \over 945} r^9",
        R"{\pi^5 \over 120} r^10",
    ]


class VolumeGrid(InteractiveScene):
    tex_to_color = {"r": BLUE}

    def construct(self):
        # Write the grid
        frame = self.frame
        n_cols = 10
        grid = self.get_grid(n_cols)
        boundary_labels, volume_labels = self.get_volume_labels()
        labels = VGroup(
            VGroup(*pair)
            for pair in zip(boundary_labels, volume_labels)
        )

        for label_pair, col in zip(labels, grid):
            for label, square in zip(label_pair, col):
                label.move_to(square)
                square.label = label

        self.add(grid[1:])

        # Row labels
        row_labels = VGroup(
            Tex(R"\partial B^n"),
            Tex(R"B^n"),
        )
        for square, label in zip(grid[1], row_labels):
            label.next_to(square, LEFT)

        col_labels = VGroup(Integer(n, font_size=40) for n in range(n_cols))
        for col, label in zip(grid, col_labels):
            label.next_to(col, UP)

        cols_label = Text("Dimension")
        cols_label.next_to(col_labels[1:4], UP)
        cols_label.to_edge(UP, buff=MED_SMALL_BUFF)

        self.add(col_labels[1:])
        self.add(cols_label)

        # Add for d=2 and d=3
        def highlight_cell(row, col, run_time=3, fill_color=TEAL_E, fill_opacity=0.5):
            kw = dict(rate_func=there_and_back_with_pause, run_time=run_time)
            cell = grid[col][row]
            return cell.animate.set_fill(fill_color, fill_opacity).set_anim_args(**kw)

        for d, n in it.product([2, 3], [0, 1]):
            self.play(
                highlight_cell(n, d),
                Write(labels[d][n]),
                run_time=1
            )

        # Add row labels
        rect = SurroundingRectangle(row_labels[1])
        rect.set_stroke(TEAL, 3)
        boundary_word = Text("“Boundary”")
        boundary_word.set_color(TEAL)
        boundary_word.next_to(row_labels[0], LEFT)

        self.play(ShowCreation(rect), Write(row_labels[1]))
        self.wait()
        self.play(
            rect.animate.surround(row_labels[0]),
            TransformMatchingTex(row_labels[1].copy(), row_labels[0]),
            run_time=1
        )
        self.wait()
        self.play(
            frame.animate.set_x(-3),
            FadeIn(boundary_word, lag_ratio=0.1),
            rect.animate.surround(row_labels[0][0])
        )
        self.wait()
        self.play(
            frame.animate.set_x(0),
            FadeOut(rect),
            FadeOut(boundary_word),
        )
        self.wait()

        # Arrows from bottom to top
        arrows = VGroup(
            Arrow(
                stack[1].get_right(),
                stack[0].get_corner(DR),
                buff=SMALL_BUFF,
                thickness=5,
                path_arc=180 * DEG
            )
            for stack in labels[2:4]
        )
        arrows.set_color(TEAL)
        self.play(Write(arrows))
        self.wait()
        self.play(FadeOut(arrows))

        # Show derivatives
        self.show_derivative_and_integral(grid, 2)
        self.show_derivative_and_integral(grid, 3)

        # Add for d=1
        self.play(
            highlight_cell(1, 1),
            FadeIn(volume_labels[1])
        )
        self.play(
            highlight_cell(0, 1),
            FadeIn(boundary_labels[1])
        )

        # Ask about the rest
        q_marks = VGroup(
            VGroup(
                Tex(R"?", font_size=72).move_to(cell)
                for cell in col
            )
            for col in grid[4:]
        )
        q_marks.set_fill(YELLOW)
        self.play(
            Write(q_marks, lag_ratio=0.05),
            Write(grid[4:], lag_ratio=0.05),
            Write(col_labels[4:], lag_ratio=0.05),
            cols_label.animate.match_x(col_labels),
        )

        # Show knights move
        knight_group = self.get_knights_move_group(grid, 3)
        circle_cell = grid[2][0]

        self.play(FadeIn(knight_group))
        self.wait()
        self.play(circle_cell.animate.set_fill(RED, 0.35))
        self.wait()

        # New knights moves
        for d in range(4, 10):
            self.play(
                knight_group.animate.move_to(grid[d - 2][1], DL),
                FadeOut(q_marks[d - 4][0])
            )
            label_copy = boundary_labels[d].copy()
            self.play(
                TransformMatchingTex(boundary_labels[2].copy(), label_copy),
                TransformMatchingTex(volume_labels[d - 2].copy(), boundary_labels[d]),
                run_time=1
            )
            self.remove(label_copy)
            self.wait()
            self.show_derivative_and_integral(
                grid, d,
                int_added_anims=[
                    FadeOut(q_marks[d - 4][1]),
                    TransformMatchingTex(boundary_labels[d].copy(), volume_labels[d]),
                ],
                skip_derivative=True
            )
            self.wait()

        # Clean up
        self.play(
            FadeOut(knight_group),
            circle_cell.animate.set_fill(opacity=0)
        )

        # Show volume constants
        t2c = {"b_n": YELLOW, "b_{n - 2}": YELLOW}
        gen_formula = Tex(R"V(B^n) = b_n r^n", t2c=t2c, font_size=72)
        gen_formula["r"].set_color(BLUE)
        gen_formula.to_edge(DOWN)
        gen_b_part = gen_formula["b_n"][0]

        kw = dict(font_size=48)
        c_formulas = VGroup(
            Tex(R"b_0 = 1", **kw),
            Tex(R"b_1 = 2", **kw),
            Tex(R"b_2 = \pi", **kw),
            Tex(R"b_3 = {4 \over 3} \pi", **kw),
            Tex(R"b_4 = {\pi^2 \over 2}", **kw),
            Tex(R"b_5 = {8 \over 15} \pi^2", **kw),
            Tex(R"b_6 = {\pi^3 \over 6}", **kw),
            Tex(R"b_7 = {16 \over 105} \pi^3", **kw),
            Tex(R"b_8 = {\pi^4 \over 24}", **kw),
        )

        self.play(Write(gen_formula))
        self.wait()

        last_highlight = VGroup()
        last_b_formula = VGroup()
        for col, b_formula, label in zip(grid[1:], c_formulas[1:], volume_labels[1:]):
            highlight = col[1].copy()
            highlight.set_fill(TEAL_E, 0.5)

            b_part = b_formula[re.compile(r"b_.")][0]
            b_part.set_color(YELLOW)
            b_formula.move_to(highlight)
            b_formula.shift(1.0 * highlight.get_height() * DOWN)

            group = VGroup(highlight, b_formula)
            self.play(
                FadeOut(last_highlight),
                FadeOut(last_b_formula),
                FadeIn(highlight),
                TransformFromCopy(gen_b_part, b_part),
                FadeTransform(
                    label[:len(b_formula) - 3].copy(),
                    b_formula[3:],
                    time_span=(0.25, 1)
                ),
                Write(b_formula[2], time_span=(0.25, 1.0)),
            )
            self.wait()

            last_highlight = highlight
            last_b_formula = b_formula
        self.play(
            FadeOut(last_highlight),
            FadeOut(last_b_formula),
        )

        # Show recursion formula
        recursion_formula = Tex(R"b_n = {2\pi \over n} b_{n - 2}", t2c=t2c, font_size=72)
        alt_recursion_formula = Tex(R"b_n = {\pi \over n / 2} b_{n - 2}", t2c=t2c, font_size=72)
        recursion_formula.to_corner(DR)
        alt_recursion_formula.move_to(recursion_formula)

        self.play(
            gen_formula.animate.match_y(recursion_formula).to_edge(LEFT, buff=LARGE_BUFF),
            TransformFromCopy(gen_formula["b_n"], recursion_formula["b_n"]),
        )
        self.play(Write(recursion_formula[2:]))
        self.wait()
        self.play(TransformMatchingTex(recursion_formula, alt_recursion_formula))
        self.wait()

        # Shrink
        zero_group = VGroup(grid[0], col_labels[0], labels[0])
        zero_group.set_fill(opacity=0)
        zero_group.set_stroke(opacity=0)
        grid_group = VGroup(grid, row_labels, col_labels, cols_label, labels)
        formula_group = VGroup(gen_formula, alt_recursion_formula)
        self.play(
            grid_group.animate.set_height(3.0, about_edge=UP),
            formula_group.animate.arrange(DOWN, buff=0.5, aligned_edge=LEFT).set_max_height(2).to_corner(DL)
        )
        self.wait()

        # Show recursion example
        stages = VGroup(
            Tex(R"b_8 = {\pi \over 4} b_6"),
            Tex(R"b_8 = {\pi \over 4} {\pi \over 3} b_4"),
            Tex(R"b_8 = {\pi \over 4} {\pi \over 3} {\pi \over 2} b_2"),
            Tex(R"b_8 = {\pi \over 4} {\pi \over 3} {\pi \over 2} {\pi \over 1} b_0"),
        )
        stages.set_height(1.2)
        stages.next_to(formula_group, RIGHT, buff=2.5)
        for stage in stages:
            stage.align_to(stages[-1], LEFT)
            stage[re.compile(r"b_.")].set_color(YELLOW)

        mult_arrows = VGroup(
            Arrow(
                col1.get_bottom(),
                col2.get_bottom(),
                path_arc=120 * DEG
            )
            for col1, col2 in zip(grid[0::2], grid[2::2])
        )
        arrow_label_texs = [
            R"\times \pi / 1",
            R"\times \pi / 2",
            R"\times \pi / 3",
            R"\times \pi / 4",
        ]
        for arrow, tex in zip(mult_arrows, arrow_label_texs):
            label = Tex(tex)
            label.next_to(arrow, DOWN, SMALL_BUFF)
            arrow.push_self_into_submobjects()
            arrow.add(label)

        zero_cells = grid[0]

        highlights = VGroup(col[1].copy() for col in grid[0::2])
        highlights.set_fill(TEAL, 0.5)

        self.play(
            FadeOut(boundary_labels[4:]),
            FadeOut(volume_labels[4:]),
        )
        self.play(
            Write(stages[0]),
        )
        self.wait()
        self.play(
            Write(mult_arrows[-1]),
            FadeIn(highlights[-2:]),
        )
        self.wait()
        self.play(
            TransformMatchingTex(stages[0], stages[1], key_map={"b_6": "b_4"}, run_time=1),
            Write(mult_arrows[-2]),
            FadeIn(highlights[-3]),
        )
        self.wait()
        self.play(
            TransformMatchingTex(stages[1], stages[2], key_map={"b_4": "b_2"}, run_time=1),
            Write(mult_arrows[-3]),
            FadeIn(highlights[-4]),
        )
        self.wait()
        self.play(
            TransformMatchingTex(stages[2], stages[3], key_map={"b_2": "b_0"}, run_time=1),
            Write(mult_arrows[-4]),
            FadeIn(highlights[-5]),
            grid[0].animate.set_stroke(opacity=1),
            Write(col_labels[0]),
            row_labels.animate.next_to(grid, LEFT, MED_SMALL_BUFF)
        )
        self.wait()

        # Fill in zero terms
        self.play(volume_labels[0].animate.set_fill(opacity=1))
        self.wait()
        self.play(boundary_labels[0].animate.set_fill(opacity=1))
        self.wait()

        # General formula
        b8_form = stages[-1]

        gen_b_form = Tex(R"b_n = {\pi^{n / 2} \over (n / 2)!}", t2c=t2c, font_size=48)
        gen_b_form.move_to(b8_form)
        gen_b_form.to_edge(RIGHT, buff=LARGE_BUFF)

        small_b8_form = b8_form.copy()
        small_b8_form.generate_target()
        small_b8_form.target[-2:].set_opacity(0)
        small_b8_form.target.shift(0.75 * LEFT)
        small_b8_form.target.scale(gen_b_form[0].get_height() / small_b8_form[0].get_height())

        pis = b8_form[3:-2]
        pis_target = gen_b_form[R"{\pi^{n / 2} \over (n / 2)!}"][0]
        pis_rect = SurroundingRectangle(pis, buff=SMALL_BUFF)
        pis_rect.set_stroke(TEAL, 3)

        self.play(ShowCreation(pis_rect))
        self.wait()
        self.play(
            TransformMatchingTex(
                b8_form, gen_b_form,
                key_map={"b_8": "b_n"},
                matched_keys=[R"\pi", R"\over"]
            ),
            pis_rect.animate.surround(pis_target),
            MoveToTarget(small_b8_form),
            run_time=1
        )
        self.play(FadeOut(pis_rect))
        self.wait()

        # Substitute in
        final_formula = Tex(
            R"V(B^n) = {\pi^{n / 2} \over (n / 2)!} {r}^n",
            t2c={"{r}": BLUE},
            font_size=72
        )
        final_formula.next_to(grid, DOWN, buff=2.25)
        final_formula.to_edge(LEFT)

        bn_parts = VGroup(
            formula[R"{\pi^{n / 2} \over (n / 2)!}"]
            for formula in [gen_b_form, final_formula]
        )
        bn_rect = SurroundingRectangle(bn_parts[0])
        bn_rect.set_stroke(YELLOW, 1)

        self.play(
            FadeOut(small_b8_form),
            FadeOut(alt_recursion_formula),
        )
        self.play(ShowCreation(bn_rect))
        self.play(
            TransformFromCopy(*bn_parts),
            TransformFromCopy(
                gen_formula[R"V(B^n) = "].copy(),
                final_formula[R"V(B^n) = "],
            ),
            TransformFromCopy(
                gen_formula[R"r^n"],
                final_formula[R"{r}^n"],
            ),
            FadeOut(gen_b_form),
            FadeOut(gen_formula),
            bn_rect.animate.surround(bn_parts[1], buff=0.05),
        )
        self.wait()
        self.play(
            bn_rect.animate.surround(final_formula, buff=0.25).set_stroke(width=2),
        )
        self.add(final_formula)
        self.wait()

        # Fill in even volume labels
        def fill_every_other_label_from(n=2):
            for vl1, vl2 in zip(volume_labels[n::2], volume_labels[n + 2:-1:2]):
                self.play(
                    TransformMatchingTex(vl1.copy(), vl2, path_arc=60 * DEG),
                    run_time=1
                )

            self.wait()
            self.play(LaggedStart(
                *(
                    TransformMatchingTex(vl.copy(), bl)
                    for vl, bl in zip(volume_labels[n + 2::2], boundary_labels[n + 2::2])
                ),
                run_time=1.5,
                lag_ratio=0.2
            ))

        fill_every_other_label_from(2)

        # Shift multiplication arrows
        pure_mult_arrows = VGroup(ma[0] for ma in mult_arrows)
        mult_arrow_labels = VGroup(ma[1] for ma in mult_arrows)

        shift_vect = grid[1].get_center() - grid[0].get_center()
        pure_mult_arrows.generate_target()
        pure_mult_arrows.target.shift(shift_vect)

        new_arrow_texs = [
            R"\times {\pi \over 3 / 2}",
            R"\times {\pi \over 5 / 2}",
            R"\times {\pi \over 7 / 2}",
            R"\times {\pi \over 9 / 2}",
        ]
        alt_new_arrow_texs = [
            R"\times {2 \pi \over 3}",
            R"\times {2 \pi \over 5}",
            R"\times {2 \pi \over 7}",
            R"\times {2 \pi \over 9}",
        ]
        new_arrow_labels = VGroup(map(Tex, new_arrow_texs))
        alt_new_arrow_labels = VGroup(map(Tex, alt_new_arrow_texs))
        for label, alt_label, arrow in zip(new_arrow_labels, alt_new_arrow_labels, pure_mult_arrows.target):
            for mob in [label, alt_label]:
                mob.next_to(arrow, DOWN, SMALL_BUFF)

        self.play(
            MoveToTarget(pure_mult_arrows, lag_ratio=0.2),
            LaggedStart(
                *(
                    TransformMatchingTex(l1, l2)
                    for l1, l2 in zip(mult_arrow_labels, new_arrow_labels)
                ),
                lag_ratio=0.2,
            ),
            run_time=1.5
        )
        self.wait()

        # Fill in odd volume labels
        fill_every_other_label_from(3)

        self.play(
            LaggedStart(
                (TransformMatchingTex(l1, l2, rate_func=there_and_back_with_pause)
                for l1, l2 in zip(new_arrow_labels, alt_new_arrow_labels)),
                lag_ratio=0.05,
                run_time=5
            )
        )
        self.remove(alt_new_arrow_labels)
        self.add(new_arrow_labels)

        # Plug it in for n = 1
        d1_form = Tex(R"V(B^1) = {\pi^{1/2} \over (1/2)!} {r} = 2{r}", t2c={"{r}": BLUE})
        alt_d1_form = Tex(R"V(B^1) = {\sqrt{\pi} \over (1/2)!} {r} = 2{r}", t2c={"{r}": BLUE})
        for form in d1_form, alt_d1_form:
            form.next_to(final_formula, RIGHT, buff=1.0, aligned_edge=DOWN)

        self.play(
            VGroup(final_formula, bn_rect).animate.scale(0.7, about_edge=DL),
            FadeTransform(final_formula.copy(), d1_form),
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                d1_form,
                alt_d1_form,
                key_map={R"^{1/2}": R"\sqrt"},
                matched_keys=[R"\pi"],
                run_time=1,
            )
        )
        self.wait()

        # Half factorial fact
        half_fact = Tex(R"(1/2)! = {\sqrt{\pi} \over 2}")
        half_fact.move_to(d1_form)

        self.play(TransformMatchingTex(alt_d1_form, half_fact, path_arc=-PI / 2))
        self.wait()

    def get_grid(self, n_cols=10, width=FRAME_WIDTH - 1):
        cell = Square()
        cell.set_stroke(WHITE, 2)
        col = cell.get_grid(2, 1, buff=0)
        grid = col.get_grid(1, n_cols, buff=0)
        grid.set_width(width)
        grid.to_edge(UP, buff=1.5)
        grid.set_z_index(-1)
        return grid

    def get_volume_labels(self):
        config = dict(
            t2c=self.tex_to_color,
            font_size=36,
        )
        return VGroup(
            VGroup(
                Tex(tex, **config)
                for tex in texs
            )
            for texs in [
                get_boundary_volume_texs(),
                get_volume_texs(),
            ]
        )

    def show_derivative_and_integral(
        self,
        grid,
        dim,
        upper_buff=1.25,
        deriv_added_anims=[],
        int_added_anims=[],
        skip_derivative=False
    ):
        top_cell = grid[dim][0]
        low_cell = grid[dim][1]
        right_point = VGroup(top_cell, low_cell).get_right()

        down_arrow = Arrow(
            top_cell.get_right(),
            low_cell.get_right(),
            buff=SMALL_BUFF,
            thickness=5,
            path_arc=-180 * DEG
        )
        down_arrow.scale(0.8, about_point=right_point)

        up_arrow = down_arrow.copy().flip(RIGHT)

        deriv_label = Tex(R"{d / dr}", t2c=self.tex_to_color)
        deriv_label.next_to(up_arrow, RIGHT, SMALL_BUFF)
        int_label = Tex(R"\int \dots dr", t2c=self.tex_to_color)
        int_label.next_to(down_arrow, RIGHT, SMALL_BUFF)

        cover_rect = Rectangle(width=grid.get_width(), height=grid.get_height() + upper_buff)
        cover_rect.set_fill(BLACK, 0.85)
        cover_rect.set_stroke(width=0)
        cover_rect.next_to(right_point, RIGHT, buff=5e-3)
        cover_rect.shift(1e-2 * RIGHT)

        if skip_derivative:
            self.play(
                FadeIn(cover_rect),
                Write(down_arrow),
                Write(int_label),
                *int_added_anims
            )
            self.wait()
        else:
            self.play(LaggedStart(
                FadeIn(cover_rect),
                Write(up_arrow),
                Write(deriv_label),
                *deriv_added_anims,
                lag_ratio=0.5,
            ))
            self.wait()
            self.play(
                TransformMatchingTex(deriv_label, int_label, run_time=1),
                ReplacementTransform(up_arrow, down_arrow),
                *int_added_anims,
            )
            self.wait()
        self.play(
            FadeOut(down_arrow),
            FadeOut(int_label),
            FadeOut(cover_rect),
        )

    def get_knights_move_group(self, grid, d, colors=[GREEN, YELLOW], opacity=0.4):
        # Test
        cells = VGroup(grid[d - 2][1], grid[d][0]).copy()
        for cell, color in zip(cells, colors):
            cell.set_fill(color, opacity)

        arrow = Arrow(cells[0], cells[1], thickness=5, buff=-0.25)
        arrow.set_backstroke(BLACK, 5)

        return VGroup(cells, arrow)
