# ==============================================================================
# Scene:      ProtocolWithDigitalSignatures
# Source:     videos/_2017/crypto.py (lines 1506-1523)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProtocolWithDigitalSignatures.py ProtocolWithDigitalSignatures -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InitialProtocol(Scene):
    def construct(self):
        self.add_title()
        self.show_first_two_items()

    def add_title(self):
        title = OldTexText("Protocol")
        title.scale(1.5)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(4)
        h_line.next_to(title, DOWN)
        self.h_line = h_line
        self.title = title
        self.add(title, h_line)

    def show_first_two_items(self):
        items = VGroup(*list(map(self.get_new_item, [
            "Anyone can add lines to the Ledger",
            "Settle up with real money each month"
        ])))

        for item in items:
            self.wait()
            self.play(LaggedStartMap(FadeIn, item))
        self.wait(2)

    def get_new_item(self, item_string):
        item = OldTexText("$\\cdot$ %s"%item_string)
        if not hasattr(self, "items"):
            self.items = VGroup(item)
            self.items.next_to(self.h_line, DOWN, MED_LARGE_BUFF)
        else:
            item.next_to(self.items, DOWN, MED_LARGE_BUFF, LEFT)
            self.items.add(item)
        return item


class ProtocolWithDigitalSignatures(InitialProtocol):
    def construct(self):
        self.force_skipping()
        InitialProtocol.construct(self)
        self.revert_to_original_skipping_status()

        rect = SurroundingRectangle(self.items[-1])
        rect.set_color(RED)

        new_item = self.get_new_item(
            "Only signed transactions are valid"
        )
        new_item.set_color(YELLOW)

        self.play(Write(new_item))
        self.wait()
        self.play(ShowCreation(rect))
        self.wait()
