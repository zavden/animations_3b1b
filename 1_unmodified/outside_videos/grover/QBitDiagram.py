# ==============================================================================
# Scene:      QBitDiagram
# Source:     videos/outside_videos/grover.py (lines 5-101)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QBitDiagram.py QBitDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QBitDiagram(InteractiveScene):
    def construct(self):
        # Axes
        axes = Axes(
            (-1.5, 1.5, 0.5), (-1.5, 1.5, 0.5),
            height=7,
            width=7,
        )
        axes.set_height(7)
        x_label = Tex(R"|0\rangle")
        y_label = Tex(R"|1\rangle")
        x_label.next_to(axes.x_axis.get_right(), UP, buff=0.15)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.15)
        axes.add(x_label, y_label)
        axes.add_coordinate_labels(font_size=16, num_decimal_places=1)

        circle = Circle(radius=axes.x_axis.get_unit_size())
        circle.move_to(axes.c2p(0, 0))
        circle.set_stroke(YELLOW, 2)

        self.add(circle)
        self.add(axes)

        # State vector
        vect = Arrow(axes.c2p(0, 0), circle.pfp(0.2), buff=0)
        vect.set_color(RED)

        coefs = DecimalNumber(edge_to_fix=RIGHT).replicate(2)
        coefs.set_color(RED)
        coefs[0].add_updater(lambda m: m.set_value(axes.x_axis.p2n(vect.get_end())))
        coefs[1].add_updater(lambda m: m.set_value(axes.y_axis.p2n(vect.get_end())))
        vect_label = VGroup(
            coefs[0], Tex(R"|0\rangle"), Tex("+"),
            coefs[1], Tex(R"|1\rangle"),
        )
        vect_label.arrange(RIGHT, buff=0.25)
        coefs.shift(0.1 * RIGHT)
        vect_label.scale(1.25)
        vect_label.to_corner(UR)

        self.add(vect)
        self.add(vect_label)

        # Probabilities
        prob_labels = VGroup(
            self.get_prob_label(coefs[0], "0"),
            self.get_prob_label(coefs[1], "1"),
        )
        prob_labels.arrange(DOWN, aligned_edge=LEFT)
        prob_labels.to_corner(UL)
        self.add(prob_labels)

        # Move around
        self.play(
            Rotate(vect, -1, about_point=axes.c2p(0, 0)),
            run_time=5
        )
        self.wait()

        # Show some flips
        line1 = DashedLine(2.5 * DL, 2.5 * UR)
        line2 = line1.copy().rotate(-30 * DEGREES)
        line3 = line1.copy().rotate(-63 * DEGREES)
        lines = [line1, line2, line3]

        last_line = VGroup()
        for line in lines:
            self.play(ShowCreation(line), FadeOut(last_line))
            self.wait()
            vect.generate_target()
            vect.target.flip(
                axis=line.get_vector(),
                about_point=axes.c2p(0, 0)
            )
            angle = vect.target.get_angle() - vect.get_angle()
            self.play(
                MoveToTarget(vect, path_arc=angle)
            )
            self.wait()
            last_line = line
        self.play(FadeOut(last_line))

    def get_prob_label(self, coef, bit="0"):
        # Test
        label = Tex(
            Rf"P(\text{{Measure a }}{bit}) = (0.00)^2 = 0.00",
            font_size=36
        )
        numbers = label.make_number_changeable("0.00", replace_all=True)
        for number in numbers:
            number.edge_to_fix = ORIGIN
        width = numbers[0].get_width()
        numbers[0].add_updater(lambda m: m.set_value(coef.get_value()).set_width(width))
        numbers[1].add_updater(lambda m: m.set_value(coef.get_value()**2).set_width(width))
        numbers.set_color(RED)

        return label
