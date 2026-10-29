# ==============================================================================
# Scene:      AveragePentagonShadow
# Source:     videos/_2021/shadows.py (lines 2443-2445)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AveragePentagonShadow.py AveragePentagonShadow -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - construct used 'fc' without defining it (NameError in the original); self.fc is saved in setup and used as about_point
#   - ShadowScene: set_style(**plane_style/object_style) no longer accepts loose reflectiveness/gloss/shadow; the helper set_style_with_shading (set_style + set_shading) is used
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/cat_outline.svg  (_lib/assets/generated/2021/shadows/make_shadows_assets.py)
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


class SingleFaceRandomRotation(ShadowScene):
    initial_wait_time = 0
    inf_light = True
    n_rotations = 1
    total_time = 60
    plane_dims = (8, 8)
    frame_rot_speed = 0.02
    theta0 = -20 * DEGREES
    CONFIG = {"random_seed": 0}

    def setup(self):
        super().setup()
        np.random.seed(self.random_seed)
        frame = self.camera.frame
        frame.set_height(5.0)
        frame.set_z(1.75)
        frame.set_theta(self.theta0)
        face = self.solid
        face.shift(0.25 * IN)
        fc = face.get_center()
        # CHANGE: the original uses `fc` in construct without defining it (NameError); it is saved in self.fc
        self.fc = fc
        z_axis = self.z_axis = VGroup(Line(ORIGIN, fc), Line(fc, 10 * OUT))
        z_axis.set_stroke(WHITE, 0.5)
        self.add(z_axis[0], face, z_axis[1])

        arrows = VGroup(
            Line(ORIGIN, RIGHT, color=RED_D),
            Line(ORIGIN, UP, color=GREEN_D),
            VGroup(
                Vector(OUT, stroke_width=4, stroke_color=BLACK),
                Vector(OUT, stroke_width=3, stroke_color=BLUE_D),
            )
        )
        arrows[:2].set_stroke(width=2)
        arrows.set_stroke(opacity=0.8)
        arrows.shift(fc)
        arrows.set_stroke(opacity=0.8)
        face.add(arrows[:2])

        face = Group(face, arrows[2])
        face.add_updater(lambda m: self.sort_to_camera(face))
        self.face = self.solid = face

        arrow_shadow = get_shadow(arrows)
        arrow_shadow.set_stroke(width=1)
        arrow_shadow[2].set_stroke(width=[1, 1, 4, 0])
        self.add(arrow_shadow)

        self.add(z_axis[0], face, z_axis[1])

    def construct(self):
        frame = self.camera.frame
        face = self.face

        frame.add_updater(lambda f, dt: f.increment_theta(self.frame_rot_speed * dt))
        self.wait(self.initial_wait_time)
        for x in range(self.n_rotations):
            self.random_toss(
                face,
                # CHANGE: `fc` was not defined in construct (NameError); self.fc from setup is used
                about_point=self.fc,
                angle=3 * PI,
                # run_time=1.5,
                run_time=8,
                rate_func=smooth,
            )
            self.wait()

        self.wait(self.total_time - 2 - self.initial_wait_time)

    def get_solid(self):
        face = Square(side_length=2)
        face.set_fill(BLUE_E, 0.75)
        face.set_stroke(WHITE, 0.5)
        return face


class AverageFaceShadow(SingleFaceRandomRotation):
    inf_light = True
    plane_dims = (16, 8)
    n_samples = 50

    def construct(self):
        # Random shadows
        self.camera.frame.set_height(6)
        face = self.face
        shadow = self.shadow
        shadow.add_updater(lambda m: m.set_fill(BLACK, 0.25))
        shadow.update()
        point = face[0].get_center()
        shadows = VGroup()
        n_samples = self.n_samples
        self.remove(self.z_axis)

        self.init_frame_rotation()
        self.add(shadows)
        for n in range(n_samples):
            self.randomly_reorient(face, about_point=point)
            if n == n_samples - 1:
                normal = next(
                    sm.get_unit_normal()
                    for sm in face.family_members_with_points()
                    if isinstance(sm, VMobject) and sm.get_fill_opacity() > 0
                )
                mat = z_to_vector(normal)
            #     face.apply_matrix(np.linalg.inv(mat), about_point=point)
            shadow.update()
            sc = shadow.copy()
            sc.clear_updaters()
            shadows.add(sc)
            shadows.set_fill(BLACK, 1.5 / len(shadows))
            shadows.set_stroke(opacity=10 / len(shadows))
            self.wait(0.1)

        # Fade out shadow
        self.remove(shadow)
        sc = shadow.copy().clear_updaters()
        self.play(FadeOut(sc))
        self.wait()

        # Scaling
        self.play(
            face.animate.scale(0.5, about_point=point),
            shadows.animate.scale(0.5, about_point=ORIGIN),
            run_time=3,
            rate_func=there_and_back,
        )
        for axis in [0, 1]:
            self.play(
                face.animate.stretch(2, axis, about_point=point),
                shadows.animate.stretch(2, axis, about_point=ORIGIN),
                run_time=3,
                rate_func=there_and_back,
            )
        self.wait()

        # Ambient rotations 106 plays
        self.play(
            self.camera.frame.animate.reorient(-10).shift(2 * LEFT),
        )
        self.add(shadow)
        for n in range(100):
            self.randomly_reorient(face, about_point=point)
            self.wait(0.2)


class AverageCatShadow(AverageFaceShadow):
    n_samples = 50

    def setup(self):
        super().setup()
        self.replace_face()

    def replace_face(self):
        face = self.face

        shape = self.get_shape().family_members_with_points()[0]
        shape.match_style(face[0])
        shape.replace(face[0])

        face[0].set_points(shape.get_points())
        face[0].set_gloss(0.25)
        face[0][0].set_gloss(0)

        self.solid = face
        self.remove(self.shadow)
        self.add_shadow()

    def get_shape(self):
        return SVGMobject("cat_outline")


class AveragePentagonShadow(AverageCatShadow):
    def get_shape(self):
        return RegularPolygon(5)
