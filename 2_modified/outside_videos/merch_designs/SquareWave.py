# ==============================================================================
# Scene:      SquareWave
# Source:     videos/outside_videos/merch_designs.py (lines 52-84)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SquareWave.py SquareWave -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the fractals import is removed (not used in this scene; besides, manimlib.once_useful_constructs no longer exists and its fractals.py does not import)
# ==============================================================================

from manim_imports_ext import *
# CHANGE: the fractals import is removed (not used in this scene; besides, manimlib.once_useful_constructs no longer exists and its fractals.py does not import)

# Socks
class SquareWave(Scene):
    def construct(self):
        L = FRAME_WIDTH / 4
        waves = VGroup(*[
            FunctionGraph(
                lambda x: self.approx_square_wave(x, L, n_terms),
                x_range=[-2 * L, 2 * L, L / 50],
            )
            for n_terms in range(1, 5)
        ])
        waves.set_color_by_gradient(BLUE, YELLOW, RED)
        stroke_widths = np.linspace(3, 1, len(waves))
        for wave, stroke_width in zip(waves, stroke_widths):
            # wave.set_stroke(width=stroke_width)
            wave.set_stroke(width=3)
        # waves.to_edge(UP)

        tex_mob = OldTex("""
            {4 \\over \\pi}
            \\sum_{n=0}^\\infty {\\sin\\big((2n + 1)\\pi x\\big) \\over (2n + 1)}
        """)
        tex_mob.scale(1.5)
        # tex_mob.next_to(waves, DOWN, MED_LARGE_BUFF)

        self.add(waves)
        # self.add(tex_mob)

    def approx_square_wave(self, x, L, n_terms=3):
        return 1.0 * sum([
            (1.0 / n) * np.sin(n * PI * x / L)
            for n in range(1, 2 * n_terms + 1, 2)
        ])
