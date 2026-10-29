# ==============================================================================
# Scene:      IntroduceNonceOnTrasactions
# Source:     videos/_2017/crypto.py (lines 2691-2872)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceNonceOnTrasactions.py IntroduceNonceOnTrasactions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
#   - assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
#   - memory: 256 ReplacementTransforms of copied points plus the ledger Transform exceeded the 5 GB cap (SIGKILL at animation 63); fade the digest in instead (same end state)
#   - memory: each Transform between 256-glyph digests keeps growing the process (SIGKILL at the 8th, animation 63, 5 GB cap); show 4 guesses instead of 12
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


class IntroduceNonceOnTrasactions(LedgerScene):
    CONFIG = {
        "denomination" : "LD",
        "ledger_width" : 5,
        "ledger_line_height" : 0.3,
    }
    def construct(self):
        self.add(self.get_ledger())
        self.hash_with_nonce()
        self.write_probability()
        self.guess_and_check()
        self.name_proof_of_work()
        self.change_ledger()
        self.guess_and_check()

    def hash_with_nonce(self):
        ledger = self.ledger
        self.add(*[
            self.add_payment_line_to_ledger(*payment)
            for payment in [
                ("Alice", "Bob", 20),
                ("Alice", "You", 30),
                ("Charlie", "You", 100),
            ]
        ])

        nonce = OldTex(str(2**30 + hash("Hey there")%(2**15)))
        nonce.next_to(ledger, RIGHT, LARGE_BUFF)
        nonce.set_color(GREEN_C)
        nonce_brace = Brace(nonce, DOWN)
        special_word = nonce_brace.get_text("Special number")
        arrow = Arrow(LEFT, RIGHT, buff = 0)
        arrow.next_to(ledger, RIGHT)
        arrow.shift(MED_LARGE_BUFF*DOWN)
        sha = OldTexText("SHA256")
        sha.next_to(arrow, UP)
        digest = sha256_tex_mob(
            """Man, you're reading this deeply into
            the code behind videos?  I'm touched,
            really touched.  Keeping loving math, my
            friend. """,
            n_forced_start_zeros = 30,
        )
        digest.next_to(arrow, RIGHT)
        zeros = VGroup(*digest[:30])
        zeros_brace = Brace(zeros, UP)
        zeros_words = zeros_brace.get_text("30 zeros")

        self.play(LaggedStartMap(
            FadeIn, VGroup(special_word, nonce_brace, nonce)
        ))
        self.wait()
        self.play(
            nonce.next_to, ledger.content, DOWN, MED_SMALL_BUFF, LEFT,
            FadeOut(special_word),
            FadeOut(nonce_brace)
        )
        ledger.content.add(nonce)
        decomposed_ledger = VGroup(*[m for m in ledger.family_members_with_points() if not m.is_subpath])
        self.play(
            ShowCreation(arrow),
            FadeIn(sha)
        )
        self.play(LaggedStartMap(
            ApplyMethod, decomposed_ledger,
            lambda m : (m.set_color, YELLOW),
            rate_func = there_and_back
        ))
        point = VectorizedPoint(sha.get_center())
        point.set_fill(opacity = 1)
        self.play(LaggedStartMap(
            Transform, decomposed_ledger.copy(),
            lambda m : (m, point),
            run_time = 1
        ))
        # CHANGE: memory: 256 ReplacementTransforms of copied points plus the ledger Transform exceeded the 5 GB cap (SIGKILL at animation 63); fade the digest in instead (same end state)
        self.play(LaggedStartMap(
            FadeIn, digest,
            run_time = 2, lag_ratio = 0.02,
        ))
        self.play(
            GrowFromCenter(zeros_brace),
            Write(zeros_words, run_time = 1)
        )
        self.play(LaggedStartMap(
            ApplyMethod, zeros,
            lambda m : (m.set_color, YELLOW)
        ))
        self.wait(2)

        self.nonce = nonce
        self.digest = digest
        self.zeros_brace = zeros_brace
        self.zeros_words = zeros_words

    def write_probability(self):
        probability = OldTexText(
            "Probability: $\\frac{1}{2^{30}}$",
            "$\\approx \\frac{1}{1{,}000{,}000{,}000}$",
        )
        probability.next_to(self.zeros_words, UP, MED_LARGE_BUFF)

        self.play(FadeIn(probability[0]))
        self.wait()
        self.play(Write(probability[1], run_time = 2))
        self.wait(2)

    def guess_and_check(self):
        q_mark = OldTex("?")
        q_mark.set_color(RED)
        q_mark.next_to(self.zeros_words, RIGHT, SMALL_BUFF)

        self.digest.save_state()
        self.nonce.save_state()

        self.play(FadeIn(q_mark))
        # CHANGE: memory: each Transform between 256-glyph digests keeps growing the process (SIGKILL at the 8th, animation 63, 5 GB cap); show 4 guesses instead of 12
        for x in range(1, 5):
            nonce = OldTex(str(x))
            nonce.move_to(self.nonce)
            nonce.set_color(GREEN_C)
            digest = sha256_tex_mob(str(x))
            digest.replace(self.digest)

            self.play(Transform(
                self.nonce, nonce,
                run_time = 1 if x == 1 else 0.3
            ))
            self.play(Transform(
                self.digest, digest,
                run_time = 1,
                lag_ratio = 0.5
            ))
        self.wait()
        self.play(self.nonce.restore)
        self.play(
            self.digest.restore, 
            lag_ratio = 0.5,
            run_time = 2
        )
        self.play(FadeOut(q_mark))
        self.wait()

    def name_proof_of_work(self):
        words = OldTexText("``Proof of work''")
        words.next_to(self.nonce, DOWN, LARGE_BUFF)
        words.shift(MED_LARGE_BUFF*RIGHT)
        words.set_color(GREEN)
        arrow = Arrow(
            words.get_top(), self.nonce.get_bottom(),
            color = WHITE,
            tip_length = 0.15
        )
        self.play(Write(words, run_time = 2))
        self.play(ShowCreation(arrow))
        self.wait()

    def change_ledger(self):
        amount = self.ledger.content[2][-1]
        new_amount = OldTexText("300 LD")
        new_amount.set_height(amount.get_height())
        new_amount.set_color(amount.get_color())
        new_amount.move_to(amount, LEFT)

        new_digest = sha256_tex_mob("Ah shucks")
        new_digest.replace(self.digest)

        dot = Dot(amount.get_center())
        dot.set_fill(opacity = 0.5)

        self.play(FocusOn(amount))
        self.play(Transform(amount, new_amount))
        self.play(
            dot.move_to, new_digest,
            dot.set_fill, None, 0
        )
        self.play(Transform(
            self.digest, new_digest,
            lag_ratio = 0.5,
        ))
