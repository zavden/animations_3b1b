# ==============================================================================
# Scene:      SequenceOfSpheres
# Source:     videos/_2018/sphere_area.py (lines 2218-2318)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SequenceOfSpheres.py SequenceOfSpheres -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Cylinder(Sphere):
    """
    Inherits from sphere so as to be as aligned as possible
    for transformations
    """

    def func(self, u, v):
        return np.array([
            np.cos(v),
            np.sin(v),
            np.cos(u)
        ])


class UnwrappedCylinder(Cylinder):
    def func(self, u, v):
        return np.array([
            v - PI,
            -self.radius,
            np.cos(u)
        ])


class SphereCylinderScene(SpecialThreeDScene):
    CONFIG = {
        "cap_config": {
            "stroke_width": 1,
            "stroke_color": WHITE,
            "fill_color": BLUE_D,
            "fill_opacity": 1,
        }
    }

    def get_cylinder(self, **kwargs):
        config = merge_dicts_recursively(self.sphere_config, kwargs)
        return Cylinder(**config)

    def get_cylinder_caps(self):
        R = self.sphere_config["radius"]
        caps = VGroup(*[
            Circle(
                radius=R,
                **self.cap_config,
            ).shift(R * vect)
            for vect in [IN, OUT]
        ])
        caps.set_shade_in_3d(True)
        return caps

    def get_unwrapped_cylinder(self):
        return UnwrappedCylinder(**self.sphere_config)

    def get_xy_plane(self):
        pass

    def get_ghost_surface(self, surface):
        result = surface.copy()
        result.set_fill(BLUE_E, opacity=0.5)
        result.set_stroke(WHITE, width=0.5, opacity=0.5)
        return result

    def project_point(self, point):
        radius = self.sphere_config["radius"]
        result = np.array(point)
        result[:2] = normalize(result[:2]) * radius
        return result

    def project_mobject(self, mobject):
        return mobject.apply_function(self.project_point)


class SequenceOfSpheres(SphereCylinderScene):
    def construct(self):
        n_shapes = 4
        spheres, cylinders = groups = VGroup(*[
            VGroup(*[
                func(resolution=(n, 2 * n))
                for k in range(1, n_shapes + 1)
                for n in [3 * (2**k)]
            ])
            for func in [self.get_sphere, self.get_cylinder]
        ])
        groups.scale(0.5)
        for group in groups:
            for shape in group:
                for piece in shape:
                    piece.make_jagged()
                shape.set_stroke(width=0)

        for group in groups:
            group.add(self.get_oriented_tex("?").scale(2))
            group.arrange(RIGHT, buff=LARGE_BUFF)
        groups.arrange(IN, buff=1.5)

        all_equals = VGroup()
        for sphere, cylinder in zip(spheres, cylinders):
            equals = self.get_oriented_tex("=")
            equals.scale(1.5)
            equals.rotate(90 * DEGREES, UP)
            equals.move_to(interpolate(
                sphere.get_nadir(), cylinder.get_zenith(), 0.5
            ))
            all_equals.add(equals)
        all_equals.remove(all_equals[-1])

        arrow_groups = VGroup()
        for group in groups:
            arrow_group = VGroup()
            for m1, m2 in zip(group, group[1:]):
                arrow = self.get_oriented_tex("\\rightarrow")
                arrow.move_to(interpolate(
                    m1.get_right(), m2.get_left(), 0.5
                ))
                arrow_group.add(arrow)
            arrow_groups.add(arrow_group)

        q_marks = VGroup(*[
            group[-1]
            for group in groups
        ])
        final_arrows = VGroup(
            arrow_groups[0][-1],
            arrow_groups[1][-1],
        )
        for arrow in final_arrows:
            dots = self.get_oriented_tex("\\dots")
            dots.next_to(arrow, RIGHT, SMALL_BUFF)
            arrow.add(dots)
        q_marks.shift(MED_LARGE_BUFF * RIGHT)
        tilted_final_arrows = VGroup(
            final_arrows[0].copy().rotate(
                -45 * DEGREES, axis=DOWN
            ).shift(0.75 * IN),
            final_arrows[1].copy().rotate(
                45 * DEGREES, axis=DOWN
            ).shift(0.75 * OUT),
        )
        final_q_mark = q_marks[0].copy()
        final_q_mark.move_to(q_marks)

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-90 * DEGREES,
        )

        for i in range(n_shapes):
            anims = [
                FadeIn(spheres[i], LEFT),
                FadeIn(cylinders[i], LEFT),
            ]
            if i > 0:
                anims += [
                    Write(arrow_group[i - 1])
                    for arrow_group in arrow_groups
                ]
            self.play(*anims, run_time=1)
            self.play(GrowFromCenter(all_equals[i]))
        self.play(
            FadeIn(q_marks, LEFT),
            Write(final_arrows)
        )
        self.wait()
        self.play(
            Transform(final_arrows, tilted_final_arrows),
            Transform(q_marks, VGroup(final_q_mark)),
        )
        self.wait()

    def get_oriented_tex(self, tex):
        result = OldTex(tex)
        result.rotate(90 * DEGREES, RIGHT)
        return result
