# ==============================================================================
# Scene:      PythagoreanIntuition
# Source:     videos/_2025/grover/qc_supplements.py (lines 1173-1362)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl PythagoreanIntuition.py PythagoreanIntuition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)



# ----- From _2025/grover/qc_supplements.py -----

class PythagoreanIntuition(InteractiveScene):
    def construct(self):
        # Set up axes
        x_range = y_range = z_range = (-2, 2)
        axes = ThreeDAxes(x_range, y_range, z_range)
        plane = NumberPlane(x_range, y_range)
        plane.fade(0.5)
        axes_group = VGroup(plane, axes)
        axes_group.scale(2)

        # Trace square
        frame = self.frame
        square = Square(2)
        square.move_to(ORIGIN, DL)
        square.set_stroke(WHITE, 2)

        side_lines = VGroup(
            Line(axes.get_origin(), axes.c2p(1, 0, 0)),
            Line(axes.c2p(1, 0, 0), axes.c2p(1, 1, 0)),
            Line(axes.c2p(1, 1, 0), axes.c2p(1, 1, 1)),
        )
        side_lines.set_stroke(RED, 4)
        ones = VGroup(
            Tex(R"1", font_size=36).next_to(line, vect, SMALL_BUFF)
            for line, vect in zip(side_lines, [DOWN, RIGHT, RIGHT])
        )
        ones[2].rotate(90 * DEG, RIGHT)

        dot = GlowDot(color=RED)
        dot.move_to(ORIGIN)

        frame.set_height(5).move_to(square)
        self.add(square, dot)
        for line, one in zip(side_lines[:2], ones):
            self.play(
                ShowCreation(line),
                FadeIn(one, 0.5 * line.get_vector()),
                dot.animate.move_to(line.get_end())
            )
        self.wait()
        self.play(
            MoveAlongPath(dot, square, rate_func=lambda t: 1 - 0.5 * smooth(t))
        )

        # Show diagonal
        diag = Line(square.get_corner(DL), square.get_corner(UR))
        diag.set_stroke(PINK, 3)

        sqrts = VGroup(
            Tex(R"\sqrt{1^2 + 1^2}", font_size=24),
            Tex(R"\sqrt{2}", font_size=36),
        )
        for sqrt in sqrts:
            sqrt.next_to(diag.pfp(0.5), UL, buff=0.05)

        self.play(
            ShowCreation(diag),
            dot.animate.move_to(square.get_corner(UR)),
            TransformFromCopy(ones[:2], sqrts[0]["1"], time_span=(1, 2)),
            *(
                Write(sqrts[0][tex], time_span=(1, 2))
                for tex in [R"\sqrt", "+", "2"]
            ),
            run_time=2,
        )
        self.wait()
        self.play(
            TransformMatchingTex(*sqrts, key_map={"1^2 + 1^2": "2"}, run_time=1)
        )
        self.wait()

        # Bring it up to a cube
        axes_group.set_z_index(-1)
        cube = VCube(2)
        cube.move_to(ORIGIN, DL + IN)
        cube.set_stroke(WHITE, 2)
        cube.set_fill(opacity=0)

        self.add(cube, side_lines[:2])
        self.play(
            FadeIn(axes_group),
            ShowCreation(cube, lag_ratio=0.1, time_span=(0.5, 2.0)),
            frame.animate.reorient(-16, 68, 0, (0.45, 0.98, 1.05), 4.36),
            run_time=2
        )
        frame.add_ambient_rotation(DEG)
        line = side_lines[2]
        self.play(
            ShowCreation(line),
            FadeIn(ones[2], 0.5 * line.get_vector()),
            dot.animate.move_to(line.get_end())
        )
        self.wait(2)

        # Show three dimensional diagonal
        diag3 = Line(axes.c2p(0, 0, 0), axes.c2p(1, 1, 1))
        diag3.set_stroke(YELLOW, 3)

        new_sqrts = VGroup(
            Tex(R"\sqrt{\sqrt{2}^2 + 1^2}", font_size=24),
            Tex(R"\sqrt{3}", font_size=36),
        )
        for sqrt in new_sqrts:
            sqrt.rotate(90 * DEG, RIGHT)
            sqrt.next_to(diag3.get_center(), LEFT + OUT, SMALL_BUFF)

        self.play(ShowCreation(diag3, run_time=2))
        self.play(
            TransformFromCopy(ones[2], new_sqrts[0]["1"][0], time_span=(1, 2)),
            TransformFromCopy(sqrts[1], new_sqrts[0][R"\sqrt{2}"][0], time_span=(1, 2)),
            *(
                Write(new_sqrts[0][tex], time_span=(1, 2))
                for tex in [R"\sqrt", "+", "2"]
            ),
            run_time=2,
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                *new_sqrts,
                key_map={R"\sqrt{2}^2 + 1^2": "3"},
                match_animation=FadeTransform,
                run_time=1,
            )
        )
        self.wait(6)

        # Show observables
        symbols = VGroup(ones, sqrts[1], new_sqrts[1])
        wireframe = VGroup(cube, side_lines, diag, diag3)

        basis_vectors = VGroup(
            Vector(2 * v, thickness=4, fill_color=color)
            for v, color in zip(np.identity(3), [BLUE_E, BLUE_D, BLUE_C])
        )
        basis_vectors.set_z_index(1)
        for vector in basis_vectors:
            vector.always.set_perpendicular_to_camera(frame)

        obs_labels = VGroup(
            KetGroup(Text(f"Obs {n}", font_size=30), height_scale_factor=1.5, buff=0.05)
            for n in range(1, 4)
        )
        obs_labels[2].rotate(90 * DEG, RIGHT)
        for vector, label, nudge in zip(basis_vectors, obs_labels, [UP, RIGHT, RIGHT]):
            label.next_to(vector.get_end(), vector.get_vector() + nudge, buff=0.05)

        self.add(Point(), basis_vectors)
        self.play(
            LaggedStartMap(GrowArrow, basis_vectors, lag_ratio=0.25),
            FadeOut(symbols),
            FadeOut(dot),
            wireframe.animate.set_stroke(opacity=0.2),
            frame.animate.reorient(13, 67, 0, (-0.04, 0.76, 0.87), 4.84),
        )
        self.play(LaggedStartMap(FadeIn, obs_labels, lag_ratio=0.25))
        self.wait(4)

        new_cube = cube.copy()
        new_cube.deactivate_depth_test()
        new_cube.set_z_index(0)
        new_cube.set_stroke(WHITE, 3, 1)
        self.play(
            Write(new_cube, stroke_width=5, lag_ratio=0.1, run_time=3),
        )
        self.play(FadeOut(new_cube))
        self.wait(4)

        # Show many diagonal directions
        diag_vects = VGroup(
            Vector(2 * normalize(np.array(tup)))
            for tup in it.product(* 3 * [[-1, 0, 1]])
            if get_norm(tup) > 0
        )
        for vect in diag_vects:
            vect.set_perpendicular_to_camera(frame)
            color = random_bright_color(
                hue_range=(0.4, 0.5),
                saturation_range=(0.5, 0.7),
                luminance_range=(0.5, 0.6)
            )
            vect.set_color(color)

        self.play(
            FadeOut(obs_labels),
            LaggedStartMap(GrowArrow, diag_vects),
            frame.animate.reorient(-19, 61, 0, (-0.17, 0.22, -0.25), 6.96),
            run_time=3
        )
        self.wait(10)
