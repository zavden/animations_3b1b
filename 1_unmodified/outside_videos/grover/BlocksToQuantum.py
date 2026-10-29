# ==============================================================================
# Scene:      BlocksToQuantum
# Source:     videos/outside_videos/grover.py (lines 105-214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BlocksToQuantum.py BlocksToQuantum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BlocksToQuantum(InteractiveScene):
    def construct(self):
        # Wall
        wall_height = 2
        block_height = 1.0
        block_style = dict(
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLUE_E,
            fill_opacity=1,
            shading=(0.5, 0.25, 0),
        )

        floor = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        floor.to_edge(DOWN, buff=0.5)
        floor.shift(RIGHT)
        wall = Line(DOWN, UP).set_height(wall_height)
        wall.move_to(floor.get_left(), DOWN)
        VGroup(floor, wall).set_stroke(WHITE, 2)

        self.add(floor, wall)

        # Blocks
        left_block = Square(side_length=block_height)
        left_block.set_style(**block_style)
        left_block.move_to(floor, DOWN)
        left_block.shift(2 * LEFT)

        right_blocks = left_block.get_grid(3, 3, buff=0)
        right_blocks.move_to(floor, DOWN)
        right_blocks.to_edge(RIGHT)

        self.add(left_block)
        self.add(right_blocks)

        all_blocks = VGroup(left_block, *right_blocks)

        # Add names
        names = [
            "David", "Bob", "Charlie",
            "Eve", "Alice", "Joan",
            "Kathy", "Morty", "Lily", "Randy"
        ]
        name_labels = VGroup(*map(Text, names))
        name_labels.set_width(0.8 * left_block.get_width())

        for block, label in zip(all_blocks, name_labels):
            label.move_to(block)
            block.add(label)

        # Show state vector
        coefs = DecimalNumber(-math.sqrt(0.1), edge_to_fix=RIGHT).replicate(4)
        coefs.set_color(RED)
        state_tex = VGroup(
            coefs[0], Tex(fR"|\text{{{names[0]}}}\rangle"), Tex("+"),
            coefs[1], Tex(fR"|\text{{{names[1]}}}\rangle"), Tex("+"),
            coefs[2], Tex(fR"|\text{{{names[2]}}}\rangle"), Tex("+"),
            Tex(R"\cdots"), Tex("+"),
            coefs[-1], Tex(fR"|\text{{{names[-1]}}}\rangle"),
        )
        state_tex.arrange(RIGHT, buff=0.15)
        state_tex.set_width(FRAME_WIDTH - 1)
        state_tex.to_edge(UP)

        self.add(state_tex)

        # Arrows
        arrows = VGroup()
        for block in all_blocks:
            arrow = Vector(0.75 * LEFT)
            arrow.set_color(RED)
            arrow.move_to(block.get_left(), RIGHT)
            arrow.shift(0.25 * block_height * UP)
            arrows.add(arrow)
            arrows.add(arrow)
            block.arrow = arrow

        self.add(arrows)

        # Slide
        dist = (left_block.get_left() - wall.get_center())[0]
        self.add(all_blocks, arrows)
        self.play(
            all_blocks.animate.shift(dist * LEFT),
            arrows.animate.shift(dist * LEFT),
            rate_func=linear,
            run_time=3,
        )
        left_block.arrow.flip(UP, about_point=left_block.get_center())
        coefs[0].set_value(-coefs[0].get_value())
        self.wait()

        dist = (right_blocks.get_left() - left_block.get_right())[0]
        self.play(
            left_block.animate.shift(0.5 * dist * RIGHT),
            right_blocks.animate.shift(0.5 * dist * LEFT),
            arrows[0].animate.shift(0.5 * dist * RIGHT),
            arrows[1:].animate.shift(0.5 * dist * LEFT),
            run_time=1.5,
            rate_func=linear
        )
        left_block.arrow.flip(UP, about_point=left_block.get_center())
        for arrow in arrows[1:]:
            arrow.scale(0.5, about_edge=RIGHT)

        coefs[0].set_value(-0.42)
        for coef in coefs[1:]:
            coef.set_value(-0.29)

        self.wait()
