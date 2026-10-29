# ==============================================================================
# Scene:      MiningIsALottery
# Source:     videos/_2017/crypto.py (lines 3671-3815)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MiningIsALottery.py MiningIsALottery -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
#   - assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
#   - Cairo arrow points were edited by hand (cubic anchors/handles of the line); GL arrows are one shape, so the points edit made a wedge: put the arrow between the blocks with put_start_and_end_on
# ==============================================================================

from manim_imports_ext import *
from hashlib import sha256

def sha256_bit_string(message):
    hexdigest = sha256(message.encode('utf-8')).hexdigest()
    return bin(int(hexdigest, 16))[2:]


def bit_string_to_mobject(bit_string):
    line = OldTex("0"*32)
    pre_result = VGroup(*[
        line.copy() for row in range(8)
    ])
    pre_result.arrange(DOWN, buff = SMALL_BUFF)
    result = VGroup(*it.chain(*pre_result))
    result.scale(0.7)
    bit_string = (256 - len(bit_string))*"0" + bit_string

    # CHANGE: assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
    parts = list(result)
    for i, (bit, part) in enumerate(zip(bit_string, parts)):
        if bit == "1":
            one = OldTex("1")[0]
            one.replace(part, dim_to_match = 1)
            parts[i] = one
    result.set_submobjects(parts)

    return result


def sha256_tex_mob(message, n_forced_start_zeros = 0):
    true_bit_string = sha256_bit_string(message)
    n = n_forced_start_zeros
    bit_string = "0"*n + true_bit_string[n:]
    return bit_string_to_mobject(bit_string)


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


class IntroduceBlockCreator(DistributedBlockChainScene):
    CONFIG = {
        "n_block_creators" : 3,
        "n_pow_guesses" : 60,
    }
    def construct(self):
        self.add_network()
        self.add_block_creators()
        self.broadcast_transactions()
        self.collect_transactions()
        self.find_proof_of_work()
        self.add_block_reward()
        self.comment_on_block_reward()
        self.write_miners()
        self.broadcast_block()

    def add_network(self):
        network = self.get_large_network()
        network.remove(network.lines)
        network.scale(0.7)
        ledgers = self.get_distributed_ledgers()
        self.add(network, ledgers)
        VGroup(network, ledgers).to_edge(RIGHT)

    def add_block_creators(self):
        block_creators = VGroup()
        labels = VGroup()
        everything = VGroup()
        for x in range(self.n_block_creators):
            block_creator = PiCreature(color = GREY)
            block_creator.set_height(self.alice.get_height())
            label = OldTexText("Block creator %d"%(x+1))
            label.scale(0.7)
            label.next_to(block_creator, DOWN, SMALL_BUFF)
            block_creator.label = label
            block_creators.add(block_creator)
            labels.add(label)
            everything.add(VGroup(block_creator, label))
        everything.arrange(DOWN, buff = LARGE_BUFF)
        everything.to_edge(LEFT)

        self.play(LaggedStartMap(FadeIn, everything))
        self.pi_creatures.add(*block_creators)
        self.wait()

        self.block_creators = block_creators
        self.block_creator_labels = labels

    def broadcast_transactions(self):
        payment_parts = [
            ("Alice", "Bob", 20),
            ("Bob", "Charlie", 10),
            ("Charlie", "You", 50),
            ("You", "Alice", 30),
        ]
        payments = VGroup()
        payment_targets = VGroup()
        for from_name, to_name, amount in payment_parts:
            verb = "pay" if from_name == "You" else "pays"
            payment = OldTexText(
                from_name, verb, to_name, "%d LD"%amount
            )
            payment.set_color_by_tex("LD", YELLOW)
            for name in self.get_names():
                payment.set_color_by_tex(
                    name.capitalize(),
                    self.get_color_from_name(name)
                )
            payment.scale(0.7)
            payment.generate_target()
            payment_targets.add(payment.target)

            pi = getattr(self, from_name.lower())
            payment.scale(0.1)
            payment.set_fill(opacity = 0)
            payment.move_to(pi)
            payments.add(payment)
        payment_targets.arrange(DOWN, aligned_edge = LEFT)
        payment_targets.next_to(
            self.block_creator_labels, RIGHT,
            MED_LARGE_BUFF
        )
        payment_targets.shift(UP)

        anims = []
        alpha_range = np.linspace(0, 0.5, len(payments))
        for pi, payment, alpha in zip(self.pi_creatures, payments, alpha_range):
            rf1 = squish_rate_func(smooth, alpha, alpha+0.5)
            rf2 = squish_rate_func(smooth, alpha, alpha+0.5)
            anims.append(Broadcast(
                pi, rate_func = rf1,
                big_radius = 3,
            ))
            anims.append(MoveToTarget(payment, rate_func = rf2))

        self.play(*anims, run_time = 5)
        self.payments = payments

    def collect_transactions(self):
        creator = self.block_creators[0]
        block = self.get_block()
        block.stretch_to_fit_height(4)
        block.stretch_to_fit_width(3.5)
        block.next_to(creator.label, RIGHT, MED_LARGE_BUFF)
        block.to_edge(UP)

        payments = self.payments
        payments.generate_target()
        payments.target.set_height(1.5)
        payments.target.move_to(block)

        prev_hash = OldTexText("Prev hash")
        prev_hash.set_color(BLUE)
        prev_hash.set_height(0.3)
        prev_hash.next_to(block.get_top(), DOWN, MED_SMALL_BUFF)
        block.add(prev_hash)

        self.play(
            FadeIn(block),
            MoveToTarget(payments),
            creator.change, "raise_right_hand"
        )
        self.wait()
        block.add(payments)

        self.block = block

    def find_proof_of_work(self):
        block = self.block

        arrow = Arrow(UP, ORIGIN, buff = 0)
        arrow.next_to(block, DOWN)
        sha = OldTexText("SHA256")
        sha.scale(0.7)
        sha.next_to(arrow, RIGHT)
        arrow.add(sha)

        self.add(arrow)
        for x in range(self.n_pow_guesses):
            guess = Integer(random.randint(10**11, 10**12))
            guess.set_color(GREEN)
            guess.set_height(0.3)
            guess.next_to(block.get_bottom(), UP, MED_SMALL_BUFF)

            if x == self.n_pow_guesses - 1:
                digest = sha256_tex_mob(str(x), 60)
                VGroup(*digest[:60]).set_color(YELLOW)
            else:
                digest = sha256_tex_mob(str(x))
            digest.set_width(block.get_width())
            digest.next_to(arrow.get_end(), DOWN)

            self.add(guess, digest)
            self.wait(1./20)
            self.remove(guess, digest)
        proof_of_work = guess
        self.add(proof_of_work, digest)
        block.add(proof_of_work)
        self.wait()

        self.hash_group = VGroup(arrow, digest)

    def add_block_reward(self):
        payments = self.payments
        new_transaction = OldTexText(
            self.block_creator_labels[0].get_tex(),
            "gets", "10 LD"
        )
        new_transaction[0].set_color(GREY_B)
        new_transaction.set_color_by_tex("LD", YELLOW)
        new_transaction.set_height(payments[0].get_height())
        new_transaction.move_to(payments.get_top())
        payments.generate_target()
        payments.target.next_to(new_transaction, DOWN, SMALL_BUFF, LEFT)
        new_transaction.shift(SMALL_BUFF*UP)

        self.play(
            MoveToTarget(payments),
            Write(new_transaction)
        )
        payments.add_to_back(new_transaction)
        self.wait()

    def comment_on_block_reward(self):
        reward = self.payments[0]
        reward_rect = SurroundingRectangle(reward)
        big_rect = SurroundingRectangle(self.ledgers)
        big_rect.set_stroke(width = 0)
        big_rect.set_fill(BLACK, opacity = 1)

        comments = VGroup(*list(map(TexText, [
            "- ``Block reward''",
            "- No sender/signature",
            "- Adds to total money supply",
        ])))
        comments.arrange(DOWN, aligned_edge = LEFT)
        comments.move_to(big_rect, UP+LEFT)

        pi_creatures = self.pi_creatures
        self.pi_creatures = VGroup()

        self.play(ShowCreation(reward_rect))
        self.play(FadeIn(big_rect))
        for comment in comments:
            self.play(FadeIn(comment))
            self.wait(2)
        self.play(*list(map(FadeOut, [big_rect, comments, reward_rect])))

        self.pi_creatures = pi_creatures

    def write_miners(self):
        for label in self.block_creator_labels:
            tex = label.get_tex()
            new_label = OldTexText("Miner " + tex[-1])
            new_label.set_color(label.get_color())
            new_label.replace(label, dim_to_match = 1)
            self.play(Transform(label, new_label))
        top_payment = self.payments[0]
        new_top_payment = OldTexText("Miner 1", "gets", "10 LD")
        new_top_payment[0].set_color(GREY_B)
        new_top_payment[-1].set_color(YELLOW)
        new_top_payment.set_height(top_payment.get_height())
        new_top_payment.move_to(top_payment, LEFT)
        self.play(Transform(top_payment, new_top_payment))
        self.wait()

    def broadcast_block(self):
        old_chains = self.block_chains
        self.n_blocks = 4
        new_chains = self.get_distributed_ledgers()
        block_target_group = VGroup()
        anims = []
        arrow_creations = []
        for old_chain, new_chain  in zip(old_chains, new_chains):
            for attr in "blocks", "arrows":
                pairs = list(zip(
                    getattr(old_chain, attr), 
                    getattr(new_chain, attr), 
                ))
                for m1, m2 in pairs:
                    anims.append(Transform(m1, m2))
            arrow_creations.append(ShowCreation(new_chain.arrows[-1]))
            block_target = self.block.copy()
            block_target.replace(new_chain.blocks[-1], stretch = True)
            block_target_group.add(block_target)
        anims.append(Transform(
            VGroup(self.block),
            block_target_group
        ))
        anims.append(Broadcast(self.block, n_circles = 4))
        anims.append(FadeOut(self.hash_group))
        anims.append(ApplyMethod(
            self.block_creators[0].change, "happy"
        ))

        self.play(*anims, run_time = 2)
        self.play(*it.chain(
            arrow_creations,
            [
                ApplyMethod(
                    pi.change, "hooray", 
                    pi.block_chain.get_right()
                )
                for pi in self.pi_creatures
            ]
        ))
        self.wait(3)


class MiningIsALottery(IntroduceBlockCreator):
    CONFIG = {
        "n_miners" : 3,
        "denomination" : "LD",
        "n_guesses" : 90,
        "n_nonce_digits" : 15,
    }
    def construct(self):
        self.add_blocks()
        self.add_arrows()
        self.make_guesses()

    def create_pi_creatures(self):
        IntroduceBlockCreator.create_pi_creatures(self)
        miners = VGroup(*[
            PiCreature(color = GREY)
            for n in range(self.n_miners)
        ])
        miners.scale(0.5)
        miners.arrange(DOWN, buff = LARGE_BUFF)
        miners.to_edge(LEFT)
        for x, miner in enumerate(miners):
            label = OldTexText("Miner %d"%(x+1))
            label.scale(0.7)
            label.next_to(miner, DOWN, SMALL_BUFF)
            miner.label = label
            self.add(label)
        self.miners = miners
        return miners

    def add_blocks(self):
        self.add(self.miners)

        blocks = VGroup()
        for miner in self.miners:
            block = self.get_block()
            block.stretch_to_fit_height(2)
            block.stretch_to_fit_width(3)
            block.next_to(miner, RIGHT)

            payments = self.get_payments(miner)
            payments.set_height(1)
            payments.move_to(block)
            block.add(payments)

            prev_hash = OldTexText("Prev hash")
            prev_hash.set_color(BLUE)
            prev_hash.set_height(0.2)
            prev_hash.next_to(block.get_top(), DOWN, SMALL_BUFF)
            block.add(prev_hash)

            miner.block = block
            miner.change("pondering", block)
            blocks.add(block)

        self.blocks = blocks
        self.add(blocks)

    def add_arrows(self):
        self.arrows = VGroup()
        for block in self.blocks:
            arrow = Arrow(LEFT, RIGHT)
            arrow.next_to(block)
            label = OldTexText("SHA256")
            label.scale(0.7)
            label.next_to(arrow, UP, buff = SMALL_BUFF)
            self.add(arrow, label)
            block.arrow = arrow
            self.arrows.add(VGroup(arrow, label))

    def make_guesses(self):
        for x in range(self.n_guesses):
            e = self.n_nonce_digits
            nonces = VGroup()
            digests = VGroup()
            for block in self.blocks:
                nonce = Integer(random.randint(10**e, 10**(e+1)))
                nonce.set_height(0.2)
                nonce.next_to(block.get_bottom(), UP, SMALL_BUFF)
                nonces.add(nonce)
                digest = sha256_tex_mob(str(x) + str(block))
                digest.set_height(block.get_height())
                digest.next_to(block.arrow, RIGHT)
                digests.add(digest)
            self.add(nonces, digests)
            self.wait(1./20)
            self.remove(nonces, digests)
        self.add(nonces, digests)

        winner_index = 1
        winner = self.miners[winner_index]
        losers = VGroup(*[m for m in self.miners if m is not winner])

        nonces[winner_index].set_color(GREEN)
        new_digest = sha256_tex_mob("Winner", 60)
        VGroup(*new_digest[:60]).set_color(YELLOW)
        old_digest = digests[winner_index]
        new_digest.replace(old_digest)
        Transform(old_digest, new_digest).update(1)

        self.play(
            winner.change, "hooray",
            *[
                ApplyMethod(VGroup(
                    self.blocks[i], self.arrows[i], 
                    nonces[i], digests[i]
                ).fade, 0.7)
                for i in range(len(self.blocks))
                if i is not winner_index
            ]
        )
        self.play(*[
            ApplyMethod(loser.change, "angry", winner)
            for loser in losers
        ])
        self.wait(2)

    #####

    def get_payments(self, miner):
        if not hasattr(self, "ledger"):
            self.get_ledger() ##Unused
        self.ledger.content.remove(*self.ledger.content[1:])

        lines = VGroup()

        miner_name = miner.label.get_tex()
        top_line = OldTexText(miner_name, "gets", "10 LD")
        top_line.set_color_by_tex(miner_name, GREY_B)
        top_line.set_color_by_tex("LD", YELLOW)
        lines.add(top_line)
        payments = [
            ("Alice", "Bob", 20),
            ("Charlie", "You", 50),
        ]
        for payment in payments:
            lines.add(self.add_payment_line_to_ledger(*payment))
        lines.add(OldTex("\\vdots"))
        for line in lines:
            line.set_height(0.5)
        lines.arrange(
            DOWN, buff = SMALL_BUFF, aligned_edge = LEFT
        )
        lines[-1].next_to(lines[-2], DOWN, buff = SMALL_BUFF)
        return lines
