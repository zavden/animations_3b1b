# ==============================================================================
# Scene:      TwoKeyFeatures
# Source:     videos/_2026/hairy_ball/supplements.py (lines 386-474)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoKeyFeatures.py TwoKeyFeatures -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoKeyFeatures(InteractiveScene):
    def construct(self):
        # Set up
        features = VGroup(
            # Text("1) Sphere turns\ninside out"),
            # Text("2) No point touches\nthe origin"),
            Text("1) Inside out"),
            Text("2) Avoids the origin"),
        )
        features[1]["the origin"].align_to(features[1]["No"], LEFT)
        features.arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        features.to_edge(LEFT)

        for feature in features:
            self.play(FadeIn(feature, lag_ratio=0.1))
            self.wait()

        # Emphasize first point
        self.play(
            features[0].animate.scale(1.25, about_edge=LEFT),
            features[1].animate.scale(0.75, about_edge=LEFT).set_fill(opacity=0.5).shift(DOWN),
        )
        self.wait()

        # Ask why
        randy = Randolph(height=1.75)
        randy.next_to(features[0], DOWN, buff=MED_LARGE_BUFF)
        why = Text("Why?", font_size=36)
        why.next_to(randy, RIGHT, aligned_edge=UP)
        why.set_color(YELLOW)

        self.play(
            VFadeIn(randy),
            randy.change("maybe"),
            Write(why),
        )
        self.play(Blink(randy))
        self.wait()

        # Ask what "inside out" means
        rect = SurroundingRectangle(features[0][2:])
        rect.set_stroke(YELLOW, 2)
        self.play(
            randy.change("confused", rect),
            FadeTransform(why, rect)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(randy), FadeOut(rect))

        # Inside out implication
        rect0 = SurroundingRectangle(features[0])
        rect0.set_stroke(BLUE, 2)

        implies0 = Tex(R"\Longrightarrow", font_size=72)
        implies0.next_to(rect0)
        net_flow_m1 = TexText("Final Flux = $-1.0$", t2c={"-1.0": RED}, font_size=60)
        net_flow_m1.next_to(implies0, RIGHT)

        self.play(
            ShowCreation(rect0),
            FadeIn(implies0, scale=2, shift=0.25 * RIGHT),
        )
        self.play(FadeIn(net_flow_m1, lag_ratio=0.1))
        self.wait()

        # No origin implication
        self.play(features[1].animate.scale(1.25 / 0.75, about_edge=UL).set_opacity(1))

        rect1 = SurroundingRectangle(features[1])
        rect1.match_style(rect0)
        implies1 = implies0.copy()
        implies1.next_to(rect1)
        net_flow_p1 = TexText(R"Final flux = $+1.0$", t2c={"+1.0": GREEN}, font_size=60)  
        net_flow_p1.next_to(implies1, RIGHT)

        self.play(
            ShowCreation(rect1),
            FadeIn(implies1, scale=2, shift=0.25 * RIGHT),
        )
        self.play(FadeIn(net_flow_p1, lag_ratio=0.1))
        self.wait()

        # Contradiction
        contra = Tex(R"\bot", font_size=90)
        contra.to_corner(DR)

        self.play(Write(contra))
        self.wait()
