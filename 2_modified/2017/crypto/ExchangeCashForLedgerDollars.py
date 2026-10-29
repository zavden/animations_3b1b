# ==============================================================================
# Scene:      ExchangeCashForLedgerDollars
# Source:     videos/_2017/crypto.py (lines 1900-1964)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExchangeCashForLedgerDollars.py ExchangeCashForLedgerDollars -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
# ==============================================================================

from manim_imports_ext import *

class TenDollarBill(VGroup):
    CONFIG = {
        "color" : GREEN,
        "height" : 0.5,
        "mark_paths_closed" : False,
    }
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        rect = Rectangle(
            height = 2.61,
            width = 6.14,
            color = self.color,
            mark_paths_closed = False,
            fill_color = BLACK,
            fill_opacity = 1,
        )
        rect.set_height(self.height)
        oval = Circle()
        oval.stretch_to_fit_height(0.7*self.height)
        oval.stretch_to_fit_width(0.4*self.height)
        rect.add_subpath(oval.get_points())

        pi = Randolph(
            mode = "pondering",
            color = GREEN_B
        )
        pi.set_width(oval.get_width())
        pi.move_to(oval)
        pi.shift(0.1*pi.get_height()*DOWN)

        self.add(pi, rect)
        for vect in UP+LEFT, DOWN+RIGHT:
            ten = OldTex("\\$10")
            ten.set_height(0.25*self.height)
            ten.next_to(self.get_corner(vect), -vect, SMALL_BUFF)
            ten.set_color(GREEN_C)
            self.add(ten)


class LedgerScene(PiCreatureScene):
    CONFIG = {
        "ledger_width" : 6,
        "ledger_height" : 7,
        "denomination" : "USD",
        "ledger_line_height" : 0.4,
        "sign_transactions" : False,
        "enumerate_lines" : False,
        "line_number_color" : YELLOW,
    }
    def setup(self):
        PiCreatureScene.setup(self)
        self.remove(self.pi_creatures)

    def add_ledger_and_network(self):
        self.add(self.get_ledger(), self.get_network())

    def get_ledger(self):
        title = OldTexText("Ledger")
        rect = Rectangle(
            width = self.ledger_width, 
            height = self.ledger_height
        )
        title.next_to(rect.get_top(), DOWN)
        h_line = Line(rect.get_left(), rect.get_right())
        h_line.scale(0.8)
        h_line.set_stroke(width = 2)
        h_line.next_to(title, DOWN)
        content = VGroup(h_line)

        self.ledger = VGroup(rect, title, content)
        self.ledger.content = content
        self.ledger.to_corner(UP+LEFT)
        return self.ledger

    def add_line_to_ledger(self, string_or_mob):
        if isinstance(string_or_mob, str):
            mob = OldTexText(string_or_mob)
        elif isinstance(string_or_mob, Mobject):
            mob = string_or_mob
        else:
            raise Exception("Invalid input")

        items = self.ledger.content

        mob.set_height(self.ledger_line_height)
        if self.enumerate_lines:
            num = OldTex(str(len(items)) + ".")
            num.scale(0.8)
            num.set_color(self.line_number_color)
            num.next_to(mob, LEFT, MED_SMALL_BUFF)
            mob.add_to_back(num)
        mob.next_to(
            items[-1], DOWN, 
            buff = MED_SMALL_BUFF, 
            aligned_edge = LEFT
        )
        if self.enumerate_lines and len(items) == 1:
            mob.shift(MED_LARGE_BUFF * LEFT)
        items.add(mob)
        return mob

    def add_payment_line_to_ledger(self, from_name, to_name, amount):
        amount_str = str(amount)
        if self.denomination == "USD":
            amount_str = "\\$" + amount_str
        else:
            amount_str += " " + self.denomination
        line_tex_parts = [
            from_name.capitalize(), 
            "pays" if from_name.lower() != "you" else "pay",
            to_name.capitalize(),
            amount_str,
        ]
        if self.sign_transactions:
            line_tex_parts.append(self.get_signature_tex())
        line = OldTexText(*line_tex_parts)
        for name in from_name, to_name:
            color = self.get_color_from_name(name)
            line.set_color_by_tex(name.capitalize(), color)
        if self.sign_transactions:
            from_part = line.get_part_by_tex(from_name.capitalize())
            line[-1].set_color(from_part.get_color())

        amount_color = {
            "USD" : GREEN,
            "BTC" : YELLOW,
            "LD" : YELLOW,
        }.get(self.denomination, WHITE)
        line.set_color_by_tex(amount_str, amount_color)

        return self.add_line_to_ledger(line)

    def get_color_from_name(self, name):
        if hasattr(self, name.lower()):
            creature = getattr(self, name.lower())
            color = creature.get_color()
            # CHANGE: get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
            if np.mean(color_to_rgb(color)) < 0.5:
                color = average_color(color, color, WHITE)
            return color
        return WHITE

    def animate_payment_addition(self, *args, **kwargs):
        line = self.add_payment_line_to_ledger(*args, **kwargs)
        self.play(LaggedStartMap(
            FadeIn, 
            VGroup(*it.chain(*line)),
            run_time = 1
        ))

    def get_network(self):
        creatures = self.pi_creatures
        lines = VGroup(*[
            Line(
                VGroup(pi1, pi1.label), VGroup(pi2, pi2.label),
                buff = MED_SMALL_BUFF,
                stroke_width = 2,
            )
            for pi1, pi2 in it.combinations(creatures, 2)
        ])
        labels = VGroup(*[pi.label for pi in creatures])
        self.network = VGroup(creatures, labels, lines)
        self.network.lines = lines
        return self.network

    def create_pi_creatures(self):
        creatures = VGroup(*[
            PiCreature(color = color, height = 1).shift(2*vect)
            for color, vect in zip(
                [BLUE_C, MAROON_D, GREY_BROWN, BLUE_E],
                [UP+LEFT, UP+RIGHT, DOWN+LEFT, DOWN+RIGHT],
            )
        ])
        creatures.to_edge(RIGHT)
        names = self.get_names()
        for name, creature in zip(names, creatures):
            setattr(self, name, creature)
            label = OldTexText(name.capitalize())
            label.scale(0.75)
            label.next_to(creature, DOWN, SMALL_BUFF)
            creature.label = label
            if (creature.get_center() - creatures.get_center())[0] > 0:
                creature.flip()
            creature.look_at(creatures.get_center())

        return creatures

    def get_names(self):
        return ["alice", "bob", "charlie", "you"]

    def get_signature_tex(self):
        if not hasattr(self, "nonce"):
            self.nonce = 0
        binary = bin(hash(str(self.nonce)))[-8:]
        self.nonce += 1
        return binary + "\\dots"

    def get_signature(self, color = BLUE_C):
        result = OldTex(self.get_signature_tex())
        result.set_color(color)
        return result

    def add_ellipsis(self):
        last_item = self.ledger.content[-1]
        dots = OldTex("\\vdots")
        dots.next_to(last_item.get_left(), DOWN)
        last_item.add(dots)
        self.add(last_item)


class ExchangeCashForLedgerDollars(LedgerScene):
    CONFIG = {
        "sign_transactions" : True,
        "denomination" : "LD",
        "ledger_width" : 7.5,
        "ledger_height" : 6,
    }
    def construct(self):
        self.add_ledger_and_network()
        self.add_ellipsis()
        self.add_title()
        self.give_ten_dollar_bill()
        self.add_bob_pays_alice_line()
        self.everyone_thinks()

    def add_title(self):
        self.ledger.shift(DOWN)
        title = OldTexText(
            "Exchange", "LD", "for", "\\$\\$\\$"
        )
        title.set_color_by_tex("LD", YELLOW)
        title.set_color_by_tex("\\$", GREEN)
        title.scale(1.3)
        title.to_edge(UP).shift(LEFT)

        self.play(Write(title))
        self.wait()

    def give_ten_dollar_bill(self):
        bill = TenDollarBill()
        bill.next_to(self.alice.get_corner(UP+RIGHT), UP)
        bill.generate_target()
        bill.target.next_to(self.bob.get_corner(UP+LEFT), UP)

        arrow = Arrow(bill, bill.target, color = GREEN)

        small_bill = bill.copy()
        small_bill.scale(0.01, about_point = bill.get_bottom())

        self.play(
            ReplacementTransform(small_bill, bill),
            self.alice.change, "raise_right_hand"
        )
        self.play(ShowCreation(arrow))
        self.play(MoveToTarget(bill))
        self.play(self.bob.change, "happy", bill)
        self.wait()

    def add_bob_pays_alice_line(self):
        line = self.add_payment_line_to_ledger(
            "Bob", "Alice", 10
        )
        line.save_state()
        line.scale(0.01)
        line.move_to(self.bob.get_corner(UP+LEFT))
        self.play(self.bob.change, "raise_right_hand", line)
        self.play(line.restore, run_time = 2)
        self.wait()

    def everyone_thinks(self):
        self.play(*[
            ApplyMethod(pi.change, "thinking", self.ledger)
            for pi in self.pi_creatures
        ])
        self.wait(4)
