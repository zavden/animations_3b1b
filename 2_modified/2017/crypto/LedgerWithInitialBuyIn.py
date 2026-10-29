# ==============================================================================
# Scene:      LedgerWithInitialBuyIn
# Source:     videos/_2017/crypto.py (lines 1610-1763)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LedgerWithInitialBuyIn.py LedgerWithInitialBuyIn -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
# ==============================================================================

from manim_imports_ext import *

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


class SignedLedgerScene(LedgerScene):
    CONFIG = {
        "sign_transactions" : True,
        "enumerate_lines" : True,
        "ledger_width" : 7.5,
    }


class LedgerWithInitialBuyIn(SignedLedgerScene):
    def construct(self):
        self.add_ledger_and_network()
        self.everyone_buys_in()
        self.add_initial_lines()
        self.add_charlie_payments()
        self.point_out_charlie_is_broke()
        self.running_balance()

    def everyone_buys_in(self):
        center = self.network.get_center()
        moneys = VGroup(*[
            OldTex("\\$100")
            for pi in self.pi_creatures
        ])
        moneys.set_color(GREEN)
        for pi, money in zip(reversed(self.pi_creatures), moneys):
            vect = pi.get_center() - center
            money.next_to(center, vect, SMALL_BUFF)
            money.add_background_rectangle()
            money.save_state()
            money.scale(0.01)
            corner = pi.get_corner(UP + np.sign(vect[0])*LEFT)
            money.move_to(corner)

        self.play(
            LaggedStartMap(
                ApplyMethod, moneys,
                lambda m : (m.restore,)
            ),
            self.charlie.change, "raise_right_hand",
            self.you.change, "raise_right_hand",
        )
        self.network.add(moneys)

    def add_initial_lines(self):
        lines = VGroup()
        for name in self.get_names():
            new_line = OldTexText(
                name.capitalize(), 
                "get" if name == "you" else "gets",
                "\\$100"
            )
            new_line.set_color_by_tex(
                name.capitalize(),
                self.get_color_from_name(name)
            )
            new_line.set_color_by_tex("100", GREEN)
            self.add_line_to_ledger(new_line)
            lines.add(new_line)
        line = Line(LEFT, RIGHT)
        line.set_width(self.ledger.get_width())
        line.scale(0.9)
        line.next_to(lines[-1], DOWN, SMALL_BUFF, LEFT)
        line.set_stroke(width = 1)
        lines[-1].add(line)

        self.play(
            LaggedStartMap(FadeIn, lines),
            *[
                ApplyMethod(pi.change, "thinking", self.ledger)
                for pi in self.pi_creatures
            ]
        )
        self.wait()

    def add_charlie_payments(self):
        payments = [
            ("Charlie", "Alice", 50),
            ("Charlie", "Bob", 50),
            ("Charlie", "You", 20),
        ]
        new_lines = VGroup(*[
            self.add_payment_line_to_ledger(*payment)
            for payment in payments
        ])

        for line in new_lines:
            self.play(Write(line, run_time = 1))
            self.wait()

    def point_out_charlie_is_broke(self):
        charlie_lines = VGroup(*[
            VGroup(*self.ledger.content[i][1:5])
            for i in (3, 5, 6, 7)
        ])
        rects = VGroup(*[
            SurroundingRectangle(line)
            for line in charlie_lines
        ])
        rects.set_color(YELLOW)
        rects.set_stroke(width = 2)
        last_rect = rects[-1]
        last_rect.set_stroke(RED, 4)
        rects.remove(last_rect)
        invalid = OldTexText("Invalid")
        invalid.set_color(RED)
        invalid.next_to(last_rect, DOWN)

        self.play(ShowCreation(rects))
        self.play(self.charlie.change_mode, "guilty")
        self.wait()
        self.play(ShowCreation(last_rect))
        self.play(*[
            ApplyMethod(pi.change, "sassy", self.charlie)
            for pi in self.pi_creatures
            if pi is not self.charlie
        ])
        self.play(Write(invalid))
        self.wait(2)
        self.play(*list(map(FadeOut, [rects, last_rect, invalid])))

    def running_balance(self):
        charlie_lines = VGroup(*[
            VGroup(*self.ledger.content[i][1:5])
            for i in (3, 5, 6, 7)
        ])
        signatures = VGroup(*[
            self.ledger.content[i][5]
            for i in (5, 6, 7)
        ])
        rect = Rectangle(color = WHITE)
        rect.set_fill(BLACK, 0.8)
        rect.stretch_to_fit_height(self.ledger.get_height() - 2*MED_SMALL_BUFF)
        title = OldTexText("Charlie's running \\\\ balance")
        rect.stretch_to_fit_width(title.get_width() + 2*MED_SMALL_BUFF)
        rect.move_to(self.ledger.get_right())
        title.next_to(rect.get_top(), DOWN)
        balance = VGroup(rect, title)

        lines = VGroup(*list(map(TexText, [
            "\\$100", "\\$50", "\\$0", "Overdrawn"
        ])))
        lines.set_color(GREEN)
        lines[-1].set_color(RED)
        arrows = VGroup()
        for line, c_line in zip(lines, charlie_lines):
            line.next_to(rect.get_left(), RIGHT, LARGE_BUFF)
            line.shift(
                (c_line.get_center() - line.get_center())[1]*UP
            )
            arrow = Arrow(c_line, line)
            arrows.add(arrow)

        self.pi_creatures.remove(self.alice, self.charlie)
        self.play(
            FadeOut(signatures),
            FadeIn(balance)
        )
        self.play(
            LaggedStartMap(FadeIn, lines, run_time = 3),
            LaggedStartMap(ShowCreation, arrows, run_time = 3),
        )
        self.wait()
