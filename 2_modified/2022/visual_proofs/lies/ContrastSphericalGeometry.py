# ==============================================================================
# Scene:      ContrastSphericalGeometry
# Source:     videos/_2022/visual_proofs/lies.py (lines 1066-1268)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ContrastSphericalGeometry.py ContrastSphericalGeometry -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - VMobject().pointwise_become_partial(...).reverse_points() -> with .set_subpath_range() in between: pointwise_become_partial does not refresh subpath_range (a manimgl bug, vectorized_mobject.py:1308) and reverse_points gave IndexError
# ==============================================================================

from manim_imports_ext import *

class ContrastSphericalGeometry(InteractiveScene):
    def construct(self):
        # Titles
        titles = VGroup(
            Text("Spherical geometry"),
            Text("Euclidean geometry"),
        )
        for title, v in zip(titles, [LEFT, RIGHT]):
            title.move_to(FRAME_WIDTH * v / 4)
            title.to_edge(UP)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(WHITE, 1)
        self.add(v_line, titles)

        # Setup sphere
        sphere = TexturedSurface(Sphere(radius=1.5), "EarthTextureMap", "NightEarthTextureMap")
        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(GREY_C, 1, opacity=0.5)
        sphere_group = Group(sphere, mesh)
        sphere_group.rotate(80 * DEGREES, LEFT)
        sphere_group.rotate(-3 * DEGREES, OUT)
        sphere_axis = mesh[0].get_end() - sphere.get_center()
        sphere_group.move_to(FRAME_WIDTH * LEFT / 4)
        sphere_group.to_edge(DOWN, buff=0.75)
        self.add(sphere_group)

        # Flat shapes
        shapes = VGroup(
            Polygon(RIGHT, UP, DL).set_fill(BLACK, 1),
            Square().set_fill(BLUE_C, 1),
            Circle().set_fill(BLUE_E, 1),
            RegularPolygon(5).set_fill(GREY_BROWN, 1)
        )
        shapes.set_stroke(WHITE, 2)
        for shape in shapes:
            shape.set_height(1)
        shapes.arrange_in_grid()
        shapes.match_x(titles[1])
        shapes.to_edge(DOWN)

        pre_tri = shapes[0].copy()
        pre_tri.scale(2.5)
        pre_tri.move_to(shapes).align_to(sphere, DOWN)
        pre_tri_arcs, pre_tri_angle_labels = self.get_flat_angle_labels(pre_tri)
        shift_line, new_arcs, new_labels = self.get_aligned_angle_labels(
            pre_tri, pre_tri_arcs, pre_tri_angle_labels
        )

        # Setup spherical triangle
        t2c = {
            "\\alpha": BLUE_B,
            "\\beta": BLUE_C,
            "\\gamma": BLUE_D,
        }
        kw = dict(tex_to_color_map=t2c)
        sph_tri = VGroup(
            VMobject().pointwise_become_partial(mesh[16], 0.5, 1.0),
            # CHANGE: pointwise_become_partial leaves subpath_range out of date (set_points(refresh=False)) and reverse_points fails with IndexError; it is recomputed beforehand
            VMobject().pointwise_become_partial(mesh[19], 0.5, 1.0).set_subpath_range().reverse_points(),
            # CHANGE: ditto: set_subpath_range() before reverse_points
            VMobject().pointwise_become_partial(mesh[26], 16 / 20, 19 / 20).set_subpath_range().reverse_points(),
        )
        sph_tri.set_stroke(BLUE, 3)
        sph_tri_angle_labels = Tex("\\alpha\\beta\\gamma", font_size=30, **kw)
        sph_tri_angle_labels.set_backstroke()
        for label, curve in zip(sph_tri_angle_labels, sph_tri):
            label.curve = curve
            label.add_updater(lambda l: l.move_to(l.curve.get_end()))
            label.add_updater(lambda l: l.shift(0.2 * normalize(sph_tri.get_center() - l.curve.get_end())))

        sph_tri.deactivate_depth_test()

        # Equations
        angle_equations = VGroup(
            Tex("\\alpha + \\beta + \\gamma > 180^\\circ", **kw),
            Tex("\\alpha + \\beta + \\gamma = 180^\\circ", **kw),
        )
        for eq, title in zip(angle_equations, titles):
            eq.next_to(title, DOWN, buff=1.5)

        # Write triangles
        sph_tri_angle_labels.suspend_updating()
        self.play(
            LaggedStartMap(Write, VGroup(
                pre_tri, pre_tri_arcs, pre_tri_angle_labels,
                sph_tri, sph_tri_angle_labels,
            )),
            *(FadeIn(eq, 0.25 * DOWN) for eq in angle_equations)
        )
        sph_tri_angle_labels.resume_updating()
        sphere_group.add(sph_tri, sph_tri_angle_labels)
        sph_tri.deactivate_depth_test()
        self.add(sphere_group)
        self.play()

        # Justify euclidean case
        self.play(
            FadeIn(shift_line, shift=shift_line.shift_vect),
            Rotate(sphere_group, -30 * DEGREES, axis=sphere_axis, run_time=2)
        )
        for i in (0, 1):
            self.play(
                TransformFromCopy(pre_tri_arcs[i + 1], new_arcs[i]),
                TransformFromCopy(pre_tri_angle_labels[i + 1], new_labels[i]),
            )
        self.wait()

        pre_tri_group = VGroup(
            pre_tri, pre_tri_arcs, pre_tri_angle_labels,
            shift_line, new_arcs, new_labels
        )

        # Write area formulas
        area_formulas = VGroup(
            Tex("\\text{Area}(\\Delta) = (\\alpha + \\beta + \\gamma - \\pi) R^2", **kw),
            Tex("\\text{Area}(\\Delta) = \\frac{1}{2} bh")
        )
        for title, formula in zip(titles, area_formulas):
            formula.move_to(title).shift(1.5 * DOWN)

        self.play(
            FadeIn(area_formulas, 0.5 * DOWN),
            angle_equations.animate.shift(0.75 * DOWN)
        )

        # Mention Gaussian Curvature
        curvature_words = VGroup(
            OldTexText("Gaussian curvature > 0", color=GREEN_B),
            OldTexText("Gaussian curvature = 0", color=YELLOW),
        )
        for words, eq in zip(curvature_words, angle_equations):
            words.next_to(eq, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(curvature_words, 0.7 * DOWN),
            sphere_group.animate.scale(0.7, about_edge=DOWN),
            pre_tri_group.animate.scale(0.7, about_edge=DOWN),
        )
        self.wait()

        # Try unraveling sphere
        unwrapped = TexturedSurface(Surface(), "EarthTextureMap", "NightEarthTextureMap")
        unwrapped.set_height(2)
        unwrapped.set_width(TAU, stretch=True)
        unwrapped.set_width(FRAME_WIDTH / 2 - 1)
        unwrapped.next_to(titles[1], DOWN, LARGE_BUFF)

        loss_words = Text("Some geometric information\nmust be lost")
        loss_words.set_color(RED)
        loss_words.set_max_width(unwrapped.get_width())
        loss_words.next_to(unwrapped, DOWN, MED_LARGE_BUFF)

        self.play(
            LaggedStart(*(
                FadeOut(mob, RIGHT)
                for mob in [area_formulas[1], angle_equations[1], curvature_words[1], pre_tri_group]
            )),
            TransformFromCopy(sphere, unwrapped, run_time=2)
        )
        self.play(Write(loss_words))
        self.wait(2)

    def get_flat_angle_labels(self, tri):
        arcs = VGroup()
        for v1, v2, v3 in adjacent_n_tuples(tri.get_vertices(), 3):
            a1 = angle_of_vector(v2 - v1)
            a2 = angle_of_vector(v3 - v2)
            arc = Arc(
                start_angle=a2,
                angle=PI - (a2 - a1) % PI,
                radius=0.2
            )
            arc.shift(v2)
            arcs.add(arc)

        labels = Tex("\\alpha \\beta \\gamma", font_size=30)
        for label, arc in zip(labels, arcs):
            vect = normalize(arc.pfp(0.5) - midpoint(arc.get_start(), arc.get_end()))
            label.move_to(arc.pfp(0.5))
            label.shift(0.25 * vect)

        result = VGroup(arcs, labels)
        for group in result:
            group.set_submobject_colors_by_gradient(BLUE_B, BLUE_C, BLUE_D)
        return result

    def get_aligned_angle_labels(self, tri, arcs, labels):
        verts = tri.get_vertices()
        line = Line(verts[0], verts[2])
        line.set_stroke(GREY_B, 2)

        vect1 = verts[1] - verts[2]
        vect2 = verts[1] - verts[0]
        line.shift_vect = (vect1 + vect2) / 2
        line.shift(line.shift_vect)

        new_arcs = arcs[1:3].copy()
        new_labels = labels[1:3].copy()
        VGroup(new_arcs[0], new_labels[0]).rotate(PI, about_point=midpoint(verts[1], verts[2]))
        VGroup(new_arcs[1], new_labels[1]).rotate(PI, about_point=midpoint(verts[1], verts[0]))
        for label in new_labels:
            label.rotate(PI)

        return VGroup(line, new_arcs, new_labels)
