# ==============================================================================
# Scene:      Credits
# Source:     videos/_2018/basel/basel2.py (lines 4393-4421)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Credits.py Credits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class Credits(Scene):
    def construct(self):
        credits = VGroup(*[
            VGroup(*list(map(TexText, pair)))
            for pair in [
                ("Primary writer and animator:", "Ben Hambrecht"),
                ("Editing, advising, narrating:", "Grant Sanderson"),
                ("Based on a paper originally by:", "Johan Wästlund"),
            ]
        ])
        for credit, color in zip(credits, [MAROON_D, BLUE_D, WHITE]):
            credit[1].set_color(color)
            credit.arrange(DOWN, buff = SMALL_BUFF)

        credits.arrange(DOWN, buff = LARGE_BUFF)

        credits.center()
        patreon_logo = PatreonLogo()
        patreon_logo.to_edge(UP)

        for credit in credits:
            self.play(LaggedStartMap(FadeIn, credit[0]))
            self.play(FadeIn(credit[1]))
        self.wait()
        self.play(
            credits.next_to, patreon_logo.get_bottom(), DOWN, MED_LARGE_BUFF,
            DrawBorderThenFill(patreon_logo)
        )
        self.wait()
