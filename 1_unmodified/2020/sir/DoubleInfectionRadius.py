# ==============================================================================
# Scene:      DoubleInfectionRadius
# Source:     videos/_2020/sir.py (lines 2701-2743)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DoubleInfectionRadius.py DoubleInfectionRadius -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DoubleInfectionRadius(Scene):
    CONFIG = {
        "random_seed": 1,
    }

    def construct(self):
        c1 = Circle(radius=0.25, color=RED)
        c2 = Circle(radius=0.5, color=RED)
        arrow = Vector(RIGHT)
        c1.next_to(arrow, LEFT)
        c2.next_to(arrow, RIGHT)

        title = OldTexText("Double the\\\\infection radius")
        title.next_to(VGroup(c1, c2), UP)

        self.add(c1, title)
        self.wait()
        self.play(
            GrowArrow(arrow),
            TransformFromCopy(c1, c2),
        )
        self.wait()

        c2.label = OldTexText("4x area")
        c2.label.scale(0.5)
        c2.label.next_to(c2, DOWN)

        for circ, count in (c1, 4), (c2, 16):
            dots = VGroup()
            for x in range(count):
                dot = Dot(color=BLUE)
                dot.set_stroke(BLACK, 2, background=True)
                dot.set_height(0.05)
                vect = rotate_vector(RIGHT, TAU * random.random())
                vect *= 0.9 * random.random() * circ.get_height() / 2
                dot.move_to(circ.get_center() + vect)
                dots.add(dot)
            circ.dot = dots
            anims = [ShowIncreasingSubsets(dots)]
            if hasattr(circ, "label"):
                anims.append(FadeIn(circ.label, 0.5 * UP))
            self.play(*anims)
            self.wait()
