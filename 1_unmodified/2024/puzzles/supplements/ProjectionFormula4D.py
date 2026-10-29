# ==============================================================================
# Scene:      ProjectionFormula4D
# Source:     videos/_2024/puzzles/supplements.py (lines 607-629)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProjectionFormula4D.py ProjectionFormula4D -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProjectionFormula4D(InteractiveScene):
    def construct(self):
        # Test
        t2c = {R"\hat{\textbf{d}}": BLUE_D, R"\vec{\textbf{v}}": YELLOW}
        form = Tex(
            R"\text{Project}(\vec{\textbf{v}}) = \vec{\textbf{v}} - \left(\vec{\textbf{v}} \cdot \hat{\textbf{d}} \right) \hat{\textbf{d}}",
            t2c=t2c
        )
        # form.to_corner(UL)
        form.move_to(UP)

        definition = Tex(
            R"\text{Where } \hat{\textbf{d}} := \frac{1}{\sqrt{4}} \left[\begin{array}{c} 1 \\ 1 \\ 1 \\ 1 \end{array}\right]",
            font_size=36,
            t2c=t2c
        )
        definition.next_to(form, DOWN, buff=0.5)

        VGroup(form, definition).set_backstroke(BLACK, 5)

        self.add(form)
        self.play(FadeIn(definition, 0.25 * DOWN))
        self.wait()
