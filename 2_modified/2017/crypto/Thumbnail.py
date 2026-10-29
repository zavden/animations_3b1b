# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/crypto.py (lines 5211-5238)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
#   - Cairo arrow points were edited by hand (cubic anchors/handles of the line); GL arrows are one shape, so the points edit made a wedge: put the arrow between the blocks with put_start_and_end_on
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


class DistributedBlockChainScene(DistributedLedgerScene):
    CONFIG = {
        "block_height" : 0.5,
        "block_width" : 0.5,
        "n_blocks" : 3,
    }
    def get_distributed_ledgers(self):
        ledgers = VGroup()
        point = self.pi_creatures.get_center()
        for pi in self.pi_creatures:
            vect = pi.get_center() - point
            vect[0] = 0
            block_chain = self.get_block_chain()
            block_chain.next_to(
                VGroup(pi, pi.label), vect, SMALL_BUFF
            )
            pi.block_chain = pi.ledger = block_chain
            ledgers.add(block_chain)
        self.ledgers = self.block_chains = ledgers
        return ledgers

    def get_block_chain(self):
        blocks = VGroup(*[
            self.get_block() 
            for x in range(self.n_blocks)
        ])
        blocks.arrange(RIGHT, buff = MED_SMALL_BUFF)
        arrows = VGroup()

        for b1, b2 in zip(blocks, blocks[1:]):
            arrow = Arrow(
                LEFT, RIGHT,
                preserve_tip_size_when_scaling = False,
                tip_length = 0.15,
            )
            arrow.set_width(b1.get_width())
            target_point = interpolate(
                b2.get_left(), b2.get_corner(UP+LEFT), 0.8
            )
            arrow.next_to(target_point, LEFT, 0.5*SMALL_BUFF)
            # CHANGE: Cairo arrow points were edited by hand (cubic anchors/handles of the line); GL arrows are one shape, so the points edit made a wedge: put the arrow between the blocks with put_start_and_end_on
            arrow.put_start_and_end_on(
                b1.get_right(), target_point + 0.5*SMALL_BUFF*LEFT
            )
            arrows.add(arrow)
        block_chain = VGroup(blocks, arrows)
        block_chain.blocks = blocks
        block_chain.arrows = arrows
        return block_chain

    def get_block(self):
        block = Rectangle(
            color = WHITE,
            height = self.block_height,
            width = self.block_width,
        )
        for vect in UP, DOWN:
            line = Line(block.get_left(), block.get_right())
            line.shift(0.3*block.get_height()*vect)
            block.add(line)
        return block

    def create_pi_creatures(self):
        creatures = DistributedLedgerScene.create_pi_creatures(self)
        VGroup(
            self.alice, self.alice.label,
            self.charlie, self.charlie.label,
        ).shift(LEFT)
        return creatures


class Thumbnail(DistributedBlockChainScene):
    CONFIG = {
        "n_blocks" : 4,
    }
    def construct(self):
        title = OldTexText("Crypto", "currencies", arg_separator = "")
        title.scale(2.5)
        title.to_edge(UP)
        title[0].set_color(YELLOW)
        title[0].set_stroke(RED, 2)
        self.add(title)

        # logos = VGroup(
        #     BitcoinLogo(), EthereumLogo(), LitecoinLogo()
        # )
        # for logo in logos:
        #     logo.set_height(1)
        # logos.add(OldTex("\\dots").scale(2))
        # logos.arrange(RIGHT)
        # logos.next_to(title, RIGHT, LARGE_BUFF)
        # self.add(logos)

        block_chain = self.get_block_chain()
        block_chain.arrows.set_color(RED)
        block_chain.blocks.set_color_by_gradient(BLUE, GREEN)
        block_chain.set_width(FRAME_WIDTH-1)
        block_chain.set_stroke(width = 12)
        self.add(block_chain)
