# ==============================================================================
# Scene:      WriteQuantumComputingTitle
# Source:     videos/_2025/grover/qc_supplements.py (lines 152-165)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteQuantumComputingTitle.py WriteQuantumComputingTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteQuantumComputingTitle(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Quantum Computing", font_size=120)
        title.move_to(UP)
        subtitle = Tex(R"\frac{1}{\sqrt{2}}\big(|0\rangle + |1\rangle \big)", font_size=90)
        subtitle.next_to(title, DOWN, LARGE_BUFF)
        title.set_color(TEAL)

        self.add(title, subtitle)
        self.play(LaggedStart(
            Flash(letter, color=TEAL, flash_radius=1.0, line_stroke_width=2)
            for letter in title
        ))
