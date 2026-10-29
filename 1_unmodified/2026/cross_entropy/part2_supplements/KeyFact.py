# ==============================================================================
# Scene:      KeyFact
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 236-277)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyFact.py KeyFact -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KeyFact(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"Q": PINK, "P": GREEN}
        kw = dict(font_size=60, t2c=t2c)
        title = Text("Key fact about Cross-Entropy\nof Q relative to P", **kw)
        title.to_corner(UL)

        key_fact = title["Key fact"]
        key_fact_underline = Underline(key_fact, buff=-0.05)
        key_fact_underline.set_stroke(YELLOW)

        pin = SVGMobject("push_pin")
        pin.set_fill((WHITE, GREY_E))
        pin.set_height(0.5)
        pin.rotate(-45 * DEG)
        pin.next_to(title["P"], RIGHT, SMALL_BUFF)
        P = title["P"][0]
        P_rect = SurroundingRectangle(P, buff=SMALL_BUFF)
        P_rect.set_stroke(WHITE, 1)

        facts = VGroup(
            Text("• Minimal when Q = P", **kw),
            Text("• Minimal value = H(P)", **kw),
        )
        facts.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)

        facts.next_to(title, DOWN, buff=2.0)
        facts.to_edge(LEFT)

        self.add(title)
        self.play(
            ShowCreation(key_fact_underline),
            key_fact.animate.set_fill(YELLOW),
        )
        self.wait()
        self.play(FadeIn(P_rect, scale=0.5, rate_func=rush_into, run_time=0.5))
        self.wait()

        for fact in facts:
            self.play(FadeIn(fact, DOWN))
            self.wait()
