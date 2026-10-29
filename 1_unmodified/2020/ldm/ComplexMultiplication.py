# ==============================================================================
# Scene:      ComplexMultiplication
# Source:     videos/_2020/ldm.py (lines 485-602)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexMultiplication.py ComplexMultiplication -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexMultiplication(Scene):
    def construct(self):
        # Add plane
        plane = ComplexPlane()
        plane.add_coordinates()

        z = complex(2, 1)
        z_dot = Dot(color=PINK)
        z_dot.move_to(plane.n2p(z))
        z_label = OldTex("z")
        z_label.next_to(z_dot, UR, buff=0.5 * SMALL_BUFF)
        z_label.match_color(z_dot)

        self.add(plane)
        self.add(z_dot)
        self.add(z_label)

        # Show 1
        one_vect = Vector(RIGHT)
        one_vect.set_color(YELLOW)
        one_vect.target = Vector(plane.n2p(z))
        one_vect.target.match_style(one_vect)

        z_rhs = OldTex("=", "z \\cdot 1")
        z_rhs[1].match_color(one_vect)
        z_rhs.next_to(z_label, RIGHT, 1.5 * SMALL_BUFF, aligned_edge=DOWN)
        z_rhs.set_stroke(BLACK, 3, background=True)

        one_label, i_label = [l for l in plane.coordinate_labels if l.get_value() == 1]

        self.play(GrowArrow(one_vect))
        self.wait()
        self.add(one_vect, z_dot)
        self.play(
            MoveToTarget(one_vect),
            TransformFromCopy(one_label, z_rhs),
        )
        self.wait()

        # Show i
        i_vect = Vector(UP, color=GREEN)
        zi_point = plane.n2p(z * complex(0, 1))
        i_vect.target = Vector(zi_point)
        i_vect.target.match_style(i_vect)
        i_vect_label = OldTex("z \\cdot i")
        i_vect_label.match_color(i_vect)
        i_vect_label.set_stroke(BLACK, 3, background=True)
        i_vect_label.next_to(zi_point, UL, SMALL_BUFF)

        self.play(GrowArrow(i_vect))
        self.wait()
        self.play(
            MoveToTarget(i_vect),
            TransformFromCopy(i_label, i_vect_label),
            run_time=1,
        )
        self.wait()

        self.play(
            TransformFromCopy(one_vect, i_vect.target, path_arc=-90 * DEGREES),
        )
        self.wait()

        # Transform plane
        plane.generate_target()
        for mob in plane.target.family_members_with_points():
            if isinstance(mob, Line):
                mob.set_stroke(GREY, opacity=0.5)
        new_plane = ComplexPlane(faded_line_ratio=0)

        self.remove(plane)
        self.add(plane, new_plane, *self.mobjects)

        new_plane.generate_target()
        new_plane.target.apply_complex_function(lambda w, z=z: w * z)

        self.play(
            MoveToTarget(plane),
            MoveToTarget(new_plane),
            run_time=6,
            rate_func=there_and_back_with_pause
        )
        self.wait()

        # Show Example Point
        w = complex(2, -1)
        w_dot = Dot(plane.n2p(w), color=WHITE)
        one_vects = VGroup(*[Vector(RIGHT) for x in range(2)])
        one_vects.arrange(RIGHT, buff=0)
        one_vects.move_to(plane.n2p(0), LEFT)
        one_vects.set_color(YELLOW)
        new_i_vect = Vector(DOWN)
        new_i_vect.move_to(plane.n2p(2), UP)
        new_i_vect.set_color(GREEN)
        vects = VGroup(*one_vects, new_i_vect)
        vects.set_opacity(0.8)

        w_group = VGroup(*vects, w_dot)
        w_group.target = VGroup(
            one_vect.copy().set_opacity(0.8),
            one_vect.copy().shift(plane.n2p(z)).set_opacity(0.8),
            i_vect.copy().rotate(PI, about_point=ORIGIN).shift(2 * plane.n2p(z)).set_opacity(0.8),
            Dot(plane.n2p(w * z), color=WHITE)
        )

        self.play(FadeInFromLarge(w_dot))
        self.wait()
        self.play(ShowCreation(vects))
        self.wait()

        self.play(
            MoveToTarget(plane),
            MoveToTarget(new_plane),
            MoveToTarget(w_group),
            run_time=2,
            path_arc=np.log(z).imag,
        )
        self.wait()
