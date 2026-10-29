# ==============================================================================
# Scene:      SingleNeuronVsMultiple
# Source:     videos/_2024/transformers/supplements.py (lines 1941-2020)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl SingleNeuronVsMultiple.py SingleNeuronVsMultiple -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


def get_network_connections(layer1, layer2, max_width=2.0, opacity_exp=1.0):
    radius = layer1[0].get_width() / 2
    return VGroup(
        Line(n1.get_center(), n2.get_center(), buff=radius).set_stroke(
            color=value_to_color(random.uniform(-10, 10)),
            width=max_width * random.random(),
            opacity=random.random()**opacity_exp,
        )
        for n1 in layer1
        for n2 in layer2
    )



# ----- From _2024/transformers/supplements.py -----

class SingleNeuronVsMultiple(InteractiveScene):
    def construct(self):
        # Add network
        radius = 0.1
        layers = VGroup(
            Dot(radius=radius).get_grid(n, 1, buff=radius)
            for n in [8, 16, 8]
        )
        layers.arrange(RIGHT, buff=2.0)
        layers.set_stroke(WHITE, 1)
        for layer in layers:
            for dot in layer:
                dot.set_fill(opacity=random.random())

        connections = VGroup(
            get_network_connections(layers[i], layers[i + 1])
            for i in (0, 1)
        )

        network = VGroup(layers, connections)
        network.set_height(5)
        network.center()

        self.add(network)

        # Show first neuron light up
        rect = SurroundingRectangle(layers[1][0])
        name = Text("Michael Jordan")
        name.next_to(rect, UP, SMALL_BUFF)
        name.save_state()
        for letter, dot in zip(*make_even(name, layers[0])):
            letter.move_to(dot)
            letter.set_opacity(0)

        thick_connections = connections.copy()
        for group in thick_connections:
            for line in group:
                line.set_stroke(width=2 * line.get_stroke_width(), opacity=1)
                line.insert_n_curves(20)
        self.play(
            LaggedStartMap(
                VShowPassingFlash,
                thick_connections[0],
                lag_ratio=1 / len(thick_connections[0]),
                time_width=2.0,
            ),
            layers[1][0].animate.set_fill(opacity=1),
            layers[1][1:].animate.set_fill(opacity=0),
            Restore(name, lag_ratio=0.05),
            run_time=2
        )
        self.play(ShowCreation(rect))
        self.wait()
        network.add(rect, name)

        # Split the image
        network_copy = network.copy()
        for dot in network_copy[0][1]:
            dot.set_fill(opacity=random.random())
        network_copy.to_edge(RIGHT)
        network_copy[-2].become(SurroundingRectangle(network_copy[0][1]))

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(WHITE, 2)
        check = Checkmark().set_fill(GREEN).scale(2)
        ex = Exmark().set_fill(RED).scale(2)
        check.next_to(network_copy[-1], RIGHT)
        ex.move_to(check).shift(0.5 * FRAME_WIDTH * LEFT)

        self.play(
            network.animate.to_edge(LEFT),
            TransformFromCopy(network, network_copy),
            ShowCreation(v_line),
        )
        self.play(LaggedStart(
            Write(ex, stroke_color=RED),
            Write(check, stroke_color=GREEN),
            lag_ratio=0.5
        ))
        self.wait()
