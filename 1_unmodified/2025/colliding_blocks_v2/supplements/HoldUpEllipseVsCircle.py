# ==============================================================================
# Scene:      HoldUpEllipseVsCircle
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 485-534)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpEllipseVsCircle.py HoldUpEllipseVsCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HoldUpEllipseVsCircle(InteractiveScene):
    def construct(self):
        # Show pi
        radius = 3
        circle = Circle(radius=radius)
        circle.set_stroke(WHITE, 3)

        radial_line = Line()
        radial_line.set_stroke(BLUE, 3)
        radial_line.f_always.put_start_and_end_on(lambda: ORIGIN, circle.get_end)
        radial_label = Tex(R"1", font_size=48)
        radial_label.add_updater(lambda m: m.move_to(
            radial_line.get_center() + 0.1 * rotate_vector(radial_line.get_vector(), -90 * DEG),
        ))

        theta_tracker = ValueTracker(0)
        get_theta = theta_tracker.get_value
        arc = always_redraw(lambda: Arc(0, get_theta(), radius=radius).set_stroke(RED, 5))
        arc_len_label = DecimalNumber(0, show_ellipsis=True, num_decimal_places=5)
        arc_len_label.set_color(RED)
        arc_len_label.f_always.set_value(get_theta)
        arc_len_label.f_always.move_to(lambda: 1.4 * arc.get_end())

        self.add(radial_line, radial_label)
        self.play(ShowCreation(circle, run_time=3))
        self.add(arc, arc_len_label)
        self.play(theta_tracker.animate.set_value(PI), run_time=3)
        self.wait()
        circle_group = VGroup(circle, radial_line, radial_label, arc, arc_len_label)
        circle_group.clear_updaters()

        # Make the comparison
        morty = Mortimer(mode="raise_right_hand").flip()
        morty.to_edge(DOWN)

        circle_group.target = circle_group.generate_target()
        circle_group.target.set_height(3)
        circle_group.target.next_to(morty.get_corner(UR), UP, buff=0.5)
        circle_group.target[1:].set_opacity(0)

        self.play(
            MoveToTarget(circle_group),
            VFadeIn(morty),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(morty.change("raise_left_hand", look_at=2 * UL))
        for _ in range(2):
            self.play(Blink(morty))
            self.wait(2)
