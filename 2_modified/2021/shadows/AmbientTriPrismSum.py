# ==============================================================================
# Scene:      AmbientTriPrismSum
# Source:     videos/_2021/shadows.py (lines 5665-5681)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AmbientTriPrismSum.py AmbientTriPrismSum -w -m --fps 15
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


def get_overline(mob):
    overline = Underline(mob).next_to(mob, UP, buff=0.05)
    overline.set_stroke(WHITE, 2)
    return overline


def get_key_result(solid_name, color=BLUE):
    eq = OldTex(
        "\\text{Area}\\big(\\text{Shadow}(\\text{" + solid_name + "})\\big)",
        "=",
        "\\frac{1}{2}", "{c}", "\\cdot",
        "(\\text{Surface area})",
        tex_to_color_map={
            "\\text{Shadow}": GREY_B,
            f"\\text{{{solid_name}}}": color,
            "\\text{Solid}": BLUE,
            "{c}": RED,
        }
    )
    eq.add_to_back(get_overline(eq[:5]))
    return eq


def get_surface_area(solid):
    return sum(get_norm(f.get_area_vector()) for f in solid)


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


class ShadowsOfDodecahedron(ShadowScene):
    inf_light = True

    def construct(self):
        # Setup
        self.camera.frame.set_height(7)
        self.camera.frame.shift(OUT)
        dodec = self.solid
        dodec.scale(5 / dodec[0].get_arc_length())
        outline = self.get_shadow_outline()
        area = DecimalNumber(font_size=36)
        area.move_to(outline)
        area.add_updater(lambda m: m.set_value(get_norm(outline.get_area_vector()) / (self.unit_size**2)))
        area.add_updater(lambda m: m.fix_in_frame())
        area.move_to(3.15 * DOWN)

        self.init_frame_rotation()

        ssf = 1.5
        self.wait()
        self.play(dodec.animate.space_out_submobjects(ssf))
        self.play(Rotate(dodec, PI, axis=RIGHT, run_time=6))
        self.play(dodec.animate.space_out_submobjects(1 / ssf))
        self.begin_ambient_rotation(dodec)

        self.play(
            VFadeIn(outline),
            VFadeIn(area),
        )

        # Add dot and line
        dot = GlowDot(0.5 * DR)
        line = DashedLine(10 * OUT, ORIGIN)
        line.set_stroke(YELLOW, 1)

        def dodec_sdf(point):
            return max(*(
                np.dot(point - pent.get_center(), pent.get_unit_normal())
                for pent in dodec
            ))

        def update_line(line):
            line.move_to(dot.get_center(), IN)
            for dash in line:
                dist = dodec_sdf(dash.get_center())
                dash.set_stroke(
                    opacity=interpolate(0.1, 1.0, clip(10 * dist, -0.5, 0.5) + 0.5)
                )
                dash.inside = (dist < 0)

        line.add_updater(update_line)

        self.play(ShowCreation(line, rate_func=rush_into))
        self.play(FadeIn(dot, rate_func=rush_from))

        # Just wait
        for n in range(8):
            self.play(dot.animate.move_to(midpoint(
                outline.get_center(),
                outline.pfp(random.random()),
            )), run_time=5)

    def get_solid(self):
        solid = self.get_solid_no_style()
        solid.set_stroke(WHITE, 1)
        solid.set_fill(self.solid_fill_color, 0.8)
        solid.set_gloss(0.1)
        solid.set_shadow(0.4)
        solid.set_reflectiveness(0.4)
        group = Group(*solid)
        group.deactivate_depth_test()
        group.add_updater(lambda m: self.sort_to_camera(m))
        return group

    def get_solid_no_style(self):
        dodec = Dodecahedron()
        dodec.scale((32 / get_surface_area(dodec))**0.5)
        return dodec


class AmbientDodecahedronShadow(ShadowsOfDodecahedron):
    solid_name = "Dodecahedron"
    solid_fill_color = BLUE_E
    name_color = BLUE_D

    def construct(self):
        self.camera.frame.reorient(20, 80)
        self.camera.frame.set_z(3)

        eq = get_key_result(self.solid_name, color=self.name_color)
        eq.to_edge(UP)
        eq.fix_in_frame()
        self.add(eq)

        self.init_frame_rotation()
        self.play(LaggedStart(*map(Write, self.solid)))
        self.add(self.solid)

        outline = self.get_shadow_outline()
        area_label = self.get_shadow_area_label()
        # area_label.scale(0.7)
        area_label.move_to(2.75 * DOWN).to_edge(LEFT)
        area_label.add_updater(lambda m: m.fix_in_frame())
        surface_area = get_surface_area(self.solid)
        surface_area /= (self.unit_size**2)
        sa_label = VGroup(Text("Surface area: "), DecimalNumber(surface_area))
        sa_label.arrange(RIGHT)
        sa_label.match_y(area_label)
        sa_label.to_edge(RIGHT)
        sa_label.set_backstroke()
        sa_label.fix_in_frame()

        self.play(
            *map(VFadeIn, (outline, area_label, sa_label))
        )
        self.add(outline)
        self.add(area_label)

        self.begin_ambient_rotation(self.solid, about_point=self.solid.get_center())
        self.wait(30)


class AmbientTriPrismSum(AmbientDodecahedronShadow):
    solid_name = "Triangular Prism"
    solid_fill_color = interpolate_color(TEAL_E, BLACK, 0.25)
    name_color = TEAL_D

    def get_solid_no_style(self):
        triangle = RegularPolygon(3)
        tri1, tri2 = triangle.replicate(2)
        tri2.shift(3 * OUT)
        sides = []
        verts1 = tri1.get_anchors()
        verts2 = tri2.get_anchors()
        for (a, b), (c, d) in zip(adjacent_pairs(verts1), adjacent_pairs(verts2)):
            sides.append(Polygon(a, b, d, c))
        result = VGroup(tri1, *sides, tri2)
        result.scale((16 / get_surface_area(result))**0.5)
        return result
