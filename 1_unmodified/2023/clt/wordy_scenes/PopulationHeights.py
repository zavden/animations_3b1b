# ==============================================================================
# Scene:      PopulationHeights
# Source:     videos/_2023/clt/wordy_scenes.py (lines 186-233)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl PopulationHeights.py PopulationHeights -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/clt/main.py -----

def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)



# ----- From _2023/clt/wordy_scenes.py -----

class PopulationHeights(InteractiveScene):
    random_seed = 2

    def construct(self):
        # Test
        func = lambda x: gauss_func(x, 1, 0.175)

        stacks = VGroup()
        all_pis = VGroup()
        for height in np.arange(0.6, 1.5, 0.1):
            n = int(10 * func(height))
            randys = VGroup(*(self.get_pi(height) for _ in range(n)))
            randys.arrange(RIGHT, buff=SMALL_BUFF)
            stacks.add(randys)
            all_pis.add(*randys)
        stacks.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        for stack, color in zip(stacks, color_gradient([BLUE_C, BLUE_E], len(stacks))):
            for pi in stack:
                pi.body.set_color(color)
        stacks.set_height(FRAME_HEIGHT - 1)
        stacks.to_edge(LEFT)

        for pi in all_pis:
            pi.save_state()

        all_pis.shuffle()
        all_pis.arrange_in_grid(n_cols=15)
        all_pis.shuffle()


        self.play(FadeIn(all_pis, lag_ratio=0.01, run_time=4))
        self.wait()
        self.play(LaggedStartMap(Restore, all_pis, lag_ratio=0.01, run_time=5))
        self.wait()

    def get_pi(self, height=1):
        pi = Randolph(
            mode=random.choice(["happy", "hooray", "pondering", "tease"]),
            height=1
        )
        pi.body.stretch(math.sqrt(height), 1, about_edge=UP)
        diff = height - pi.get_height()
        new_points = np.array(pi.body.get_points())
        new_points[3:26] += diff * DOWN
        new_points[63:82] += diff * DOWN
        pi.body.set_points(new_points)

        return pi
