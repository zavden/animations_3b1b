# ==============================================================================
# Scene:      AreaCircleOverAreaSquareThenVolume
# Source:     videos/_2026/spheres_talk/supplements.py (lines 340-455)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AreaCircleOverAreaSquareThenVolume.py AreaCircleOverAreaSquareThenVolume -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AreaCircleOverAreaSquareThenVolume(InteractiveScene):
    def construct(self):
        # Left hand side
        circle_color = TEAL
        square_color = GREEN
        circle_color = BLUE
        square_color = RED

        font_size = 72
        c_tex = R"{CC \over CC}"
        s_tex = R"{SS \over SS}"
        frac = Tex(
            fR"{{\text{{Area}}\left( {c_tex} \right) \over \text{{Area}}\left( {s_tex} \right)}}",
            font_size=font_size
        )
        area_words = frac[R"\text{Area}"]
        for part in area_words:
            part.scale(0.75, about_edge=RIGHT).shift(SMALL_BUFF * RIGHT)
        frac.next_to(ORIGIN, LEFT)
        frac.to_edge(UP, LARGE_BUFF)
        circle = Circle()
        circle.set_stroke(circle_color, 3)
        circle.set_fill(circle_color, 0.25)
        square = Square()
        square.set_stroke(square_color, 3)
        square.set_fill(square_color, 0.25)

        circle.replace(frac[c_tex])
        circle.shift(0.05 * UP)
        square.replace(frac[s_tex])
        frac[c_tex].scale(0).set_opacity(0)
        frac[s_tex].scale(0).set_opacity(0)

        self.wait(0.1)
        self.play(
            Write(frac, lag_ratio=1e-1),
            LaggedStart(
                Write(circle),
                Write(square),
                lag_ratio=0.5
            )
        )
        self.wait()

        # Right hand side
        equals = Tex(R"=", font_size=90)
        equals.rotate(90 * DEG)
        equals.next_to(frac, DOWN)
        approx = Tex(R"\approx", font_size=font_size)
        value = DecimalNumber(PI / 4, num_decimal_places=3, font_size=font_size)
        rhs = Tex(
            R"{\pi (1)^2 \over 2 \times 2}",
            font_size=font_size,
            t2c={R"\pi (1)^2": circle_color, R"2 \times 2": square_color}
        )
        rhs.next_to(equals, DOWN)
        approx.next_to(rhs, RIGHT)
        value.next_to(approx, RIGHT)

        self.play(Write(equals), Write(rhs))
        self.wait()
        self.play(Write(approx), FadeIn(value, RIGHT))
        self.wait()

        # Make it three d
        sphere = Sphere()
        sphere.set_color(circle_color, 1)
        sphere.rotate(90 * DEG, RIGHT)
        sphere.replace(circle)
        sphere_mesh = SurfaceMesh(sphere)
        sphere_mesh.set_stroke(WHITE, 1, 0.25)
        sphere_mesh.deactivate_depth_test()
        cube = VCube()
        cube.set_fill(square_color, 0.2)
        cube.set_stroke(square_color, 3)
        cube.deactivate_depth_test()
        cube.rotate(20 * DEG, RIGHT).rotate(0 * DEG, UP)
        cube.replace(square).scale(0.9)

        volume_words = Text("Volume").replicate(2)
        for v_word, a_word in zip(volume_words, area_words):
            v_word.move_to(a_word, RIGHT)

        new_frac = Tex(
            R"{(4/3) \pi (1)^3 \over 2 \times 2 \times 2}",
            t2c={R"(4/3) \pi (1)^3": circle_color, R"2 \times 2 \times 2": square_color},
            font_size=font_size
        )
        new_frac.next_to(equals, DOWN)

        self.play(
            Write(sphere_mesh, lag_ratio=1e-2),
            FadeOut(VGroup(equals, rhs, approx, value)),
            FadeTransform(circle, sphere),
            FadeTransform(square, cube),
            *(
                FadeTransformPieces(a_word, v_word)
                for v_word, a_word in zip(volume_words, area_words)
            )
        )
        self.play(
            Write(equals),
            FadeIn(new_frac, DOWN),
        )
        self.wait()

        # New approx
        value = DecimalNumber((4 / 3) * PI / 8, font_size=font_size, num_decimal_places=3)
        approx = Tex(R"\approx", font_size=font_size)
        approx.next_to(new_frac, RIGHT)
        value.next_to(approx, RIGHT)

        self.play(
            Write(approx),
            FadeIn(value, RIGHT),
        )
