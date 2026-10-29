# ==============================================================================
# Scene:      IntroduceBlockChain
# Source:     videos/_2017/crypto.py (lines 2920-3233)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceBlockChain.py IntroduceBlockChain -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
#   - assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
#   - Cairo arrow points were edited by hand (cubic anchors/handles); GL arrows are one shape: build the arrow from the block edge to the target
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


class IntroduceBlockChain(Scene):
    CONFIG = {
        "transaction_color" : YELLOW,
        "proof_of_work_color" : GREEN,
        "prev_hash_color" : BLUE,
        "block_width" : 3,
        "block_height" : 3.5,
        "n_transaction_lines" : 8,
        "payment_height_to_block_height" : 0.15,
    }
    def setup(self):
        ls = LedgerScene()
        self.names = [
            name.capitalize()
            for name in ls.get_names()
        ]
        self.name_colors = [
            ls.get_color_from_name(name)
            for name in self.names
        ]

    def construct(self):
        self.divide_ledger_into_blocks()
        self.show_proofs_of_work()
        self.chain_blocks_together()
        self.mess_with_early_block()
        self.propagate_hash_change()
        self.redo_proof_of_work()
        self.write_block_chain()


    def divide_ledger_into_blocks(self):
        blocks = VGroup(*[
            self.get_block() for x in range(3)
        ])
        blocks.arrange(RIGHT, buff = 1.5)
        blocks.to_edge(UP)

        all_payments = VGroup()
        all_proofs_of_work = VGroup()
        for block in blocks:
            block.remove(block.prev_hash)
            all_payments.add(*block.payments)
            all_proofs_of_work.add(block.proof_of_work)

        blocks_word = OldTexText("Blocks")
        blocks_word.scale(1.5)
        blocks_word.shift(2*DOWN)
        arrows = VGroup(*[
            Arrow(
                blocks_word.get_top(), block.get_bottom(),
                buff = MED_LARGE_BUFF,
                color = WHITE
            )
            for block in blocks
        ])

        self.play(LaggedStartMap(FadeIn, blocks))
        self.play(
            Write(blocks_word),
            LaggedStartMap(
                ShowCreation, arrows, 
                run_time = 1,
            )
        )
        self.wait()
        for group in all_payments, all_proofs_of_work:
            self.play(LaggedStartMap(
                Indicate, group,
                rate_func = there_and_back,
                scale_factor = 1.1,
            ))
        self.play(*list(map(FadeOut, [blocks_word, arrows])))

        self.blocks = blocks

    def show_proofs_of_work(self):
        random.seed(0)
        blocks = self.blocks

        proofs_of_work = VGroup()
        new_proofs_of_work = VGroup()
        digests = VGroup()
        arrows = VGroup()
        sha_words = VGroup()
        signatures = VGroup()

        for block in blocks:
            proofs_of_work.add(block.proof_of_work)
            num_str = str(random.randint(0, 10**12))
            number = OldTex(num_str)
            number.set_color(self.proof_of_work_color)
            number.replace(block.proof_of_work, dim_to_match = 1)
            new_proofs_of_work.add(number)

            digest = sha256_tex_mob(num_str, 60)
            digest.scale(0.7)
            digest.move_to(block).to_edge(DOWN)
            VGroup(*digest[:60]).set_color(YELLOW)
            arrow = Arrow(block, digest)
            sha = OldTexText("SHA256")
            sha.scale(0.7)
            point = arrow.get_center()
            sha.next_to(point, UP, SMALL_BUFF)
            sha.rotate(-np.pi/2, about_point = point)
            sha.shift(SMALL_BUFF*(UP+RIGHT))
            digests.add(digest)
            arrows.add(arrow)
            sha_words.add(sha)

            for payment in block.payments[:2]:
                signatures.add(payment[-1])

        proofs_of_work.save_state()

        self.play(Transform(
            proofs_of_work, new_proofs_of_work,
            lag_ratio = 0.5
        ))
        self.play(
            ShowCreation(arrows),
            Write(sha_words),
            run_time = 2
        )
        self.play(Write(digests))
        self.wait()
        for group in signatures, proofs_of_work:
            self.play(LaggedStartMap(
                Indicate, group,
                run_time = 2,
                rate_func = there_and_back,
            ))
            self.wait()
        self.play(
            proofs_of_work.restore,
            FadeOut(sha_words)
        )

        self.digests = digests
        self.sha_arrows = arrows

    def chain_blocks_together(self):
        blocks = self.blocks
        digests = self.digests
        sha_arrows = self.sha_arrows
        block_spacing = blocks[1].get_center() - blocks[0].get_center()
        prev_hashes = VGroup(*[
            block.prev_hash for block in blocks
        ])

        prev_hashes.add(
            prev_hashes[-1].copy().shift(block_spacing).fade(1)
        )

        new_arrows = VGroup()
        for block in blocks:
            end = np.array([
                block.get_left()[0] + block_spacing[0],
                block.prev_hash.get_center()[1],
                0
            ])
            # CHANGE: Cairo arrow points were edited by hand (cubic anchors/handles); GL arrows are one shape: build the arrow from the block edge to the target
            arrow = Arrow(block.get_right(), end, buff = SMALL_BUFF)
            new_arrows.add(arrow)

        for i in range(3):
            self.play(
                ReplacementTransform(digests[i], prev_hashes[i+1]),
                Transform(sha_arrows[i], new_arrows[i])
            )
        arrow = new_arrows[0].copy().shift(-block_spacing)
        sha_arrows.add_to_back(arrow)
        self.play(*list(map(FadeIn, [arrow, prev_hashes[0]])))
        self.wait(2)

        self.prev_hashes = prev_hashes

    def mess_with_early_block(self):
        blocks = self.blocks
        amount = blocks[0].payments[1][3]
        new_amount = OldTexText("400 LD")
        new_amount.set_height(amount.get_height())
        new_amount.set_color(RED)
        new_amount.move_to(amount, LEFT)

        self.play(FocusOn(amount))
        self.play(Transform(amount, new_amount))
        self.wait()
        self.play(Swap(*blocks[:2]))
        self.wait()

        blocks.submobjects[:2] = blocks.submobjects[1::-1]

    def propagate_hash_change(self):
        prev_hashes = self.prev_hashes

        for block, prev_hash in zip(self.blocks, prev_hashes[1:]):
            rect = block.rect.copy()
            rect.set_stroke(RED, 8)
            rect.target = SurroundingRectangle(prev_hash)
            rect.target.set_stroke(rect.get_color(), 0)
            self.play(ShowCreation(rect))
            self.play(
                MoveToTarget(rect),
                prev_hash.set_color, RED
            )

    def redo_proof_of_work(self):
        proofs_of_work = VGroup(*[
            block.proof_of_work for block in self.blocks
        ])
        hashes = self.prev_hashes[1:]

        self.play(FadeOut(proofs_of_work))
        for proof_of_work, prev_hash in zip(proofs_of_work, hashes):
            num_pow_group = VGroup(*[
                Integer(random.randint(10**9, 10**10))
                for x in range(50)
            ])
            num_pow_group.set_color(proof_of_work.get_color())
            num_pow_group.set_width(proof_of_work.get_width())
            num_pow_group.move_to(proof_of_work)
            for num_pow in num_pow_group:
                self.add(num_pow)
                self.wait(1./20)
                prev_hash.set_color(random_bright_color())
                self.remove(num_pow)
            self.add(num_pow)
            prev_hash.set_color(BLUE)

    def write_block_chain(self):
        ledger = OldTexText("Ledger")
        ledger.next_to(self.blocks, DOWN, LARGE_BUFF)
        cross = Cross(ledger)
        block_chain = OldTexText("``Block Chain''")
        block_chain.next_to(ledger, DOWN)

        self.play(FadeIn(ledger))
        self.play(
            ShowCreation(cross),
            Write(block_chain)
        )
        self.wait(2)


    ######

    def get_block(self):
        block = VGroup()
        rect = Rectangle(
            color = WHITE,
            height = self.block_height,
            width = self.block_width,
        )
        h_line1, h_line2 = [
            Line(
                rect.get_left(), rect.get_right()
            ).shift(0.3*rect.get_height()*vect)
            for vect in (UP, DOWN)
        ]

        payments = VGroup()
        if not hasattr(self, "transaction_counter"):
            self.transaction_counter = 0
        for x in range(2):
            hashes = [
                hash("%d %d"%(seed, self.transaction_counter))
                for seed in range(3)
            ]
            payment = OldTexText(
                self.names[hashes[0]%3],
                "pays",
                self.names[hashes[1]%4],
                "%d0 LD"%(hashes[2]%9 + 1),
            )
            payment.set_color_by_tex("LD", YELLOW)
            for name, color in zip(self.names, self.name_colors):
                payment.set_color_by_tex(name, color)
            signature = OldTexText("$\\langle$ Signature $\\rangle$")
            signature.set_color(payment[0].get_color())
            signature.next_to(payment, DOWN, SMALL_BUFF)
            payment.add(signature)

            factor = self.payment_height_to_block_height
            payment.set_height(factor*rect.get_height())
            payments.add(payment)
            self.transaction_counter += 1
        payments.add(OldTex("\\dots").scale(0.5))
        payments.arrange(DOWN, buff = MED_SMALL_BUFF)
        payments.next_to(h_line1, DOWN)

        proof_of_work = OldTexText("Proof of work")
        proof_of_work.set_color(self.proof_of_work_color)
        proof_of_work.scale(0.8)
        proof_of_work.move_to(
            VGroup(h_line2, VectorizedPoint(rect.get_bottom()))
        )

        prev_hash = OldTexText("Prev hash")
        prev_hash.scale(0.8)
        prev_hash.set_color(self.prev_hash_color)
        prev_hash.move_to(
            VGroup(h_line1, VectorizedPoint(rect.get_top()))
        )

        block.rect = rect
        block.h_lines = VGroup(h_line1, h_line2)
        block.payments = payments
        block.proof_of_work = proof_of_work
        block.prev_hash = prev_hash
        block.digest_mobject_attrs()
        return block
