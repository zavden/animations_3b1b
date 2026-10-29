# ==============================================================================
# Scene:      ShowProjection
# Source:     videos/_2018/sphere_area.py (lines 673-1052)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowProjection.py ShowProjection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - GL set_points([]) cannot broadcast an empty list; clear_points() empties the line
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


class ShowProjection(SphereCylinderScene):
    CONFIG = {
        # "default_angled_camera_position": {
        #     "theta": -155 * DEGREES,
        # }
    }

    def construct(self):
        self.setup_shapes()
        self.show_many_tiny_rectangles()
        self.project_all_rectangles()
        self.focus_on_one()
        self.label_sides()
        self.show_length_scaled_up()
        self.show_height_scaled_down()

    def setup_shapes(self):
        self.sphere = self.get_sphere()
        self.cylinder = self.get_cylinder()
        self.ghost_sphere = self.get_ghost_surface(self.sphere)
        self.ghost_sphere.scale(0.99)
        self.ghost_cylinder = self.get_ghost_surface(self.cylinder)
        self.ghost_cylinder.set_stroke(width=0)

        self.add(self.get_axes())
        self.set_camera_to_default_position()
        self.begin_ambient_camera_rotation()

    def show_many_tiny_rectangles(self):
        ghost_sphere = self.ghost_sphere
        pieces = self.sphere.copy()
        random.shuffle(pieces.submobjects)
        for piece in pieces:
            piece.save_state()
        pieces.space_out_submobjects(2)
        pieces.fade(1)

        self.add(ghost_sphere)
        self.play(LaggedStartMap(Restore, pieces))
        self.wait()

        self.pieces = pieces

    def project_all_rectangles(self):
        pieces = self.pieces
        for piece in pieces:
            piece.save_state()
            piece.generate_target()
            self.project_mobject(piece.target)
            piece.target.set_fill(opacity=0.5)

        example_group = self.get_example_group([1, -1, 2])
        proj_lines = example_group[1]
        self.example_group = example_group

        self.play(*map(ShowCreation, proj_lines))
        self.play(
            LaggedStartMap(MoveToTarget, pieces),
        )
        self.wait()

    def focus_on_one(self):
        ghost_cylinder = self.ghost_cylinder
        pieces = self.pieces

        example_group = self.example_group
        original_rect, rect_proj_lines, rect = example_group

        equation = self.get_equation(rect)
        lhs, equals, rhs = equation[:3]
        lhs.save_state()
        rhs.save_state()

        self.play(
            FadeIn(ghost_cylinder),
            FadeOut(pieces),
            FadeIn(original_rect),
        )
        self.play(TransformFromCopy(original_rect, rect))
        self.wait()
        self.add_fixed_in_frame_mobjects(lhs, equals, rhs)
        self.move_fixed_in_frame_mob_to_unfixed_mob(lhs, original_rect)
        self.move_fixed_in_frame_mob_to_unfixed_mob(rhs, rect)
        self.play(
            Restore(lhs),
            Restore(rhs),
            FadeInFromDown(equals),
        )
        self.wait(5)

        self.equation = equation
        self.example_group = example_group

    def label_sides(self):
        sphere = self.sphere
        equation = self.equation
        w_brace, h_brace = equation.braces
        width_label, height_label = equation.labels

        u_values, v_values = sphere.get_u_values_and_v_values()
        radius = sphere.radius
        lat_lines = VGroup(*[
            ParametricCurve(
                lambda t: radius * sphere.func(u, t),
                t_min=sphere.v_min,
                t_max=sphere.v_max,
            )
            for u in u_values
        ])
        lon_lines = VGroup(*[
            ParametricCurve(
                lambda t: radius * sphere.func(t, v),
                t_min=sphere.u_min,
                t_max=sphere.u_max,
            )
            for v in v_values
        ])
        for lines in lat_lines, lon_lines:
            for line in lines:
                line.add(DashedVMobject(line, spacing=-1))
                # CHANGE: GL set_points([]) cannot broadcast an empty list; clear_points() empties the line
                line.clear_points()
                line.set_stroke(width=2)
            lines.set_shade_in_3d(True)
        lat_lines.set_color(RED)
        lon_lines.set_color(PINK)

        self.play(
            *map(ShowCreationThenDestruction, lat_lines),
            run_time=2
        )
        self.add_fixed_in_frame_mobjects(w_brace, width_label)
        self.play(
            GrowFromCenter(w_brace),
            Write(width_label),
        )
        self.wait()
        self.play(
            *map(ShowCreationThenDestruction, lon_lines),
            run_time=2
        )
        self.add_fixed_in_frame_mobjects(h_brace, height_label)
        self.play(
            GrowFromCenter(h_brace),
            Write(height_label),
        )
        self.wait(2)

    def show_length_scaled_up(self):
        ghost_sphere = self.ghost_sphere
        example_group = self.example_group
        equation = self.equation
        equation.save_state()
        new_example_groups = [
            self.get_example_group([1, -1, z])
            for z in [6, 0.25]
        ]
        r1, lines, r2 = example_group

        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=65 * DEGREES,
            theta=-80 * DEGREES,
            added_anims=[
                ghost_sphere.set_stroke, {"opacity": 0.1},
                lines.set_stroke, {"width": 3},
            ]
        )
        for eg in new_example_groups:
            eg[1].set_stroke(width=3)
        self.show_length_stretch_of_rect(example_group)
        all_example_groups = [example_group, *new_example_groups]
        for eg1, eg2 in zip(all_example_groups, all_example_groups[1:]):
            if eg1 is new_example_groups[0]:
                self.move_camera(
                    phi=70 * DEGREES,
                    theta=-110 * DEGREES
                )
            self.remove(eg1)
            self.play(
                ReplacementTransform(eg1.deepcopy(), eg2),
                Transform(
                    equation,
                    self.get_equation(eg2[2])
                )
            )
            if eg1 is example_group:
                self.move_camera(
                    phi=0,
                    theta=-90 * DEGREES,
                )
            self.show_length_stretch_of_rect(eg2)
        self.play(
            ReplacementTransform(all_example_groups[-1], example_group),
            Restore(equation)
        )

    def show_length_stretch_of_rect(self, example_group):
        s_rect, proj_lines, c_rect = example_group
        rects = VGroup(s_rect, c_rect)
        line1, line2 = lines = VGroup(*[
            Line(m.get_anchors()[1], m.get_anchors()[2])
            for m in rects
        ])
        lines.set_stroke(YELLOW, 5)
        lines.set_shade_in_3d(True)
        proj_lines_to_fade = VGroup(
            proj_lines[0],
            proj_lines[3],
        )
        self.play(
            FadeIn(lines[0]),
            FadeOut(rects),
            FadeOut(proj_lines_to_fade)
        )
        for x in range(3):
            anims = []
            if lines[1] in self.mobjects:
                anims.append(FadeOut(lines[1]))
            self.play(
                TransformFromCopy(lines[0], lines[1]),
                *anims
            )
        self.play(
            FadeOut(lines),
            FadeIn(rects),
            FadeIn(proj_lines_to_fade),
        )
        self.remove(rects, proj_lines_to_fade)
        self.add(example_group)

    def show_height_scaled_down(self):
        ghost_sphere = self.ghost_sphere
        ghost_cylinder = self.ghost_cylinder
        example_group = self.example_group
        equation = self.equation
        r1, lines, r2 = example_group
        to_fade = VGroup(*[
            mob
            for mob in it.chain(ghost_sphere, ghost_cylinder)
            if np.dot(mob.get_center(), [1, 1, 0]) < 0
        ])
        to_fade.save_state()

        new_example_groups = [
            self.get_example_group([1, -1, z])
            for z in [6, 0.25]
        ]
        for eg in new_example_groups:
            eg[::2].set_stroke(YELLOW, 2)
            eg.set_stroke(width=1)
        all_example_groups = VGroup(example_group, *new_example_groups)

        self.play(
            to_fade.shift, IN,
            to_fade.fade, 1,
            remover=True
        )
        self.move_camera(
            phi=85 * DEGREES,
            theta=-135 * DEGREES,
            added_anims=[
                lines.set_stroke, {"width": 1},
                r1.set_stroke, YELLOW, 2, 1,
                r2.set_stroke, YELLOW, 2, 1,
            ]
        )
        self.show_shadow(example_group)
        for eg1, eg2 in zip(all_example_groups, all_example_groups[1:]):
            self.remove(*eg1.get_family())
            self.play(
                ReplacementTransform(eg1.deepcopy(), eg2),
                Transform(
                    equation,
                    self.get_equation(eg2[2])
                )
            )
            self.show_shadow(eg2)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-115 * DEGREES,
            added_anims=[
                ReplacementTransform(
                    all_example_groups[-1],
                    example_group,
                ),
                Restore(equation),
            ]
        )
        self.begin_ambient_camera_rotation()
        self.play(Restore(to_fade))
        self.wait(5)

    def show_shadow(self, example_group):
        s_rect, lines, c_rect = example_group
        for x in range(3):
            self.play(TransformFromCopy(s_rect, c_rect))

    #
    def get_projection_lines(self, piece):
        result = VGroup()
        radius = self.sphere_config["radius"]
        for corner in piece.get_anchors()[:-1]:
            start = np.array(corner)
            end = np.array(corner)
            start[:2] = np.zeros(2)
            end[:2] = (radius + 0.03) * normalize(end[:2])
            kwargs = {
                "color": YELLOW,
                "stroke_width": 0.5,
            }
            result.add(VGroup(*[
                Line(p1, p2, **kwargs)
                for p1, p2 in [(start, corner), (corner, end)]
            ]))
        result.set_shade_in_3d(True)
        return result

    def get_equation(self, rect):
        length = get_norm(rect.get_anchors()[1] - rect.get_anchors()[0])
        height = get_norm(rect.get_anchors()[2] - rect.get_anchors()[1])
        lhs = Rectangle(width=length, height=height)
        rhs = Rectangle(width=height, height=length)
        eq_rects = VGroup(lhs, rhs)
        eq_rects.set_stroke(width=0)
        eq_rects.set_fill(YELLOW, 1)
        eq_rects.scale(2)
        equals = OldTex("=")
        equation = VGroup(lhs, equals, rhs)
        equation.arrange(RIGHT)
        equation.to_corner(UR)

        brace = Brace(Line(ORIGIN, 0.5 * RIGHT), DOWN)
        w_brace = brace.copy().match_width(lhs, stretch=True)
        h_brace = brace.copy().rotate(-90 * DEGREES)
        h_brace.match_height(lhs, stretch=True)
        w_brace.next_to(lhs, DOWN, buff=SMALL_BUFF)
        h_brace.next_to(lhs, LEFT, buff=SMALL_BUFF)
        braces = VGroup(w_brace, h_brace)

        width_label = OldTexText("Width")
        height_label = OldTexText("Height")
        labels = VGroup(width_label, height_label)
        labels.scale(0.75)
        width_label.next_to(w_brace, DOWN, SMALL_BUFF)
        height_label.next_to(h_brace, LEFT, SMALL_BUFF)

        equation.braces = braces
        equation.labels = labels
        equation.add(braces, labels)

        return equation

    def move_fixed_in_frame_mob_to_unfixed_mob(self, m1, m2):
        phi = self.camera.phi_tracker.get_value()
        theta = self.camera.theta_tracker.get_value()
        target = m2.get_center()
        target = rotate_vector(target, -theta - 90 * DEGREES, OUT)
        target = rotate_vector(target, -phi, RIGHT)

        m1.move_to(target)
        m1.scale(0.1)
        m1.shift(SMALL_BUFF * UR)
        return m1

    def get_example_group(self, vect):
        pieces = self.pieces
        rect = pieces[np.argmax([
            np.dot(r.saved_state.get_center(), vect)
            for r in pieces
        ])].saved_state.copy()
        rect_proj_lines = self.get_projection_lines(rect)
        rect.set_fill(YELLOW, 1)
        original_rect = rect.copy()
        self.project_mobject(rect)
        rect.shift(
            0.001 * np.array([*rect.get_center()[:2], 0])
        )
        result = VGroup(original_rect, rect_proj_lines, rect)
        result.set_shade_in_3d(True)
        return result
