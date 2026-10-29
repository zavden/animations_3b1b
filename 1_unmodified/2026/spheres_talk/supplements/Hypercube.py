# ==============================================================================
# Scene:      Hypercube
# Source:     videos/_2026/spheres_talk/supplements.py (lines 142-207)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Hypercube.py Hypercube -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Hypercube(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        bases = [RIGHT, UP, OUT, np.array([1.5, 1.0, 0.5])]
        pre_cube = self.get_cube([*bases[:3], ORIGIN])
        hypercube = self.get_cube(bases)

        frame.reorient(-21, 79, 0, (1.13, 0.35, 0.88), 3.81)
        frame.add_ambient_rotation(2 * DEG)
        self.add(pre_cube)
        self.wait()
        self.play(ReplacementTransform(pre_cube, hypercube, run_time=2))
        self.wait(8)

        # Flatten
        flat_bases = [RIGHT, UP, np.array([0.2, 0.5, 0]), 1 * OUT]
        flat_cube = self.get_cube(flat_bases)

        leg1 = Line(bases[0], bases[1] + bases[2])
        leg2 = Line(bases[0], bases[0] + bases[3])
        leg1.set_stroke(RED, 3)
        leg2.set_stroke(TEAL, 3)

        root3_label = Tex(R"\sqrt{3}", font_size=24)
        root3_label.rotate(90 * DEG, RIGHT)
        root3_label.next_to(leg1.get_center(), LEFT)
        one_label = Tex(R"1", font_size=24)
        one_label.rotate(90 * DEG, RIGHT)
        one_label.next_to(leg2.get_center(), IN)

        hyp = Line(leg1.get_end(), leg2.get_end())
        hyp.set_stroke(YELLOW, 3)
        hyp_label = Tex(R"\sqrt{3 + 1}", font_size=24)
        hyp_label.rotate(90 * DEG, RIGHT)
        hyp_label.next_to(hyp.get_center(), OUT, buff=SMALL_BUFF)

        self.play(
            hypercube.animate.set_stroke(WHITE, 1, 0.5),
            ShowCreation(leg1),
            FadeIn(root3_label)
        )
        self.play(
            ShowCreation(leg2),
            FadeIn(one_label),
        )
        self.wait()
        self.play(
            FadeTransformPieces(VGroup(root3_label, one_label).copy(), hyp_label),
            ShowCreation(hyp)
        )
        self.wait(12)

    def get_cube(self, bases, stroke_color=WHITE, stroke_width=2):
        n = len(bases)
        lines = VGroup()
        for bits in it.product(*n * [[0, 1]]):
            base_point = sum([
                bit * basis
                for bit, basis in zip(bits, bases)
            ])
            for bit, basis in zip(bits, bases):
                if bit == 0:
                    lines.add(Line(base_point, base_point + basis))
        lines.set_stroke(stroke_color, stroke_width)
        return lines
