# ==============================================================================
# Scene:      S4WithMultipleChildren
# Source:     videos/_2020/monster.py (lines 2844-2912)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl S4WithMultipleChildren.py S4WithMultipleChildren -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class S4WithMultipleChildren(Scene):
    def construct(self):
        # Setup
        bg_rect = FullScreenFadeRectangle()
        bg_rect.set_fill(GREY_E, 1)
        self.add(bg_rect)

        s_rects = VGroup(*[ScreenRectangle() for x in range(3)])
        s_rects.arrange(RIGHT, buff=MED_LARGE_BUFF)
        s_rects.set_width(FRAME_WIDTH - 1)
        s_rects.set_stroke(WHITE, 2)
        s_rects.set_fill(BLACK, 1)
        s_rects.move_to(DOWN)
        self.add(s_rects)

        s4_label = OldTex("S_4")
        s4_label.scale(2)
        s4_label.to_edge(UP)

        lines = VGroup(*[
            Line(rect.get_top(), s4_label.get_bottom(), buff=0.2)
            for rect in s_rects
        ])

        # Arising
        self.play(LaggedStartMap(ShowCreation, lines, lag_ratio=0.5))
        self.play(FadeIn(s4_label, DOWN))
        self.wait(2)

        # Triplets
        three = Integer(3)
        three.scale(2)
        three.move_to(s4_label)

        pis = VGroup(*[Randolph(color=c) for c in [BLUE_C, BLUE_E, BLUE_D]])
        pis.arrange(RIGHT)
        vects = VGroup(*[Vector(RIGHT) for x in range(3)])
        vects.arrange(RIGHT, buff=SMALL_BUFF)
        vects.rotate(30 * DEGREES)
        vects.set_color(TEAL)
        triangle = RegularPolygon(3)
        triangle.set_stroke(BLUE_B, 4)
        triangle.add(*[Dot(vert, color=BLUE_D) for vert in triangle.get_vertices()])
        triangle.set_stroke(background=True)
        triplets = VGroup(pis, vects, triangle)

        for trip, rect in zip(triplets, s_rects):
            trip.set_width(0.8 * rect.get_width())
            if trip.get_height() > 0.8 * rect.get_height():
                trip.set_height(0.8 * rect.get_height())
            trip.move_to(rect)

        self.play(
            FadeOut(s4_label, UP),
            FadeIn(three, DOWN),
            LaggedStartMap(FadeIn, pis, lag_ratio=0.5, run_time=1),
        )
        for trip in triplets[1:]:
            self.play(FadeIn(trip, lag_ratio=0.5))
        self.play(Blink(pis[0]))
        self.play(Blink(pis[2]))

        # Back to s4
        self.play(
            FadeOut(three, DOWN),
            FadeIn(s4_label, UP),
            FadeOut(triplets, lag_ratio=0.2, run_time=2),
        )
        self.wait()
