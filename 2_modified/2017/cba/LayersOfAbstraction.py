# ==============================================================================
# Scene:      LayersOfAbstraction
# Source:     videos/_2017/cba.py (lines 19-221)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LayersOfAbstraction.py LayersOfAbstraction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo saved numbered stills with file_writer.get_image_file_path/get_image; GL has no such API: hold each state for 1 s in the video instead
# ==============================================================================

from manim_imports_ext import *

class EnumerableSaveScene(Scene):
    def setup(self):
        self.save_count = 0

    def save_enumerated_image(self):
        # CHANGE: Cairo saved numbered stills with file_writer.get_image_file_path/get_image; GL has no such API: hold each state for 1 s in the video instead
        self.wait(1)
        self.save_count += 1


class LayersOfAbstraction(EnumerableSaveScene):
    def construct(self):
        self.save_count = 0
        # self.add_title()
        self.show_layers()
        self.show_pairwise_relations()
        self.circle_certain_pairs()

    def add_title(self):
        title = OldTexText("Layers of abstraction")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        line = Line(LEFT, RIGHT)
        line.set_width(FRAME_WIDTH)
        line.next_to(title, DOWN, SMALL_BUFF)

        self.add(title, line)

    def show_layers(self):
        layers = self.layers = self.get_layers()
        for layer in layers:
            self.add(layer[0])

        self.save_enumerated_image()
        for layer in layers:
            self.add(layer)
            self.save_enumerated_image()

    def show_pairwise_relations(self):
        p1, p2 = [l.get_left() for l in self.layers[2:4]]
        down_arrow = Arrow(p2, p1, path_arc=PI)
        down_words = OldTexText("``For example''")
        down_words.scale(0.8)
        down_words.next_to(down_arrow, LEFT)
        up_arrow = Arrow(p1, p2, path_arc=-PI)
        up_words = OldTexText("``In general''")
        up_words.scale(0.8)
        up_words.next_to(up_arrow, LEFT)

        VGroup(up_words, down_words).set_color(YELLOW)

        self.add(down_arrow, down_words)
        self.save_enumerated_image()
        self.remove(down_arrow, down_words)
        self.add(up_arrow, up_words)
        self.save_enumerated_image()
        self.remove(up_arrow, up_words)

    def circle_certain_pairs(self):
        layers = self.layers

        for l1, l2 in zip(layers, layers[1:]):
            group = VGroup(l1, l2)
            group.save_state()
            layers.save_state()
            layers.fade(0.75)
            rect = SurroundingRectangle(group)
            rect.set_stroke(YELLOW, 5)
            group.restore()
            self.add(rect)
            self.save_enumerated_image()
            self.remove(rect)
            layers.restore()

    #

    def get_layers(self):
        layers = VGroup(*[
            VGroup(Rectangle(height=1, width=5))
            for x in range(6)
        ])
        layers.arrange(UP, buff=0)
        layers.set_stroke(GREY, 2)
        layers.set_sheen(1, UL)

        # Layer 0: Quantities
        triangle = Triangle().set_height(0.25)
        tri_dots = VGroup(*[Dot(v) for v in triangle.get_vertices()])
        dots_rect = VGroup(*[Dot() for x in range(12)])
        dots_rect.arrange_in_grid(3, 4, buff=SMALL_BUFF)
        for i, color in enumerate([RED, GREEN, BLUE]):
            dots_rect[i::4].set_color(color)
        pi_chart = VGroup(*[
            Sector(start_angle=a, angle=TAU / 3)
            for a in np.arange(0, TAU, TAU / 3)
        ])
        pi_chart.set_fill(opacity=0)
        pi_chart.set_stroke(WHITE, 2)
        pi_chart[0].set_fill(BLUE, 1)
        pi_chart.rotate(PI / 3)
        pi_chart.match_height(dots_rect)
        quantities = VGroup(tri_dots, dots_rect, pi_chart)
        quantities.arrange(RIGHT, buff=LARGE_BUFF)

        # Layer 1: Numbers
        numbers = VGroup(
            OldTex("3"),
            OldTex("3 \\times 4"),
            OldTex("1 / 3"),
        )
        for number, quantity in zip(numbers, quantities):
            number.move_to(quantity)

        # Layer 2: Algebra
        algebra = VGroup(
            OldTex("x^2 - 1 = (x + 1)(x - 1)")
        )
        algebra.set_width(layers.get_width() - MED_LARGE_BUFF)

        # Layer 3: Functions
        functions = VGroup(
            OldTex("f(x) = 0"),
            OldTex("\\frac{df}{dx}"),
        )
        functions.set_height(layers[0].get_height() - 2 * SMALL_BUFF)
        functions.arrange(RIGHT, buff=LARGE_BUFF)
        # functions.match_width(algebra)

        # Layer 4: Vector space
        t2c_map = {
            "\\textbf{v}": YELLOW,
            "\\textbf{w}": PINK,
        }
        vector_spaces = VGroup(
            OldTex(
                "\\textbf{v} + \\textbf{w} ="
                "\\textbf{w} + \\textbf{v}",
                tex_to_color_map=t2c_map,
            ),
            OldTex(
                "s(\\textbf{v} + \\textbf{w}) ="
                "s\\textbf{v} + s\\textbf{w}",
                tex_to_color_map=t2c_map,
            ),
        )
        vector_spaces.arrange(DOWN, buff=MED_SMALL_BUFF)
        vector_spaces.set_height(layers[0].get_height() - MED_LARGE_BUFF)
        v, w = vectors = VGroup(
            Vector([2, 1, 0], color=YELLOW),
            Vector([1, 2, 0], color=PINK),
        )
        vectors.add(DashedLine(v.get_end(), v.get_end() + w.get_vector()))
        vectors.add(DashedLine(w.get_end(), w.get_end() + v.get_vector()))
        vectors.match_height(vector_spaces)
        vectors.next_to(vector_spaces, RIGHT)
        vectors.set_stroke(width=2)
        # vector_spaces.add(vectors)

        inner_product = OldTex(
            "\\langle f, g \\rangle ="
            "\\int f(x)g(x)dx"
        )
        inner_product.match_height(vector_spaces)
        inner_product.next_to(vector_spaces, RIGHT)
        vector_spaces.add(inner_product)

        # Layer 5: Categories
        dots = VGroup(Dot(UP), Dot(UR), Dot(RIGHT))
        arrows = VGroup(
            Arrow(dots[0], dots[1], buff=SMALL_BUFF),
            Arrow(dots[1], dots[2], buff=SMALL_BUFF),
            Arrow(dots[0], dots[2], buff=SMALL_BUFF),
        )
        arrows.set_stroke(width=2)
        arrow_labels = VGroup(
            OldTex("m_1").next_to(arrows[0], UP, SMALL_BUFF),
            OldTex("m_2").next_to(arrows[1], RIGHT, SMALL_BUFF),
            OldTex("m_2 \\circ m_1").rotate(-45 * DEGREES).move_to(
                arrows[2]
            ).shift(MED_SMALL_BUFF * DL)
        )
        categories = VGroup(dots, arrows, arrow_labels)
        categories.set_height(layers[0].get_height() - MED_SMALL_BUFF)

        # Put it all together
        all_content = [
            quantities, numbers, algebra,
            functions, vector_spaces, categories,
        ]

        for layer, content in zip(layers, all_content):
            content.move_to(layer)
            layer.add(content)
            layer.content = content

        layer_titles = VGroup(*map(TexText, [
            "Quantities",
            "Numbers",
            "Algebra",
            "Functions",
            "Vector spaces",
            "Categories",
        ]))
        for layer, title in zip(layers, layer_titles):
            title.next_to(layer, RIGHT)
            layer.add(title)
            layer.title = title
        layers.titles = layer_titles

        layers.center()
        layers.to_edge(DOWN)
        layers.shift(0.5 * RIGHT)
        return layers
