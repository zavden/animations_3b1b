# ==============================================================================
# Scene:      ShowGridSum
# Source:     videos/_2021/shadows.py (lines 4796-5160)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowGridSum.py ShowGridSum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ShadowScene: set_style(**plane_style/object_style) no longer accepts loose reflectiveness/gloss/shadow; the helper set_style_with_shading (set_style + set_shading) is used
# ==============================================================================

from manim_imports_ext import *
import scipy.spatial

# Helpers
def project_to_xy_plane(p1, p2):
    """
    Draw a line from source to p1 to p2.  Where does it
    intersect the xy plane?
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    if z2 < z1:
        z2 = z1 + 1e-2  # TODO, bad hack
    vect = p2 - p1
    return p1 - (z2 / vect[2]) * vect


def flat_project(point):
    # return [*point[:2], 0]
    return [*point[:2], 0.05 * point[2]]  # TODO


def get_pre_shadow(mobject, opacity):
    result = mobject.deepcopy()
    if isinstance(result, Group) and all((isinstance(sm, VMobject) for sm in mobject)):
        result = VGroup(*result)
    result.clear_updaters()

    for sm in result.family_members_with_points():
        color = interpolate_color(sm.get_color(), BLACK, opacity)
        sm.set_color(color)
        sm.set_opacity(opacity)
        if isinstance(sm, VMobject):
            sm.set_stroke(
                interpolate_color(sm.get_stroke_color(), BLACK, opacity)
            )
        sm.set_gloss(sm.get_gloss() * 0.5)
        sm.set_shadow(0)
        sm.set_reflectiveness(0)
    return result


def update_shadow(shadow, mobject, light_source):
    lp = light_source.get_center() if light_source is not None else None

    def project(point):
        if lp is None:
            return flat_project(point)
        else:
            return project_to_xy_plane(lp, point)

    for sm, mm in zip(shadow.family_members_with_points(), mobject.family_members_with_points()):
        sm.set_points(np.apply_along_axis(project, 1, mm.get_points()))
        if isinstance(sm, VMobject) and sm.get_unit_normal()[2] < 0:
            sm.reverse_points()
        if isinstance(sm, VMobject):
            sm.set_fill(opacity=mm.get_fill_opacity())
        else:
            sm.set_opacity(mm.get_opacity())


def get_shadow(mobject, light_source=None, opacity=0.7):
    shadow = get_pre_shadow(mobject, opacity)
    shadow.add_updater(lambda s: update_shadow(s, mobject, light_source))
    return shadow


def get_area(shadow):
    return 0.5 * sum(
        get_norm(sm.get_area_vector())
        for sm in shadow.get_family()
    )


def get_convex_hull(mobject):
    points = mobject.get_all_points()
    hull = scipy.spatial.ConvexHull(points[:, :2])
    return points[hull.vertices]


def sort_to_camera(mobject, camera_frame):
    cl = camera_frame.get_implied_camera_location()
    mobject.sort(lambda p: -get_norm(p - cl))
    return mobject


def cube_sdf(point, cube):
    c = cube.get_center()
    vect = point - c
    face_vects = [face.get_center() - c for face in cube]
    return max(*(
        abs(np.dot(fv, vect) / np.dot(fv, fv))
        for fv in face_vects
    )) - 1


def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


# CHANGE: set_style no longer accepts reflectiveness/gloss/shadow separately (now shading=(reflectiveness, gloss,
# shadow)); this helper splits them and applies them with set_shading
def set_style_with_shading(mobject, **style):
    shading = {k: style.pop(k) for k in ("reflectiveness", "gloss", "shadow") if k in style}
    mobject.set_style(**style)
    if shading:
        mobject.set_shading(**shading)
    return mobject


class ShadowScene(ThreeDScene):
    object_center = [0, 0, 3]
    frame_center = [0, 0, 2]
    area_label_center = [0, -1.5, 0]
    surface_area = 6.0
    num_reorientations = 10
    plane_dims = (20, 20)
    plane_style = {
        "stroke_width": 0,
        "fill_color": GREY_A,
        "fill_opacity": 0.5,
        "gloss": 0.5,
        "shadow": 0.2,
    }
    limited_plane_extension = 0
    object_style = {
        "stroke_color": WHITE,
        "stroke_width": 0.5,
        "fill_color": BLUE_E,
        "fill_opacity": 0.7,
        "reflectiveness": 0.3,
        "gloss": 0.1,
        "shadow": 0.5,
    }
    inf_light = False
    glow_radius = 10
    glow_factor = 10
    area_label_center = [-2, -1, 0]
    unit_size = 2

    def setup(self):
        self.camera.frame.reorient(-30, 75)
        self.camera.frame.move_to(self.frame_center)
        self.add_plane()
        self.add_solid()
        self.add_shadow()
        self.setup_light_source()

    def add_plane(self):
        width, height = self.plane_dims

        grid = NumberPlane(
            x_range=(-width // 2, width // 2, 2),
            y_range=(-height // 2, height // 2, 2),
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
            },
            faded_line_ratio=4,
        )
        grid.shift(-grid.get_origin())
        grid.set_width(width)
        grid.axes.match_style(grid.background_lines)
        grid.set_flat_stroke(True)
        grid.insert_n_curves(3)

        plane = Rectangle()
        plane.replace(grid, stretch=True)
        set_style_with_shading(plane, **self.plane_style)
        plane.set_stroke(width=0)
        if self.limited_plane_extension > 0:
            plane.set_height(height // 2 + self.limited_plane_extension, about_edge=UP, stretch=True)
        self.plane = plane

        plane.add(grid)
        self.add(plane)

    def add_solid(self):
        self.solid = self.get_solid()
        self.solid.move_to(self.object_center)
        self.add(self.solid)

    def get_solid(self):
        cube = VCube()
        cube.deactivate_depth_test()
        cube.set_height(2)
        set_style_with_shading(cube, **self.object_style)
        # Wrap in group so that strokes and fills
        # are rendered in separate passes
        cube = self.cube = Group(*cube)
        cube.add_updater(lambda m: self.sort_to_camera(m))
        return cube

    def add_shadow(self):
        light_source = None if self.inf_light else self.camera.light_source
        shadow = get_shadow(self.solid, light_source)

        self.add(shadow, self.solid)
        self.shadow = shadow

    def setup_light_source(self):
        self.light = self.camera.light_source
        if self.inf_light:
            self.light.move_to(100 * OUT)
        else:
            glow = self.glow = TrueDot(
                radius=self.glow_radius,
                glow_factor=self.glow_factor,
            )
            glow.set_color(interpolate_color(YELLOW, WHITE, 0.5))
            glow.add_updater(lambda m: m.move_to(self.light))
            self.add(glow)

    def sort_to_camera(self, mobject):
        return sort_to_camera(mobject, self.camera.frame)

    def get_shadow_area_label(self):
        text = OldTexText("Shadow area: ")
        decimal = DecimalNumber(100)

        label = VGroup(text, decimal)
        label.arrange(RIGHT)
        label.move_to(self.area_label_center - decimal.get_center())
        label.fix_in_frame()
        label.set_backstroke()
        decimal.add_updater(lambda d: d.set_value(
            get_area(self.shadow) / (self.unit_size**2)
        ).set_backstroke())
        return label

    def begin_ambient_rotation(self, mobject, speed=0.2, about_point=None, initial_axis=[1, 1, 1]):
        mobject.rot_axis = np.array(initial_axis)

        def update_mob(mob, dt):
            mob.rotate(speed * dt, mob.rot_axis, about_point=about_point)
            mob.rot_axis = rotate_vector(mob.rot_axis, speed * dt, OUT)
            return mob
        mobject.add_updater(update_mob)
        return mobject

    def get_shadow_outline(self, stroke_width=1):
        outline = VMobject()
        outline.set_stroke(WHITE, stroke_width)
        outline.add_updater(lambda m: m.set_points_as_corners(get_convex_hull(self.shadow)).close_path())
        return outline

    def get_light_lines(self, outline=None, n_lines=100, only_vertices=False):
        if outline is None:
            outline = self.get_shadow_outline()

        def update_lines(lines):
            lp = self.light.get_center()
            if only_vertices:
                points = outline.get_vertices()
            else:
                points = [outline.pfp(a) for a in np.linspace(0, 1, n_lines)]
            for line, point in zip(lines, points):
                if self.inf_light:
                    line.set_points_as_corners([point + 10 * OUT, point])
                else:
                    line.set_points_as_corners([lp, point])

        line = Line(IN, OUT)
        light_lines = line.replicate(n_lines)
        light_lines.set_stroke(YELLOW, 0.5, 0.1)
        light_lines.add_updater(update_lines)
        return light_lines

    def random_toss(self, mobject=None, angle=TAU, about_point=None, meta_speed=5, **kwargs):
        if mobject is None:
            mobject = self.solid

        mobject.rot_axis = normalize(np.random.random(3))
        mobject.rot_time = 0

        def update(mob, time):
            dt = time - mob.rot_time
            mob.rot_time = time
            mob.rot_axis = rotate_vector(mob.rot_axis, meta_speed * dt, normalize(np.random.random(3)))
            mob.rotate(angle * dt, mob.rot_axis, about_point=about_point)

        self.play(
            UpdateFromAlphaFunc(mobject, update),
            **kwargs
        )

    def randomly_reorient(self, solid=None, about_point=None):
        solid = self.solid if solid is None else solid
        solid.rotate(
            random.uniform(0, TAU),
            axis=normalize(np.random.uniform(-1, 1, 3)),
            about_point=about_point,
        )
        return solid

    def init_frame_rotation(self, factor=0.0025, max_speed=0.01):
        frame = self.camera.frame
        frame.d_theta = 0

        def update_frame(frame, dt):
            frame.d_theta += -factor * frame.get_theta()
            frame.increment_theta(clip(
                factor * frame.d_theta,
                -max_speed * dt,
                max_speed * dt
            ))

        frame.add_updater(update_frame)
        return frame


class TwoToOneCover(ShadowScene):
    inf_light = True
    plane_dims = (20, 12)
    limited_plane_extension = 8
    highlighted_face_color = YELLOW

    def construct(self):
        # Setup
        frame = self.camera.frame
        frame.reorient(-20, 75)
        frame.set_z(3)
        self.init_frame_rotation()

        cube = self.solid
        for face in cube:
            face.set_fill(opacity=0.9)
            face.set_reflectiveness(0.1)
            face.set_gloss(0.2)
        cube.add_updater(lambda m: self.sort_to_camera(m))
        cube.rotate(PI / 3, normalize([3, 4, 5]))
        shadow = self.shadow
        outline = self.get_shadow_outline()

        # Inequality
        ineq = self.get_top_expression("$<$")
        ineq.fix_in_frame()

        lhs = ineq.slice_by_tex(None, "<")
        lt = ineq.get_part_by_tex("<")
        rhs = ineq.slice_by_tex("sum", None)
        af_label = ineq[-7:]
        lhs.save_state()
        lhs.set_x(0)

        # Shadow of the cube
        wireframe = cube.copy()
        for face in wireframe:
            face.set_fill(opacity=0)
            face.set_stroke(WHITE, 1)
        wireframe_shadow = wireframe.copy()
        wireframe_shadow.apply_function(flat_project)
        wireframe_shadow.set_gloss(0)
        wireframe_shadow.set_reflectiveness(0)
        wireframe_shadow.set_shadow(0)
        for face in wireframe_shadow:
            face.set_stroke(GREY_D, 1)

        self.play(
            ShowCreation(wireframe, lag_ratio=0.1),
            Write(lhs[2:-1])
        )
        self.play(TransformFromCopy(wireframe, wireframe_shadow))
        self.play(*map(FadeOut, (wireframe, wireframe_shadow)))
        self.wait()
        self.play(
            FadeIn(lhs[:2]), FadeIn(lhs[-1]),
            Write(outline),
            VShowPassingFlash(
                outline.copy().set_stroke(YELLOW, 4),
                time_width=1.5
            ),
        )
        self.wait()

        # Show faces and shadows
        cube.save_state()
        faces, face_shadows = self.get_faces_and_face_shadows()
        faces[:3].set_opacity(0.1)
        face_shadow_lines = VGroup(*(
            VGroup(*(
                Line(v1, v2)
                for v1, v2 in zip(f.get_vertices(), fs.get_vertices())
            ))
            for f, fs in zip(faces, face_shadows)
        ))
        face_shadow_lines.set_stroke(YELLOW, 0.5, 0.5)

        self.play(
            Restore(lhs),
            FadeIn(af_label, shift=0.5 * RIGHT)
        )
        self.play(
            *(
                LaggedStart(*(
                    VFadeInThenOut(sm)
                    for sm in reversed(mobject)
                ), lag_ratio=0.5, run_time=6)
                for mobject in [faces, face_shadows, face_shadow_lines]
            ),
        )
        self.play(
            ApplyMethod(cube.space_out_submobjects, 1.7, rate_func=there_and_back_with_pause, run_time=8),
            ApplyMethod(frame.reorient, 20, run_time=8),
            Write(lt),
            Write(rhs[0]),
        )
        self.wait(2)

        # Show a given pair of faces
        face_pair = Group(faces[3], faces[5]).copy()
        face_pair[1].set_color(RED)
        face_pair.save_state()
        fp_shadow = get_shadow(face_pair)

        self.add(fp_shadow)
        self.play(
            FadeOut(cube),
            *map(VFadeOut, shadow),
            FadeOut(outline),
            *map(Write, face_pair),
        )
        self.wait(1)
        self.play(Rotate(
            face_pair, PI / 2, DOWN,
            about_point=cube.get_center(),
            run_time=3,
        ))
        self.wait()
        self.random_toss(face_pair, about_point=cube.get_center(), run_time=6)
        fp_shadow.clear_updaters()
        self.play(
            FadeIn(cube),
            *map(VFadeIn, shadow),
            FadeOut(face_pair, scale=0),
            FadeOut(fp_shadow, scale=0),
        )
        self.add(shadow)

        # Half of sum
        new_expression = self.get_top_expression(" = ", "$\\displaystyle \\frac{1}{2}$")
        new_expression.fix_in_frame()
        eq_half = VGroup(
            new_expression.get_part_by_tex("="),
            new_expression.get_part_by_tex("frac"),
        )

        cube.save_state()
        cube.generate_target(use_deepcopy=True)
        cube.target.clear_updaters()
        z_sorted_faces = Group(*sorted(list(cube.target), key=lambda f: f.get_z()))
        z_sorted_faces[:3].shift(2 * LEFT)
        z_sorted_faces[3:].shift(2 * RIGHT)

        cube.clear_updaters()
        self.play(
            MoveToTarget(cube),
            ApplyMethod(frame.reorient, 0, run_time=2)
        )
        self.play(
            FadeOut(lt, UP),
            Write(eq_half),
            ReplacementTransform(rhs, new_expression[-len(rhs):]),
            ReplacementTransform(lhs, new_expression[:len(lhs)]),
        )
        self.remove(ineq)
        self.add(new_expression)
        self.wait(2)
        anims = []
        for part in z_sorted_faces:
            pc = part.copy()
            pc.set_fill(YELLOW, 0.25)
            pc_shadow = get_shadow(pc)
            pc_shadow.clear_updaters()
            pc_shadow.match_style(pc)
            lines = VGroup(*(
                Line(v, flat_project(v))
                for v in pc.get_vertices()
            ))
            lines.set_stroke(YELLOW, 1, 0.1)
            anims.append(AnimationGroup(
                VFadeInThenOut(pc),
                VFadeInThenOut(pc_shadow),
                VFadeInThenOut(lines),
            ))
        self.play(LaggedStart(*anims, lag_ratio=0.4, run_time=6))
        self.play(Restore(cube))

        # Show the double cover
        shadow_point = shadow.get_bottom() + [0.5, 0.75, 0]
        dot = GlowDot(shadow_point)
        line = DashedLine(
            shadow_point + 5 * OUT, shadow_point,
            dash_length=0.025
        )
        line.set_stroke(YELLOW, 1)

        def update_line(line):
            line.move_to(dot.get_center(), IN)
            for dash in line:
                dist = cube_sdf(dash.get_center(), cube)
                dash.set_stroke(
                    opacity=interpolate(0.1, 1.0, clip(10 * dist, -0.5, 0.5) + 0.5)
                )
                dash.inside = (dist < 0)

        line.add_updater(update_line)

        entry_point = next(dash for dash in line if dash.inside).get_center()
        exit_point = next(dash for dash in reversed(line) if dash.inside).get_center()
        arrows = VGroup(*(
            Arrow(point + RIGHT, point, buff=0.1)
            for point in (entry_point, exit_point)
        ))

        self.play(ShowCreation(line, rate_func=rush_into))
        self.play(FadeIn(dot, scale=10, rate_func=rush_from, run_time=0.5))
        self.wait()
        self.play(
            Rotate(
                dot, TAU,
                about_point=ORIGIN,
                run_time=6,
            ),
        )
        self.wait()
        for arrow in arrows:
            self.play(ShowCreation(arrow))
        self.wait()
        self.play(FadeOut(arrows))

        cube.add_updater(lambda m: self.sort_to_camera(m))
        self.random_toss(cube, angle=1.5 * TAU, run_time=8)

        # Just show wireframe
        cube.save_state()
        cube.generate_target()
        for sm in cube.target:
            sm.set_fill(opacity=0)
            sm.set_stroke(WHITE, 2)
        outline = self.get_shadow_outline()
        outline.rotate(PI)
        self.play(
            MoveToTarget(cube),
            dot.animate.move_to(outline.get_start())
        )
        self.play(MoveAlongPath(dot, outline, run_time=8))
        self.wait(2)
        self.play(Restore(cube))
        self.play(dot.animate.move_to(outline.get_center()), run_time=2)

        # Make room for equation animations
        # Start here for new scene
        area_label = self.get_shadow_area_label()
        area_label.shift(1.75 * DOWN + 2.25 * RIGHT)
        area_label[0].scale(0, about_edge=RIGHT)
        area_label.scale(0.7)
        outline.update()
        line.clear_updaters()
        self.play(
            FadeOut(dot),
            FadeOut(line),
            ShowCreation(outline),
            VFadeIn(area_label),
        )

        # Single out a face
        self.remove(new_expression)
        self.wait(2)
        face = cube[np.argmax([f.get_z() for f in cube])].copy()
        face.set_color(YELLOW)
        face_shadow = get_shadow(face)
        face_shadow_area = DecimalNumber(get_norm(face_shadow.get_area_vector()) / (self.unit_size**2))
        face_shadow_area.scale(0.65)
        face_shadow_area.move_to(area_label)
        face_shadow_area.shift(flat_project(face.get_center() - cube.get_center()))
        face_shadow_area.shift(SMALL_BUFF * UR)
        face_shadow_area.fix_in_frame()

        cube.save_state()
        self.remove(cube)
        self.play(
            *(
                f.animate.set_fill(opacity=0)
                for f in cube
            ),
            FadeOut(outline),
            FadeOut(area_label),
            Write(face),
            FadeIn(face_shadow),
            FadeIn(face_shadow_area),
        )
        self.wait(2)
        self.play(
            Restore(cube),
            *map(FadeOut, (face, face_shadow, face_shadow_area)),
            *map(FadeIn, (outline, area_label)),
        )

        # Show simple rotations
        for x in range(2):
            self.random_toss(cube)
            self.wait()
        self.wait()

        # Many random orientations
        for x in range(40):
            self.randomly_reorient(cube)
            self.wait(0.25)

        # Show sum of faces again (play 78)
        self.random_toss(cube, 2 * TAU, run_time=8, meta_speed=10)
        self.wait()

        cube.save_state()
        sff = 1.5
        self.play(
            VFadeOut(outline),
            VFadeOut(area_label),
            cube.animate.space_out_submobjects(sff)
        )
        for x in range(3):
            self.random_toss(cube, angle=PI)
            self.wait()
        self.play(cube.animate.space_out_submobjects(1 / sff))

        # Mean shadow of a single face
        cube_style = cube[0].get_style()

        def isolate_face_anims(i, color=YELLOW):
            return (
                shadow.animate.set_fill(
                    interpolate_color(color, BLACK, 0.75)
                ),
                *(
                    f.animate.set_fill(
                        color if f is cube[i] else BLUE,
                        0.75 if f is cube[i] else 0,
                    )
                    for f in cube
                )
            )

        def tour_orientations():
            self.random_toss(cube, 2 * TAU, run_time=5, meta_speed=10)

        self.play(*isolate_face_anims(5))
        tour_orientations()
        for i, color in ((4, GREEN), (3, RED)):
            self.play(
                *isolate_face_anims(i, color),
            )
            tour_orientations()
        cube.update()
        self.play(
            *(
                f.animate.set_style(**cube_style)
                for f in cube
            ),
            shadow.animate.set_fill(interpolate_color(BLUE, BLACK, 0.85)),
            VFadeIn(outline),
            VFadeIn(area_label),
        )
        self.add(cube)

        # Ambient rotation
        self.add(cube)
        self.begin_ambient_rotation(cube, speed=0.4)
        self.wait(20)

    def get_top_expression(self, *mid_tex, n_faces=6):
        t2c = {
            "Shadow": GREY_B,
            "Cube": BLUE_D,
            "Face$_j$": YELLOW,
        }
        ineq = OldTexText(
            "Area(Shadow(Cube))",
            *mid_tex,
            " $\\displaystyle \\sum_{j=1}^" + f"{{{n_faces}}}" + "$ ",
            "Area(Shadow(Face$_j$))",
            tex_to_color_map=t2c,
            isolate=["(", ")"],
        )
        ineq.to_edge(UP, buff=MED_SMALL_BUFF)
        return ineq

    def get_faces_and_face_shadows(self):
        faces = self.solid.deepcopy()
        VGroup(*faces).set_fill(self.highlighted_face_color)

        shadows = get_pre_shadow(faces, opacity=0.7)
        shadows.apply_function(flat_project)
        return faces, shadows


class ShowGridSum(TwoToOneCover):
    def construct(self):
        # Setup
        self.clear()
        shape_name = "Cube"
        n_faces = 6
        # shape_name = "Dodec."
        # n_faces = 12

        frame = self.camera.frame
        frame.reorient(0, 0)
        frame.move_to(ORIGIN)
        equation = self.get_top_expression(" = ", "$\\displaystyle \\frac{1}{2}$", n_faces=n_faces)
        self.add(equation)

        lhs = equation.slice_by_tex(None, "=")
        summand = equation.slice_by_tex("sum", None)[1:]

        # Abbreviate
        t2c = {
            f"\\text{{{shape_name}}}": BLUE,
            "\\text{F}_j": YELLOW,
            "\\text{Face}": YELLOW,
            "\\text{Total}": GREEN,
            "S": GREY_B,
            "{c}": RED,
        }
        kw = {
            "tex_to_color_map": t2c
        }
        lhs.alt1 = OldTex(f"S(\\text{{{shape_name}}})", **kw)
        summand.alt1 = OldTex("S(\\text{F}_j)", **kw)

        def get_s_cube_term(i="i"):
            return OldTex(f"S\\big(R_{{{i}}}", f"(\\text{{{shape_name}}})\\big)", **kw)

        def get_s_f_term(i="i", j="j"):
            result = OldTex(
                f"S\\big(R_{{{i}}}",
                "(", "\\text{F}_{" + str(j) + "}", ")",
                "\\big)",
                **kw
            )
            result[3].set_color(YELLOW)
            return result

        lhs.alt2 = get_s_cube_term(1)
        summand.alt2 = get_s_f_term(1)

        for mob, vect in (lhs, RIGHT), (summand, LEFT):
            mob.brace = Brace(mob, DOWN, buff=SMALL_BUFF)
            mob.alt1.next_to(mob.brace, DOWN)
            self.play(
                GrowFromCenter(mob.brace),
                FadeIn(mob.alt1, shift=0.5 * DOWN),
            )
            self.wait()
            self.play(
                FadeOut(mob.brace, scale=0.5),
                FadeOut(mob, shift=0.5 * UP),
                mob.alt1.animate.move_to(mob, vect),
            )
            mob.alt2.move_to(mob, vect)
        self.wait()

        for mob in lhs, summand:
            self.play(TransformMatchingShapes(mob.alt1, mob.alt2))
            self.wait()

        # Add up many rotations
        lhss = VGroup(
            get_s_cube_term(1),
            get_s_cube_term(2),
            get_s_cube_term(3),
            OldTex("\\vdots"),
            get_s_cube_term("n"),
        )
        buff = 0.6
        lhss.arrange(DOWN, buff=buff)
        lhss.move_to(lhs.alt2, UP)

        self.remove(lhs.alt2)
        self.play(
            LaggedStart(*(
                ReplacementTransform(lhs.alt2.copy(), target)
                for target in lhss
            )),
            frame.animate.set_height(10, about_edge=UP),
            run_time=2,
        )

        # Show empirical mean
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(lhss.get_width() + 0.75)
        h_line.next_to(lhss, DOWN, MED_SMALL_BUFF, aligned_edge=RIGHT)
        plus = OldTex("+")
        plus.align_to(h_line, LEFT).shift(0.1 * RIGHT)
        plus.match_y(lhss[-1])
        total = Text("Total", font_size=60)
        total.set_color(GREEN)
        total.next_to(h_line, DOWN, buff=0.35)
        total.match_x(lhss)

        mean_sa = OldTex(
            f"S(\\text{{{shape_name}}})", "=", "\\frac{1}{n}",
            "\\sum_{i=1}^n S\\big(R_i(" + f"\\text{{{shape_name}}})\\big)",
            **kw,
        )

        mean_sa.add_to_back(get_overline(mean_sa.slice_by_tex(None, "=")))
        mean_sa.next_to(total, DOWN, LARGE_BUFF, aligned_edge=RIGHT)

        corner_rect = SurroundingRectangle(mean_sa, buff=0.25)
        corner_rect.set_stroke(WHITE, 2)
        corner_rect.set_fill(GREY_E, 1)
        corner_rect.move_to(frame, DL)
        corner_rect.shift(0.025 * UR)
        mean_sa.move_to(corner_rect)

        sum_part = mean_sa.slice_by_tex("sum")
        sigma = sum_part[0]
        sigma.save_state()
        lhss_rect = SurroundingRectangle(lhss)
        lhss_rect.set_stroke(BLUE, 2)
        sigma.next_to(lhss_rect, LEFT)
        sum_group = VGroup(lhss, lhss_rect)

        self.play(
            Write(lhss_rect),
            Write(sigma),
        )
        self.wait()
        self.add(corner_rect, sigma)
        self.play(
            FadeIn(corner_rect),
            *(
                FadeTransform(term.copy(), sum_part[1:])
                for term in lhss
            ),
            Restore(sigma),
        )
        self.play(Write(mean_sa.get_part_by_tex("frac")))
        self.wait()
        self.play(
            FadeIn(mean_sa.slice_by_tex(None, "frac")),
        )
        self.wait()

        # Create grid
        sf = get_s_f_term
        grid_terms = [
            [sf(1, 1), sf(1, 2), OldTex("\\dots"), sf(1, n_faces)],
            [sf(2, 1), sf(2, 2), OldTex("\\dots"), sf(2, n_faces)],
            [sf(3, 1), sf(3, 2), OldTex("\\dots"), sf(3, n_faces)],
            [Tex("\\vdots"), OldTex("\\vdots"), OldTex("\\ddots"), OldTex("\\vdots")],
            [sf("n", 1), sf("n", 2), OldTex("\\dots"), sf("n", n_faces)],
        ]
        grid = VGroup(*(VGroup(*row) for row in grid_terms))
        for lhs, row in zip(lhss, grid):
            for i in range(len(row) - 1, 0, -1):
                is_dots = "dots" in row[0].get_tex()
                sym = VectorizedPoint() if is_dots else OldTex("+")
                row.insert_submobject(i, sym)
            row.arrange(RIGHT, buff=MED_SMALL_BUFF)
            for m1, m2 in zip(row, grid[0]):
                m1.match_x(m2)
                m1.match_y(lhs)
            if not is_dots:
                parens = OldTex("[]", font_size=72)[0]
                parens.set_stroke(width=2)
                parens.set_color(BLUE_B)
                parens[0].next_to(row, LEFT, buff=SMALL_BUFF)
                parens[1].next_to(row, RIGHT, buff=SMALL_BUFF)
                row.add(*parens)
                eq_half = OldTex("=", "\\frac{1}{2}")
                eq_half[1].match_height(parens)
                eq_half.next_to(parens[0], LEFT, MED_SMALL_BUFF)
                row.add(*eq_half)

        grid.set_x(frame.get_right()[0] - 1.5, RIGHT)

        self.remove(summand.alt2)
        self.play(
            sum_group.animate.set_x(grid.get_left()[0] - MED_SMALL_BUFF, RIGHT),
            TransformMatchingShapes(
                VGroup(
                    equation.get_part_by_tex("frac"),
                    equation.get_part_by_tex("="),
                ),
                grid[0][-4:],
            ),
            LaggedStart(*(
                FadeTransform(summand.alt2.copy(), part)
                for part in grid[0][0:7:2]
            )),
            FadeOut(equation.get_part_by_tex("sum"), scale=0.25),
            Write(grid[0][1:7:2]),  # Plus signs
        )
        self.wait(2)
        self.play(FadeTransform(grid[0].copy(), grid[1]))
        self.play(FadeTransform(grid[1].copy(), grid[2]))
        self.play(FadeTransform(grid[2].copy(), grid[4]), FadeIn(grid[3]))
        self.wait(2)

        # Average along columns
        cols = VGroup(*(
            VGroup(*(row[i] for row in grid)).copy()
            for i in [0, 2, 6]
        ))
        col_rects = VGroup(*(
            SurroundingRectangle(col, buff=SMALL_BUFF)
            for col in cols
        ))
        col_rects.set_stroke(YELLOW, 1)

        mean_face = OldTex("S(\\text{Face})", **kw)
        mean_face.add_to_back(get_overline(mean_face))
        mean_face.next_to(grid, DOWN, buff=2)
        mean_face_words = OldTexText("Average shadow\\\\of one face")
        mean_face_words.move_to(mean_face, UP)

        arrows = VGroup(*(
            Arrow(rect.get_bottom(), mean_face)
            for rect in col_rects
        ))
        arrow_labels = OldTex("\\frac{1}{n} \\sum \\cdots", font_size=30).replicate(3)
        for arrow, label in zip(arrows, arrow_labels):
            vect = rotate_vector(normalize(arrow.get_vector()), PI / 2)
            label.next_to(arrow.pfp(0.5), vect, SMALL_BUFF)

        self.add(cols[0])
        self.play(
            grid.animate.set_opacity(0.4),
            ShowCreation(col_rects[0])
        )
        self.wait()
        self.play(
            ShowCreation(arrows[0]),
            FadeIn(arrow_labels[0]),
            FadeIn(mean_face_words, DR),
        )
        self.wait()
        self.play(
            mean_face_words.animate.scale(0.7).next_to(mean_face, DOWN, MED_LARGE_BUFF),
            FadeIn(mean_face, scale=2),
        )
        self.wait()
        for i in [1, 2]:
            self.play(
                FadeOut(cols[i - 1]),
                FadeIn(cols[i]),
                *(
                    ReplacementTransform(group[i - 1], group[i])
                    for group in (col_rects, arrows, arrow_labels)
                )
            )
            self.wait()
        self.wait()

        # Reposition
        frame.generate_target()
        frame.target.align_to(total, DOWN)
        frame.target.shift(0.5 * DOWN)
        frame.target.scale(1.15)
        frame.target.align_to(lhss, LEFT).shift(0.25 * LEFT)

        self.play(LaggedStart(
            VGroup(corner_rect, mean_sa).animate.scale(1.25).move_to(
                frame.target, UL
            ).shift(0.1 * DR),
            MoveToTarget(frame),
            FadeOut(mean_face_words),
            FadeOut(mean_face),
            grid.animate.set_opacity(1),
            *(
                FadeOut(group[-1])
                for group in (cols, col_rects, arrows, arrow_labels)
            ),
            run_time=3
        ))
        mean_sa.refresh_bounding_box()  # ??

        # Show final result
        rhss = VGroup(
            OldTex("=", "\\frac{1}{2}", "\\sum_{j=1}^" + f"{{{n_faces}}}", " S(\\text{F}_j})", **kw),
            OldTex("=", "\\frac{1}{2}", "\\sum_{j=1}^" + f"{{{n_faces}}}", " {c}", "\\cdot ", "A(\\text{F}_j)", **kw),
            OldTex("=", "\\frac{1}{2}", "{c}", "\\cdot ", "(\\text{Surface area})", **kw),
        )
        rhss[0].add(get_overline(rhss[0].slice_by_tex("S")))
        rhss[2][-2].set_color(WHITE)

        rhss.arrange(RIGHT)
        rhss.next_to(mean_sa, RIGHT)

        corner_rect.generate_target()
        corner_rect.target.set_width(
            frame.get_width() - 0.2,
            stretch=True,
            about_edge=LEFT,
        )

        grid_rect = SurroundingRectangle(grid, buff=SMALL_BUFF)
        grid_rect.set_stroke(YELLOW, 1)
        grid_rect.set_fill(YELLOW, 0.25)

        rects = VGroup(
            SurroundingRectangle(mean_sa.slice_by_tex("frac")),
            SurroundingRectangle(rhss[0][1:])
        )
        for rect in rects:
            rect.match_height(corner_rect.target, stretch=True)
            rect.match_y(corner_rect.target)
        rects[0].set_color(BLUE)
        rects[1].set_color(YELLOW)
        rects.set_stroke(width=2)
        rects.set_fill(opacity=0.25)

        rows_first = Text("Rows first")
        rows_first.next_to(rects[0], DOWN)
        rows_first.match_color(rects[0])
        cols_first = Text("Columns first")
        cols_first.next_to(rects[1], DOWN)
        cols_first.match_color(rects[1])

        self.add(corner_rect, mean_sa)
        self.play(
            MoveToTarget(corner_rect),
            Write(rhss[0])
        )
        self.add(grid_rect, grid)
        self.play(VFadeInThenOut(grid_rect, run_time=2))
        self.wait()

        self.play(
            Write(rects[0]),
            Write(rows_first),
        )
        self.wait()
        self.play(
            Write(rects[1]),
            Write(cols_first),
        )
        self.wait()
        self.play(LaggedStart(*map(FadeOut, (
            *rects, rows_first, cols_first
        ))))

        self.play(
            TransformMatchingShapes(rhss[0].copy(), rhss[1])
        )
        self.wait()
        self.play(
            FadeTransform(rhss[1].copy(), rhss[2]),
        )
        self.wait()

        key_part = rhss[2][1:]
        final_rect = SurroundingRectangle(key_part)
        final_rect.set_stroke(YELLOW, 1)
        self.play(
            corner_rect.animate.set_stroke(width=0).scale(1.1),
            FlashAround(key_part, time_width=1.5),
            FadeIn(final_rect),
            run_time=2,
        )
