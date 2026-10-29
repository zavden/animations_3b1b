# ==============================================================================
# Scene:      IllustrateNChooseK
# Source:     videos/_2023/moser_reboot/main.py (lines 1195-1225)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IllustrateNChooseK.py IllustrateNChooseK -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IllustrateNChooseK(InteractiveScene):
    n = 7
    k = 3
    show_count = False

    def construct(self):
        # Test2
        n = 7
        k = 3

        dots = Dot(radius=0.1).replicate(self.n)
        dots.arrange(RIGHT, buff=0.5)
        self.add(dots)

        rects = SurroundingRectangle(dots[0], buff=SMALL_BUFF).replicate(self.k)
        rects.set_stroke(BLUE)
        self.add(rects)

        if self.show_count:
            count = Integer(0, font_size=60)
            count.next_to(dots, DOWN, buff=MED_LARGE_BUFF)
            self.add(count)

        for subdots in it.combinations(dots, self.k):
            dots.set_color(WHITE)
            for dot, rect in zip(subdots, rects):
                rect.move_to(dot)
                dot.set_fill(BLUE)
            if self.show_count:
                count.set_value(count.get_value() + 1)
            self.wait(0.2)
