# ==============================================================================
# Scene:      ComplexConjugateFact
# Source:     videos/_2024/holograms/supplements.py (lines 1448-1511)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexConjugateFact.py ComplexConjugateFact -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexConjugateFact(InteractiveScene):
    def construct(self):
        # Show conjugate
        z = complex(2, 1)
        plane = ComplexPlane(
            (-6, 6), (-4, 4),
            faded_line_ratio=4,
            background_line_style=dict(
                stroke_color=BLUE_D,
                stroke_width=1,
            ),
            faded_line_style=dict(
                stroke_color=BLUE_E,
                stroke_width=1,
                stroke_opacity=0.5,
            ),
        )
        plane.set_height(7)
        plane.to_edge(DOWN, buff=0.25)
        plane.add_coordinate_labels(font_size=16)
        title = Text("Complex plane")
        title.next_to(plane, UP, buff=SMALL_BUFF)

        z_arrow = Arrow(plane.get_origin(), plane.n2p(z), buff=0)
        z_arrow.set_color(YELLOW)
        z_label = Tex(R"z = a + bi")
        z_label.next_to(z_arrow.get_end(), UP)

        z_conj = complex(z.real, -z.imag)
        z_conj_arrow = Arrow(plane.get_origin(), plane.n2p(z_conj), buff=0)
        z_conj_arrow.set_color(TEAL)
        z_conj_label = Tex("z^* = a - bi")
        z_conj_label.next_to(z_conj_arrow.get_end(), DOWN)

        conj_label = Text("Complex conjugate")
        conj_label.next_to(z_conj_label, DOWN, aligned_edge=LEFT)
        conj_label.set_backstroke(BLACK, 5)

        self.add(plane, title)
        self.add(z_arrow, z_label)
        self.wait()
        self.play(Write(conj_label, stroke_color=WHITE))
        self.play(
            TransformFromCopy(z_arrow, z_conj_arrow, path_arc=-PI / 2),
            TransformMatchingStrings(z_label.copy(), z_conj_label, path_arc=-PI / 2),
            run_time=2
        )
        self.wait()

        # Show product
        product_arrow = Arrow(plane.get_origin(), plane.n2p(z * z_conj), buff=0)
        product_arrow.set_color(WHITE)
        product_label = Tex(R"z \cdot z^* = |z|^2")
        product_label.next_to(product_arrow.get_end(), UP)
        product_label.shift(0.75 * RIGHT)

        self.play(
            TransformFromCopy(z_label[0], product_label[R"z \cdot"][0]),
            TransformFromCopy(z_conj_label[:2], product_label["z^*"][0]),
            TransformFromCopy(z_arrow, product_arrow),
            TransformFromCopy(z_conj_arrow, product_arrow),
        )
        self.play(Write(product_label["= |z|^2"][0]))
        self.wait()
