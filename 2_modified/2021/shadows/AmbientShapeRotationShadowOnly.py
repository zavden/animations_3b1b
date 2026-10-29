# ==============================================================================
# Scene:      AmbientShapeRotationShadowOnly
# Source:     videos/_2021/shadows.py (lines 2188-2189)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AmbientShapeRotationShadowOnly.py AmbientShapeRotationShadowOnly -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - play(..., path_arc=PI) -> animate(path_arc=PI) (Scene.play no longer accepts path_arc)
#   - ShadowScene: set_style(**plane_style/object_style) no longer accepts loose reflectiveness/gloss/shadow; the helper set_style_with_shading (set_style + set_shading) is used
#   - project_to_xy_plane: the shadow fell at z=-0.01 and was not drawn under the translucent plane; it is raised 0.03 above the plane
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/cat_outline.svg  (_lib/assets/generated/2021/shadows/make_shadows_assets.py)
#   - _lib/assets/svg_images/dog_outline.svg  (_lib/assets/generated/2021/shadows/make_shadows_assets.py)
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


class AmbientShapeRotationPreimage(ShadowScene):
    inf_light = False
    display_mode = "preimage_only"  # Or "full_3d" or "shadow_only"
    rotate_in_3d = True
    only_show_shadow = False

    def construct(self):
        # Setup
        display_mode = self.display_mode
        frame = self.camera.frame
        frame.set_height(6)
        light = self.light
        light.move_to(75 * OUT)

        shape = self.solid
        fc = 2.5 * OUT
        shape.move_to(fc)

        self.solid.rotate(-0.5 * PI)
        self.solid.insert_n_curves(20)
        preimage = self.solid.deepcopy()
        preimage.move_to(ORIGIN)
        rotated = self.solid

        self.remove(self.shadow)
        shadow = rotated.deepcopy()
        shadow.set_fill(interpolate_color(BLUE_E, BLACK, 0.5), 0.7)
        shadow.set_stroke(BLACK, 1)

        def update_shadow(shadow):
            shadow.set_points(
                np.apply_along_axis(
                    lambda p: project_to_xy_plane(self.light.get_center(), p),
                    1, rotated.get_points()
                )
            )
            return shadow

        shadow.add_updater(update_shadow)

        rotated.axis_tracker = VectorizedPoint(RIGHT)
        rotated.angle_tracker = ValueTracker(0)
        rotated.rot_speed_tracker = ValueTracker(0.15)

        def update_rotated(mob, dt):
            mob.set_points(preimage.get_points())
            mob.shift(fc)
            axis = mob.axis_tracker.get_location()
            angle = mob.angle_tracker.get_value()
            speed = mob.rot_speed_tracker.get_value()
            mob.axis_tracker.rotate(speed * dt, axis=OUT, about_point=ORIGIN)
            mob.angle_tracker.increment_value(speed * dt)
            mob.rotate(angle, axis, about_point=fc)
            return rotated

        rotated.add_updater(update_rotated)

        # Conditionals
        if display_mode == "full_3d":
            preimage.set_opacity(0)
            self.add(shadow)
            self.add(rotated)

            z_axis = VGroup(
                Line(ORIGIN, fc),
                Line(fc, 10 * OUT),
            )
            z_axis.set_stroke(WHITE, 1)
            self.add(z_axis[0], rotated, z_axis[1])

            orientation_arrows = VGroup(
                Vector(RIGHT, stroke_color=RED_D),
                Vector(UP, stroke_color=GREEN_D),
                Vector(OUT, stroke_color=BLUE_D),
            )

            orientation_arrows.set_stroke(opacity=0.85)
            orientation_arrows.shift(fc)
            orientation_arrows.save_state()
            orientation_arrows.add_updater(lambda m: m.restore().rotate(
                rotated.angle_tracker.get_value(),
                rotated.axis_tracker.get_location(),
            ))
            orientation_arrows.add_updater(lambda m: m.shift(fc - m[0].get_start()))
            orientation_arrows.apply_depth_test()
            self.add(orientation_arrows)

            proj_lines = always_redraw(lambda: VGroup(*(
                Line(
                    rotated.pfp(a),
                    flat_project(rotated.pfp(a))
                ).set_stroke(WHITE, 0.5, 0.2)
                for a in np.linspace(0, 1, 100)
            )))
            self.add(proj_lines)

            frame.reorient(20, 70)
            self.init_frame_rotation()
            # frame_speed = -0.02
            # frame.add_updater(lambda f, dt: f.increment_theta(frame_speed * dt))
        elif display_mode == "shadow_only":
            frame.reorient(0, 0)
            frame.set_height(3)
            rotated.set_opacity(0)
            preimage.set_opacity(0)
            self.glow.set_opacity(0.2)
            self.add(rotated)
            self.add(shadow)
        elif display_mode == "preimage_only":
            self.glow.set_opacity(0)
            self.remove(self.plane)
            self.add(preimage)
            frame.reorient(0, 0)
            frame.set_height(3)
            rotated.set_opacity(0)

        # Just hang around
        self.wait(15)

        # Change to cat
        cat = SVGMobject("cat_outline").family_members_with_points()[0]
        dog = SVGMobject("dog_outline").family_members_with_points()[0]
        dog.insert_n_curves(87)
        for mob in cat, dog:
            mob.match_style(preimage)
            mob.replace(preimage, dim_to_match=0)
        pass

        # Stretch
        self.play(rotated.rot_speed_tracker.animate.set_value(0))
        rotated.rot_speed = 0
        for axis, diag in zip((0, 1, 0, 1), (False, False, True, True)):
            preimage.generate_target()
            if diag:
                preimage.target.rotate(PI / 4)
            preimage.target.stretch(2, axis)
            if diag:
                preimage.target.rotate(-PI / 4)
            self.play(
                MoveToTarget(preimage),
                rate_func=there_and_back,
                run_time=4
            )
        self.wait(5)
        self.play(rotated.rot_speed_tracker.animate.set_value(0.1))

        # Change shape
        cat = SVGMobject("cat_outline").family_members_with_points()[0]
        dog = SVGMobject("dog_outline").family_members_with_points()[0]
        dog.insert_n_curves(87)
        for mob in cat, dog:
            mob.match_style(preimage)
            mob.replace(preimage, dim_to_match=0)
        self.play(Transform(preimage, cat, run_time=4))
        cat.insert_n_curves(87)
        preimage.become(cat)
        self.wait(2)

        # More shape changes
        self.play(
            preimage.animate.scale(2),
            rate_func=there_and_back,
            run_time=3,
        )
        # CHANGE: Scene.play no longer accepts path_arc; it goes in animate(...)
        self.play(
            preimage.animate(path_arc=PI).become(dog),
            rate_func=there_and_back_with_pause,  # Or rather, with paws...
            run_time=5,
        )
        self.wait(6)

        # Bring light source closer
        self.play(rotated.rot_speed_tracker.animate.set_value(0))
        anims = [
            light.animate.move_to(4 * OUT)
        ]

        angle = rotated.angle_tracker.get_value()
        angle_anim = rotated.angle_tracker.animate.set_value(np.round(angle / TAU, 0) * TAU)

        if self.display_mode == "full_3d":
            light_lines = self.get_light_lines(shadow)
            lso = light_lines[0].get_stroke_opacity()
            pso = proj_lines[0].get_stroke_opacity()
            proj_lines.clear_updaters()
            anims += [
                UpdateFromAlphaFunc(proj_lines, lambda m, a: m.set_stroke(opacity=pso * (1 - a))),
                UpdateFromAlphaFunc(light_lines, lambda m, a: m.set_stroke(opacity=lso * a)),
                angle_anim,
                frame.animate.reorient(20, 70).set_height(8),
            ]
            frame.clear_updaters()
        if self.display_mode == "shadow_only":
            anims += [
                frame.animate.set_height(10),
                angle_anim,
            ]
        self.play(*anims, run_time=4)
        self.wait()
        rotated.axis_tracker.move_to(UP)
        self.play(
            rotated.angle_tracker.animate.set_value(70 * DEGREES + TAU),
            run_time=2
        )
        self.play(
            preimage.animate.stretch(1.5, 0),
            rate_func=there_and_back,
            run_time=5,
        )
        anims = [rotated.axis_tracker.animate.move_to(RIGHT)]
        if self.display_mode == "full_3d":
            anims.append(frame.animate.reorient(-20, 70))
        self.play(*anims, run_time=2)
        self.play(
            preimage.animate.stretch(2, 1),
            rate_func=there_and_back,
            run_time=7,
        )

        # More ambient motion
        self.play(rotated.rot_speed_tracker.animate.set_value(0.1))
        self.wait(30)

    def get_solid(self):
        face = Square(side_length=2)
        face.set_fill(BLUE, 0.5)
        face.set_stroke(WHITE, 1)
        return face


class AmbientShapeRotationShadowOnly(AmbientShapeRotationPreimage):
    display_mode = "shadow_only"
