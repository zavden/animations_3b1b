# ==============================================================================
# Scene:      HiddenConnections
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1161-1220)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HiddenConnections.py HiddenConnections -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HiddenConnections(InteractiveScene):
    def construct(self):
        # Transition from circle
        circle = Circle(radius=2)
        circle.set_stroke(WHITE, 3)
        self.add(circle)
        self.wait()

        background = FullScreenFadeRectangle()
        background.set_fill(GREY_E, 0.5)
        background.set_z_index(-1)

        # Screens
        screens = ScreenRectangle(height=3.0).get_grid(2, 2, h_buff=2.0, v_buff=1.5)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 1)
        screens.set_height(7.5)

        q_marks = VGroup(
            Tex(R"???", font_size=72).move_to(screen)
            for screen in screens
        )

        connections = VGroup()
        for s1, s2 in it.combinations(screens, 2):
            vect = s2.get_center() - s1.get_center()
            line = Line(s1.get_corner(vect), s2.get_corner(-vect))
            connections.add(line)
        connections.set_stroke(BLUE, 3)
        screens[1:].set_fill(GREY_E, 0.5)

        self.remove(circle)
        self.play(
            FadeIn(background),
            ReplacementTransform(circle.replicate(len(connections)), connections, lag_ratio=0.1),
            LaggedStartMap(FadeIn, screens, scale=1.25),
            Write(q_marks[1:], time_span=(1, 3)),
            run_time=3
        )
        self.wait()

        # Expose individual screens
        self.play(
            FadeOut(q_marks[1]),
            screens[1].animate.set_fill(BLACK, 1),
            connections[1:].animate.set_stroke(width=1, opacity=0.5),
        )
        self.wait()
        self.play(
            FadeOut(q_marks[2]),
            screens[2].animate.set_fill(BLACK, 1),
            connections[1:4:2].animate.set_stroke(width=3, opacity=1),
        )
        self.wait()
        self.play(
            FadeOut(q_marks[3]),
            screens[3].animate.set_fill(BLACK, 1),
            connections.animate.set_stroke(width=3, opacity=1),
        )
        self.wait()
