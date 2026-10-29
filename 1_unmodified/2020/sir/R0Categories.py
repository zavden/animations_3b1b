# ==============================================================================
# Scene:      R0Categories
# Source:     videos/_2020/sir.py (lines 2767-2871)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl R0Categories.py R0Categories -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class R0Categories(Scene):
    def construct(self):
        # Titles
        titles = VGroup(
            OldTex("R > 1", color=RED),
            OldTex("R = 1", color=YELLOW),
            OldTex("R < 1", color=GREEN),
        )
        titles.scale(1.25)
        titles.arrange(RIGHT, buff=2.7)
        titles.to_edge(UP)

        v_lines = VGroup()
        for t1, t2 in zip(titles, titles[1:]):
            v_line = Line(UP, DOWN)
            v_line.set_height(FRAME_HEIGHT)
            v_line.set_x(midpoint(t1.get_right(), t2.get_left())[0])
            v_lines.add(v_line)

        self.add(titles)
        self.add(v_lines)

        # Names
        names = VGroup(
            OldTexText("Epidemic", color=RED),
            OldTexText("Endemic", color=YELLOW),
            OldTexText("...Hypodemic?", color=GREEN),
        )
        for name, title in zip(names, titles):
            name.next_to(title, DOWN, MED_LARGE_BUFF)

        # Doubling dots
        dot = Dot(color=RED)
        dot.next_to(names[0], DOWN, LARGE_BUFF)
        rows = VGroup(VGroup(dot))
        lines = VGroup()
        for x in range(4):
            new_row = VGroup()
            new_lines = VGroup()
            for dot in rows[-1]:
                dot.children = [dot.copy(), dot.copy()]
                new_row.add(*dot.children)
            new_row.arrange(RIGHT)
            max_width = 4
            if new_row.get_width() > max_width:
                new_row.set_width(max_width)
            new_row.next_to(rows[-1], DOWN, LARGE_BUFF)
            for dot in rows[-1]:
                for child in dot.children:
                    new_lines.add(Line(
                        dot.get_center(),
                        child.get_center(),
                        buff=0.2,
                    ))
            rows.add(new_row)
            lines.add(new_lines)

        for row, line_row in zip(rows[:-1], lines):
            self.add(row)
            anims = []
            for dot in row:
                for child in dot.children:
                    anims.append(TransformFromCopy(dot, child))
            for line in line_row:
                anims.append(ShowCreation(line))
            self.play(*anims)
        self.play(FadeIn(names[0], UP))
        self.wait()

        exp_tree = VGroup(rows, lines)

        # Singleton dots
        mid_rows = VGroup()
        mid_lines = VGroup()

        for row in rows:
            dot = Dot(color=RED)
            dot.match_y(row)
            mid_rows.add(dot)

        for d1, d2 in zip(mid_rows[:-1], mid_rows[1:]):
            d1.child = d2
            mid_lines.add(Line(
                d1.get_center(),
                d2.get_center(),
                buff=0.2,
            ))

        for dot, line in zip(mid_rows[:-1], mid_lines):
            self.add(dot)
            self.play(
                TransformFromCopy(dot, dot.child),
                ShowCreation(line)
            )
        self.play(FadeIn(names[1], UP))
        self.wait()

        # Inverted tree
        exp_tree_copy = exp_tree.copy()
        exp_tree_copy.rotate(PI)
        exp_tree_copy.match_x(titles[2])

        self.play(TransformFromCopy(exp_tree, exp_tree_copy))
        self.play(FadeIn(names[2], UP))
        self.wait()
