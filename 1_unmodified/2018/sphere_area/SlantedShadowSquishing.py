# ==============================================================================
# Scene:      SlantedShadowSquishing
# Source:     videos/_2018/sphere_area.py (lines 1055-1093)
# Category:   1 · Renders unmodified
# Includes code copied from: _2021/shadows.py
#
# Run from this folder:
#     manimgl SlantedShadowSquishing.py SlantedShadowSquishing -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/shadows.py -----

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



# ----- From _2018/sphere_area.py -----

class SlantedShadowSquishing(ShowShadows):
    CONFIG = {
        "num_reorientations": 4,
        "random_seed": 2,
    }

    def setup(self):
        ShowShadows.setup(self)
        self.surface_area_label.fade(1)
        self.shadow_area_label.fade(1)
        self.shadow_area_decimal.fade(1)

    def construct(self):
        # Show creation
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-150 * DEGREES,
        )
        self.begin_ambient_camera_rotation(0.01)
        square = self.obj3d.deepcopy()
        square.clear_updaters()
        shadow = always_redraw(lambda: get_shadow(square))

        # Reorient
        self.add(square, shadow)
        for n in range(self.num_reorientations):
            angle = 40 * DEGREES
            self.play(
                Rotate(square, angle, axis=RIGHT),
                run_time=2
            )

    def get_object(self):
        square = Square()
        square.set_shade_in_3d(True)
        square.set_height(2)
        square.set_stroke(WHITE, 0.5)
        square.set_fill(BLUE_C, 1)
        return square
