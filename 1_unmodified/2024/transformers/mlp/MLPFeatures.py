# ==============================================================================
# Scene:      MLPFeatures
# Source:     videos/_2024/transformers/mlp.py (lines 2202-2296)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl MLPFeatures.py MLPFeatures -w -m --fps 15
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



# ----- From _2024/transformers/mlp.py -----

class MLPFeatures(InteractiveScene):
    def construct(self):
        # Add neurons
        radius = 0.15
        layer1, layer2 = layers = VGroup(
            Dot(radius=radius).get_grid(n, 1, buff=radius / 2)
            for n in [8, 16]
        )
        layer2.arrange(DOWN, buff=radius)
        layers.arrange(RIGHT, buff=3.0)
        layers.to_edge(LEFT, buff=LARGE_BUFF)
        layers.set_stroke(WHITE, 1)
        for neuron in layer1:
            neuron.set_fill(opacity=random.random())
        layer2.set_fill(opacity=0)

        self.add(layers)

        # Add connections
        connections = get_network_connections(layer1, layer2)
        self.add(connections)

        # Show single-neuron features
        features = iter([
            "Table",
            "Slang",
            "AM Radio",
            "Humble",
            "Notebook",
            "Transparent",
            "Duration",
            "Madonna",
            "Mirror",
            "Pole Vaulting",
            "Albert Einstein",
            "Authentic",
            "Scientific",
            "Passionate",
            "Bell Laboratories",
            "Uzbekistan",
            "Umbrella",
            "Immanuel Kant",
            "Baroque Music",
            "Intense",
            "Clock",
            "Water skiing",
            "Ancient Egypt",
            "Ambiguous",
            "Volume",
            "Alexander the Great",
            "Innovative",
            "Religious",
        ])

        last_neuron = VGroup()
        last_feature_label = VGroup()
        for neuron in layer2[:15]:
            feature_label = Text(next(features), font_size=36)
            feature_label.next_to(neuron, buff=SMALL_BUFF)

            self.play(
                FadeOut(last_feature_label),
                FadeIn(feature_label),
                last_neuron.animate.set_fill(opacity=0),
                neuron.animate.set_fill(opacity=1),
            )

            last_neuron = neuron
            last_feature_label = feature_label

        # Show polysemantic features
        brace = Brace(layer2, RIGHT)

        def to_random_state(layer):
            for dot in layer.generate_target():
                dot.set_fill(opacity=random.random())
            return MoveToTarget(layer)

        self.play(
            feature_label.animate.scale(48 / 36).next_to(brace, RIGHT),
            GrowFromCenter(brace),
            to_random_state(layer2),
        )
        self.wait()
        for n in range(12):
            feature_label = Text(next(features))
            feature_label.next_to(brace, RIGHT)
            self.play(
                FadeOut(last_feature_label),
                FadeIn(feature_label),
                to_random_state(layer2),
            )
            self.wait(0.5)

            last_feature_label = feature_label
