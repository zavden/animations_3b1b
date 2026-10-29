# ==============================================================================
# Scene:      IntersectionAndUnion
# Source:     videos/_2022/some2/announcement.py (lines 4-74)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntersectionAndUnion.py IntersectionAndUnion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntersectionAndUnion(InteractiveScene):
    def construct(self):
        self.camera.frame.scale(1.1)
        # Title
        title = Text("Educational content creation by individuals", font_size=60)
        title.to_edge(UP)
        title_start = title.select_part("Educational content creation")
        by_ind = title.select_part("by individuals")
        by_ind.set_color(TEAL)
        self.add(title_start)

        self.play(
            Write(by_ind),
            FlashUnder(by_ind, run_time=3, color=TEAL, buff=0.1)
        )

        # Circles
        circles = Circle(radius=2.5).replicate(2)
        circles.arrange(RIGHT, buff=-2.0)
        circles.set_stroke(WHITE, width=0)
        circles[0].set_fill(BLUE_D, 0.5)
        circles[1].set_fill(TEAL_D, 0.5)
        circles.next_to(title, DOWN, LARGE_BUFF)

        circle_titles = VGroup(
            Text("People with\ngood lessons"),
            Text("People with the\ntime and know-how\nto produce videos,\ninteractives, etc.", alignment="LEFT"),
        )
        circle_titles.scale(0.75)
        for ct, circ, vect in zip(circle_titles, circles, [LEFT, RIGHT]):
            ct.next_to(circ, vect, buff=0, aligned_edge=UP)
            ct.match_color(circ)

        self.play(
            LaggedStartMap(Write, circle_titles, lag_ratio=0.25),
            LaggedStartMap(DrawBorderThenFill, circles, lag_ratio=0.25),
        )
        self.wait()

        # Intersection
        inter = Intersection(*circles)
        inter.set_stroke(WHITE, 3)
        inter.set_fill(TEAL, 1.0)
        inter.flip()
        self.play(
            DrawBorderThenFill(inter),
            circles.animate.set_fill(opacity=0.25)
        )
        self.wait()

        # Collaboration
        cross = Cross(by_ind)
        new_text = Text("from collaborations", font_size=60)
        new_text.set_color(YELLOW)
        new_text.move_to(by_ind, UL)
        title_start.generate_target()
        VGroup(title_start.target, new_text).set_x(0)

        union = Union(*circles)
        union.set_stroke(WHITE, 3)

        self.play(ShowCreation(cross))
        self.play(
            VGroup(by_ind, cross).animate.scale(0.5).shift(0.75 * DOWN),
            FadeIn(new_text, 0.5 * DOWN),
            MoveToTarget(title_start),
            FadeOut(inter),
            circles.animate.set_fill(opacity=0.7),
            ShowCreation(union)
        )
        self.wait(3)
