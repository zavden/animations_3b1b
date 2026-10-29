# ==============================================================================
# Scene:      ScalingAPattern
# Source:     videos/_2024/transformers/attention.py (lines 2259-2310)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ScalingAPattern.py ScalingAPattern -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import warnings


# ----- From _2024/transformers/helpers.py -----

def softmax(logits, temperature=1.0):
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # Ignore all warnings within this block
        logits = logits - np.max(logits)  # For numerical stability
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))
    
    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)



# ----- From _2024/transformers/attention.py -----

class ScalingAPattern(InteractiveScene):
    def construct(self):
        # Position grid
        N = 50
        grid = Square(side_length=1.0).get_grid(N, N, buff=0)
        grid.set_stroke(GREY_A, 1)
        grid.stretch(0.89, 0)
        grid.stretch(0.70, 1)
        # grid.move_to(1.67 * LEFT + 1.596 * UP, UL)
        grid.move_to(5.0 * LEFT + 2.5 * UP, UL)
        self.add(grid)

        # Dots
        values = np.random.normal(0, 1, (N, N))
        dots = VGroup()
        for n, row in enumerate(values):
            row[:n] = -np.inf
        for k, col in enumerate(values.T):
            for n, value in enumerate(softmax(col)):
                dot = Dot(radius=0.3 * value**0.75)
                dot.move_to(grid[n * N + k])
                dots.add(dot)
        dots.set_fill(GREY_C, 1)
        self.add(dots)

        # Add symbols
        q_template = Tex(R"\vec{\textbf{Q}}_0").set_color(YELLOW)
        k_template = Tex(R"\vec{\textbf{K}}_0").set_color(TEAL)
        for template in [q_template, k_template]:
            template.scale(0.75)
            template.substr = template.make_number_changeable("0")

        qs = VGroup()
        ks = VGroup()
        for n, square in enumerate(grid[:N], start=1):
            q_template.substr.set_value(n)
            q_template.next_to(square, UP, buff=SMALL_BUFF)
            qs.add(q_template.copy())
        for k, square in enumerate(grid[::N], start=1):
            k_template.substr.set_value(k)
            k_template.next_to(square, LEFT, buff=2 * SMALL_BUFF)
            ks.add(k_template.copy())
        self.add(qs, ks)

        # Slowly zoom out
        self.play(
            self.frame.animate.reorient(0, 0, 0, (14.72, -14.71, 0.0), 38.06),
            grid.animate.set_stroke(width=1, opacity=0.25),
            dots.animate.set_fill(GREY_B, 1).set_stroke(GREY_B, 1),
            run_time=20,
        )
        self.wait()
