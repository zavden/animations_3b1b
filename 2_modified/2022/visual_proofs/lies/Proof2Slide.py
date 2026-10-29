# ==============================================================================
# Scene:      Proof2Slide
# Source:     videos/_2022/visual_proofs/lies.py (lines 416-478)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Proof2Slide.py Proof2Slide -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - circum.set_points(vstack(line, arc)) -> arc without its first point: set_points requires 2n+1 points
# ==============================================================================

from manim_imports_ext import *

class Proof2Slide(InteractiveScene):
    def construct(self):
        # Setup
        self.add(FullScreenRectangle())
        title = OldTexText("``Proof'' \\#2", font_size=60)
        title.to_edge(UP)
        subtitle = OldTex("\\pi = 4", font_size=60)
        subtitle.next_to(title, DOWN)
        subtitle.set_color(RED)
        self.add(title, subtitle)

        # Number line
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        radius = 1.25

        circle = Circle(radius=radius)
        circle.to_edge(DOWN)
        circle.set_fill(BLUE_E, 1)
        circle.set_stroke(width=0)
        circle.rotate(-TAU / 4)

        nl = NumberLine((0, 4), width=4 * circle.get_width())
        nl.add_numbers()
        nl.move_to(2 * DOWN)

        v_lines = VGroup(*(
            DashedLine(ORIGIN, circle.get_height() * UP).move_to(nl.n2p(x), DOWN)
            for x in range(5)
        ))
        v_lines.set_stroke(GREY_B, 1)

        circum = circle.copy()
        circum.set_fill(opacity=0)
        circum.set_stroke(YELLOW, 2)

        def update_circum(circum):
            line = Line(nl.n2p(0), nl.n2p(get_t() * 4))
            arc = Arc(start_angle=-TAU / 4, angle=TAU * (1 - get_t()), radius=radius)
            arc.shift(circle.get_bottom() - arc.get_start())
            # CHANGE: set_points requires 2n+1 points (anchors and handles): the first point of the arc, which coincides with the end of the line, is removed
            circum.set_points(np.vstack([line.get_points(), arc.get_points()[1:]]))
            return circum

        circum.add_updater(update_circum)

        radial_line = Line(circle.get_bottom(), circle.get_center(), stroke_width=1)
        radial_line.add_updater(lambda m: m.set_angle(TAU * (0.75 - get_t())).shift(circle.get_center() - m.get_start()))

        circle.move_to(nl.n2p(0.5), DOWN)

        self.add(nl, circle, radial_line, circum)
        self.play(LaggedStartMap(ShowCreation, v_lines, run_time=1))

        # Roll
        self.play(circle.animate.set_x(nl.n2p(0)[0]))
        self.play(
            circle.animate.set_x(nl.n2p(4)[0]),
            t_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=4,
        )
        self.wait()
