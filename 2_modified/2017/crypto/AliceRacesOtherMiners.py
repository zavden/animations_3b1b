# ==============================================================================
# Scene:      AliceRacesOtherMiners
# Source:     videos/_2017/crypto.py (lines 4125-4374)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AliceRacesOtherMiners.py AliceRacesOtherMiners -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
#   - Transform(a, b).update(1) in a loop leaks memory in GL (SIGKILL): become() gives the same state
#   - Cairo Arrow was [line, tip] with cubic points; GL Arrow is one shape: move its end point with put_start_and_end_on
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


class DoubleSpendingAttack(DistributedBlockChainScene):
    CONFIG = {
        "fraud_block_height" : 3,
    }
    def construct(self):
        self.initialize_characters()
        self.show_fraudulent_block()
        self.send_to_bob()
        self.dont_send_to_rest_of_network()

    def initialize_characters(self):
        network = self.get_large_network()
        network.scale(0.7)
        block_chains = self.get_distributed_ledgers()
        self.add(network, block_chains)
        self.play(self.alice.change, "conniving")
        self.wait()

    def show_fraudulent_block(self):
        block = self.get_fraud_block()
        block.next_to(self.alice, LEFT, LARGE_BUFF)
        block.remove(block.content)
        self.play(
            ShowCreation(block),
            Write(block.content),
            self.alice.change, "raise_left_hand"
        )
        block.add(block.content)
        self.wait()

        self.block = block

    def send_to_bob(self):
        block = self.block.copy()
        block.generate_target()
        block.target.replace(
            self.bob.block_chain.blocks[-1],
            stretch = True
        )
        arrow = self.bob.block_chain.arrows[-1].copy()
        VGroup(arrow, block.target).next_to(
            self.bob.block_chain.blocks[-1], RIGHT, buff = 0
        )

        self.play(
            MoveToTarget(block),
            self.alice.change, "happy"
        )
        self.play(ShowCreation(arrow))
        self.wait()

    def dont_send_to_rest_of_network(self):
        bubble = ThoughtBubble()
        words = OldTexText("Alice", "never \\\\ paid", "Bob")
        for name in "Alice", "Bob":
            words.set_color_by_tex(name, self.get_color_from_name(name))
        bubble.add_content(words)
        bubble.resize_to_content()
        bubble.add(*bubble.content)
        bubble.move_to(self.you.get_corner(UP+RIGHT), DOWN+LEFT)

        self.play(
            self.charlie.change, "shruggie",
            self.you.change, "shruggie",
        )
        self.play(LaggedStartMap(FadeIn, bubble))
        self.play(self.bob.change, "confused", words)
        self.wait(2)

    ###

    def get_fraud_block(self):
        block = self.get_block()
        block.set_height(self.fraud_block_height)
        content = VGroup()

        tuples = [
            ("Prev hash", UP, BLUE), 
            ("Proof of work", DOWN, GREEN),
        ]
        for word, vect, color in tuples:
            mob = OldTexText(word)
            mob.set_color(color)
            mob.set_height(0.07*block.get_height())
            mob.next_to(
                block.get_edge_center(vect), -vect,
                buff = 0.06*block.get_height()
            )
            content.add(mob)
            attr = word.lower().replace(" ", "_")
            setattr(block, attr, mob)

        payment = OldTexText("Alice", "pays", "Bob", "100 LD")
        for name in "Alice", "Bob":
            payment.set_color_by_tex(name, self.get_color_from_name(name))
        payment.set_color_by_tex("LD", YELLOW)
        payments = VGroup(
            OldTex("\\vdots"),
            payment,
            OldTex("\\vdots")
        )
        payments.arrange(DOWN)
        payments.set_width(0.9*block.get_width())
        payments.move_to(block)
        content.add(payments)

        block.content = content
        block.add(content)
        return block


class AliceRacesOtherMiners(DoubleSpendingAttack):
    CONFIG = {
        "n_frames_per_pow" : 3,
        "fraud_block_height" : 2,
        "n_miners" : 3,
        "n_proof_of_work_digits" : 11,
        "proof_of_work_update_counter" : 0,
    }
    def construct(self):
        self.initialize_characters()
        self.find_proof_of_work()
        self.receive_broadcast_from_other_miners()
        self.race_between_alice_and_miners()

    def initialize_characters(self):
        alice = self.alice
        bob = self.bob
        alice_l = VGroup(alice, alice.label)
        bob_l = VGroup(bob, bob.label)
        bob_l.move_to(ORIGIN)
        alice_l.to_corner(UP+LEFT)
        alice_l.shift(DOWN)
        self.add(bob_l, alice_l)

        chain = self.get_block_chain()
        chain.next_to(bob, UP)
        self.block_chain = chain
        self.add(chain)

        fraud_block = self.get_fraud_block()
        fraud_block.next_to(alice, RIGHT)
        fraud_block.to_edge(UP)
        proof_of_work = self.get_rand_int_mob()
        proof_of_work.replace(fraud_block.proof_of_work, dim_to_match = 1)
        fraud_block.content.remove(fraud_block.proof_of_work)
        fraud_block.content.add(proof_of_work)
        fraud_block.proof_of_work = proof_of_work
        self.fraud_block = fraud_block
        self.add(fraud_block)

        miners = VGroup(*[
            PiCreature(color = GREY)
            for x in range(self.n_miners)
        ])
        miners.set_height(alice.get_height())
        miners.arrange(RIGHT, buff = LARGE_BUFF)
        miners.to_edge(DOWN+LEFT)
        miners.shift(0.5*UP)
        miners_word = OldTexText("Miners")
        miners_word.next_to(miners, DOWN)
        self.miners = miners
        self.add(miners_word, miners)

        miner_blocks = VGroup()
        self.proofs_of_work = VGroup()
        self.add_foreground_mobject(self.proofs_of_work)
        for miner in miners:
            block = self.get_block()
            block.set_width(1.5*miner.get_width())
            block.next_to(miner, UP)

            transactions = self.get_block_filler(block)
            block.add(transactions)

            proof_of_work = self.get_rand_int_mob()
            prev_hash = OldTexText("Prev hash").set_color(BLUE)
            for mob, vect in (proof_of_work, DOWN), (prev_hash, UP):
                mob.set_height(0.1*block.get_height())
                mob.next_to(
                    block.get_edge_center(vect), -vect, 
                    buff = 0.05*block.get_height()
                )
                block.add(mob)
            block.proof_of_work = proof_of_work
            block.prev_hash = prev_hash
            self.proofs_of_work.add(proof_of_work)

            miner.block = block
            miner_blocks.add(block)
        self.add(miner_blocks)

    def find_proof_of_work(self):
        fraud_block = self.fraud_block
        chain = self.block_chain

        self.proofs_of_work.add(self.fraud_block.proof_of_work)
        self.wait(3)
        self.proofs_of_work.remove(self.fraud_block.proof_of_work)
        fraud_block.proof_of_work.set_color(GREEN)
        self.play(
            Indicate(fraud_block.proof_of_work),
            self.alice.change, "hooray"
        )
        self.wait()
    
        block = fraud_block.copy()        
        block.generate_target()
        block.target.replace(chain.blocks[-1], stretch = True)
        arrow = chain.arrows[-1].copy()
        VGroup(arrow, block.target).next_to(
            chain.blocks[-1], RIGHT, buff = 0
        )
        self.remove(fraud_block)
        self.clean_fraud_block_content()
        self.fraud_fork_head = block
        self.fraud_fork_arrow = arrow

        self.play(MoveToTarget(block))
        self.play(ShowCreation(arrow))
        self.play(self.alice.change, "happy")
        self.wait()

    def receive_broadcast_from_other_miners(self):
        winner = self.miners[-1]
        proof_of_work = winner.block.proof_of_work
        self.proofs_of_work.remove(proof_of_work)
        proof_of_work.set_color(GREEN)
        self.play(
            Indicate(proof_of_work),
            winner.change, "hooray"
        )
        block = winner.block.copy()
        proof_of_work.set_color(WHITE)
        self.remove(winner.block)

        ff_head = self.fraud_fork_head
        ff_arrow = self.fraud_fork_arrow
        arrow = ff_arrow.copy()
        movers = [ff_head, ff_arrow, block, arrow]
        for mover in movers:
            mover.generate_target()
        block.target.replace(ff_head, stretch = True)

        dist = 0.5*ff_head.get_height() + MED_SMALL_BUFF
        block.target.shift(dist*DOWN)
        ff_head.target.shift(dist*UP)
        # CHANGE: Cairo Arrow was [line, tip] with cubic points; GL Arrow is one shape: move its end point with put_start_and_end_on
        arrow.target.put_start_and_end_on(arrow.get_start(), arrow.get_end() + dist*DOWN)
        ff_arrow.target.put_start_and_end_on(ff_arrow.get_start(), ff_arrow.get_end() + dist*UP)

        self.play(
            Broadcast(block),
            *[
                MoveToTarget(
                    mover, run_time = 3, 
                    rate_func = squish_rate_func(smooth, 0.3, 0.8)
                )
                for mover in movers
            ]
        )
        self.play(
            FadeIn(winner.block),
            winner.change_mode, "plain",
            self.alice.change, "sassy",
        )
        self.proofs_of_work.add(winner.block.proof_of_work)
        self.wait(2)
        self.play(
            self.alice.change, "pondering",
            FadeIn(self.fraud_block)
        )
        self.proofs_of_work.add(self.fraud_block.proof_of_work)

        self.valid_fork_head = block

    def race_between_alice_and_miners(self):
        last_fraud_block = self.fraud_fork_head
        last_valid_block = self.valid_fork_head
        chain = self.block_chain
        winners = [
            "Alice", "Alice",
            "Miners", "Miners", "Miners",
            "Alice", "Miners", "Miners", "Miners",
            "Alice", "Miners", "Miners"
        ]

        self.revert_to_original_skipping_status()
        for winner in winners:
            self.wait()
            if winner == "Alice":
                block = self.fraud_block
                prev_block = last_fraud_block
            else:
                block = random.choice(self.miners).block
                prev_block = last_valid_block
            block_copy = block.deepcopy()
            block_copy.proof_of_work.set_color(GREEN)
            block_copy.generate_target()
            block_copy.target.replace(chain.blocks[1], stretch = True)
            arrow = chain.arrows[0].copy()
            VGroup(arrow, block_copy.target).next_to(
                prev_block, RIGHT, buff = 0
            )
            anims = [
                MoveToTarget(block_copy, run_time = 2),
                ShowCreation(
                    arrow,
                    run_time = 2,
                    rate_func = squish_rate_func(smooth, 0.5, 1),
                ),
                FadeIn(block),
            ]
            if winner == "Alice":
                last_fraud_block = block_copy
            else:
                last_valid_block = block_copy
                anims.append(Broadcast(block, run_time = 2))
            self.proofs_of_work.remove(block.proof_of_work)
            self.play(*anims)
            self.proofs_of_work.add(block.proof_of_work)


    #####

    def wait(self, time = 1):
        self.play(
            Animation(VGroup(*self.foreground_mobjects)),
            run_time = time
        )

    def update_frame(self, *args, **kwargs):
        self.update_proofs_of_work()
        Scene.update_frame(self, *args, **kwargs)

    def update_proofs_of_work(self):
        self.proof_of_work_update_counter += 1
        if self.proof_of_work_update_counter%self.n_frames_per_pow != 0:
            return
        for proof_of_work in self.proofs_of_work:
            new_pow = self.get_rand_int_mob()
            new_pow.replace(proof_of_work, dim_to_match = 1)
            # CHANGE: Transform(a, b).update(1) in a loop leaks memory in GL (SIGKILL): become() gives the same state
            proof_of_work.become(new_pow)

    def get_rand_int_mob(self):
        e = self.n_proof_of_work_digits
        return Integer(random.randint(10**e, 10**(e+1)))

    def clean_fraud_block_content(self):
        content = self.fraud_block.content
        payments = content[1]
        content.remove(payments)
        transactions = self.get_block_filler(self.fraud_block)
        content.add(transactions)

    def get_block_filler(self, block):
        result = OldTexText("$\\langle$Transactions$\\rangle$")
        result.set_width(0.8*block.get_width())
        result.move_to(block)
        return result
