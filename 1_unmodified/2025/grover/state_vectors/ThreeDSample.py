# ==============================================================================
# Scene:      ThreeDSample
# Source:     videos/_2025/grover/state_vectors.py (lines 2059-2263)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl ThreeDSample.py ThreeDSample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/qc_supplements.py -----

def get_key_icon(height=0.5):
    key_icon = SVGMobject("key").rotate(135 * DEG)
    key_icon.set_fill(YELLOW)
    key_icon.set_height(height)
    return key_icon



# ----- From _2025/grover/state_vectors.py -----

class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)


class ThreeDSample(InteractiveScene):
    def construct(self):
        # Set up axes
        frame = self.frame
        x_range = y_range = z_range = (-2, 2)
        axes = ThreeDAxes(x_range, y_range, z_range, axis_config=dict(tick_size=0.05))
        plane = NumberPlane(x_range, y_range, faded_line_ratio=5)
        plane.axes.set_opacity(0)
        plane.background_lines.set_stroke(BLUE, 1, 0.5)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)

        rot_vel_tracker = ValueTracker(DEG)

        frame.reorient(-31, 71, 0, (0.22, 0.17, 0.13), 2.88)
        frame.add_updater(lambda m, dt: m.increment_theta(dt * rot_vel_tracker.get_value()))
        self.add(axes, plane, Point())

        # Add vector
        vector = Vector(normalize([1, -1, 2]), thickness=2, fill_color=TEAL)
        vector.always.set_perpendicular_to_camera(self.frame)
        vector.set_z_index(2)

        coord_array = DecimalMatrix(
            np.zeros((3, 1)),
            decimal_config=dict(include_sign=True)
        )
        coord_array.set_height(1.25)
        coord_array.to_corner(UL)
        coord_array.fix_in_frame()

        def update_coord_array(coord_array):
            for elem, coord in zip(coord_array.elements, vector.get_end()):
                elem.set_value(coord)
            coord_array.set_fill(GREY_B, border_width=1)

        coord_array.add_updater(update_coord_array)

        self.play(
            GrowArrow(vector),
            VFadeIn(coord_array),
        )
        self.play(Rotate(vector, TAU, axis=OUT, about_point=ORIGIN, run_time=6))
        self.wait(5)

        # Show 0, 1, and 2 directions
        symbols = VGroup(KetGroup(Integer(n)) for n in range(3))
        symbols.scale(0.5)
        symbols.set_backstroke(BLACK, 5)
        symbols.rotate(90 * DEG, RIGHT)
        directions = [UP + 0.5 * OUT, LEFT, LEFT]

        for symbol, direction, trg_coords in zip(symbols, directions, np.identity(3)):
            symbol.next_to(0.5 * trg_coords, direction, SMALL_BUFF)
            self.play(
                self.set_vect_anim(vector, trg_coords),
                FadeIn(symbol, 0.25 * OUT)
            )
            self.play(symbol.animate.scale(0.5).next_to(trg_coords, direction, SMALL_BUFF))
            self.wait(0.5)
        self.wait(2)

        # Highlight a secret key
        key_icon = get_key_icon()
        key_icon.rotate(90 * DEG, RIGHT)
        key_icon.match_depth(symbols[2])
        key_icon.next_to(symbols[2], LEFT, buff=0.05)

        self.play(
            FadeIn(key_icon, 0.25 * LEFT),
            symbols[2].animate.set_fill(YELLOW),
        )
        self.wait(3)

        # Go to the balanced state
        coord_rects = VGroup(
            SurroundingRectangle(elem)
            for elem in coord_array.elements
        )
        coord_rects.set_stroke(TEAL, 3)
        coord_rects.fix_in_frame()

        balanced_state = normalize([1, 1, 1])
        balance_name = Text("balanced state", font_size=16)
        balance_ket = KetGroup(Text("b", font_size=16), buff=0.035)
        for mob in [balance_name, balance_ket]:
            mob.rotate(90 * DEG, RIGHT)
            mob.next_to(balanced_state, OUT + RIGHT, buff=0.025)

        self.play(
            self.set_vect_anim(vector, balanced_state, run_time=4),
            FadeIn(balance_name, lag_ratio=0.1, time_span=(3, 4)),
        )
        self.play(LaggedStartMap(ShowCreation, coord_rects, lag_ratio=0.25))
        self.play(LaggedStartMap(FadeOut, coord_rects, lag_ratio=0.25))
        self.wait()
        self.play(
            FadeTransformPieces(balance_name, balance_ket[1]),
            Write(balance_ket[0])
        )
        self.play(rot_vel_tracker.animate.set_value(-DEG), run_time=3)
        self.wait(7)

        # Show the goal
        z_vect = vector.copy()
        z_vect.set_fill(YELLOW)

        tail = TracingTail(z_vect.get_end, stroke_color=YELLOW, time_traced=3)
        self.add(tail)
        self.wait(2)
        self.play(FadeIn(z_vect))
        self.play(
            self.set_vect_anim(z_vect, OUT, run_time=2)
        )
        self.wait(3)
        self.remove(tail)

        # Show 2d slice
        v_slice = NumberPlane(x_range, y_range, faded_line_ratio=5)
        v_slice.rotate(90 * DEG, RIGHT)
        v_slice.rotate(45 * DEG, OUT)
        v_slice.axes.set_stroke(WHITE, 1, 0.5)
        v_slice.background_lines.set_stroke(BLUE, 1, 1)
        v_slice.faded_lines.set_stroke(BLUE, 0.5, 0.25)

        b_vect_ghost = vector.copy()
        b_vect_ghost.set_fill(opacity=0.5)
        tail = TracingTail(vector.get_end, stroke_color=TEAL, time_traced=8)
        symbols[2].set_z_index(1)

        self.add(tail)
        self.play(
            frame.animate.reorient(43, 79, 0, (-0.26, 0.37, 0.15), 4.97),
            rot_vel_tracker.animate.set_value(-2 * DEG),
            FadeIn(v_slice),
            plane.animate.fade(0.75),
            axes.animate.set_stroke(opacity=0.5),
            run_time=3
        )
        self.add(b_vect_ghost)
        self.play(
            Rotate(
                vector,
                TAU,
                axis=np.cross(vector.get_end(), OUT),
                run_time=8,
                about_point=ORIGIN,
            )
        )
        self.play(
            frame.animate.reorient(-1, 79, 0, (-0.13, 0.55, 1.08), 7.67),
            coord_array.animate.set_x(0),
            run_time=2,
        )
        tail.clear_updaters()
        self.play(FadeOut(tail))
        self.wait(20)

        # Show xy line
        xy_line = v_slice.x_axis.copy()
        xy_line.set_stroke(WHITE, 3, 1)
        self.play(
            frame.animate.reorient(67, 77, 0, (-0.57, 0.12, 0.86), 6.62),
            run_time=2
        )
        self.wait(4)
        self.play(
            GrowFromCenter(xy_line),
            self.set_vect_anim(vector, normalize(UR)),
        )
        self.wait(10)
        self.play(self.set_vect_anim(vector, balanced_state))
        self.wait(20)

    def set_vect_anim(self, vector, trg_coords, run_time=1, **kwargs):
        return Rotate(
            vector,
            angle_between_vectors(vector.get_end(), trg_coords),
            axis=np.cross(vector.get_end(), trg_coords),
            about_point=ORIGIN,
            run_time=run_time,
            **kwargs
        )

    def flip_along_key_axis(self):
        # To be inserted after highlighting the key state above
        sphere = Sphere(radius=vector.get_length())
        mesh = SurfaceMesh(sphere, resolution=(51, 101))
        mesh.set_stroke(WHITE, 2, 0.1)

        key_vect = vector.copy()
        key_vect.clear_updaters()
        key_vect.set_fill(YELLOW, 0.5)

        self.add(key_vect)
        self.play(
            self.set_vect_anim(vector, normalize([1, 1, 1])),
            FadeIn(mesh)
        )
        vector.clear_updaters()
        for _ in range(4):
            self.play(
                Group(mesh, vector, key_vect).animate.stretch(-1, 2, about_point=ORIGIN),
                run_time=2
            )
            self.wait()
