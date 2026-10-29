# ==============================================================================
# Scene:      TransitionToDistributedLedger
# Source:     videos/_2017/crypto.py (lines 2084-2233)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TransitionToDistributedLedger.py TransitionToDistributedLedger -w -m --fps 15
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


class DistributedLedgerScene(LedgerScene):
    def get_large_network(self):
        network = self.get_network()
        network.set_height(FRAME_HEIGHT - LARGE_BUFF)
        network.center()
        for pi in self.pi_creatures:
            pi.label.scale(0.8, about_point = pi.get_bottom())
        return network

    def get_distributed_ledgers(self):
        ledger = self.get_ledger()
        title = ledger[1]
        h_line = ledger.content
        title.set_width(0.7*ledger.get_width())
        title.next_to(ledger.get_top(), DOWN, MED_LARGE_BUFF)
        h_line.next_to(title, DOWN)
        added_lines = VGroup(*[h_line.copy() for x in range(5)])
        added_lines.arrange(DOWN, buff = MED_LARGE_BUFF)
        added_lines.next_to(h_line, DOWN, MED_LARGE_BUFF)
        ledger.content.add(added_lines)

        ledgers = VGroup()
        for pi in self.pi_creatures:
            pi.ledger = ledger.copy()
            pi.ledger.set_height(pi.get_height())
            pi.ledger[0].set_color(pi.get_color())
            vect = pi.get_center()-self.pi_creatures.get_center()
            x_vect = vect[0]*RIGHT
            pi.ledger.next_to(pi, x_vect, SMALL_BUFF)
            ledgers.add(pi.ledger)
        return ledgers

    def add_large_network_and_distributed_ledger(self):
        self.add(self.get_large_network())
        self.add(self.get_distributed_ledgers())


class TransitionToDistributedLedger(DistributedLedgerScene):
    CONFIG = {
        "sign_transactions" : True,
        "ledger_width" : 7.5,
        "ledger_height" : 6,
        "enumerate_lines" : True,
        "denomination" : "LD",
        "line_number_color" : WHITE,
        "ledger_line_height" : 0.35,
    }
    def construct(self):
        self.add_ledger_and_network()
        self.ledger.shift(DOWN)
        self.add_ellipsis()

        self.ask_where_is_ledger()
        self.add_various_payements()
        self.ask_who_controls_ledger()
        self.distribute_ledger()
        self.broadcast_transaction()
        self.ask_about_ledger_consistency()

    def ask_where_is_ledger(self):
        question = OldTexText("Where", "is", "this?!")
        question.set_color(RED)
        question.scale(1.5)
        question.next_to(self.ledger, UP)

        self.play(Write(question))
        self.wait()

        self.question = question

    def add_various_payements(self):
        payments = VGroup(*[
            self.add_payment_line_to_ledger(*payment)
            for payment in [
                ("Alice", "Bob", 20),
                ("Charlie", "You", 100),
                ("You", "Alice", 50),
                ("Bob", "You", 30),
            ]
        ])

        for payment in payments:
            self.play(LaggedStartMap(FadeIn, payment, run_time = 1))
            self.wait()

    def ask_who_controls_ledger(self):
        new_question = OldTexText("Who", "controls", "this?!")
        new_question.scale(1.3)
        new_question.move_to(self.question)
        new_question.set_color(RED)

        self.play(Transform(self.question, new_question))
        self.play(*[
            ApplyMethod(pi.change, "confused", new_question)
            for pi in self.pi_creatures
        ])
        self.wait(2)

    def distribute_ledger(self):
        ledger = self.ledger
        self.ledger_width = 6
        self.ledger_height = 7
        distribute_ledgers = self.get_distributed_ledgers()
        group = VGroup(self.network, distribute_ledgers)

        self.play(FadeOut(self.question))
        self.play(ReplacementTransform(
            VGroup(ledger), distribute_ledgers
        ))
        self.play(*[
            ApplyMethod(pi.change, "pondering", pi.ledger)
            for pi in self.pi_creatures
        ])
        self.play(
            group.set_height, FRAME_HEIGHT - 2,
            group.center
        )
        self.wait(2)

    def broadcast_transaction(self):
        payment = OldTexText(
            "Alice", "pays", "Bob", "100 LD"
        )
        payment.set_color_by_tex("Alice", self.alice.get_color())
        payment.set_color_by_tex("Bob", self.bob.get_color())
        payment.set_color_by_tex("LD", YELLOW)
        payment.scale(0.75)
        payment.add_background_rectangle()
        payment_copies = VGroup(*[
            payment.copy().next_to(pi, UP)
            for pi in self.pi_creatures
        ])
        payment = payment_copies[0]

        self.play(
            self.alice.change, "raise_right_hand", payment,
            Write(payment, run_time = 2)
        )
        self.wait()
        self.play(
            ReplacementTransform(
                VGroup(payment), payment_copies, 
                run_time = 3,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            Broadcast(self.alice.get_corner(UP+RIGHT)),
            self.alice.change, "happy"
        )
        self.wait()
        pairs = list(zip(payment_copies, self.pi_creatures))
        Scene.play(self, *it.chain(*[
            [
                pi.look_at, pi.ledger[-1],
                line.scale, 0.2,
                line.next_to, pi.ledger[-1], DOWN, SMALL_BUFF,
            ]
            for line, pi in pairs
        ]))
        self.wait(3)

        for line, pi in pairs:
            pi.ledger.add(line)

    def ask_about_ledger_consistency(self):
        ledgers = VGroup(*[
            pi.ledger
            for pi in self.pi_creatures
        ])

        self.play(
            FadeOut(self.network),
            ledgers.scale, 2,
            ledgers.arrange, RIGHT,
            ledgers.space_out_submobjects,
        )

        question = OldTexText("Are these the same?")
        question.scale(1.5)
        question.to_edge(UP)
        arrows = VGroup(*[
            Arrow(question.get_bottom(), ledger.get_top())
            for ledger in ledgers
        ])

        self.play(*list(map(ShowCreation, arrows)))
        self.play(Write(question))
        self.wait()
