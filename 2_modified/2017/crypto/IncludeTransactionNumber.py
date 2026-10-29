# ==============================================================================
# Scene:      IncludeTransactionNumber
# Source:     videos/_2017/crypto.py (lines 1401-1504)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IncludeTransactionNumber.py IncludeTransactionNumber -w -m --fps 15
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


class IncludeTransactionNumber(LedgerScene):
    CONFIG = {
        "ledger_width" : 7,
    }
    def construct(self):
        self.add_ledger_and_network()
        self.add_signed_payment()
        self.fail_to_sign_new_transaction()
        self.copy_payment_many_times()
        self.add_ids()

    def add_signed_payment(self):
        line = self.add_payment_line_to_ledger(
            "Alice", "Bob", 100
        )
        signature = self.get_signature()
        signature.scale(0.7)
        signature.next_to(line, RIGHT)
        signature.save_state()
        signature.scale(0.1)
        signature.move_to(self.alice)

        self.play(Write(line, run_time = 1))
        self.play(
            signature.restore,
            self.alice.change, "raise_left_hand"
        )
        self.wait()
        self.play(self.alice.change, "happy")
        self.wait()

        line.add(signature)

    def fail_to_sign_new_transaction(self):
        payment = self.add_payment_line_to_ledger("Alice", "Bob", 3000)
        q_marks = OldTex("???")
        q_marks.next_to(payment, RIGHT)
        cross = Cross(payment)
        payment.save_state()
        payment.move_to(self.bob.get_corner(UP+LEFT))
        payment.set_fill(opacity = 0)

        self.play(
            self.bob.change, "raise_right_hand",
            payment.restore,
        )
        self.play(
            self.bob.change, "confused",
            Write(q_marks)
        )
        self.play(ShowCreation(cross))
        self.wait()
        self.play(*list(map(FadeOut, [payment, cross, q_marks])))
        self.ledger.content.remove(payment)

    def copy_payment_many_times(self):
        line = self.ledger.content[-1]
        copies = VGroup(*[line.copy() for x in range(4)])
        copies.arrange(DOWN, buff = MED_SMALL_BUFF)
        copies.next_to(line, DOWN, buff = MED_SMALL_BUFF)

        self.play(
            LaggedStartMap(FadeIn, copies, run_time = 3),
            self.bob.change, "conniving",
        )
        self.play(self.alice.change, "angry")
        self.wait()

        self.copies = copies

    def add_ids(self):
        top_line = self.ledger.content[-1]
        lines = VGroup(top_line, *self.copies)
        numbers = VGroup()
        old_signatures = VGroup()
        new_signatures = VGroup()
        colors = list(Color(BLUE_B).range_to(GREEN_B, len(lines)))
        for i, line in enumerate(lines):
            number = OldTex(str(i))
            number.scale(0.7)
            number.set_color(YELLOW)
            number.next_to(line, LEFT)
            numbers.add(number)
            line.add_to_back(number)
            old_signature = line[-1]
            new_signature = self.get_signature()
            new_signature.replace(old_signature)
            new_signature.set_color(colors[i])
            old_signatures.add(old_signature)
            new_signatures.add(VGroup(new_signature))
            line.remove(old_signature)

        self.play(
            Write(numbers),
            self.alice.change, "thinking"
        )
        self.play(FadeOut(old_signatures))
        self.play(ReplacementTransform(
            lines.copy(), new_signatures,
            lag_ratio = 0.5,
            run_time = 2,
        ))
        self.play(self.bob.change, "erm")
        self.wait(2)
