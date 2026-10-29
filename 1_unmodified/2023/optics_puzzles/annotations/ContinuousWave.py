# ==============================================================================
# Scene:      ContinuousWave
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 761-776)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContinuousWave.py ContinuousWave -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ContinuousWave(InteractiveScene):
    def construct(self):
        wave = self.get_wave()
        points = wave.get_points().copy()
        wave.add_updater(lambda m: m.set_points(points).stretch(
            (1 - math.sin(self.time)), 1,
        ))
        self.add(wave)
        self.wait(20)

    def get_wave(self):
        axes = Axes((0, 2 * TAU), (0, 1))
        wave = axes.get_graph(np.sin)
        wave.set_stroke(BLUE, 4)
        wave.set_width(2.0)
        return wave
