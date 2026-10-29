# ==============================================================================
# Scene:      NameElectromagneticField
# Source:     videos/_2024/holograms/supplements.py (lines 639-665)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameElectromagneticField.py NameElectromagneticField -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NameElectromagneticField(InteractiveScene):
    def construct(self):
        # Test
        name1 = Text("Electromagetic Field")
        name2 = Text("Electric Field")
        for name in [name1, name2]:
            name.set_backstroke(BLACK, 5)
            name.scale(1.5)
            name.to_edge(UP)

        expl = Text("3d Vector\nat each point")
        expl.set_x(FRAME_WIDTH / 4)
        expl.to_edge(UP)
        arrow = Vector(RIGHT)
        arrow = Vector(2 * RIGHT)
        arrow.next_to(expl, LEFT)

        self.play(Write(name1), run_time=1)
        self.wait()
        self.play(TransformMatchingStrings(name1, name2), run_time=1)
        self.wait()
        self.play(
            name2.animate.next_to(arrow, LEFT),
            GrowArrow(arrow),
            FadeIn(expl, RIGHT),
        )
        self.wait()
