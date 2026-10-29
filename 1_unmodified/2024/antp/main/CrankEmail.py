# ==============================================================================
# Scene:      CrankEmail
# Source:     videos/_2024/antp/main.py (lines 806-1009)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CrankEmail.py CrankEmail -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CrankEmail(InteractiveScene):
    def construct(self):
        # Background
        rect = FullScreenRectangle(fill_color=WHITE, fill_opacity=1)
        rect.scale(2)
        rect.stretch(10, 1, about_edge=UP)
        self.add(rect)

        frame = self.frame
        frame.set_height(9)
        frame.to_edge(UP, buff=0)

        # Rows of numbers
        numbers1 = list(range(1, 100))
        numbers2 = list(filter(lambda m: m % 2 != 0, numbers1))
        numbers3 = list(filter(lambda m: m % 3 != 0, numbers2))

        arrays = VGroup(
            self.create_array(numbers1[:30], 2, BLUE_D),
            self.create_array(numbers2[:30], 3, GREEN_D),
            self.create_array(numbers3[:20], 5, RED_D),
        )

        arrays.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        arrays.to_corner(UL)

        # Paragraphs
        kw = dict(alignment="LEFT", font_size=48, fill_color=BLACK, font="Roboto")
        paragraphs = VGroup(
            Text("""
                Dear sir,

                I have proven the twin prime conjecture.

                I study an elegant proof of prime generation:
                List all natural numbers, and start by
                reducing each of them modulo 2:
            """, **kw),
            arrays[0],
            Text("""
                Remove numbers which have reduced
                to 0, reduce what remains modulo 3:
            """, **kw),
            arrays[1],
            Text("""
                Again, remove numbers which have reduced
                to 0, reduce what remains modulo 5:
            """, **kw),
            arrays[2],
        )

        paragraphs.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        paragraphs.shift(paragraphs[0].get_x() * LEFT)
        paragraphs.to_edge(UP, buff=0.2)

        self.add(paragraphs)
        for array in arrays:
            for grid in array:
                self.remove(grid[1])

        # Fill in grid, slide frame
        self.anticipate_frame_to_y(-5, run_time=3)
        for grid in arrays[0]:
            self.animate_reduction(grid)

        self.cross_out_the_zeros(arrays[0])
        self.wait(0.5)
        self.play(frame.animate.set_y(-11))

        for n, grid in enumerate(arrays[1]):
            self.animate_reduction(grid)
            if n == 0:
                self.anticipate_frame_to_y(-15, run_time=2)

        self.anticipate_frame_to_y(-22, run_time=2)
        self.cross_out_the_zeros(arrays[1])
        self.wait(2)

        for grid in arrays[2]:
            self.animate_reduction(grid)
        self.cross_out_the_zeros(arrays[2])

    def create_array(
        self,
        numbers,
        modulus,
        color=BLUE,
        height=0.85,
        spacing=10,
        buff=0.75,
        width=10,
    ):
        result = VGroup()
        row1_content = numbers
        row2_content = [n % modulus for n in numbers]
        row1_title = "Numbers: "
        row2_title = f"Mod {modulus}:"
        n = 0
        while n < len(row1_content):
            result.add(self.create_table(
                row1_title, row2_title,
                row1_content[n:n + spacing],
                row2_content[n:n + spacing],
                color=color,
                height=height,
            ))
            n += spacing
            row1_title = ""
            row2_title = ""
        result.arrange(DOWN, buff=buff, aligned_edge=RIGHT)
        result.set_width(width)
        return result

    def create_table(
        self,
        row1_title,
        row2_title,
        row1_content,
        row2_content,
        x_spacing=0.6,
        font_size=36,
        color=BLUE,
        height=0.85
    ):
        # Numbers
        row1_mobs, row2_mobs = (
            VGroup(*(
                Integer(n, font_size=font_size)
                for n in content
            ))
            for content in [row1_content, row2_content]
        )
        for x, mob in enumerate(row1_mobs):
            mob.set_x(x_spacing * x)
        row1_mobs.to_edge(LEFT)
        row1_mobs.set_fill(BLACK)

        row2_mobs.set_color(color)
        for m1, m2 in zip(row1_mobs, row2_mobs):
            m2.set_max_width(0.5 * x_spacing)
            m2.next_to(m1, DOWN, 0.5)

        grid = VGroup(row1_mobs, row2_mobs)

        # Titles
        row1_label = Text(row1_title, font_size=font_size)
        row2_label = Text(row2_title, font_size=font_size)
        row1_label.set_color(BLACK)
        row1_label.next_to(row1_mobs, LEFT, buff=0.5)
        row2_label.next_to(row2_mobs, LEFT, buff=0.5)
        row2_label.set_color(color)
        grid.add(row1_label, row2_label)

        # Grid lines
        h_line = Line(ORIGIN, grid.get_width() * RIGHT)
        h_line.move_to(grid, LEFT)
        v_lines = VGroup(*(
            Line(grid.get_height() * UP, ORIGIN).set_x(
                0.5 * (row1_mobs[i].get_right()[0] + row1_mobs[i + 1].get_left()[0])
            ).align_to(grid, UP)
            for i in range(len(row1_mobs) - 1)
        ))
        v_lines.set_stroke(BLACK, width=1)
        h_line.set_stroke(BLACK, width=1)

        grid.add(h_line, v_lines)
        grid.set_height(height, about_edge=LEFT)

        return grid

    def animate_reduction(self, array, beat_time=0.17):
        reductions = array[1]
        self.remove(reductions)
        self.wait(0.1)
        for i, term in enumerate(reductions):
            self.add(term)
            self.wait(beat_time)
            m10 = i % 10
            if m10 % 2 == 1:
                self.wait(beat_time)
            if m10 == 9:
                self.wait(beat_time)
        self.add(array)

    def cross_out_the_zeros(self, array):
        crosses = VGroup()
        rects = VGroup()
        for grid in array:
            for m1, m2 in zip(grid[0], grid[1]):
                if m2.get_value() == 0:
                    crosses.add(Cross(m1).scale(1.5))
                    rect = SurroundingRectangle(VGroup(m1, m2))
                    rect.set_fill(RED, 0.2)
                    rect.set_stroke(width=0)
                    rects.add(rect)
        self.play(
            ShowCreation(crosses, lag_ratio=0),
            FadeIn(rects, lag_ratio=0.1)
        )

    def anticipate_frame_to_y(self, y, run_time=3):
        turn_animation_into_updater(
            ApplyMethod(self.frame.set_y, y, run_time=run_time)
        )
