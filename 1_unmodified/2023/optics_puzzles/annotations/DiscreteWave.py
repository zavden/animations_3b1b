# ==============================================================================
# Scene:      DiscreteWave
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 779-800)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiscreteWave.py DiscreteWave -w -m --fps 15
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


class DiscreteWave(ContinuousWave):
    def construct(self):
        # Test
        waves = self.get_wave().replicate(3)
        waves.scale(2)
        waves.arrange(DOWN, buff=1.0)
        labels = VGroup()
        for n, wave in zip(it.count(1), waves):
            wave.stretch(0.5 * n, 1)
            label = TexText(f"{n} $hf$" + ("" if n > 1 else ""))
            label.scale(0.5)
            label.next_to(wave, UP, buff=0.2)
            labels.add(label)
            self.play(
                FadeIn(wave),
                FadeIn(label),
            )

        dots = Tex(R"\vdots", font_size=60)
        dots.next_to(waves, DOWN)
        self.play(Write(dots))
        self.wait()
