# ==============================================================================
# Scene:      Illustrate5Choose3
# Source:     videos/_2023/moser_reboot/main.py (lines 1228-1257)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Illustrate5Choose3.py Illustrate5Choose3 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Illustrate5Choose3(InteractiveScene):
    n = 5
    k = 3

    def construct(self):
        # Test
        row = Dot().replicate(self.n)
        row.arrange(RIGHT)
        rows = row.replicate(choose(self.n, self.k))
        rows.arrange(DOWN)

        indices = list(range(self.n))
        for tup, row in zip(it.combinations(indices, self.k), rows):
            for i in tup:
                row[i].set_color(BLUE)
                rect = SurroundingRectangle(row[i], buff=SMALL_BUFF)
                rect.set_stroke(BLUE, 2)
                row[i].add(rect)

        brace = Brace(rows, RIGHT, buff=SMALL_BUFF)
        count = Integer(1, font_size=60)
        count.next_to(brace, RIGHT, SMALL_BUFF)
        count.add_updater(lambda m: m.set_value(len(rows)))

        self.add(count)
        self.play(
            ShowIncreasingSubsets(rows),
            run_time=2,
        )
        self.wait()
