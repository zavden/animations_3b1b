# ==============================================================================
# Scene:      PuzzleOverMobiusDiagram
# Source:     videos/_2024/inscribed_rect/loops.py (lines 2475-2522)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl PuzzleOverMobiusDiagram.py PuzzleOverMobiusDiagram -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/inscribed_rect/helpers.py -----

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



# ----- From _2024/inscribed_rect/loops.py -----

class ConstructKleinBottle(InteractiveScene):
    def construct(self):
        # Add arrow diagram
        square = Square()
        square.set_fill(GREY_E, 1).set_stroke(BLACK, width=0)
        square.set_height(4)

        dr_tri = Polygon(DL, DR, UR)
        dr_tri.match_style(square)
        dr_tri.replace(square)

        mobius_diagram = VGroup(
            dr_tri,
            self.get_tri_arrow(square.get_corner(DL), square.get_corner(DR)),
            self.get_tri_arrow(square.get_corner(DR), square.get_corner(UR)),
            Line(square.get_corner(DL), square.get_corner(UR)).set_stroke(Color("red"), 3)
        )

        mobius_label = Text("Möbius Strip", font_size=60)
        mobius_label.next_to(mobius_diagram, UR)
        mobius_label.shift(DOWN + 0.25 * RIGHT)
        mobius_arrow = Arrow(
            mobius_label.get_bottom(),
            mobius_diagram.get_center() + 0.5 * DR,
            path_arc=-90 * DEG,
            thickness=5
        )
        mobius_arrow.set_z_index(1)

        self.add(mobius_diagram)
        self.play(
            FadeIn(mobius_label),
            FadeIn(mobius_arrow),
        )
        self.wait()

        # Show a reflection
        reflection = mobius_diagram.copy()
        reflection.flip(UR, about_point=square.get_center())
        reflection.shift(UL)
        reflection[1:3].set_color(PINK)

        reflection_label = Text("Reflected\nMöbius Strip", font_size=60)
        reflection_label.next_to(reflection, LEFT, aligned_edge=DOWN)
        reflection_arrow = Arrow(
            reflection_label.get_top(),
            reflection.get_center() + 0.5 * LEFT + 0.25 * UP,
            path_arc=-90 * DEG,
            thickness=5
        )

        self.play(
            LaggedStart(
                TransformMatchingStrings(mobius_label.copy(), reflection_label, run_time=1),
                TransformFromCopy(mobius_diagram, reflection),
                TransformFromCopy(mobius_arrow, reflection_arrow),
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait()

        # Glue along boundary
        glue_label = Text("Glue the boundaries", font_size=36)
        glue_label.next_to(ORIGIN, DOWN, SMALL_BUFF)
        glue_label.rotate(45 * DEG, about_point=ORIGIN)
        glue_label.shift(square.get_center())

        self.play(
            LaggedStart(
                FadeOut(reflection_arrow),
                FadeOut(mobius_arrow),
                reflection.animate.shift(DR),
                reflection_label.animate.scale(0.75).next_to(square, LEFT, MED_SMALL_BUFF),
                mobius_label.animate.scale(0.75).next_to(square, RIGHT, MED_SMALL_BUFF),
            ),
            FadeIn(glue_label, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(glue_label, reflection_label, mobius_label)),
            mobius_diagram[-1].animate.set_stroke(width=0),
            reflection[-1].animate.set_stroke(width=0),
        )

        # Cut along diagonal
        teal_arrows = mobius_diagram[1:3]
        pink_arrows = reflection[1:3]
        yellow_arrows = self.get_tri_arrow(square.get_corner(UL), square.get_corner(DR), color=YELLOW).replicate(2)
        ur_tri = Polygon(DR, UR, UL)
        dl_tri = Polygon(DR, DL, UL)
        for tri in [ur_tri, dl_tri]:
            tri.match_style(square)
            tri.replace(square)

        ur_group = VGroup(ur_tri, teal_arrows[1], pink_arrows[1])
        dl_group = VGroup(dl_tri, teal_arrows[0], pink_arrows[0])

        self.remove(mobius_diagram, reflection)
        self.add(ur_group)
        self.add(dl_group)

        self.play(*(Write(arrow, stroke_color=YELLOW) for arrow in yellow_arrows))
        ur_group.add(yellow_arrows[0])
        dl_group.add(yellow_arrows[1])
        self.play(VGroup(ur_group, dl_group).animate.space_out_submobjects(3))
        self.wait()

        # Flip and glue
        frame = self.frame
        self.play(
            dl_group.animate.next_to(ORIGIN, UP, 0.5),
            ur_group.animate.flip(UR).next_to(ORIGIN, DOWN, 0.5),
            frame.animate.set_height(10),
            run_time=2,
        )
        self.wait()
        self.play(
            ur_group.animate.shift(-ur_tri.get_top()),
            dl_group.animate.shift(-dl_tri.get_bottom()),
        )
        self.play(teal_arrows.animate.set_stroke(width=0).set_fill(opacity=0))

        # Shear back into square
        pre_square = square.copy()
        pre_square.apply_matrix(np.matrix([[1, -1], [0, 1]]).T)
        pre_square.move_to(VGroup(dl_tri, dr_tri), UP)

        trg_yellow_arrows = VGroup(
            self.get_tri_arrow(square.get_corner(DR), square.get_corner(DL), color=YELLOW).flip(RIGHT),
            self.get_tri_arrow(square.get_corner(UL), square.get_corner(UR), color=YELLOW),
        )

        self.remove(ur_tri, dl_tri)
        self.add(pre_square, pink_arrows, yellow_arrows)
        self.play(
            Transform(pre_square, square),
            Transform(yellow_arrows, trg_yellow_arrows),
            pink_arrows[0].animate.move_to(square.get_left()),
            pink_arrows[1].animate.move_to(square.get_right()),
            frame.animate.set_height(8),
            run_time=2
        )
        self.wait()

        # Fold into half tube
        klein_func = self.get_kelin_bottle_func()
        near_smooth = bezier([0, 0.1, 0.9, 1])
        surfaces = Group(
            TexturedSurface(ParametricSurface(func), "KleinBottleTexture")
            for func in [
                square_func,
                tube_func,
                lambda u, v: torus_func(u, 0.5 * v),
                lambda u, v: klein_func(u, 0.5 * near_smooth(v)),
            ]
        )
        for surface in surfaces:
            surface.set_opacity(0.9)
            surface.set_shading(0.3, 0.2, 0)
        square3d, tube, half_torus, half_klein = surfaces
        square3d.replace(square)
        square3d.shift(4 * OUT)
        moving_surface = square3d.copy()

        tube.set_width(square.get_width() / PI)
        tube.set_height(square.get_height(), stretch=True)
        tube.move_to(square3d)

        half_torus.match_depth(tube)
        half_torus.move_to(tube)

        self.play(
            FadeIn(moving_surface, shift=square3d.get_z() * OUT),
            frame.animate.reorient(0, 56, 0, (0.07, 0.52, 2.39), 11.25),
            run_time=3,
        )
        self.play(Transform(moving_surface, tube), run_time=4)
        self.wait()
        self.play(Transform(moving_surface, half_torus, path_arc=PI / 2), run_time=4)
        self.wait()
        self.play(Transform(moving_surface, half_klein), run_time=4)

        # Transition to full Klein Bottle
        klein_diagram = VGroup(pre_square, pink_arrows, yellow_arrows)
        v_upper_bound = 0.85
        self.play(
            UpdateFromAlphaFunc(moving_surface, lambda m, a: m.match_points(
                ParametricSurface(lambda u, v: klein_func(u, interpolate(0.5, 1, a) * near_smooth(v)))
            ).set_opacity(interpolate(0.9, 0.75, a))),
            klein_diagram.animate.set_x(-5),
            frame.animate.reorient(0, 46, 0, (-0.71, -0.11, 1.71), 10.87),
            run_time=8
        )
        self.wait()
        self.play(
            klein_diagram.animate.next_to(moving_surface, LEFT, buff=2),
            frame.animate.reorient(0, 0, 0, (-3.2, 0.03, 0.0), 12.58),
            run_time=4
        )
        self.wait()

    def get_tri_arrow(self, start, end, color=TEAL, stroke_width=3, tip_width=0.35):
        line = Line(start, end)
        line.set_stroke(color, stroke_width)
        tips = ArrowTip().replicate(3)
        tips.set_fill(color)
        tips.set_width(tip_width)
        tips.rotate(line.get_angle())
        for alpha, tip in zip(np.linspace(0.2, 0.8, 3), tips):
            tip.move_to(line.pfp(alpha))

        return VGroup(line, tips)

    def get_kelin_bottle_func(self, width=4, z=4):
        # Test kelin func
        ref_svg = SVGMobject("KleinReference")[0]
        ref_svg.make_smooth(approx=False)
        ref_svg.add_line_to(ref_svg.get_start())
        ref_svg.set_stroke(WHITE, 3)
        ref_svg.set_width(width)
        ref_svg.rotate(PI)
        ref_svg.set_z(4)
        ref_svg.insert_n_curves(100)

        # curve_func = get_quick_loop_func(ref_svg)
        curve_func = ref_svg.quick_point_from_proportion
        radius_func = bezier([1, 1, 0.5, 0.3, 0.3, 0.3, 1.0])
        tan_alpha_func = bezier([1, 1, 0, 0, 0, 0, 1, 1])
        v_alpha_func = squish_rate_func(smooth, 0.25, 0.75)

        def pre_klein_func(u, v):
            dv = 1e-2
            c_point = curve_func(v)
            c_prime = normalize((curve_func(v + dv) - curve_func(v - dv)) / (2 * dv))
            tangent_alpha = tan_alpha_func(v)
            # tangent = interpolate(c_prime, UP if v < 0.5 else DOWN, tangent_alpha)
            tangent = interpolate(c_prime, interpolate(UP, DOWN, v_alpha_func(v)), tangent_alpha)

            perp = normalize(cross(tangent, OUT))
            radius = radius_func(v)

            return c_point + radius * (math.cos(TAU * u) * OUT - math.sin(TAU * u) * perp)

        v_upper_bound = 0.85

        def true_kelin_func(u, v):
            if v <= v_upper_bound:
                return pre_klein_func(u, v)
            else:
                alpha = inverse_interpolate(v_upper_bound, 1, v)
                return interpolate(pre_klein_func(u, v_upper_bound), pre_klein_func(1 - u, 0), alpha)

        return true_kelin_func


class PuzzleOverMobiusDiagram(ConstructKleinBottle):
    def construct(self):
        # Test
        triangle = Polygon(DL, DR, UR)
        triangle.set_fill(GREY_E, 1)
        triangle.set_stroke(WHITE, 0)
        triangle.set_height(4)
        triangle.to_edge(UP, buff=1)

        low_arrow = self.get_tri_arrow(triangle.get_corner(DL), triangle.get_corner(DR), stroke_width=4)
        right_arrow = self.get_tri_arrow(triangle.get_corner(DR), triangle.get_corner(UR), stroke_width=4)
        edge = Line(triangle.get_corner(DL), triangle.get_corner(UR))
        edge.set_stroke(Color("red"), 3)

        self.add(triangle, edge, low_arrow, right_arrow)
        self.wait()

        low_arrow.save_state()
        self.play(
            triangle.animate.set_opacity(0.25),
            edge.animate.set_opacity(0.1),
            low_arrow.animate.rotate(90 * DEG).next_to(right_arrow, RIGHT)
        )
        self.wait()
        self.play(low_arrow.animate.move_to(right_arrow))
        self.play(low_arrow.animate.next_to(right_arrow, RIGHT))
        self.play(
            Restore(low_arrow),
            triangle.animate.set_fill(opacity=1),
            edge.animate.set_stroke(opacity=1),
        )

        # Show the dots
        dots = GlowDot(color=BLUE, radius=0.25, glow_factor=1.5).replicate(2)
        top_dot = dots[0].copy()
        top_dot.move_to(right_arrow.get_top())
        for _ in range(3):
            dots[0].move_to(low_arrow.get_left())
            dots[1].move_to(right_arrow.get_bottom())
            self.add(top_dot)
            self.wait(1 / 30)
            self.remove(top_dot)
            self.play(
                dots[0].animate.move_to(low_arrow.get_right()),
                dots[1].animate.move_to(right_arrow.get_top()),
                run_time=3,
                rate_func=linear
            )
