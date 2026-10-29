# ==============================================================================
# Scene:      WalkEquatorPostTransform
# Source:     videos/_2017/borsuk.py (lines 730-960)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WalkEquatorPostTransform.py WalkEquatorPostTransform -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WalkEquatorPostTransform(GraphScene):
    CONFIG = {
        "x_labeled_nums" : [],
        "y_labeled_nums" : [],
        "graph_origin" : 2.5*DOWN + 2*LEFT,
        "curved_arrow_color" : WHITE,
        "curved_arrow_radius" : 3,
        "num_great_arcs" : 10,
    }
    def construct(self):
        self.setup_axes()
        self.add_curved_arrow()
        self.great_arc_images = self.get_great_arc_images()

        self.walk_equator()
        self.walk_tilted_equator()
        self.draw_transverse_curve()
        self.walk_transverse_curve()

    def add_curved_arrow(self):
        arc = Arc(
            start_angle = 2*np.pi/3, angle = -np.pi/2, 
            radius = self.curved_arrow_radius,
            color = self.curved_arrow_color
        )
        arc.add_tip()
        arc.move_to(self.coords_to_point(0, 7))

        self.add(arc)

    def walk_equator(self):
        equator = self.great_arc_images[0]
        dots = VGroup(Dot(), Dot())
        dots.set_color(MAROON_B)
        dot_movement = self.get_arc_walk_dot_movement(equator, dots)
        dot_movement.update(0)

        self.play(ShowCreation(equator, run_time = 3))
        self.play(FadeIn(dots[0]))
        dots[1].set_fill(opacity = 0)
        self.play(dot_movement)
        self.play(dots[1].set_fill, None, 1)
        self.play(dot_movement)
        self.play(dot_movement)

        proportion = equator.collision_point_proportion
        self.play(self.get_arc_walk_dot_movement(
            equator, dots,
            rate_func = lambda t : 2*proportion*smooth(t)
        ))
        v_line = DashedLine(FRAME_Y_RADIUS*UP, FRAME_Y_RADIUS*DOWN)
        v_line.shift(dots.get_center()[0]*RIGHT)
        self.play(ShowCreation(v_line))
        self.wait()
        self.play(FadeOut(v_line))

        dots.save_state()
        equator.save_state()
        self.play(
            equator.fade,
            dots.fade
        )

        self.first_dots = dots

    def walk_tilted_equator(self):
        equator = self.great_arc_images[0]
        tilted_eq = self.great_arc_images[1]

        dots = VGroup(Dot(), Dot())
        dots.set_color(MAROON_B)
        dot_movement = self.get_arc_walk_dot_movement(tilted_eq, dots)
        dot_movement.update(0)

        self.play(ReplacementTransform(equator.copy(), tilted_eq))
        self.wait()
        self.play(FadeIn(dots))
        self.play(dot_movement)

        proportion = tilted_eq.collision_point_proportion
        self.play(self.get_arc_walk_dot_movement(
            tilted_eq, dots,
            rate_func = lambda t : 2*proportion*smooth(t)
        ))
        v_line = DashedLine(FRAME_Y_RADIUS*UP, FRAME_Y_RADIUS*DOWN)
        v_line.shift(dots.get_center()[0]*RIGHT)
        self.play(ShowCreation(v_line))
        self.wait()
        self.play(FadeOut(v_line))
        self.play(*list(map(FadeOut, [tilted_eq, dots])))

    def draw_transverse_curve(self):
        transverse_curve = self.get_transverse_curve(self.great_arc_images)
        dots = self.first_dots
        equator = self.great_arc_images[0]

        self.play(dots.restore)
        equator.restore()
        self.great_arc_images.fade()

        target_arcs = list(self.great_arc_images[1:])
        target_dots = []
        for arc in target_arcs:
            new_dots = dots.copy()
            for dot, point in zip(new_dots, arc.x_collision_points):
                dot.move_to(point)
            target_dots.append(new_dots)

        alt_eq = equator.copy()
        alt_eq.set_points(list(reversed(alt_eq.get_points())))
        alt_dots = dots.copy()
        alt_dots.submobjects.reverse()
        target_arcs += [alt_eq, alt_eq.copy()]
        target_dots += [alt_dots, alt_dots.copy()]

        equator_transform = Succession(*[
            Transform(equator, arc, rate_func=linear)
            for arc in target_arcs
        ])
        dots_transform = Succession(*[
            Transform(dots, target, rate_func=linear)
            for target in target_dots
        ])

        self.play(
            ShowCreation(transverse_curve, lag_ratio = 0),
            equator_transform,
            dots_transform,
            run_time = 10,
            rate_func=linear,
        )
        self.wait(2)

    def walk_transverse_curve(self):
        transverse_curve = self.get_transverse_curve(self.great_arc_images)
        dots = self.first_dots

        def dot_update(dots, alpha):
            for dot, curve in zip(dots, transverse_curve):
                dot.move_to(curve.point_from_proportion(alpha))
            return dots

        for x in range(2):
            self.play(
                UpdateFromAlphaFunc(dots, dot_update),
                run_time = 4
            )
        self.play(
            UpdateFromAlphaFunc(dots, dot_update),
            run_time = 4,
            rate_func = lambda t : 0.455*smooth(t)
        )
        self.play(
            dots.set_color, YELLOW,
            dots.scale, 1.2,
            rate_func = there_and_back
        )
        self.wait()

    #######

    def get_arc_walk_dot_movement(self, arc, dots, **kwargs):
        def dot_update(dots, alpha):
            dots[0].move_to(arc.point_from_proportion(0.5*alpha))
            dots[1].move_to(arc.point_from_proportion(0.5+0.5*alpha))
            return dots
        if "run_time" not in kwargs:
            kwargs["run_time"] = 5
        return UpdateFromAlphaFunc(dots, dot_update, **kwargs)

    def sphere_to_plane(self, point):
        x, y, z = point
        return np.array([
            x - 2*x*z + y + 1,
            y+0.5*y*np.cos(z*np.pi),
            0
        ])

    def sphere_point(self, portion_around_equator, equator_tilt = 0):
        theta = portion_around_equator*2*np.pi
        point = np.cos(theta)*RIGHT + np.sin(theta)*UP
        phi = equator_tilt*np.pi
        return rotate_vector(point, phi, RIGHT)

    def get_great_arc_images(self):
        curves = VGroup(*[
            ParametricCurve(
                lambda t : self.sphere_point(t, s)
            ).apply_function(self.sphere_to_plane)
            for s in np.arange(0, 1, 1./self.num_great_arcs)
            # for s in [0]
        ])
        curves.set_color(YELLOW)
        curves[0].set_color(RED)
        for curve in curves:
            antipodal_x_diff = lambda x : \
                curve.point_from_proportion(x+0.5)[0]-\
                curve.point_from_proportion(x)[0]
            last_x = 0                
            last_sign = np.sign(antipodal_x_diff(last_x))
            for x in np.linspace(0, 0.5, 100):
                sign = np.sign(antipodal_x_diff(x))
                if sign != last_sign:
                    mean = np.mean([last_x, x])
                    curve.x_collision_points = [
                        curve.point_from_proportion(mean),
                        curve.point_from_proportion(mean+0.5),
                    ]
                    curve.collision_point_proportion = mean
                    break
                last_x = x
                last_sign = sign
        return curves

    def get_transverse_curve(self, gerat_arc_images):
        points = list(it.chain(*[
            [
                curve.x_collision_points[i]
                for curve in gerat_arc_images
            ]
            for i in (0, 1)
        ]))
        full_curve = VMobject(close_new_points = True)
        full_curve.set_points_smoothly(points + [points[0]])
        full_curve.set_color(MAROON_B)
        first_half = full_curve.copy().pointwise_become_partial(
            full_curve, 0, 0.5
        )
        second_half = first_half.copy().rotate(np.pi, RIGHT)
        broken_curve = VGroup(first_half, second_half)
        return broken_curve
