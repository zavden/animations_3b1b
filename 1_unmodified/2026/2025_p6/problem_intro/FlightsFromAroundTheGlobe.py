# ==============================================================================
# Scene:      FlightsFromAroundTheGlobe
# Source:     videos/_2026/2025_p6/problem_intro.py (lines 50-140)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FlightsFromAroundTheGlobe.py FlightsFromAroundTheGlobe -w -m --fps 15
# ==============================================================================

import importlib.util
from manim_imports_ext import *

def _load_sibling(name):
    """
    Import a module from this file's directory. Needed since the directory
    name starts with a digit, so it cannot be reached by a dotted import.
    """
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).parent / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_geography = _load_sibling("imo_2025_geography")


IMO_2025_PARTICIPANTS = _geography.IMO_2025_PARTICIPANTS


HOST_LATITUDE = _geography.HOST_LATITUDE


HOST_LONGITUDE = _geography.HOST_LONGITUDE


def lat_lon_to_uv(latitude, longitude):
    """
    Convert a (latitude, longitude) pair in degrees to the (u, v) parameters
    of a Sphere, whose uv_func sends u to the angle about the z-axis and v to
    the angle down from the north pole.

    A TexturedSurface built over that Sphere maps u linearly across the width
    of the image and v up its height, so this matches a standard equirect-
    angular map, with the left edge of the image at longitude 180W.
    """
    u = (longitude + 180) * DEGREES
    v = (latitude + 90) * DEGREES
    return (u, v)


def lat_lon_to_point(latitude, longitude, sphere):
    """
    Point on a given Sphere (or TexturedSurface over one) corresponding to a
    (latitude, longitude) pair in degrees.
    """
    u, v = lat_lon_to_uv(latitude, longitude)
    return sphere.uv_func(u, v) + sphere.get_center()


class FlightsFromAroundTheGlobe(InteractiveScene):
    def construct(self):
        # Add earth
        frame = self.frame
        light = self.camera.light_source
        light.move_to([10, 0, 5])
        radius = 3
        day_texture = "EarthTextureMap"
        night_texture = "NightEarthTextureMap"
        globe = TexturedSurface(Sphere(radius=3), day_texture, night_texture)
        mesh = SurfaceMesh(globe, resolution=(41, 21))
        mesh.set_stroke(WHITE, 0.5, 0.25)
        mesh.rotate(90 * DEG)

        frame.reorient(-163, 64, 0)
        self.add(globe, mesh)

        # Add start and end points
        student_height = 0.07
        dot_radius = 0.025
        dot_glow_factor = 0.1
        students = Group()
        for country, n_participants, lat, lon, color in IMO_2025_PARTICIPANTS:
            point = lat_lon_to_point(lat, lon, globe)
            for n in range(n_participants):
                randy = Randolph(mode="pondering", color=color, height=student_height)
                randy.rotate(angle_of_vector(point) + 90 * DEG)
                randy.move_to(globe.get_zenith())
                randy.apply_matrix(z_to_vector(normalize(point)), about_point=ORIGIN)
                students.add(randy)
        target_point = lat_lon_to_point(HOST_LATITUDE, HOST_LONGITUDE, globe)
        students.shuffle()
        students.apply_depth_test()

        arcs = VGroup(
            self.get_arc_between_points(dot.get_center(), target_point).match_color(dot)
            for dot in students
        )
        arcs.set_stroke(width=1, opacity=0.5)
        arcs.apply_depth_test()

        self.add(students)

        # Animate
        lag_ratio = 1 / len(students)
        start_orientation = frame.get_euler_angles() / DEG
        target_orientation = np.array([64, 110, 0])
        end_dot = GlowDot(target_point, color="#FFCD00")
        location_title = Text("Sunshine Coast, Australia", font_size=24)
        location_title.add_updater(lambda m: m.next_to(frame.to_fixed_frame_point(end_dot.get_center()), UR, SMALL_BUFF))
        location_title.fix_in_frame()

        self.play(
            LaggedStart(
                (MoveAlongPath(student, arc)
                for student, arc in zip(students, arcs)),
                group=students,
                lag_ratio=lag_ratio,
            ),
            LaggedStart(
                (VShowPassingFlash(arc.copy().set_stroke(width=2, opacity=0.5), time_width=2)
                for arc in arcs),
                lag_ratio=lag_ratio
            ),
            UpdateFromAlphaFunc(
                frame,
                lambda m, a: m.reorient(
                    *interpolate(start_orientation, target_orientation, a),
                    interpolate(ORIGIN, np.array((-0.13, 0.06, -0.39)), a),
                    interpolate(11, 6, a),
                ),
            ),
            Rotate(light, -75 * DEG, axis=OUT, about_point=light.get_z() * OUT),
            FadeIn(end_dot, time_span=(6, 12)),
            VFadeIn(location_title, time_span=(6, 12)),
            run_time=12
        )
        self.play(FadeOut(students))
        self.wait()

    def get_arc_between_points(self, p1, p2, n_anchors=100):
        lerp_points = np.array([
            interpolate(p1, p2, alpha)
            for alpha in np.linspace(0, 1, n_anchors)
        ])
        radius = get_norm(p1)
        normalized_points = np.array([radius * normalize(p) for p in lerp_points])
        result = VMobject().set_points_smoothly(
            lerp_points + 1.2 * (normalized_points - lerp_points)
        )
        return result
