# ==============================================================================
# Scene:      ThreeExplanations
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 465-528)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeExplanations.py ThreeExplanations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeExplanations(InteractiveScene):
    def construct(self):
        # Add terms
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        title = Tex(R"\text{Why } \mathcal{L}\big\{f'({t})\big\} = {s} F({s}) - f(0)", t2c=t2c)
        title.to_edge(UP)
        title_underline = Underline(title)

        num_mobs = VGroup(Text(f"{n}) ") for n in range(1, 4))
        num_mobs.scale(1.25)
        num_mobs.arrange(DOWN, buff=1.25, aligned_edge=LEFT)
        num_mobs.next_to(title, DOWN, buff=1.25).to_edge(LEFT, buff=LARGE_BUFF)

        by_parts = Tex(R"\text{Integration by parts}", t2c=t2c)
        inversion = Tex(R"\frac{d}{d{t}} \Big(\text{Inverse Laplace Transform}\Big)", t2c=t2c)

        descriptors = VGroup(
            Text("[Elementary, but limited]"),
            Text("[General, but opaque]"),
            Text("[My favorite, but theoretical]"),
        )
        descriptors.set_fill(GREY_B)
        explanations = VGroup(
            Tex(R"\text{Start with } e^{a{t}}", t2c=t2c),
            by_parts,
            inversion,
        )

        for num, desc, expl in zip(num_mobs, descriptors, explanations):
            for mob in [desc, expl]:
                mob.next_to(num, RIGHT, buff=MED_LARGE_BUFF)
        explanations[0].shift(SMALL_BUFF * UP)

        self.add(title)
        self.play(ShowCreation(title_underline))
        self.wait()
        self.play(LaggedStartMap(FadeIn, num_mobs, shift=UP, lag_ratio=0.25))
        self.wait()
        for desc in descriptors:
            self.play(FadeIn(desc, lag_ratio=0.2))
            self.wait()

        # Show explanations
        for i, desc, expl in zip(it.count(), descriptors, explanations):
            self.play(
                FadeOut(desc, 0.5 * UP),
                FadeIn(expl, 0.5 * UP),
                num_mobs[:i].animate.set_opacity(0.25),
                explanations[:i].animate.set_opacity(0.25),
            )
            self.wait()

        # Show all of them
        num_mobs.set_fill(opacity=1)
        explanations.set_fill(opacity=1)
        self.play(
            LaggedStartMap(FadeIn, num_mobs, shift=UP, lag_ratio=0.25),
            LaggedStartMap(FadeIn, explanations, shift=UP, lag_ratio=0.25),
        )
        self.wait()
        fade_group = VGroup(title, title_underline, *num_mobs, *explanations)
        fade_group.sort(lambda p: np.dot(p, DOWN + 0.1 * RIGHT))
        self.play(LaggedStartMap(FadeOut, fade_group, shift=LEFT, lag_ratio=0.15, run_time=2))
        self.wait()
