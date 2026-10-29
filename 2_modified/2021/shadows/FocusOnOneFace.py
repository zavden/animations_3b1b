# ==============================================================================
# Scene:      FocusOnOneFace
# Source:     videos/_2021/shadows.py (lines 1033-1575)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FocusOnOneFace.py FocusOnOneFace -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_unit_normal(recompute=True) -> get_unit_normal(refresh=True) (parameter renamed in manimgl)
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex now requires StringMobject and OldTex is passed here)
#   - ShadowScene: set_style(**plane_style/object_style) no longer accepts loose reflectiveness/gloss/shadow; the helper set_style_with_shading (set_style + set_shading) is used
#   - NumberLine.add_numbers: unit="^\\circ" -> unit_tex="^\\circ" (the unit text is now unit_tex)
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


class FocusOnOneFace(ShadowScene):
    inf_light = True
    limited_plane_extension = 10

    def construct(self):
        # Some random tumbling
        cube = self.solid
        shadow = self.shadow
        frame = self.camera.frame

        words = VGroup(
            Text("Just one orientation"),
            Text("Just one face"),
        )
        words.fix_in_frame()
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        words.to_corner(UL)
        average_words = Text("Average over all orientations")
        average_words.move_to(words[0], LEFT)
        average_words.fix_in_frame()
        self.add(average_words)

        self.random_toss(run_time=3, rate_func=linear)
        self.play(
            FadeIn(words[0], 0.75 * UP),
            FadeOut(average_words, 0.75 * UP),
            run_time=0.5,
        )
        self.wait()

        # Just one face
        cube.update()
        index = np.argmax([f.get_z() for f in cube])
        face = cube[index]
        prev_opacity = face.get_fill_opacity()
        cube.generate_target(use_deepcopy=True)
        cube.target.clear_updaters()
        cube.target.space_out_submobjects(2, about_point=face.get_center())
        cube.target.set_opacity(0)
        cube.target[index].set_opacity(prev_opacity)

        self.shadow.set_stroke(width=0)
        self.play(
            MoveToTarget(cube),
            FadeIn(words[1]),
        )
        self.play(
            frame.animate.reorient(-10, 65),
            FlashAround(words[1], rate_func=squish_rate_func(smooth, 0.2, 0.5)),
            FlashAround(words[0], rate_func=squish_rate_func(smooth, 0.5, 0.8)),
            run_time=5,
        )
        frame.add_updater(lambda f, dt: f.increment_theta(0.01 * dt))

        self.solid = face
        self.remove(shadow)
        self.add_shadow()
        shadow = self.shadow

        # Ask about area
        area_q = Text("Area?")
        area_q.add_updater(lambda m: m.move_to(shadow))
        self.play(Write(area_q))
        self.wait()

        # Orient straight up
        unit_normal = face.get_unit_normal()
        axis = rotate_vector(normalize([*unit_normal[:2], 0]), PI / 2, OUT)
        angle = np.arccos(unit_normal[2])
        face.generate_target()
        face.target.rotate(-angle, axis)
        face.target.move_to(3 * OUT)
        face.target.rotate(-PI / 4, OUT)
        self.play(MoveToTarget(face))

        light_lines = self.get_light_lines(n_lines=4, outline=shadow, only_vertices=True)
        light_lines.set_stroke(YELLOW, 1, 0.5)

        self.play(
            frame.animate.set_phi(70 * DEGREES),
            FadeIn(light_lines, lag_ratio=0.5),
            TransformFromCopy(face, face.deepcopy().set_opacity(0).set_z(0), remover=True),
            run_time=3,
        )
        self.wait(3)
        self.play(
            Rotate(face, PI / 2, UP),
            FadeOut(area_q, scale=0),
            run_time=3,
        )
        self.wait(3)
        self.play(
            Rotate(face, -PI / 3, UP),
            UpdateFromAlphaFunc(light_lines, lambda m, a: m.set_opacity(0.5 * (1 - a)), remover=True),
            run_time=2,
        )

        # Show normal vector
        z_axis = VGroup(
            Line(ORIGIN, face.get_center()),
            Line(face.get_center(), 10 * OUT),
        )
        z_axis.set_stroke(WHITE, 1)

        normal_vect = Vector()
        get_fc = face.get_center

        def get_un():
            # CHANGE: get_unit_normal is now called with refresh=True (before, recompute=True)
            return face.get_unit_normal(refresh=True)

        def get_theta():
            return np.arccos(get_un()[2])

        normal_vect.add_updater(lambda v: v.put_start_and_end_on(
            get_fc(), get_fc() + get_un(),
        ))
        arc = always_redraw(lambda: Arc(
            start_angle=PI / 2,
            angle=-get_theta(),
            radius=0.5,
            stroke_width=2,
        ).rotate(PI / 2, RIGHT, about_point=ORIGIN).shift(get_fc()))
        theta = OldTex("\\theta", font_size=30)
        theta.set_backstroke()
        theta.rotate(PI / 2, RIGHT)
        theta.add_updater(lambda m: m.move_to(
            get_fc() + 1.3 * (arc.pfp(0.5) - get_fc())
        ))
        theta.add_updater(lambda m: m.set_width(min(0.123, max(0.01, arc.get_width()))))

        self.play(ShowCreation(normal_vect))
        self.wait()
        self.add(z_axis[0], face, z_axis[1], normal_vect)
        self.play(*map(FadeIn, z_axis))
        self.play(
            FadeIn(theta, 0.5 * OUT), ShowCreation(arc),
        )

        # Vary Theta
        frame.reorient(2)
        face.rotate(-35 * DEGREES, get_un(), about_point=face.get_center())
        self.play(
            Rotate(face, 50 * DEGREES, UP),
            rate_func=there_and_back,
            run_time=8,
        )

        # Show shadow area in the corner
        axes = Axes(
            (0, 180, 22.5), (0, 1, 0.25),
            width=5,
            height=2,
            axis_config={
                "include_tip": False,
                "tick_size": 0.05,
                "numbers_to_exclude": [],
            },
        )
        axes.to_corner(UR, buff=MED_SMALL_BUFF)
        # CHANGE: in NumberLine.add_numbers the unit text is now unit_tex (unit is the numeric factor)
        axes.x_axis.add_numbers([0, 45, 90, 135, 180], unit_tex="^\\circ")
        y_label = OldTexText("Shadow's area", font_size=24)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, MED_SMALL_BUFF)
        y_label.set_backstroke()
        ly_label = OldTex("s^2", font_size=24)
        ly_label.next_to(axes.y_axis.get_top(), LEFT, SMALL_BUFF)
        ly_label.shift(0.05 * UP)
        axes.add(y_label, ly_label)
        axes.fix_in_frame()

        graph = axes.get_graph(
            lambda x: math.cos(x * DEGREES),
            x_range=(0, 90),
        )
        graph.set_stroke(RED, 3)
        graph.fix_in_frame()

        question = Text("Can you guess?", font_size=36)
        question.to_corner(UR)
        question.set_color(RED)

        dot = Dot(color=RED)
        dot.scale(0.5)
        dot.move_to(axes.c2p(0, 1))
        dot.fix_in_frame()

        self.play(
            FadeIn(axes),
            Rotate(face, -get_theta(), UP, run_time=2),
        )
        self.play(FadeIn(dot, shift=2 * UP + RIGHT))
        self.wait(2)
        self.add(graph, axes)
        self.play(
            UpdateFromFunc(dot, lambda d: d.move_to(graph.get_end())),
            ShowCreation(graph),
            Rotate(face, PI / 2, UP),
            run_time=5
        )
        self.play(frame.animate.reorient(45), run_time=2)
        self.play(frame.animate.reorient(5), run_time=4)

        # Show vertical plane
        plane = Rectangle(width=self.plane.get_width(), height=5)
        plane.insert_n_curves(100)
        plane.set_fill(WHITE, 0.25)
        plane.set_stroke(width=0)
        plane.apply_depth_test()

        plane.rotate(PI / 2, RIGHT)
        plane.move_to(ORIGIN, IN)
        plane.save_state()
        plane.stretch(0, 2, about_edge=IN)

        face.apply_depth_test()
        z_axis.apply_depth_test()
        self.shadow.apply_depth_test()

        self.play(
            LaggedStartMap(FadeOut, VGroup(*words, graph, axes, dot)),
            Restore(plane, run_time=3)
        )
        self.play(Rotate(face, -60 * DEGREES, UP, run_time=2))

        # Slice up face
        face_copy = face.deepcopy()
        face_copy.rotate(-get_theta(), UP)
        face_copy.move_to(ORIGIN)

        n_slices = 25
        rects = Rectangle().replicate(n_slices)
        rects.arrange(DOWN, buff=0)
        rects.replace(face_copy, stretch=True)
        slices = VGroup(*(Intersection(face_copy, rect) for rect in rects))
        slices.match_style(face_copy)
        slices.set_stroke(width=0)
        slices.rotate(get_theta(), UP)
        slices.move_to(face)
        slices.apply_depth_test()
        slices.save_state()
        slice_outlines = slices.copy()
        slice_outlines.set_stroke(RED, 1)
        slice_outlines.set_fill(opacity=0)
        slice_outlines.deactivate_depth_test()

        frame.clear_updaters()
        self.play(
            frame.animate.set_euler_angles(PI / 2, get_theta()),
            FadeOut(VGroup(theta, arc)),
            run_time=2
        )
        self.play(ShowCreation(slice_outlines, lag_ratio=0.05))

        self.remove(face)
        self.add(slices)
        self.remove(self.shadow)
        self.solid = slices
        self.add_shadow()
        self.shadow.set_stroke(width=0)
        self.add(normal_vect, plane, slice_outlines)

        slices.insert_n_curves(10)
        slices.generate_target()
        for sm in slices.target:
            sm.stretch(0.5, 1)
        self.play(
            MoveToTarget(slices),
            FadeOut(slice_outlines),
            run_time=2
        )
        self.wait(2)

        # Focus on one slice
        long_slice = slices[len(slices) // 2].deepcopy()
        line = Line(long_slice.get_corner(LEFT + OUT), long_slice.get_corner(RIGHT + IN))
        line.scale(0.97)
        line.set_stroke(BLUE, 3)

        frame.generate_target()
        frame.target.reorient(0, 90)
        frame.target.set_height(6)
        frame.target.move_to(2.5 * OUT)
        self.shadow.clear_updaters()
        self.play(
            MoveToTarget(frame),
            *map(FadeIn, (theta, arc)),
            FadeOut(plane),
            FadeOut(slices),
            FadeOut(self.shadow),
            FadeIn(line),
            run_time=2,
        )
        self.wait()

        # Analyze slice
        shadow = line.copy()
        shadow.stretch(0, 2, about_edge=IN)
        shadow.set_stroke(BLUE_E)
        vert_line = Line(line.get_start(), shadow.get_start())
        vert_line.set_stroke(GREY_B, 3)

        shadow_label = Text("Shadow")
        shadow_label.set_fill(BLUE_E)
        shadow_label.set_backstroke()
        shadow_label.rotate(PI / 2, RIGHT)
        shadow_label.next_to(shadow, IN, SMALL_BUFF)

        self.play(
            TransformFromCopy(line, shadow),
            FadeIn(shadow_label, 0.5 * IN),
        )
        self.wait()
        self.play(ShowCreation(vert_line))
        self.wait()

        top_theta_group = VGroup(
            z_axis[1].copy(),
            arc.copy().clear_updaters(),
            theta.copy().clear_updaters(),
            Line(*normal_vect.get_start_and_end()).match_style(z_axis[1].copy()),
        )
        self.play(
            top_theta_group.animate.move_to(line.get_start(), LEFT + IN)
        )

        elbow = Elbow(angle=-get_theta())
        elbow.set_stroke(WHITE, 2)
        ul_arc = Arc(
            radius=0.4,
            start_angle=-get_theta(),
            angle=-(PI / 2 - get_theta())
        )
        ul_arc.match_style(elbow)
        supl = OldTex("90^\\circ - \\theta", font_size=24)
        supl.next_to(ul_arc, DOWN, SMALL_BUFF, aligned_edge=LEFT)
        supl.set_backstroke()
        supl[0][:3].shift(SMALL_BUFF * RIGHT / 2)

        ul_angle_group = VGroup(elbow, ul_arc, supl)
        ul_angle_group.rotate(PI / 2, RIGHT, about_point=ORIGIN)
        ul_angle_group.shift(line.get_start())

        dr_arc = Arc(
            radius=0.4,
            start_angle=PI,
            angle=-get_theta(),
        )
        dr_arc.match_style(ul_arc)
        dr_arc.rotate(PI / 2, RIGHT, about_point=ORIGIN)
        dr_arc.shift(line.get_end())
        dr_theta = OldTex("\\theta", font_size=24)
        dr_theta.rotate(PI / 2, RIGHT)
        dr_theta.next_to(dr_arc, LEFT, SMALL_BUFF)
        dr_theta.shift(SMALL_BUFF * OUT / 2)

        self.play(ShowCreation(elbow))
        self.play(
            ShowCreation(ul_arc),
            FadeTransform(top_theta_group[2].copy(), supl),
        )
        self.play(
            TransformFromCopy(ul_arc, dr_arc),
            TransformFromCopy(supl[0][4].copy().set_stroke(width=0), dr_theta[0][0]),
        )
        self.wait()

        # Highlight lower right
        rect = Rectangle(0.8, 0.5)
        rect.set_stroke(YELLOW, 2)
        rect.rotate(PI / 2, RIGHT)
        rect.move_to(dr_theta, LEFT).shift(SMALL_BUFF * LEFT)

        self.play(
            ShowCreation(rect),
            top_theta_group.animate.fade(0.8),
            ul_angle_group.animate.fade(0.8),
        )
        self.wait()

        # Show cosine
        cos_formula = OldTex(
            "\\cos(\\theta)", "=",
            "{\\text{Length of }", "\\text{shadow}",
            "\\over",
            "\\text{Length of }", "\\text{slice}"
            "}",
        )
        cos_formula[2:].scale(0.75, about_edge=LEFT)
        cos_formula.to_corner(UR)
        cos_formula.fix_in_frame()

        lower_formula = OldTex(
            "\\text{shadow}", "=",
            "\\cos(\\theta)", "\\cdot", "\\text{slice}"
        )
        lower_formula.match_width(cos_formula)
        lower_formula.next_to(cos_formula, DOWN, MED_LARGE_BUFF)
        lower_formula.fix_in_frame()

        for tex in cos_formula, lower_formula:
            tex.set_color_by_tex("shadow", BLUE_D)
            tex.set_color_by_tex("slice", BLUE_B)

        self.play(Write(cos_formula))
        self.wait()
        # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used
        self.play(TransformMatchingShapes(
            VGroup(*(cos_formula[i].copy() for i in [0, 1, 3, 6])),
            lower_formula,
            path_arc=PI / 4,
        ))
        self.wait()

        # Bring full face back
        frame.generate_target()
        frame.target.reorient(20, 75)
        frame.target.set_height(6)
        frame.target.set_z(2)

        line_shadow = get_shadow(line)
        line_shadow.set_stroke(BLUE_E, opacity=0.5)

        self.solid = face
        self.add_shadow()
        self.add(z_axis[0], face, z_axis[1], line, normal_vect, theta, arc)
        self.play(
            MoveToTarget(frame, run_time=5),
            FadeIn(face, run_time=3),
            FadeIn(self.shadow, run_time=3),
            FadeIn(line_shadow, run_time=3),
            LaggedStart(*map(FadeOut, [
                top_theta_group, ul_angle_group, rect,
                dr_theta, dr_arc,
                vert_line, shadow, shadow_label,
            ]), run_time=4),
        )
        frame.add_updater(lambda f, dt: f.increment_theta(0.01 * dt))
        self.wait(2)

        # Show perpendicular
        perp = Line(
            face.pfp(binary_search(
                lambda a: face.pfp(a)[2],
                face.get_center()[2], 0, 0.5,
            )),
            face.pfp(binary_search(
                lambda a: face.pfp(a)[2],
                face.get_center()[2], 0.5, 1.0,
            )),
        )
        perp.set_stroke(RED, 3)
        perp_shadow = get_shadow(perp)
        perp_shadow.set_stroke(RED_E, 3, opacity=0.2)

        self.add(perp, normal_vect, arc)
        self.play(
            ShowCreation(perp),
            ShowCreation(perp_shadow),
        )
        face.add(line)
        self.play(Rotate(face, 45 * DEGREES, UP), run_time=3)
        self.play(Rotate(face, -55 * DEGREES, UP), run_time=3)
        self.play(Rotate(face, 20 * DEGREES, UP), run_time=2)

        # Give final area formula
        final_formula = OldTex(
            "\\text{Area}(", "\\text{shadow}", ")",
            "=",
            "|", "\\cos(\\theta)", "|", "s^2"
        )
        final_formula.set_color_by_tex("shadow", BLUE_D)
        final_formula.match_width(lower_formula)
        final_formula.next_to(lower_formula, DOWN, MED_LARGE_BUFF)
        final_formula.fix_in_frame()
        final_formula.get_parts_by_tex("|").set_opacity(0)
        final_formula.set_stroke(BLACK, 3, background=True)
        rect = SurroundingRectangle(final_formula)
        rect.set_stroke(YELLOW, 2)
        rect.fix_in_frame()

        self.play(Write(final_formula))
        self.play(ShowCreation(rect))
        final_formula.add(rect)
        self.wait(10)

        # Absolute value
        face.remove(line)
        self.play(
            frame.animate.shift(0.5 * DOWN + RIGHT).reorient(10),
            LaggedStart(*map(FadeOut, [cos_formula, lower_formula])),
            FadeIn(graph),
            FadeIn(axes),
            FadeOut(line),
            FadeOut(line_shadow),
            FadeOut(perp),
            FadeOut(perp_shadow),
            final_formula.animate.shift(2 * DOWN),
            run_time=2
        )
        self.play(
            Rotate(face, PI / 2 - get_theta(), UP),
            run_time=2
        )

        new_graph = axes.get_graph(
            lambda x: math.cos(x * DEGREES),
            (90, 180),
        )
        new_graph.match_style(graph)
        new_graph.fix_in_frame()
        self.play(
            Rotate(face, PI / 2, UP),
            ShowCreation(new_graph),
            run_time=5,
        )
        self.play(
            Rotate(face, -PI / 4, UP),
            run_time=2,
        )
        self.wait(3)

        alt_normal = normal_vect.copy()
        alt_normal.clear_updaters()
        alt_normal.rotate(PI, UP, about_point=face.get_center())
        alt_normal.set_color(YELLOW)

        self.add(alt_normal, face, normal_vect, arc, theta)
        self.play(ShowCreation(alt_normal))
        self.wait()
        self.play(FadeOut(alt_normal))

        new_graph.generate_target()
        new_graph.target.flip(RIGHT)
        new_graph.target.move_to(graph.get_end(), DL)

        self.play(
            MoveToTarget(new_graph),
            final_formula.get_parts_by_tex("|").animate.set_opacity(1),
        )
        self.play(
            final_formula.animate.next_to(axes, DOWN)
        )
        self.wait()
        self.play(Rotate(face, -PI / 2, UP), run_time=5)
        self.wait(10)
