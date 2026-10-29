# ==============================================================================
# Scene:      ShowBitcoinBlockSize
# Source:     videos/_2017/crypto.py (lines 4817-4905)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowBitcoinBlockSize.py ShowBitcoinBlockSize -w -m --fps 15
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


class ShowBitcoinBlockSize(LedgerScene):
    CONFIG = {
        "denomination" : "BTC"
    }
    def construct(self):
        block = VGroup()
        ledger = self.get_ledger()

        payments = VGroup(*[
            self.add_payment_line_to_ledger(*args)
            for args in [
                ("Alice", "Bob", "0.42"),
                ("You", "Charlie", "3.14"),
                ("Bob", "You", "2.72"),
                ("Alice", "Charlie", "4.67"),
            ]
        ])
        dots = OldTex("\\vdots")
        dots.next_to(payments, DOWN)
        payments.add(dots)
        payments.to_edge(LEFT)
        payments.shift(DOWN+0.5*RIGHT)
        payments_rect = SurroundingRectangle(
            payments, color = WHITE, buff = MED_LARGE_BUFF
        )
        block.add(payments_rect, payments)

        tuples = [
            ("Prev hash", UP, BLUE_C), 
            ("Proof of work", DOWN, GREEN),
        ]
        for word, vect, color in tuples:
            mob = OldTexText(word)
            mob.set_color(color)
            rect = SurroundingRectangle(
                mob, color = WHITE, buff = MED_SMALL_BUFF
            )
            VGroup(mob, rect).next_to(payments_rect, vect, 0)
            rect.stretch_to_fit_width(payments_rect.get_width())
            block.add(mob, rect)

        title = VGroup(
            BitcoinLogo(height = 0.75), 
            OldTexText("Block").scale(1.5)
        )
        title.arrange(RIGHT, SMALL_BUFF)
        title.next_to(block, UP)

        brace = Brace(payments_rect, RIGHT)
        limit = brace.get_text(
            "Limited to\\\\", 
            "$\\sim 2{,}400$", "transactions"
        )
        limit.set_color_by_tex("2{,}400", RED)

        self.add(title, block)
        self.remove(payments)
        self.play(
            GrowFromCenter(brace),
            Write(limit)
        )
        self.play(LaggedStartMap(FadeIn, payments))
        self.wait()

        ####Visa

        visa_logo = SVGMobject(
            file_name = "visa_logo",
            height = 0.5,
            stroke_width = 0,
            fill_color = BLUE_D,
            fill_opacity = 1,
        )
        visa_logo[-1].set_color("#faa61a")
        visa_logo.sort()
        avg_rate = OldTexText("Avg: $1{,}700$/second")
        max_rate = OldTexText("Max: $>24{,}000$/second")
        rates = VGroup(avg_rate, max_rate)
        rates.scale(0.8)
        rates.arrange(DOWN, aligned_edge = LEFT)
        rates.next_to(visa_logo, RIGHT, buff = MED_SMALL_BUFF)
        visa = VGroup(visa_logo, rates)
        visa.to_corner(UP+RIGHT)

        self.play(LaggedStartMap(DrawBorderThenFill, visa_logo))
        self.play(LaggedStartMap(FadeIn, avg_rate))
        self.wait()
        self.play(LaggedStartMap(FadeIn, max_rate))
        self.wait(2)
