# ==============================================================================
# Scene:      ReferenceNeedleInAHaystack
# Source:     videos/_2025/grover/runtime.py (lines 501-539)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceNeedleInAHaystack.py ReferenceNeedleInAHaystack -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceNeedleInAHaystack(InteractiveScene):
    key = 61

    def construct(self):
        # Show that grid of 100 values, with arrows to exes or checks
        N = 10
        grid = VGroup(Integer(n) for n in range(int(N * N)))
        grid.arrange_in_grid(fill_rows_first=False, h_buff=1.35, v_buff=0.75)
        grid.set_height(FRAME_HEIGHT - 1)

        self.add(grid)

        # Show marks
        key = self.key
        symbols = VGroup()
        for n in range(N * N):
            if n == key:
                symbol = Checkmark().set_color(GREEN)
            else:
                symbol = Exmark().set_color(RED)
            symbol.set_height(grid[0].get_height())
            symbol.next_to(grid[n], RIGHT, SMALL_BUFF)
            symbols.add(symbol)

        key_group = VGroup(grid[key], symbols[key])
        symbols.shuffle()

        self.play(LaggedStartMap(FadeIn, symbols, shift=0.25 * RIGHT, lag_ratio=0.05))
        self.wait()

        # Show key
        rect = SurroundingRectangle(key_group)
        rect.set_stroke(GREEN, 2)
        fader = FullScreenFadeRectangle(fill_opacity=0.5)
        self.add(fader, key_group, rect)
        self.play(
            FadeIn(fader),
            ShowCreation(rect),
        )
