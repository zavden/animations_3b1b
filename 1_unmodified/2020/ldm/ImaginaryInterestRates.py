# ==============================================================================
# Scene:      ImaginaryInterestRates
# Source:     videos/_2020/ldm.py (lines 799-900)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImaginaryInterestRates.py ImaginaryInterestRates -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ImaginaryInterestRates(Scene):
    def construct(self):
        plane = ComplexPlane(x_min=-20, x_max=20, y_min=-20, y_max=20)
        plane.add_coordinate_labels()
        circle = Circle(radius=1)
        circle.set_stroke(YELLOW, 1)
        self.add(plane, circle)

        frame = self.camera.frame
        frame.save_state()
        frame.generate_target()
        frame.target.set_width(25)
        frame.target.move_to(8 * RIGHT + 2 * DOWN)

        dt_tracker = ValueTracker(1)

        def get_vectors(tracker=dt_tracker, plane=plane, T=8):
            dt = tracker.get_value()
            last_z = 1
            vects = VGroup()
            for t in np.arange(0, T, dt):
                next_z = last_z + complex(0, 1) * last_z * dt
                vects.add(Arrow(
                    plane.n2p(last_z),
                    plane.n2p(next_z),
                    buff=0,
                ))
                last_z = next_z
            vects.set_submobject_colors_by_gradient(YELLOW, GREEN, BLUE)
            return vects

        vects = get_vectors()

        line = Line()
        line.add_updater(lambda m, v=vects: m.put_start_and_end_on(
            ORIGIN, v[-1].get_start() if len(v) > 0 else RIGHT,
        ))

        self.add(line)
        self.play(
            ShowIncreasingSubsets(
                vects,
                rate_func=linear,
                int_func=np.ceil,
            ),
            MoveToTarget(
                frame,
                rate_func=squish_rate_func(smooth, 0.5, 1),
            ),
            run_time=8,
        )
        self.wait()
        self.play(FadeOut(line))

        self.remove(vects)
        vects = always_redraw(get_vectors)
        self.add(vects)
        self.play(
            Restore(frame),
            dt_tracker.set_value, 0.2,
            run_time=5,
        )
        self.wait()
        self.play(dt_tracker.set_value, 0.01, run_time=3)
        vects.clear_updaters()
        self.wait()

        theta_tracker = ValueTracker(0)

        def get_arc(tracker=theta_tracker):
            theta = tracker.get_value()
            arc = Arc(
                radius=1,
                stroke_width=3,
                stroke_color=RED,
                start_angle=0,
                angle=theta
            )
            return arc

        arc = always_redraw(get_arc)
        dot = Dot()
        dot.add_updater(lambda m, arc=arc: m.move_to(arc.get_end()))

        label = VGroup(
            DecimalNumber(0, num_decimal_places=3),
            OldTexText("Years")
        )
        label.arrange(RIGHT, aligned_edge=DOWN)
        label.move_to(3 * LEFT + 1.5 * UP)

        label[0].set_color(RED)
        label[0].add_updater(lambda m, tt=theta_tracker: m.set_value(tt.get_value()))

        self.add(BackgroundRectangle(label), label, arc, dot)
        for n in range(1, 5):
            target = n * PI / 2
            self.play(
                theta_tracker.set_value, target,
                run_time=3
            )
            self.wait(2)
