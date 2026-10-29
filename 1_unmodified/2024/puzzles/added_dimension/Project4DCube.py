# ==============================================================================
# Scene:      Project4DCube
# Source:     videos/_2024/puzzles/added_dimension.py (lines 810-1190)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Project4DCube.py Project4DCube -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Project3DCube(InteractiveScene):
    def construct(self):
        # Set axes
        frame = self.frame
        light_source = self.camera.light_source

        frame.reorient(28, 68, 0, (0.99, 0.63, 0.66), 2.89)
        light_source.move_to([3, 5, 7])

        axes = ThreeDAxes(
            (-3, 3), (-3, 3), (-3, 3),
            axis_config=dict(tick_size=0.05)
        )
        axes.set_stroke(GREY_A, 1)
        plane = NumberPlane((-3, 3), (-3, 3))
        plane.axes.set_stroke(GREY_A, 1)
        plane.background_lines.set_stroke(BLUE_E, 0.5)
        plane.faded_lines.set_stroke(BLUE_E, 0.5, 0.25)

        self.add(plane, axes)

        # Add cube
        vertices = np.array(list(it.product(*3 * [[0, 1]])))
        vert_dots = DotCloud(vertices)
        vert_dots.make_3d()
        vert_dots.set_radius(0.025)
        vert_dots.set_color(TEAL)

        cube_shell = VGroup(
            Line(vertices[i], vertices[j])
            for i, p1 in enumerate(vertices)
            for j, p2 in enumerate(vertices[i + 1:], start=i + 1)
            if get_norm(p2 - p1) == 1
        )
        cube_shell.set_stroke(YELLOW, 1)
        cube_shell.set_anti_alias_width(1)
        cube_shell.set_width(1)
        cube_shell.move_to(ORIGIN, [-1, -1, -1])

        self.play(Write(cube_shell, lag_ratio=0.1, run_time=2))
        self.wait()

        # Show the coordinates
        labels = VGroup()
        for vert in vertices:
            coords = vert.astype(int)
            label = Tex(str(tuple(coords)), font_size=12)
            label.next_to(vert, DR, buff=0.05)
            label.rotate(45 * DEGREES, RIGHT, about_point=vert)
            label.set_backstroke(BLACK, 2)
            labels.add(label)

        self.play(
            LaggedStartMap(FadeIn, labels),
            FadeIn(vert_dots),
            frame.animate.reorient(10, 61, 0, (0.9, 0.51, 0.48), 2.44),
            run_time=3,
        )
        self.wait(note="Talk through the coordinates")

        # Show base and top square
        edges = VGroup(*cube_shell)
        edges.sort(lambda p: p[2])

        self.play(
            edges[4:].animate.set_stroke(width=0.5, opacity=0.25),
            labels[1::2].animate.set_opacity(0.1)
        )
        self.wait()
        self.play(
            edges[8:].animate.set_stroke(width=2, opacity=1),
            labels[1::2].animate.set_opacity(1),
            edges[:4].animate.set_stroke(width=0.5, opacity=0.25),
            labels[0::2].animate.set_opacity(0.1)
        )
        self.wait()
        self.play(
            edges.animate.set_stroke(width=1, opacity=1),
            labels.animate.set_opacity(1)
        )

        self.play(FadeOut(labels))

        # Orient to look down the corner
        self.play(frame.animate.reorient(135.795, 55.795, 0, (-0.02, -0.08, 0.05), 3.61), run_time=4)
        self.wait(2, note="Take a moment to look down the corner")
        self.play(frame.animate.reorient(50, 68, 0, (-0.46, 0.29, 0.23), 3.45), run_time=4)

        # Show the flat projection
        diag_vect = Vector([1, 1, 1], thickness=2)
        diag_vect.set_perpendicular_to_camera(frame)
        diag_label = labels[-1].copy()

        proj_mat = self.construct_proj_matrix()
        perp_plane = Square3D().set_width(20)
        perp_plane.set_color(GREY_E, 0.5)
        perp_plane.apply_matrix(proj_mat)

        proj_cube_shell = cube_shell.copy().apply_matrix(proj_mat)
        proj_vert_dots = vert_dots.copy().apply_matrix(proj_mat)

        self.play(
            GrowArrow(diag_vect),
            FadeIn(diag_label, shift=np.ones(3)),
            cube_shell.animate.set_stroke(opacity=0.25),
        )
        self.wait()
        self.play(
            TransformFromCopy(cube_shell, proj_cube_shell),
            TransformFromCopy(vert_dots, proj_vert_dots),
        )

        self.wait(10, note="Talk through projection")
        frame.save_state()
        self.play(
            frame.animate.reorient(134.75, 54.47, 0, (-0.46, 0.29, 0.23), 3.45).set_field_of_view(1 * DEGREES),
            run_time=4
        )
        self.wait()
        self.play(Restore(frame, run_time=3))
        self.wait()

        # Project more cubes down
        cube_grid = VGroup(
            cube_shell.copy().shift(vect)
            for vect in it.product(*3 * [[0, 1, 2]])
        )
        cube_grid.remove(cube_grid[0])
        proj_cube_grid = cube_grid.copy().apply_matrix(proj_mat)
        proj_cube_grid.set_stroke(YELLOW, 2, 0.5)

        ghost_cube = cube_shell.copy().set_opacity(0)
        self.play(
            LaggedStart(
                (TransformFromCopy(ghost_cube, new_cube)
                for new_cube in cube_grid),
                lag_ratio=0.05,
            ),
            frame.animate.reorient(40, 72, 0, (1.25, 1.69, 0.99), 5.10),
            run_time=5
        )
        self.wait()
        self.play(
            TransformFromCopy(cube_grid, proj_cube_grid),
            frame.animate.reorient(60, 68, 0, (0.81, 1.09, 0.94), 5.36),
            run_time=3
        )
        self.wait(note="Any commentary?")
        self.play(
            FadeOut(cube_grid),
            FadeOut(proj_cube_grid),
            FadeOut(diag_label),
            FadeOut(diag_vect),
            FadeOut(vert_dots),
            FadeOut(proj_vert_dots),
            frame.animate.reorient(42, 62, 0, (0.68, 0.48, 0.41), 2.34),
            run_time=2,
        )

        # Show cube faces
        cube = Cube()
        cube.set_color(BLUE_E, 1)
        cube.set_shading(0.75, 0.25, 0.5)
        cube.replace(cube_shell)
        cube.sort(lambda p: np.dot(p, np.ones(3)))
        inner_faces = cube[:3]
        outer_faces = cube[3:]

        for mob in [cube_shell, proj_cube_shell, plane]:  # No axes?
            mob.apply_depth_test()
        self.add(axes, cube, cube_shell, plane, proj_cube_shell)
        self.play(
            FadeIn(cube),
            proj_cube_shell.animate.set_stroke(width=1, opacity=0.2),
        )
        self.wait(10, note="Note the outer faces")
        self.add(axes, inner_faces, cube_shell, plane, proj_cube_shell)
        self.play(
            FadeOut(outer_faces),
            inner_faces.animate.set_submobject_colors_by_gradient(RED, GREEN, BLUE),
        )
        self.wait(10, note="Gesture at inner faces")
        inner_faces.save_state()
        self.play(inner_faces.animate.apply_matrix(proj_mat), run_time=2)
        self.play(inner_faces.animate.space_out_submobjects(1.2), rate_func=there_and_back, run_time=2)
        self.wait(10)

        # Shuffle faces around
        inner_proj_state = inner_faces.copy()
        self.wait()
        self.play(Restore(inner_faces), run_time=2)
        inner_faces.target = inner_faces.generate_target()
        for face, vect in zip(inner_faces.target, [UP, RIGHT, OUT]):
            face.shift(vect)
        outer_state = inner_faces.target.copy()
        self.play(MoveToTarget(inner_faces, lag_ratio=0.5, run_time=3))
        self.wait()
        self.play(inner_faces.animate.apply_matrix(proj_mat), run_time=2)
        self.play(inner_faces.animate.space_out_submobjects(1.2), rate_func=there_and_back, run_time=2)
        self.wait()

        for u in [-1, 1]:
            self.play(Rotate(inner_faces, u * PI / 3, axis=np.ones(3), run_time=2))
            self.wait()

        for group in inner_faces, inner_proj_state:
            for i, mob in enumerate(group):
                mob.shift(i * 0.0001 * IN)
        self.play(Transform(inner_faces, inner_proj_state, lag_ratio=0.5, run_time=3))
        self.wait()
        self.play(Restore(inner_faces), run_time=2)

        # Show coordinates for inner faces
        bases = np.identity(3, dtype=int)
        vects = VGroup(Vector(basis, thickness=2) for basis in bases)
        coord_labels = VGroup(
            Tex(str(tuple(basis)), font_size=16).next_to(basis, UR, buff=0.05).rotate(45 * DEGREES, RIGHT, about_point=basis)
            for basis in bases
        )

        self.play(
            axes.animate.set_stroke(width=0.5),
            plane.axes.animate.set_stroke(width=0.5),
            FadeOut(inner_faces),
            LaggedStartMap(GrowArrow, vects),
            run_time=2
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, coord_labels),
            frame.animate.reorient(9, 63, 0, (1.03, 0.61, 0.56), 2.72),
            run_time=2
        )
        self.wait()

        # Emphasize pairs
        vects_state = vects.copy()
        labels_state = coord_labels.copy()
        last_face = VectorizedPoint()
        ordered_faces = Group(inner_faces[i] for i in [1, 0, 2])
        ordered_faces.set_opacity(0.8)
        ordered_faces.deactivate_depth_test()

        for i in range(3):
            vects_target = vects_state.copy()
            labels_target = labels_state.copy()
            vects_target[i].fade(0.8)
            labels_target[i].fade(0.8)
            self.add(ordered_faces[i], vects, coord_labels)
            self.play(
                Transform(vects, vects_target),
                Transform(coord_labels, labels_target),
                FadeIn(ordered_faces[i]),
                FadeOut(last_face),
            )
            self.wait()

            last_face = ordered_faces[i]

        # Project all the vectors
        proj_vects = VGroup(
            Vector(np.dot(basis, proj_mat.T), thickness=3)
            for basis in np.identity(3)
        )
        proj_coords = VGroup(
            Tex(f"P{str(tuple(basis))}", font_size=16)
            for basis in np.identity(3, dtype=int)
        )
        for label, vect in zip(proj_coords, proj_vects):
            label.move_to(vect.get_end() + 0.25 * vect.get_vector())
            label.rotate(45 * DEGREES, RIGHT)
            label.rotate(45 * DEGREES, OUT)
            vect.set_perpendicular_to_camera(self.frame)
        proj_coords[1].shift(0.25 * UP)
        faces = Group(ordered_faces[2], ordered_faces[0], ordered_faces[1])

        self.add(faces, vects, coord_labels)
        self.play(
            Transform(vects, vects_state),
            Transform(coord_labels, labels_state),
            FadeIn(faces),
            frame.animate.reorient(44, 55, 0, (1.03, 0.61, 0.56), 2.72),
            run_time=2
        )
        self.play(
            Transform(vects, proj_vects),
            Transform(coord_labels, proj_coords),
            faces.animate.apply_matrix(proj_mat),
        )
        self.play(frame.animate.reorient(56, 58, 0, (0.7, 0.32, 0.6), 2.72), run_time=5)

    def add_coordinate_labels(self, axes):
        coordinate_config = dict(font_size=12, buff=0.1)
        axes.add_coordinate_labels(**coordinate_config)
        axes.z_axis.add_numbers(
            **coordinate_config,
            excluding=[0],
            direction=LEFT
        )
        for number in axes.z_axis.numbers:
            number.scale(0.75, about_edge=RIGHT)
            number.rotate(90 * DEGREES, RIGHT)

    def construct_proj_matrix(self):
        diag = normalize(np.ones(3))
        id3 = np.identity(3)
        return np.array([self.project(basis, diag) for basis in id3]).T

    def gram_schmitt(self, vects):
        for i in range(len(vects)):
            for j in range(i):
                vects[i] = self.project(vects[i], vects[j])
            vects[i] = normalize(vects[i])
        return vects

    def project(self, vect, unit_norm):
        """
        Project v1 onto the orthogonal subspace of norm
        """
        return vect - np.dot(unit_norm, vect) * unit_norm


class Project4DCube(Project3DCube):
    def construct(self):
        # Get hypercube data
        frame = self.frame
        hypercube_points, edge_indices = self.get_hypercube_data()

        # Prepare pre-projectiong
        w_shift = 2 * RIGHT + UP + OUT

        cube_verts = np.array(list(it.product(*3 * [[0, 1]])))
        cube_shell = VGroup(
            Line(cube_verts[i], cube_verts[j])
            for i, p1 in enumerate(cube_verts)
            for j, p2 in enumerate(cube_verts[i + 1:], start=i + 1)
            if get_norm(p2 - p1) == 1
        )
        cube_shells = cube_shell.replicate(2)
        cube_shells[1].shift(w_shift)
        edge_connectors = VGroup(Line(v, v + w_shift) for v in cube_verts)

        cube_shells[0].set_stroke(BLUE, 2)
        cube_shells[1].set_stroke(YELLOW, 2)
        edge_connectors.set_stroke(WHITE, 1)

        coord_labels = VGroup()
        for point in hypercube_points:
            label = Tex(str(tuple(point)), font_size=12)
            point_3d = point[:3] + point[3] * w_shift
            label.next_to(point_3d, DR, buff=0.05)
            label.rotate(45 * DEGREES, RIGHT, about_point=point_3d)
            coord_labels.add(label)
        coord_labels.set_backstroke(BLACK, 2)

        low_labels = coord_labels[0::2]
        high_labels = coord_labels[1::2]
        low_labels.set_z_index(1)
        high_labels.set_z_index(1)
        for group in [low_labels, high_labels]:
            group.generate_target()
            for part in group.target:
                part[-2].set_fill(RED)

        # Show lists of coordinates
        titles = VGroup(Text(f"{n}D Cube Vertices") for n in [3, 4])
        coords3d = VGroup(Tex(str(tuple(coords))) for coords in it.product(*3 * [[0, 1]]))
        coords4d = VGroup(Tex(str(tuple(coords))) for coords in it.product(*4 * [[0, 1]]))

        coords3d.scale(0.75).arrange(DOWN, buff=MED_SMALL_BUFF)
        coords4d.scale(0.75).arrange_in_grid(8, 2, v_buff=MED_SMALL_BUFF, h_buff=0.5)

        for title, vect, coords in zip(titles, [LEFT, RIGHT], [coords3d, coords4d]):
            title.move_to(vect * FRAME_WIDTH / 4).to_edge(UP)
            title.add(Underline(title))
            coords.set_backstroke(BLACK, 2)
            coords.next_to(title, DOWN)

        self.add(titles)
        self.add(coords3d)
        self.play(LaggedStartMap(FadeIn, coords4d, shift=0.1 * DOWN, lag_ratio=0.1, run_time=3))
        self.wait()

        label_group3d = VGroup(titles[0], coords3d)
        label_group4d = VGroup(titles[1], coords4d)
        VGroup(label_group3d, label_group4d).fix_in_frame()

        # Show pre-projection
        pre_low_labels = coords4d[0::2].copy()
        pre_low_labels.unfix_from_frame()
        pre_low_labels.set_backstroke(BLACK, 2)

        label_group4d.target = label_group4d.generate_target()
        label_group4d.target.scale(0.5).to_corner(UL)
        label_group4d.target[1][1::2].set_opacity(0.2)

        self.play(
            Write(cube_shells[0]),
            TransformFromCopy(pre_low_labels, low_labels),
            frame.animate.reorient(11, 67, 0, (1.08, 0.47, 0.77), 3.22),
            FadeOut(label_group3d, 3 * LEFT),
            MoveToTarget(label_group4d),
            run_time=3
        )
        self.wait(6, note="Pan somewhat")
        self.play(
            MoveToTarget(low_labels),
            LaggedStart(
                (FlashUnder(label[-3:], color=RED)
                for label in low_labels),
                lag_ratio=0.05,
            )
        )
        self.wait()
        self.play(
            ShowCreation(edge_connectors, lag_ratio=0),
            TransformFromCopy(*cube_shells),
            TransformFromCopy(low_labels, high_labels),
            label_group4d[1][1::2].animate.set_opacity(1),
            run_time=3
        )
        self.wait()
        self.play(
            MoveToTarget(high_labels),
            LaggedStart(
                (FlashUnder(label[-3:], color=RED)
                for label in high_labels),
                lag_ratio=0.05,
            )
        )
        self.wait(20, note="Pan and gesture")

        # Put pre-projection in the corner
        axes = ThreeDAxes((-3, 3), (-3, 3), (-3, 3))
        axes.set_height(12)
        pre_proj_points = np.array([
            *hypercube_points[:8, 1:],
            *(hypercube_points[:8, 1:] + w_shift),
        ])
        pre_proj_frame = VGroup(
            Line(pre_proj_points[i], pre_proj_points[j])
            for i, j in edge_indices
        )
        pre_proj_frame.set_stroke(WHITE, 1)
        pre_proj_frame.generate_target()
        pre_proj_frame.target.fix_in_frame()
        pre_proj_frame.target.set_height(1.0)
        pre_proj_frame.target.rotate(60 * DEGREES, LEFT).rotate(45 * DEGREES, UP).rotate(15 * DEGREES, OUT)
        pre_proj_frame.target.to_corner(UL, buff=LARGE_BUFF)

        cloud = ThoughtBubble(Rectangle(2, 1.5))[0][3]
        cloud.set_fill(GREY_E, 1)
        cloud.to_corner(UL, buff=MED_SMALL_BUFF)
        cloud.fix_in_frame()
        cloud_label = Text("4D")
        cloud_label.next_to(cloud, DOWN)
        cloud_label.fix_in_frame()
        pre_proj_frame.target.move_to(cloud)

        arrow = Arrow(cloud.get_right(), UL, path_arc=-60 * DEGREES, thickness=5)
        arrow.set_fill(border_width=0.5)
        arrow.fix_in_frame()
        arrow_label = TexText("Project along [1, 1, 1, 1]", font_size=24)
        arrow_label.next_to(arrow.pfp(0.15), UR, buff=0.15)
        arrow_label.fix_in_frame()

        self.play(
            FadeOut(label_group4d),
            FadeOut(VGroup(cube_shells, edge_connectors, coord_labels)),
            FadeIn(pre_proj_frame),
        )
        self.add(cloud, pre_proj_frame),
        self.play(
            FadeIn(cloud, time_span=(2, 3)),
            Write(cloud_label, time_span=(2, 3)),
            MoveToTarget(pre_proj_frame),
            frame.animate.reorient(22, 76, 0, (-1.33, 0.51, 0.63), 7.64),
            run_time=3,
        )
        self.wait()
        self.play(
            GrowArrow(arrow, path_arc=-30 * DEGREES),
            Write(arrow_label),
            Write(axes),
        )
        self.wait()

        corner_group = VGroup(cloud, cloud_label, pre_proj_frame, arrow, arrow_label)

        # Project down
        proj_coords = self.project_along_diagonal(hypercube_points)
        proj_points = axes.c2p(*proj_coords.T)
        proj_frame = VGroup(
            Line(proj_points[i], proj_points[j])
            for i, j in edge_indices
        )
        proj_frame.set_stroke(YELLOW, 2)

        self.add(Point(), pre_proj_frame)
        self.play(Transform(pre_proj_frame.copy(), proj_frame.copy(), run_time=3, remover=True))
        self.add(Point(), proj_frame)
        self.wait()

        # Show solid faces
        inner_cells = self.get_rhombic_dodec(side_length=axes.x_axis.get_unit_size())
        inner_cells.set_color(BLUE_E, 1)

        axes.apply_depth_test()
        self.play(
            FadeOut(proj_frame),
            FadeIn(inner_cells),
        )
        self.wait()

        # Break up inner cells
        space_factor = 1.5
        ghost_cells = inner_cells.copy()
        ghost_cells.deactivate_depth_test()
        ghost_cells.set_opacity(0.1)
        inner_cells.target = inner_cells.generate_target()
        inner_cells.target.space_out_submobjects(space_factor)

        for group in [inner_cells.target, ghost_cells]:
            group.set_submobject_colors_by_gradient(RED_E, GREEN_E, BLUE_E, PINK)

        self.play(
            MoveToTarget(inner_cells),
            FadeOut(corner_group),
            run_time=2
        )
        self.wait()
        self.play(
            FadeOut(inner_cells),
            FadeIn(ghost_cells, scale=0.8),
        )

        # Projected bases
        proj_bases = self.construct_proj_matrix().T
        proj_basis_vectors = VGroup(
            Vector(axes.c2p(*basis))
            for basis in proj_bases
        )
        proj_basis_labels = VGroup(
            Tex(Rf"P{tuple(basis)}", font_size=24)
            for basis in np.identity(4).astype(int)
        )
        for vect, label in zip(proj_basis_vectors, proj_basis_labels):
            vect.set_perpendicular_to_camera(frame)  # Always?
            label.next_to(vect.get_end(), RIGHT, SMALL_BUFF)
            label.rotate(45 * DEGREES, about_point=vect.get_end(), axis=RIGHT)
        proj_basis_labels[0].shift(0.25 * DOWN) 

        self.play(
            axes.animate.set_stroke(width=1),
            LaggedStartMap(GrowArrow, proj_basis_vectors, suspend_mobject_updating=True),
            FadeIn(proj_basis_labels),
        )
        self.wait()

        self.play(
            ghost_cells.animate.space_out_submobjects(space_factor).set_opacity(0.5),
            run_time=2
        )

        # Iterate through triplets
        ordered_cells = Group(ghost_cells[i] for i in [0, 1, 2, 3])
        vect_groups = VGroup(
            VGroup(vect, label)
            for vect, label in zip(proj_basis_vectors, proj_basis_labels)
        )
        self.add(ordered_cells)
        for i in range(4):
            vect_groups.generate_target()
            vect_groups.target.set_fill(opacity=1)
            vect_groups.target[i].set_fill(opacity=0.1)
            ordered_cells.generate_target()
            ordered_cells.target.set_opacity(0.05)
            ordered_cells.target[i].set_opacity(0.5)
            self.play(
                MoveToTarget(vect_groups),
                MoveToTarget(ordered_cells),
            )
            self.wait()

        self.play(
            FadeOut(vect_groups),
            FadeOut(ordered_cells),
            FadeIn(inner_cells),
        )

        # Play more
        self.wait(5)
        self.play(inner_cells.animate.space_out_submobjects(1.0 / space_factor))
        self.wait(10)

        # Show inversion
        self.play(FadeOut(inner_cells[1:]))
        self.wait()
        self.play(
            inner_cells[0].animate.move_to(-inner_cells[0].get_center()),
            rate_func=there_and_back_with_pause,
            run_time=6,
        )
        self.wait()
        self.play(FadeIn(inner_cells[1:]))
        self.wait()

        inner_cells.save_state()
        self.play(
            LaggedStart(
                (cell.animate.move_to(-cell.get_center())
                for cell in inner_cells),
                group=inner_cells,
                group_type=Group,
                run_time=3,
                lag_ratio=0.25
            ),
        )
        self.wait()
        self.play(Restore(inner_cells))
        self.wait()

        # Tile space
        N = 4
        small_space_factor = 1.1
        tiling = Group()

        for i in range(4):
            indices = list(range(4))
            indices.remove(i)
            bases = proj_bases[indices]
            for coords in it.product(*3 * [list(range(N))]):
                vect = axes.c2p(*np.dot(coords, bases))
                new_cell = inner_cells[i].copy().shift(vect)
                tiling.add(new_cell)

        tiling.space_out_submobjects(small_space_factor)
        tiling.sort(lambda p: get_norm(p))
        colored_tiling = tiling.copy()
        tiling.set_color(BLUE_E)

        self.play(
            FadeOut(inner_cells[:2]),
            FadeOut(inner_cells[3:]),
            axes.animate.set_stroke(width=0, opacity=0),
        )
        self.wait(15)

        self.remove(inner_cells)
        self.play(
            LaggedStart(
                (TransformFromCopy(inner_cells[2], cell)
                for cell in tiling),
                group_type=Group,
                lag_ratio=0.05,
            ),
            frame.animate.reorient(19, 65, 0, (1.39, 1.51, 0.57), 21.55),
            run_time=8
        )
        self.wait(20)
        self.play(frame.animate.reorient(36, 66, 0, (-1.32, 0.25, -0.7), 22.55), run_time=3)
        self.play(frame.animate.increment_theta(PI), run_time=10)
        self.play(Transform(tiling, colored_tiling))
        self.wait()

    def get_hypercube_data(self):
        points = np.array(list(it.product(*4 * [[0, 1]])))
        edge_indices = [
            (i, j)
            for i, p1 in enumerate(points)
            for j, p2 in enumerate(points[i + 1:], start=i + 1)
            if get_norm(p2 - p1) == 1
        ]

        return points, edge_indices

    def project_along_diagonal(self, points):
        if not hasattr(self, "diag_4d_projection"):
            self.diag_4d_projection = self.construct_proj_matrix()
        return np.dot(points, self.diag_4d_projection.T)

    def construct_proj_matrix(self):
        diag = normalize(np.ones(4))
        id4 = np.identity(4)
        pre_basis = np.array([diag, id4[1] - id4[0], id4[2], id4[3]])
        basis = self.gram_schmitt(pre_basis)
        return basis[1:, :]

    def get_rhombic_dodec(self, side_length=1):
        cube = Cube()
        cube.set_width(side_length)
        cube.move_to(ORIGIN, -np.ones(3))

        proj_bases = self.project_along_diagonal(np.identity(4))
        cells = Group()
        for i in range(4):
            indices = list(range(4))
            indices.remove(i)
            mat = proj_bases[indices]
            cells.add(cube.copy().apply_matrix(mat.T, about_point=ORIGIN))

        cells.set_color(BLUE_E, 1)
        return cells
