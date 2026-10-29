# ==============================================================================
# Scene:      KScaling
# Source:     videos/_2026/2025_p6/problem_intro.py (lines 486-634)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KScaling.py KScaling -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KScaling(InteractiveScene):
    def construct(self):
        # Expression
        expression = Tex(R"k^2 + 2k - 3", font_size=60)
        expression.to_edge(UP)

        k_tracker = ValueTracker(5)
        get_k = lambda: int(k_tracker.get_value())

        self.add(expression)

        # Blocks
        block_size = 0.15
        block_template = Square(side_length=block_size).set_stroke(WHITE, 1).set_fill(BLUE, 1)
        block_template = VGroup(
            Square(block_size).set_stroke(WHITE, 1).set_fill(BLUE, 0.5),
            Cross(Square(0.8 * block_size)).set_stroke(RED, 2)
        )
        block_top = 1.0 * UP

        def get_k_squared_blocks():
            k = int(get_k())
            squares = block_template.get_grid(k, k)
            squares.set_max_width(4.25)
            squares.move_to(4.5 * LEFT + block_top, UP).shift_onto_screen()
            return squares

        def get_k_blocks():
            k = int(get_k())
            squares = block_template.get_grid(2, k)
            squares.set_max_width(4.25)
            squares.move_to(RIGHT).shift_onto_screen()
            squares.align_to(block_top, UP)
            return squares

        k_squared_blocks = get_k_squared_blocks()
        k_blocks = get_k_blocks()

        neg_3 = block_template.get_grid(1, 3)
        neg_3.set_stroke(RED, 2).set_fill(opacity=0)
        neg_3.move_to(5.5 * RIGHT).align_to(k_squared_blocks, UP)

        # Add k label
        k_label = Tex(R"k = 0")
        k_label.to_edge(UP, buff=0.25)
        num_part = k_label.make_number_changeable("0", edge_to_fix=LEFT)
        num_part.add_updater(lambda m: m.set_value(get_k()))

        number_line = NumberLine(
            (0, 50),
            tick_size=0.05,
            longer_tick_multiple=2,
            big_tick_spacing=10,
            width=6
        )
        number_line.to_edge(UP, buff=0.75)
        k_tip = ArrowTip(angle=-90 * DEG).set_height(0.2)
        k_tip.set_fill(TEAL)
        k_tip.add_updater(lambda m: m.move_to(number_line.n2p(get_k()), DOWN))
        k_label.add_updater(lambda m: m.next_to(k_tip, UP, SMALL_BUFF, aligned_edge=LEFT))

        # Animate
        terms = [expression["k^2"], expression["+ 2k"], expression["- 3"]]
        self.play(
            LaggedStart(
                terms[0].animate.next_to(k_squared_blocks, UP),
                terms[1].animate.next_to(k_blocks, UP),
                terms[2].animate.next_to(neg_3, UP),
                lag_ratio=0.5,
            ),
            LaggedStart(
                ShowIncreasingSubsets(k_squared_blocks, suspend_mobject_updating=True),
                ShowIncreasingSubsets(k_blocks, suspend_mobject_updating=True),
                ShowIncreasingSubsets(neg_3),
                lag_ratio=0.5,
            ),
            FadeIn(k_tip, time_span=(1, 2)),
            FadeIn(k_label, time_span=(1, 2)),
            FadeIn(number_line, time_span=(1, 2)),
            run_time=2
        )

        self.play(
            k_tracker.animate.set_value(30),
            UpdateFromFunc(k_squared_blocks, lambda m: m.become(get_k_squared_blocks())),
            UpdateFromFunc(k_blocks, lambda m: m.become(get_k_blocks())),
            run_time=5
        )
        self.wait()

        # Highlight parts
        frame = self.frame
        rect = SurroundingRectangle(VGroup(expression["k^2"], k_squared_blocks))
        k = get_k()

        edges1 = VGroup(
            Line(
                block.get_corner(DR),
                block.get_corner(UR)
            )
            for block in k_squared_blocks
        )
        edges2 = VGroup(
            VMobject().set_points_as_corners([
                block.get_corner(DR),
                block.get_corner(UR),
                block.get_corner(UL),
            ])
            for block in k_squared_blocks[:2 * k]
        )
        edges1.set_stroke(YELLOW, 4)
        edges2.set_stroke(YELLOW, 4)

        k_squared_blocks.target = k_squared_blocks.generate_target()
        for block in k_squared_blocks.target:
            block[0].set_opacity(0.25)
            block[1].set_stroke(width=1)

        self.play(
            MoveToTarget(k_squared_blocks),
            FadeIn(edges1, lag_ratio=0.01, time_span=(1, 3)),
            frame.animate.reorient(0, 0, 0, (-4.52, 0.34, 0.00), 2.83),
            terms[0].animate.scale(0.75, about_edge=DOWN),
            run_time=3,
        )
        self.wait()

        terms[0].target = terms[0].generate_target()
        terms[0].target.shift(0.25 * LEFT)
        terms[1].target = terms[1].generate_target()
        terms[1].target.scale(0.75, about_edge=DOWN)
        terms[1].target.next_to(terms[0].target, RIGHT, SMALL_BUFF, aligned_edge=DOWN)

        k_squared_blocks.target = k_squared_blocks.generate_target()
        for block in k_squared_blocks.target[:2 * k]:
            block[0].set_opacity(0.5)

        self.play(
            MoveToTarget(terms[0]),
            MoveToTarget(terms[1]),
            MoveToTarget(k_squared_blocks),
            VGroup(k_squared_blocks[2 * k:], edges1[2 * k:]).animate.shift(0.25 * DOWN),
            run_time=2,
        )
        self.play(
            ShowCreation(edges2, lag_ratio=0.01),
            k_blocks.animate.set_opacity(0.25)
        )
        self.wait(2)
