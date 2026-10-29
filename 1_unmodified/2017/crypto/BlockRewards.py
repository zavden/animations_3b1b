# ==============================================================================
# Scene:      BlockRewards
# Source:     videos/_2017/crypto.py (lines 4687-4728)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BlockRewards.py BlockRewards -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BlockRewards(Scene):
    def construct(self):
        title = OldTexText("Block rewards")
        title.scale(1.5)
        logo = BitcoinLogo()
        logo.set_height(0.75)
        logo.next_to(title, LEFT)
        title.add(logo)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_X_RADIUS)
        h_line.next_to(title, DOWN)
        self.add(title, logo, h_line)

        rewards = VGroup(
            OldTexText("Jan 2009 - Nov 2012:", "50", "BTC"),
            OldTexText("Nov 2012 - Jul 2016:", "25", "BTC"),
            OldTexText("Jul 2016 - Feb 2020$^*$:", "12.5", "BTC"),
            OldTexText("Feb 2020$^*$ - Sep 2023$^*$:", "6.25", "BTC"),
        )
        rewards.arrange(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        rewards.next_to(h_line, DOWN)
        for reward in rewards:
            reward[1].set_color(YELLOW)

        footnote = OldTexText(
            "$^*$ Extrapolating from the 25 BTC reward period"
        )
        footnote.scale(0.5)
        footnote.to_corner(DOWN+RIGHT)

        self.play(LaggedStartMap(
            FadeIn, rewards,
            run_time = 4,
            lag_ratio = 0.5
        ))
        self.play(FadeIn(footnote))
        self.wait(3)
