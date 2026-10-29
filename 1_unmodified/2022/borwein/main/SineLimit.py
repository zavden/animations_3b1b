# ==============================================================================
# Scene:      SineLimit
# Source:     videos/_2022/borwein/main.py (lines 318-404)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SineLimit.py SineLimit -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SineLimit(InteractiveScene):
    def construct(self):
        axes = Axes((-4, 4), (-2, 2), width=14, height=7, axis_config=dict(tick_size=0))
        radius = axes.x_axis.unit_size
        circle = Circle(radius=radius)
        circle.move_to(axes.get_origin())
        circle.set_stroke(WHITE, 1)

        self.add(axes, circle)

        # Set up components
        x_tracker = ValueTracker(1)
        get_x = x_tracker.get_value
        origin = axes.get_origin()

        def get_point():
            x = get_x()
            return axes.c2p(math.cos(x), math.sin(x))

        arc = VMobject().set_stroke(YELLOW, 3)
        arc.add_updater(lambda m: m.match_points(Arc(
            radius=radius,
            arc_center=origin,
            start_angle=0,
            angle=get_x(),
        )))

        h_line = Line()
        h_line.set_stroke(RED)
        h_line.add_updater(lambda m: m.put_start_and_end_on(
            get_point(),
            get_point()[0] * RIGHT,
        ))

        radial_line = Line()
        radial_line.add_updater(lambda m: m.put_start_and_end_on(origin, get_point()))

        one_label = Integer(1, font_size=24)
        one_label.add_updater(lambda m: m.next_to(
            radial_line.get_center(),
            normalize(rotate_vector(radial_line.get_vector(), PI / 2)),
            buff=SMALL_BUFF,
        ))
        sine_label = OldTex(R"\sin(x)", font_size=24)
        sine_label.set_backstroke()
        sine_label.add_updater(lambda m: m.set_max_height(0.2 * h_line.get_height()))
        sine_label.add_updater(lambda m: m.next_to(h_line, LEFT, buff=0.25 * m.get_width()))

        x_label = OldTex("x", font_size=24)
        x_label.add_updater(lambda m: m.match_width(sine_label[0][4]))
        x_label.add_updater(lambda m: m.next_to(arc.pfp(0.5), RIGHT, buff=m.get_height()))

        self.add(arc, h_line, radial_line)
        self.add(one_label)
        self.add(sine_label)
        self.add(x_label)

        value_label = VGroup(
            OldTex(R"\frac{\sin(x)}{x} = "),
            DecimalNumber(1, num_decimal_places=4)
        )
        value_label.arrange(RIGHT, buff=SMALL_BUFF)
        value_label.fix_in_frame()
        value_label.to_corner(UR)
        value_label.add_updater(lambda m: m[1].set_value(math.sin(get_x()) / get_x()))
        self.add(value_label)

        # Zoom in
        frame = self.camera.frame
        frame.set_height(4)
        x_tracker.add_updater(lambda m: m.set_value((1 / (self.time**1.5 + 1.5))))
        self.add(x_tracker)

        target_frame = frame.deepcopy()
        target_frame.add_updater(lambda m: m.set_height(4 * h_line.get_height()).move_to(h_line.get_bottom()))
        self.add(target_frame)

        alpha_tracker = ValueTracker(0)
        get_alpha = alpha_tracker.get_value

        self.play(
            UpdateFromFunc(
                frame, lambda m: m.interpolate(m, target_frame, get_alpha()),
                run_time=15,
            ),
            alpha_tracker.animate.set_value(1 / 30).set_anim_args(run_time=1)
        )
