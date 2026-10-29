# ==============================================================================
# Scene:      SimpleNetwork
# Source:     videos/_2026/cross_entropy/supplements.py (lines 208-260)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleNetwork.py SimpleNetwork -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleNetwork(InteractiveScene):
    random_seed = 2

    def construct(self):
        # Set up a basic network
        frame = self.frame
        layer_sizes = [4, 6, 6, 4]
        layer_spacing = 4

        layers = VGroup(self.get_layer(size) for size in layer_sizes)
        layers.arrange(RIGHT, buff=layer_spacing)
        layers.set_height(6)

        connections = VGroup()
        for l1, l2 in zip(layers, layers[1:]):
            lines = VGroup()
            for n2 in l2:
                n2.connections = self.get_connections(n2, l1)
                lines.add(n2.connections)
            connections.add(lines)

        network = VGroup(layers, connections)
        network.set_height(3).to_edge(DOWN)

        self.add(network)
        # self.play(network.animate.set_height(0.75).center(), run_time=2)
        network.set_height(0.75).center()
        self.play(Write(network, run_time=2, lag_ratio=0.01))
        self.wait()

    def get_layer(self, layer_size, radius=0.3, fill_opacity=0.5, stroke_width=3, buff=1):
        layer = VGroup(
            Circle(radius=radius)
            for n in range(layer_size)
        )
        layer.set_fill(GREY, fill_opacity)
        layer.set_stroke(WHITE, stroke_width)
        layer.arrange(DOWN, buff=buff)

        return layer

    def get_connections(self, target, sources, max_stroke_width=1.5, colors=[BLUE, RED]):
        target.connections = VGroup()
        for neuron in sources:
            line = Line(
                neuron.get_center(),
                target.get_center(),
                buff=neuron.get_radius(),
                stroke_width=max_stroke_width * random.random(),
                stroke_color=random.choice(colors)
            )
            target.connections.add(line)
        return target.connections
