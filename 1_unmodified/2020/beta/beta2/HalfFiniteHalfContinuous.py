# ==============================================================================
# Scene:      HalfFiniteHalfContinuous
# Source:     videos/_2020/beta/beta2.py (lines 1555-1671)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl HalfFiniteHalfContinuous.py HalfFiniteHalfContinuous -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

def close_off_graph(axes, graph):
    x_max = axes.x_axis.p2n(graph.get_end())
    graph.add_line_to(axes.c2p(x_max, 0))
    graph.add_line_to(axes.c2p(0, 0))
    return graph



# ----- From _2020/beta/beta2.py -----

class HalfFiniteHalfContinuous(Scene):
    def construct(self):
        # Basic symbols
        box = Rectangle(width=3, height=1.2)
        box.set_stroke(WHITE, 2)
        box.set_fill(GREY_E, 1)
        box.move_to(2.5 * LEFT, RIGHT)

        arrows = VGroup()
        arrow_labels = VGroup()
        for vect in [UP, DOWN]:
            arrow = Arrow(
                box.get_corner(vect + RIGHT),
                box.get_corner(vect + RIGHT) + 3 * RIGHT + 1.5 * vect,
                buff=MED_SMALL_BUFF,
            )
            label = OldTex("50\\%")
            fix_percent(label[0][-1])
            label.set_color(YELLOW)
            label.next_to(
                arrow.get_center(),
                vect + LEFT,
                buff=SMALL_BUFF,
            )

            arrow_labels.add(label)
            arrows.add(arrow)

        zero = Integer(0)
        zero.set_height(0.5)
        zero.next_to(arrows[0].get_end(), RIGHT)

        # Half Gaussian
        axes = Axes(
            x_min=0,
            x_max=6.5,
            y_min=0,
            y_max=0.25,
            y_axis_config={
                "tick_frequency": 1 / 16,
                "unit_size": 10,
                "include_tip": False,
            }
        )
        axes.next_to(arrows[1].get_end(), RIGHT)

        dist = scipy.stats.norm(0, 2)
        graph = axes.get_graph(dist.pdf)
        graph_fill = graph.copy()
        close_off_graph(axes, graph_fill)
        graph.set_stroke(BLUE, 3)
        graph_fill.set_fill(BLUE_E, 1)
        graph_fill.set_stroke(BLUE_E, 0)

        half_gauss = Group(
            graph, graph_fill, axes,
        )

        # Random Decimal
        number = DecimalNumber(num_decimal_places=4)
        number.set_height(0.6)
        number.move_to(box)

        number.time = 0
        number.last_change = 0
        number.change_freq = 0.2

        def update_number(number, dt, dist=dist):
            number.time += dt

            if (number.time - number.last_change) < number.change_freq:
                return

            number.last_change = number.time
            rand_val = random.random()
            if rand_val < 0.5:
                number.set_value(0)
            else:
                number.set_value(dist.ppf(rand_val))

        number.add_updater(update_number)

        v_line = SurroundingRectangle(zero)
        v_line.save_state()
        v_line.set_stroke(YELLOW, 3)

        def update_v_line(v_line, number=number, axes=axes, graph=graph):
            x = number.get_value()
            if x < 0.5:
                v_line.restore()
            else:
                v_line.set_width(1e-6)
                p1 = axes.c2p(x, 0)
                p2 = axes.input_to_graph_point(x, graph)
                v_line.set_height(get_norm(p2 - p1), stretch=True)
                v_line.move_to(p1, DOWN)

        v_line.add_updater(update_v_line)

        # Add everything
        self.add(box)
        self.add(number)
        self.wait(4)
        self.play(
            GrowArrow(arrows[0]),
            FadeIn(arrow_labels[0]),
            GrowFromPoint(zero, box.get_corner(UR))
        )
        self.wait(2)
        self.play(
            GrowArrow(arrows[1]),
            FadeIn(arrow_labels[1]),
            FadeIn(half_gauss),
        )
        self.add(v_line)

        self.wait(30)
