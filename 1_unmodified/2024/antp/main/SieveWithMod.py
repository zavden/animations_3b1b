# ==============================================================================
# Scene:      SieveWithMod
# Source:     videos/_2024/antp/main.py (lines 506-661)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SieveWithMod.py SieveWithMod -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy

class SieveWithMod(InteractiveScene):
    def construct(self):
        # Setup prime list title
        prime_title = Text("Primes: ", font_size=72)
        prime_title.to_edge(UP)
        prime_title.set_x(-5)

        self.add(prime_title)

        # Setup grid
        row_size = 12
        grid = Square().get_grid(20, row_size, buff=0)
        grid.set_stroke(GREY_B, 1)
        grid.set_width(FRAME_WIDTH - 5)
        grid.move_to(1.65 * UP, UP)
        labels = VGroup()
        labeled_boxes = VGroup()
        for n, square in enumerate(grid, start=1):
            label = Integer(n)
            label.set_max_width(0.5 * square.get_width())
            label.move_to(square)
            square.label = label
            labels.add(label)
            labeled_boxes.add(VGroup(square, label))

        self.add(grid)
        self.add(labels)

        # Do the initial sift
        non_primes = VGroup(
            label for label in labels
            if not sympy.isprime(label.get_value())
        )
        primes = VGroup(
            label for label in labels
            if sympy.isprime(label.get_value())
        )
        prime_list = primes.copy()
        prime_list.scale(72 / 48)
        prime_list.arrange(RIGHT, buff=MED_LARGE_BUFF, aligned_edge=DOWN)
        prime_list.next_to(prime_title, RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)
        self.play(
            non_primes.animate.set_fill(opacity=0.25),
            lag_ratio=0.025,
            run_time=5
        )
        self.wait()
        self.play(
            TransformFromCopy(primes, prime_list)
        )
        self.play(
            labels.animate.set_fill(opacity=1),
            FadeOut(prime_list)
        )

        # Reduction title
        reduction_label = Text("Reduce all mod")
        reduction_label.next_to(grid, UP, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        reduction_label.set_fill(GREY_A)
        reduction_label.set_fill(opacity=0)

        self.add(reduction_label)

        # Reduction game (this will be looped)
        arrows = VGroup()
        reductions = VGroup()
        colors = color_gradient([BLUE_E, BLUE_A, RED_E], 8)

        for _ in range(5):
            # Pull out the next prime
            prime_label = labels[1]
            prime_value = int(prime_label.get_value())
            highlight = SurroundingRectangle(prime_label)
            list_prime = prime_label.copy()
            list_prime.scale(72 / 48)
            list_prime.next_to(prime_title, RIGHT, buff=0.35, aligned_edge=DOWN)
            list_prime_highlight = SurroundingRectangle(list_prime)
            comma = Text(",")
            comma.next_to(list_prime.get_corner(DR), RIGHT, SMALL_BUFF)
            reduction_prime = prime_label.copy()
            reduction_prime.next_to(reduction_label, RIGHT, MED_SMALL_BUFF, DOWN)

            rows = VGroup(
                labeled_boxes[n:n + row_size]
                for n in range(0, len(grid), row_size)
            )
            rows.target = rows.generate_target()
            for row in rows.target:
                row.arrange(RIGHT, buff=0)
                row.set_width(grid.get_width())
                row.set_max_height(rows.target[0].get_height())
                row.align_to(rows.target[0], LEFT)
            rows.target.arrange(DOWN, buff=1.2)
            rows.target.move_to(grid, UP)

            self.play(
                ShowCreation(highlight),
                FadeOut(arrows),
                FadeOut(reductions),
            )
            self.play(
                TransformFromCopy(prime_label, list_prime),
                FadeIn(comma, UP),
                TransformFromCopy(highlight, list_prime_highlight),
            )
            self.play(
                FadeOut(list_prime_highlight),
                FadeOut(highlight),
                TransformFromCopy(list_prime, reduction_prime),
                reduction_label.animate.set_opacity(1),
                MoveToTarget(rows),
            )
            prime_title.add(list_prime)

            # Add reductions
            arrows = VGroup()
            reductions = VGroup()
            for label, box in zip(labels, grid):
                reduction = Integer(label.get_value() % prime_value)
                reduction.next_to(box, DOWN, buff=MED_LARGE_BUFF)
                reductions.add(reduction)
                color = YELLOW if label.get_value() % prime_value == 0 else BLUE
                arrow = Arrow(
                    label, reduction,
                    buff=0.15,
                    max_tip_length_to_length_ratio=0.4,
                    stroke_width=3,
                    stroke_color=GREY_A,
                )
                arrows.add(arrow)
                rect = SurroundingRectangle(reduction)
                rect.set_stroke(color, width=1)
                reduction.add(rect)

            for n, arrow, reduction in zip(it.count(), arrows, reductions):
                self.add(arrow, reduction)
                if n < 36:
                    self.wait(0.2 * (1 + (n % 2)))

            # Kill the zeros
            killed_indices = [
                n
                for n, label in enumerate(labels)
                if label.get_value() % prime_value == 0
            ]
            self.play(
                *(
                    LaggedStartMap(FadeOut, VGroup(group[n] for n in killed_indices), shift=0.1 * DOWN, lag_ratio=0.1)
                    for group in [labeled_boxes, arrows, reductions]
                ),
                FadeOut(reduction_prime)
            )

            for group in [labeled_boxes, grid, labels, arrows, reductions]:
                to_remove = [group[n] for n in killed_indices]
                group.remove(*to_remove)
