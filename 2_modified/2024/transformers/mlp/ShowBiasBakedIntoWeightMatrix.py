# ==============================================================================
# Scene:      ShowBiasBakedIntoWeightMatrix
# Source:     videos/_2024/transformers/mlp.py (lines 2520-2622)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ShowBiasBakedIntoWeightMatrix.py ShowBiasBakedIntoWeightMatrix -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR now points to _lib/data (get_directories()["data"]) instead of Grant's output folder (GloVe, placeholder texts)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Chapter5_TN5.png  (_lib/assets/generated/2024/transformers/make_mlp_images.py)
#   - _lib/assets/raster_images/Chapter6_TN4.png  (_lib/assets/generated/2024/transformers/make_mlp_images.py)
# ==============================================================================

from __future__ import annotations
from scipy.stats import norm
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")


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



# ----- From _2024/transformers/mlp.py -----

class LastTwoChapters(InteractiveScene):
    def construct(self):
        # Show last two chapters
        frame = self.frame
        self.camera.light_source.set_z(15)
        self.set_floor_plane("xz")

        thumbnails = self.get_thumbnails()
        self.play(
            LaggedStartMap(FadeIn, thumbnails, shift=UP, lag_ratio=0.5)
        )
        self.wait()

        # Show transformer schematic
        blocks = Group(self.get_block() for x in range(10))
        blocks[1::2].stretch(2, 2).set_opacity(1)

        blocks.arrange(OUT, buff=0.5)
        blocks.set_depth(8, stretch=True)
        blocks.set_opacity(0.8)
        blocks.apply_depth_test()

        trans_title = Text("Transformer", font_size=96)
        trans_title.next_to(blocks, UP, buff=0.5)

        self.play(
            frame.animate.reorient(-32, 0, 0, (0.56, 2.48, 0.32), 12.75),
            thumbnails.animate.scale(0.5).arrange(RIGHT, buff=2.0).to_edge(UP, buff=0.25),
            LaggedStartMap(FadeIn, blocks, shift=0.25 * UP, scale=1.5, lag_ratio=0.1),
            FadeIn(trans_title, UP),
        )
        self.wait()

        # Break out transformer as sequence of blocks
        att_blocks = blocks[0::2]
        mlp_blocks = blocks[1::2]

        att_title = Text("Attention", font_size=72)
        mlp_title_full = Text("Multilayer Perceptron", font_size=72)
        mlp_title = Text("MLP", font_size=72)

        self.play(
            frame.animate.reorient(-3, -2, 0, (0.23, 2.57, 0.3), 12.75),
            trans_title.animate.shift(2 * UP),
            att_blocks.animate.shift(4 * LEFT),
            mlp_blocks.animate.shift(4 * RIGHT),
        )

        att_icon = self.get_att_icon(att_blocks[-1])
        mlp_icon = self.get_mlp_icon(mlp_blocks[-1])
        att_title.next_to(att_blocks[-1], UP, buff=0.75)
        for title in [mlp_title, mlp_title_full]:
            title.next_to(mlp_blocks[-1], UP, buff=0.75)
        self.play(
            FadeIn(att_icon, lag_ratio=1e-3),
            FadeIn(att_title, UP),
            trans_title.animate.scale(0.75).set_opacity(0.5)
        )
        self.wait()
        self.play(
            Write(mlp_icon),
            FadeIn(mlp_title_full, UP),
        )
        self.wait()
        self.play(
            TransformMatchingStrings(mlp_title_full, mlp_title)
        )
        self.wait()

        # Show sports facts
        sport_facts = VGroup(
            Text(line)
            for line in Path(DATA_DIR, "athlete_sports.txt").read_text().split("\n")
        )
        for fact in sport_facts:
            fact.next_to(trans_title, UP)
            fact.shift(random.uniform(-3, 3) * RIGHT)
            fact.shift(random.uniform(0, 3) * UP)

        self.remove(mlp_icon, mlp_title)
        self.play(
            FadeOut(thumbnails),
            FadeOut(trans_title),
            LaggedStart(
                (Succession(FadeIn(fact), fact.animate.scale(0.5).set_opacity(0).move_to(mlp_blocks))
                for fact in sport_facts),
                lag_ratio=0.15,
            )
        )
        self.wait()

        # Ask what is the MLP
        rect = SurroundingRectangle(Group(mlp_blocks, mlp_title), buff=1.0)
        rect.stretch(0.8, 1)
        rect.match_z(mlp_blocks[-1])
        question = Text("What are these?", font_size=90)
        question.next_to(rect, UP, buff=3.0)
        question.match_color(rect)
        question.set_fill(border_width=0.5)
        arrow = Arrow(question, rect)
        arrow.match_color(rect)

        self.play(
            Group(att_blocks, att_title).animate.fade(0.5),
            ShowCreation(rect),
            Write(question),
            GrowArrow(arrow),
        )
        self.wait()

    def get_thumbnails(self):
        folder = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2024/transformers/Thumbnails"
        images = [
            ImageMobject(str(Path(folder, "Chapter5_TN5"))),
            ImageMobject(str(Path(folder, "Chapter6_TN4"))),
        ]
        thumbnails = Group(
            Group(
                SurroundingRectangle(image, buff=0).set_stroke(WHITE, 3),
                image
            )
            for n, image in zip([5, 6], images)
        )
        thumbnails.set_height(3.5)
        thumbnails.arrange(RIGHT, buff=1.0)
        thumbnails.fix_in_frame()
        return thumbnails

    def get_att_icon(self, block, n_rows=8):
        att_icon = Dot().get_grid(n_rows, n_rows)
        att_icon.set_height(block.get_height() * 0.9)
        att_icon.set_backstroke(BLACK, 0.5)
        for dot in att_icon:
            dot.set_fill(opacity=random.random()**5)
        att_icon.move_to(block, OUT)
        return att_icon

    def get_mlp_icon(self, block, dot_buff=0.15, layer_buff=1.5, layer0_size=5):
        layers = VGroup(
            Dot().get_grid(layer0_size, 1, buff=dot_buff),
            Dot().get_grid(2 * layer0_size, 1, buff=dot_buff),
            Dot().get_grid(layer0_size, 1, buff=dot_buff),
        )
        layers.set_height(block.get_height() * 0.9)
        layers.arrange(RIGHT, buff=layer_buff)
        for layer in layers:
            for dot in layer:
                dot.set_fill(opacity=random.random())
        layers.set_stroke(WHITE, 0.5)
        lines = VGroup(
            Line(dot1.get_center(), dot2.get_center(), buff=dot1.get_width() / 2)
            for l1, l2 in zip(layers, layers[1:])
            for dot1 in l1
            for dot2 in l2
        )
        for line in lines:
            line.set_stroke(
                color=value_to_color(random.uniform(-10, 10)),
                width=3 * random.random()**3
            )

        icon = VGroup(layers, lines)
        icon.move_to(block, OUT)
        return icon

    def get_block(self, width=5, height=3, depth=1, color=GREY_D, opacity=0.8):
        block = Cube(color=color, opacity=opacity)
        block.deactivate_depth_test()
        block.set_shape(width, height, depth)
        block.set_shading(0.5, 0.5, 0.0)
        block.sort(lambda p: np.dot(p, [-1, 1, 1]))
        return block


class ShowBiasBakedIntoWeightMatrix(LastTwoChapters):
    def construct(self):
        # Add initial blocks
        frame = self.frame
        square = Square(2.0)
        att_icon = self.get_att_icon(square)
        att_icon.set_stroke(WHITE, 1, 0.5)
        mlp_icon = self.get_mlp_icon(square, layer_buff=1.0)
        lnm_icon = self.get_layer_norm_icon()
        lnm_icon.match_height(mlp_icon)

        att_block = self.get_block(att_icon, "Attention", "604M Parameters", color=YELLOW)
        mlp_block = self.get_block(mlp_icon, "MLP", "1.2B Parameters", color=BLUE)
        lnm_block = self.get_block(lnm_icon, "Layer Norm", "49K Parameters", color=GREY_B)

        blocks = VGroup(att_block, mlp_block, lnm_block)
        blocks.arrange(RIGHT, buff=1.5)

        lil_wrapper = self.get_layer_wrapper(blocks[:2].copy())
        big_wrapper = self.get_layer_wrapper(blocks)

        self.add(lil_wrapper, blocks[:2])
        frame.match_x(blocks[:2])
        self.wait()
        self.play(
            frame.animate.match_x(blocks),
            ReplacementTransform(lil_wrapper, big_wrapper),
            FadeIn(lnm_block, RIGHT),
        )
        self.wait()
        self.play(FlashAround(lnm_block[2], run_time=3, time_width=2))
        self.wait()

    def get_layer_norm_icon(self):
        axes1, axes2 = all_axes = VGroup(
            Axes((-4, 4), (0, 1, 0.25))
            for x in range(2)
        )
        all_axes.set_shape(1.5, 0.5)
        all_axes.arrange(DOWN, buff=1.0)
        graph1 = axes1.get_graph(lambda x: 0.5 * norm.pdf(0.5 * x - 0.5))
        graph2 = axes2.get_graph(lambda x: 1.5 * norm.pdf(x))
        graph1.set_stroke(BLUE).set_fill(BLUE, 0.25)
        graph2.set_stroke(BLUE).set_fill(BLUE, 0.25)
        arrow = Arrow(axes1, axes2, buff=0.1)

        return VGroup(axes1, graph1, arrow, axes2, graph2)

    def get_layer_wrapper(self, blocks):
        beige = "#F5F5DC"
        rect = self.get_block(blocks, color=beige, buff=0.5, height=4)[0]
        wrapped_arrow = self.get_wrapped_arrow(rect)
        multiple = Tex(R"\times 96")
        multiple.next_to(wrapped_arrow, UP)

        arrows = VGroup()
        for b1, b2 in zip(blocks, blocks[1:]):
            arrows.add(Arrow(b1[0], b2[0], buff=0.1))

        return VGroup(rect, arrows, wrapped_arrow, multiple)

    def get_block(
        self, content,
        upper_label="",
        lower_label="",
        upper_font_size=42,
        lower_font_size=36,
        buff=0.25,
        height=2,
        color=BLUE,
        stroke_width=3,
        fill_opacity=0.2
    ):
        block = SurroundingRectangle(content, buff=buff)
        block.set_height(height, stretch=True)
        block.round_corners(radius=0.25)
        block.set_stroke(color, 3)
        block.set_fill(color, fill_opacity)

        low_label = Text(lower_label, font_size=lower_font_size)
        low_label.next_to(block, DOWN, MED_SMALL_BUFF)
        top_label = Text(upper_label, font_size=upper_font_size)
        top_label.next_to(block, UP, MED_SMALL_BUFF)

        return VGroup(block, content, low_label, top_label)

    def get_wrapped_arrow(self, big_block, buff=0.75, color=GREY_B, stroke_width=4):
        vertices = [
            big_block.get_corner(RIGHT),
            big_block.get_corner(RIGHT) + buff * RIGHT,
            big_block.get_corner(UR) + buff * UR,
            big_block.get_corner(UL) + buff * UL,
            big_block.get_corner(LEFT) + buff * LEFT,
            big_block.get_corner(LEFT),
        ]
        line = Polygon(*vertices)
        line.round_corners()
        line.set_points(line.get_points()[:-2, :])
        line.set_stroke(color, stroke_width)
        tip = ArrowTip().move_to(line.get_end(), RIGHT)
        tip.set_color(color)
        line.add(tip)
        return line
