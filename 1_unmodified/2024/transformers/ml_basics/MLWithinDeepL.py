# ==============================================================================
# Scene:      MLWithinDeepL
# Source:     videos/_2024/transformers/ml_basics.py (lines 20-295)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl MLWithinDeepL.py MLWithinDeepL -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/transformers/helpers.py -----

if TYPE_CHECKING:
    from typing import Optional
    from manimlib.typing import Vect3, ManimColor


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


class NeuralNetwork(VGroup):
    def __init__(
        self,
        layer_sizes=[6, 12, 6],
        neuron_radius=0.1,
        v_buff_ratio=1.0,
        h_buff_ratio=7.0,
        max_stroke_width=2.0,
        stroke_decay=2.0,
    ):
        self.max_stroke_width = max_stroke_width
        self.stroke_decay = stroke_decay
        layers = VGroup(*(
            Dot(radius=neuron_radius).get_grid(n, 1, v_buff_ratio=v_buff_ratio)
            for n in layer_sizes
        ))
        layers.arrange(RIGHT, buff=h_buff_ratio * layers[0].get_width())

        lines = VGroup(*(
            VGroup(*(
                Line(
                    n1.get_center(),
                    n2.get_center(),
                    buff=n1.get_width() / 2,
                )
                for n1, n2 in it.product(l1, l2)
            ))
            for l1, l2 in zip(layers, layers[1:])
        ))

        super().__init__(layers, lines)
        self.layers = layers
        self.lines = lines

        self.randomize_layer_values()
        self.randomize_line_style()

    def randomize_layer_values(self):
        for group in self.lines:
            for line in group:
                line.set_stroke(
                    value_to_color(random.uniform(-10, 10)),
                    self.max_stroke_width * random.random()**self.stroke_decay,
                )
        return self

    def randomize_line_style(self):
        for layer in self.layers:
            for dot in layer:
                dot.set_stroke(WHITE, 1)
                dot.set_fill(WHITE, random.random())
        return self


class WeightMatrix(DecimalMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: tuple[int, int] = (6, 8),
        value_range: tuple[float, float] = (-9.9, 9.9),
        ellipses_row: Optional[int] = -2,
        ellipses_col: Optional[int] = -2,
        num_decimal_places: int = 1,
        bracket_h_buff: float = 0.1,
        decimal_config=dict(include_sign=True),
        low_positive_color: ManimColor = BLUE_E,
        high_positive_color: ManimColor = BLUE_B,
        low_negative_color: ManimColor = RED_E,
        high_negative_color: ManimColor = RED_B,
    ):
        if values is not None:
            shape = values.shape
        self.shape = shape
        self.value_range = value_range
        self.low_positive_color = low_positive_color
        self.high_positive_color = high_positive_color
        self.low_negative_color = low_negative_color
        self.high_negative_color = high_negative_color
        self.ellipses_row = ellipses_row
        self.ellipses_col = ellipses_col

        if values is None:
            values = np.random.uniform(*self.value_range, size=shape)

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_fill(color=value_to_color(
                entry.get_value(),
                self.low_positive_color,
                self.high_positive_color,
                self.low_negative_color,
                self.high_negative_color,
                0, max(self.value_range),
            ))
        return self



# ----- From _2024/transformers/ml_basics.py -----

class MLWithinDeepL(InteractiveScene):
    def construct(self):
        # Organize boxes
        kw = dict(font_size=36, opacity=0.25)
        model_boxes = VGroup(
            self.get_titled_box("Multilayer Perceptrons", BLUE_D, **kw),
            self.get_titled_box("Convolutional Neural Networks", BLUE_D, **kw),
            self.get_titled_box("Transformers", BLUE, **kw),
        )
        for box in model_boxes:
            box.box.set_width(model_boxes.get_width(), stretch=True)
        dots = Tex(R"\vdots", font_size=72)
        model_boxes.add(dots)
        model_boxes.arrange(DOWN, buff=0.1)
        dots.shift(0.2 * DOWN)
        transformer_box = model_boxes[2]

        dl_box = self.get_titled_box(
            "Deep Learning", TEAL,
            font_size=60,
            y_space=model_boxes.get_height() + 1.0,
            x_space=2.75,
            opacity=0.05
        )

        model_boxes.next_to(dl_box.title, DOWN)

        # Animate in word
        transformer_box.save_state()
        transformer_box.box.set_opacity(0)
        transformer_box.set_height(1)
        transformer_box.move_to(np.array([-1.58, -2.01, 0]))

        self.add(transformer_box)
        self.wait()
        self.add(dl_box, transformer_box)
        self.play(LaggedStart(
            FadeIn(dl_box, scale=1.2),
            Restore(transformer_box),
            *(FadeIn(model_boxes[i]) for i in [0, 1, 3]),
        ), lag_ratio=0.75, run_time=2)
        self.wait()

        dl_box.add(model_boxes)
        self.add(dl_box)

        # Place within ML box
        ml_box = self.get_titled_box(
            "Machine Learning",
            GREEN,
            opacity=0.1,
            font_size=72,
            x_space=6.0,
            y_space=5.0
        )
        dl_box.target = dl_box.generate_target()
        blank_boxes = dl_box.box.replicate(2)
        inner_boxes = VGroup(*blank_boxes, dl_box.target)
        reg_drawing = self.get_regression_drawing()
        bayes_net = self.get_bayes_net_drawing()
        for drawing, box in zip([reg_drawing, bayes_net], blank_boxes):
            drawing.set_height(0.8 * box.get_height())
            drawing.move_to(box)
            box.add(drawing)
        inner_boxes.set_height(3.5)
        inner_boxes.arrange(RIGHT)
        inner_boxes.set_max_width(ml_box.get_width() - 0.5)
        inner_boxes.next_to(ml_box.title, DOWN, buff=1.0)

        self.add(ml_box, dl_box, blank_boxes)
        self.play(
            FadeIn(ml_box),
            MoveToTarget(dl_box),
            LaggedStartMap(FadeIn, blank_boxes, scale=2.0, lag_ratio=0.5)
        )
        self.wait()

        ml_box.add(dl_box, blank_boxes)

        # Learn from data
        words = Text("Learn from data", font_size=72)
        words.to_edge(UP, buff=MED_SMALL_BUFF)
        learn = words["Learn"][0]
        learn.save_state()
        learn.set_x(0)
        words["data"].set_color(YELLOW)
        ml_box.target = ml_box.generate_target()
        ml_box.target.scale(0.75)
        ml_box.target.to_edge(DOWN)
        arrow = Arrow(ml_box.target, words)

        self.play(
            MoveToTarget(ml_box),
            GrowFromCenter(arrow),
            TransformFromCopy(ml_box.title["Learn"][0], learn),
        )
        self.play(
            Restore(learn),
            FadeIn(words["from data"][0], lag_ratio=0.1, shift=0.2 * RIGHT),
        )
        self.wait()
        self.play(
            FadeOut(ml_box),
            FadeOut(arrow),
        )
        self.wait()

        # Go back to the box
        self.clear()
        ml_box.center()
        self.add(ml_box)

        # Pop out
        ml_box.remove(dl_box)
        ml_box.add(dl_box.copy())
        ml_box.target = ml_box.generate_target()
        ml_box.target.scale(0.25).to_edge(LEFT)
        dl_box.target = dl_box.generate_target()
        dl_box.target.scale(2.0)
        dl_box.target.next_to(ml_box.target, RIGHT, buff=0.75),
        lines = VGroup(*(
            Line(
                ml_box.target[-1].get_corner(RIGHT + v),
                dl_box.target.get_corner(LEFT + v)
            )
            for v in [UP, DOWN]
        ))
        lines.set_stroke(TEAL, 2)

        self.play(
            MoveToTarget(ml_box),
            MoveToTarget(dl_box),
            GrowFromPoint(lines[0], dl_box.get_corner(UR)),
            GrowFromPoint(lines[1], dl_box.get_corner(DR)),
            run_time=1.5,
        )
        self.wait()

        # Show a neural network
        network = NeuralNetwork([5, 10, 5])
        network.next_to(dl_box, RIGHT, buff=1.0)

        self.play(
            FadeIn(network.layers[0]),
            ShowCreation(network.lines[0], lag_ratio=0.01),
            FadeIn(network.layers[1], lag_ratio=0.5),
            run_time=2
        )
        self.play(
            ShowCreation(network.lines[1], lag_ratio=0.01),
            FadeIn(network.layers[2], lag_ratio=0.5),
            run_time=2
        )

        # Ambiently change the network
        for _ in range(6):
            self.play(
                network.animate.randomize_line_style().randomize_layer_values(),
                run_time=3,
                lag_ratio=1e-4
            )

        # Pile of matrices
        pile_words = Text("Pile of matrices")
        pile_words.next_to(network, UP)
        path_arc = -60 * DEGREES
        arrow = Arrow(dl_box.get_top(), pile_words.get_corner(UL), path_arc=path_arc)
        matrices = VGroup(*(
            WeightMatrix(shape=(8, 6), ellipses_row=None, ellipses_col=None)
            for x in range(10)
        ))
        matrices.match_width(network)
        matrices.move_to(network, UP)
        matrices.shift(0.5 * DOWN)
        matrix_shift = 0.5 * (IN + RIGHT)

        matrices.arrange(OUT, buff=0.25)
        matrices.move_to(network)

        for matrix in matrices[:-1]:
            matrix.target = matrix.generate_target()
            for entry in matrix.target.get_entries():
                dot = Dot(radius=0.05)
                dot.set_fill(entry.get_fill_color(), opacity=0.25)
                dot.move_to(entry)
                entry.become(dot)
            matrix.target[-1].set_opacity(0.25)
        matrices[-1].get_entries().set_backstroke(BLACK, 8)

        self.play(
            FadeOut(network, 2 * DOWN),
            ShowCreation(arrow),
            FadeInFromPoint(pile_words, dl_box.title.get_center(), path_arc=path_arc),
            FadeOut(network, DOWN)
        )
        mat_shift = 0.5 * IN + 0.25 * DOWN
        self.play(
            LaggedStart(*(
                Succession(
                    FadeIn(matrix, shift=mat_shift),
                    MoveToTarget(matrix)
                )
                for matrix in matrices[:-1]
            ), lag_ratio=0.25, run_time=5),
            Animation(Point()),
            FadeIn(matrices[-1], shift=mat_shift, time_span=(3.75, 4.75))
        )
        self.wait()

    def get_titled_box(self, text, color, font_size=48, y_space=0.5, x_space=0.5, opacity=0.1):
        title = Text(text, font_size=font_size)
        box = Rectangle(
            title.get_width() + x_space,
            title.get_height() + y_space
        )
        box.set_fill(interpolate_color(BLACK, color, opacity), 1)
        box.set_stroke(color, 2)
        title.next_to(box.get_top(), DOWN, buff=MED_SMALL_BUFF)
        result = VGroup(box, title)
        result.box = box
        result.title = title
        return result

    def get_regression_drawing(self):
        axes = Axes((-1, 10), (-1, 10))
        m = 0.5
        y0 = 2
        line = axes.get_graph(lambda x: y0 + m * x)
        line.set_stroke(YELLOW, 2)
        dots = VGroup(
            Dot(axes.c2p(x, y0 + m * x + np.random.normal()))
            for x in np.random.uniform(0, 10, 15)
        )

        reg_drawing = VGroup(axes, dots, line)
        return reg_drawing

    def get_bayes_net_drawing(self):
        radius = MED_SMALL_BUFF
        node = Circle(radius=radius)
        node.set_stroke(GREY_B, 2)
        node.shift(2 * DOWN)
        nodes = VGroup(
            node.copy().shift(x * RIGHT + y * UP)
            for x, y in [
                (-1, 0),  
                (1, 0),
                (-2, 2),
                (0, 2),
                (2, 2),
                (-2, 4),
                (0, 4),
            ]
        )
        edge_index_pairs = [
            (2, 0),
            (3, 0),
            (3, 1),
            (4, 1),
            (5, 2),
            (6, 3),
        ]
        edges = VGroup()
        for i1, i2 in edge_index_pairs:
            n1, n2 = nodes[i1], nodes[i2]
            edge = Arrow(
                n1.get_center(), 
                n2.get_center(),
                buff=radius,
                color=WHITE,
                stroke_width=3
            )
            edges.add(edge)

        network = VGroup(nodes, edges)
        return network
