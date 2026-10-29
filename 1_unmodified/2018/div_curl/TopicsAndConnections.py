# ==============================================================================
# Scene:      TopicsAndConnections
# Source:     videos/_2018/div_curl.py (lines 1023-1087)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TopicsAndConnections.py TopicsAndConnections -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TopicsAndConnections(Scene):
    CONFIG = {
        "random_seed": 1,
    }

    def construct(self):
        dots = VGroup(*[
            Dot(8 * np.array([
                random.random(),
                random.random(),
                0
            ]))
            for n in range(5)
        ])
        topics = VGroup(*[
            OldTexText(word).next_to(
                dot, RIGHT, SMALL_BUFF
            )
            for dot, word in zip(dots, [
                "Divergence/curl",
                "Fluid flow",
                "Electricity and magnetism",
                "Conformal maps",
                "Complex numbers"
            ])
        ])
        for topic in topics:
            topic.add_to_back(
                topic.copy().set_stroke(BLACK, 2)
            )

        VGroup(dots, topics).center()
        for dot in dots:
            dot.save_state()
            dot.scale(3)
            dot.set_fill(opacity=0)

        connections = VGroup(*[
            DashedLine(d1.get_center(), d2.get_center())
            for d1, d2 in it.combinations(dots, 2)
        ])
        connections.set_stroke(YELLOW, 2)

        full_rect = FullScreenFadeRectangle()

        self.play(
            LaggedStartMap(
                ApplyMethod, dots,
                lambda d: (d.restore,)
            ),
            LaggedStartMap(Write, topics),
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, connections),
            Animation(topics),
            Animation(dots),
        )
        self.wait()
        self.play(
            FadeIn(full_rect),
            Animation(topics[0]),
            Animation(dots[0]),
        )
        self.wait()
