# ==============================================================================
# Scene:      ThreeStepPlan
# Source:     videos/_2023/gauss_int/supplements.py (lines 255-303)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeStepPlan.py ThreeStepPlan -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeStepPlan(InteractiveScene):
    def construct(self):
        # Steps
        step_titles = VGroup(*(
            Text(f"Step {n}", font_size=48) for n in [1, 2, 3]
        ))
        kw = dict(t2c={"e^{-{x}^2}": BLUE, R"\sqrt{\pi}": TEAL}, color=GREY_A, font_size=36, alignment="")
        step_contents = VGroup(
            TexText(R"Explain why the area under \\$e^{-{x}^2}$ is $\sqrt{\pi}$", **kw),
            TexText(R"Explain where $e^{-{x}^2}$ comes from \\ in the first place", **kw),
            TexText(R"Connect it all to the \\ Central Limit Theorem", **kw),
        )

        steps = VGroup()
        for title, content in zip(step_titles, step_contents):
            content.next_to(title, DOWN, aligned_edge=LEFT)
            steps.add(VGroup(title, content))
        steps.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        steps.to_corner(UL)

        step_rects = VGroup(*(
            SurroundingRectangle(content)
            for content in step_contents
        ))
        step_rects.set_fill(GREY_E, 1)
        step_rects.set_stroke(RED, 1, 0.5)

        self.add(steps)
        self.add(step_rects)
        self.remove(step_contents)
        self.wait()

        for rect, content in zip(step_rects, step_contents):
            self.add(content, rect)
            self.play(rect.animate.stretch(0, 0, about_edge=RIGHT).set_stroke(opacity=0))
            self.remove(rect)
            self.wait()

        # Step by step
        for step in steps:
            step.save_state()

        for step in steps:
            anims = [Restore(step)]
            for other_step in steps:
                if other_step is not step:
                    anims.append(other_step.animate.restore().scale(0.75, about_edge=LEFT).set_opacity(0.5))
            self.play(*anims)
            self.wait()
