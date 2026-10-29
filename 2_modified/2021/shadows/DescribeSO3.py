# ==============================================================================
# Scene:      DescribeSO3
# Source:     videos/_2021/shadows.py (lines 823-922)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DescribeSO3.py DescribeSO3 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DecimalMatrix: element_to_mobject_config -> num_decimal_places + decimal_config (current API)
#   - ShadowScene: set_style(**plane_style/object_style) no longer accepts loose reflectiveness/gloss/shadow; the helper set_style_with_shading (set_style + set_shading) is used
#   - project_to_xy_plane: the shadow fell at z=-0.01 and was not drawn under the translucent plane; it is raised 0.03 above the plane
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
    # CHANGE: the shadow fell at z=-0.01 (under the plane) and was not drawn; it is raised 0.03 above the plane
    return p1 - (z2 / vect[2]) * vect + 0.03 * OUT


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


class DescribeSO3(ShadowScene):
    def construct(self):
        frame = self.camera.frame
        frame.set_z(1)
        frame.reorient(0)
        cube = self.solid
        cube.set_opacity(0.95)
        cube.move_to(ORIGIN)
        self.remove(self.plane)
        self.remove(self.shadow)

        x_point = VectorizedPoint(cube.get_right())
        y_point = VectorizedPoint(cube.get_top())
        z_point = VectorizedPoint(cube.get_zenith())
        cube.add(x_point, y_point, z_point)

        def get_matrix():
            return np.array([
                x_point.get_center(),
                y_point.get_center(),
                z_point.get_center(),
            ]).T

        def get_mat_mob():
            matrix = DecimalMatrix(
                get_matrix(),
                # CHANGE: DecimalMatrix no longer accepts element_to_mobject_config: num_decimal_places goes directly and the rest in decimal_config
                num_decimal_places=2,
                decimal_config=dict(
                    edge_to_fix=LEFT,
                    include_sign=True,
                ),
                h_buff=2.0,
                element_alignment_corner=LEFT,
            )
            matrix.fix_in_frame()
            matrix.set_height(1.25)
            brackets = matrix.get_brackets()
            brackets[1].move_to(brackets[0].get_center() + 3.45 * RIGHT)
            matrix.to_corner(UL)
            return matrix

        matrix = always_redraw(get_mat_mob)
        self.add(matrix)

        # Space of orientations
        self.begin_ambient_rotation(cube, speed=0.4)
        self.wait(2)

        question = Text("What is the space of all orientations?")
        question.to_corner(UR)
        question.fix_in_frame()
        SO3 = OldTex("SO(3)")
        SO3.next_to(question, DOWN)
        SO3.set_color(BLUE)
        SO3.fix_in_frame()

        self.play(Write(question))
        self.wait(2)
        self.play(FadeIn(SO3, DOWN))
        self.wait(2)
        self.play(SO3.animate.next_to(matrix, DOWN, MED_LARGE_BUFF))
        self.wait(5)

        new_question = Text(
            "What probability distribution are we placing\n"
            "on the space of all orientations?",
            t2c={"probability distribution": YELLOW},
            t2s={"probability distribution": ITALIC},
        )
        new_question.match_width(question)
        new_question.move_to(question, UP)
        new_question.fix_in_frame()

        n = len("the space of all orientations?")
        self.play(
            FadeTransform(question[-n:], new_question[-n:]),
            FadeOut(question[:-n]),
            FadeIn(new_question[:-n]),
        )
        self.wait()
        cube.clear_updaters()

        N = 15
        cube_field = cube.get_grid(N, N)
        cube_field.set_height(10)

        for n, c in enumerate(cube_field):
            c.rotate(PI * (n // N) / N, axis=RIGHT)
            c.rotate(PI * (n % N) / N, axis=UP)
            for face in c:
                face.set_stroke(width=0)
            self.sort_to_camera(c)

        matrix.clear_updaters()
        self.play(
            FadeTransform(cube, cube_field[0]),
            LaggedStartMap(FadeIn, cube_field, run_time=15, lag_ratio=0.1)
        )
        self.add(cube_field)
        self.wait()
