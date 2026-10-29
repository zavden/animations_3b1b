# ==============================================================================
# Scene:      AskWhatToAddToProtocol
# Source:     videos/_2017/crypto.py (lines 2340-2358)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhatToAddToProtocol.py AskWhatToAddToProtocol -w -m --fps 15
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


class AskWhatToAddToProtocol(InitialProtocol):
    def construct(self):
        self.add_title()
        items = VGroup(*list(map(self.get_new_item, [
            "Broadcast transactions",
            "Only accept signed transactions",
            "No overspending",
        ] + [""]*6)))
        brace = Brace(VGroup(*items[3:]), LEFT)
        question = OldTexText("What to \\\\ add here?")
        question.set_color(RED)
        question.scale(1.5)
        brace.set_color(RED)
        question.next_to(brace, LEFT)

        self.add(*items[:3])
        self.play(GrowFromCenter(brace))
        self.play(Write(question))
        self.wait()
