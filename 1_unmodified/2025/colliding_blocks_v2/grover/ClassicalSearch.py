# ==============================================================================
# Scene:      ClassicalSearch
# Source:     videos/_2025/colliding_blocks_v2/grover.py (lines 95-138)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ClassicalSearch.py ClassicalSearch -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ClassicalSearch(InteractiveScene):
    def construct(self):
        # Test
        in_out = VGroup(ArrowTip(), ArrowTip(angle=PI))
        in_out.arrange(RIGHT, buff=0.5)
        in_out.set_shape(1.75, 0.75)
        box = Square().set_shape(1.5, 1)
        machine = Union(in_out, box)
        machine.set_fill(GREY_E, 1).set_stroke(GREY_B, 2)
        machine.set_z_index(1)
        self.add(machine)

        items = VGroup(Integer(n) for n in range(25))
        items.arrange(DOWN, buff=0.5)
        items.next_to(box, LEFT, LARGE_BUFF)
        items.shift((box.get_y() - items[0].get_y()) * UP)

        self.add(items)

        # Loop through
        key = 12
        last_sym = VMobject()
        for n in range(key + 1):
            item = items[n]
            self.play(
                items.animate.shift((box.get_y() - item.get_y()) * UP),
                FadeOut(last_sym)
            )
            sym = Checkmark().set_color(GREEN) if n == key else Exmark().set_color(RED)
            sym.set_height(0.75)
            sym.next_to(box, RIGHT, LARGE_BUFF)
            self.play(
                FadeOutToPoint(item.copy(), box.get_right(), time_span=(0, 0.7)),
                FadeInFromPoint(sym, box.get_left(), time_span=(0.3, 1)),
            )
            last_sym = sym

        rect = SurroundingRectangle(items[key])
        rect.set_stroke(GREEN, 3)
        self.play(
            items[:n].animate.set_opacity(0.5),
            ShowCreation(rect),
            items[n + 1:].animate.set_opacity(0.5),
        )
