# ==============================================================================
# Scene:      DescribeDigitalSignatures
# Source:     videos/_2017/crypto.py (lines 998-1270)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DescribeDigitalSignatures.py DescribeDigitalSignatures -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() is a hex string in GL (no get_rgb()); use color_to_rgb
# ==============================================================================

from manim_imports_ext import *

def get_cursive_name(name):
    result = OldTexText("\\normalfont\\calligra %s"%name)
    result.set_stroke(width = 0.5)
    return result


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


class DescribeDigitalSignatures(LedgerScene):
    CONFIG = {
        "public_color" : GREEN,
        "private_color" : RED,
        "signature_color" : BLUE_C,
    }
    def construct(self):
        self.reorganize_pi_creatures()
        self.generate_key_pairs()
        self.keep_secret_key_secret()
        self.show_handwritten_signatures()
        self.show_digital_signatures()
        self.show_signing_functions()

    def reorganize_pi_creatures(self):
        self.pi_creatures.remove(self.you)
        creature_groups = VGroup(*[
            VGroup(pi, pi.label).scale(1.7)
            for pi in self.pi_creatures
        ])
        creature_groups.arrange(RIGHT, buff = 2)
        creature_groups.to_edge(DOWN)
        self.add(creature_groups)
        for pi in self.pi_creatures:
            if pi.is_flipped():
                pi.flip()

    def generate_key_pairs(self):
        title = OldTexText("Private", "key /", "Public", "key")
        title.to_edge(UP)
        private, public = list(map(title.get_part_by_tex, ["Private", "Public"]))
        private.set_color(self.private_color)
        public.set_color(self.public_color)
        secret = OldTexText("Secret")
        secret.move_to(private, RIGHT)
        secret.set_color(self.private_color)

        names = self.get_names()[:-1]
        public_key_strings = [
            bin(256+ord(name[0].capitalize()))[3:]
            for name in names
        ]
        private_key_strings = [
            bin(hash(name))[2:10]
            for name in names
        ]
        public_keys, private_keys = [
            VGroup(*[
                OldTexText(key_name+":"," $%s\\dots$"%key)
                for key in keys
            ])
            for key_name, keys in [
                ("pk", public_key_strings),
                ("sk", private_key_strings)
            ]
        ]
        key_pairs = [
            VGroup(*pair).arrange(DOWN, aligned_edge = LEFT)
            for pair in zip(public_keys, private_keys)
        ]
        for key_pair, pi in zip(key_pairs, self.pi_creatures):
            key_pair.next_to(pi, UP, MED_LARGE_BUFF)
            for key in key_pair:
                key.set_color_by_tex("sk", self.private_color)
                key.set_color_by_tex("pk", self.public_color)

        self.play(Write(title, run_time = 2))
        self.play(ReplacementTransform(
            VGroup(VGroup(public.copy())),
            public_keys
        ))
        self.play(ReplacementTransform(
            VGroup(VGroup(private.copy())),
            private_keys
        ))
        self.wait()
        self.play(private.shift, DOWN)
        self.play(FadeIn(secret))
        self.play(FadeOut(private))
        self.wait()

        title.remove(private)
        title.add(secret)
        self.title = title
        self.private_keys = private_keys
        self.public_keys = public_keys

    def keep_secret_key_secret(self):
        keys = self.private_keys
        rects = VGroup(*list(map(SurroundingRectangle, keys)))
        rects.set_color(self.private_color)
        lock = SVGMobject(
            file_name = "lock",
            height = rects.get_height(),
            fill_color = GREY_B,
            fill_opacity = 1,
            stroke_width = 0,
        )
        locks = VGroup(*[
            lock.copy().next_to(rect, LEFT, SMALL_BUFF)
            for rect in rects
        ])

        self.play(ShowCreation(rects))
        self.play(LaggedStartMap(DrawBorderThenFill, locks))
        self.wait()

        self.private_key_rects = rects
        self.locks = locks

    def show_handwritten_signatures(self):
        lines = VGroup(*[Line(LEFT, RIGHT) for x in range(5)])
        lines.arrange(DOWN)
        last_line = lines[-1]
        last_line.scale(0.7, about_point = last_line.get_left())

        signature_line = lines[0].copy()
        signature_line.set_stroke(width = 2)
        signature_line.next_to(lines, DOWN, LARGE_BUFF)
        ex = OldTex("\\times")
        ex.scale(0.7)
        ex.next_to(signature_line, UP, SMALL_BUFF, LEFT)
        lines.add(ex, signature_line)

        rect = SurroundingRectangle(
            lines, 
            color = GREY_B, 
            buff = MED_SMALL_BUFF
        )
        document = VGroup(rect, lines)
        documents = VGroup(*[
            document.copy()
            for x in range(2)
        ])
        documents.arrange(RIGHT, buff = MED_LARGE_BUFF)
        documents.to_corner(UP+LEFT)

        signatures = VGroup()
        for document in documents:
            signature = get_cursive_name("Alice")
            signature.set_color(self.signature_color)
            line = document[1][-1]
            signature.next_to(line, UP, SMALL_BUFF)
            signatures.add(signature)

        self.play(
            FadeOut(self.title),
            LaggedStartMap(FadeIn, documents, run_time = 1)
        )
        self.play(Write(signatures))
        self.wait()

        self.signatures = signatures
        self.documents = documents

    def show_digital_signatures(self):
        rect = SurroundingRectangle(VGroup(
            self.public_keys[0],
            self.private_key_rects[0],
            self.locks[0]
        ))
        digital_signatures = VGroup()
        for i, signature in enumerate(self.signatures):
            bits = bin(hash(str(i)))[-8:]
            digital_signature = OldTex(bits + "\\dots")
            digital_signature.scale(0.7)
            digital_signature.set_color(signature.get_color())
            digital_signature.move_to(signature, DOWN)
            digital_signatures.add(digital_signature)

        arrows = VGroup(*[
            Arrow(
                rect.get_corner(UP), sig.get_bottom(),
                tip_length = 0.15,
                color = WHITE
            )
            for sig in digital_signatures
        ])

        words = VGroup(*list(map(
            TexText,
            ["Different messages", "Completely different signatures"]
        )))
        words.arrange(DOWN, aligned_edge = LEFT)
        words.scale(1.3)
        words.next_to(self.documents, RIGHT)

        self.play(FadeIn(rect))
        self.play(*list(map(ShowCreation, arrows)))
        self.play(Transform(self.signatures, digital_signatures))
        self.play(*[
            ApplyMethod(pi.change, "pondering", digital_signatures)
            for pi in self.pi_creatures
        ])
        for word in words:
            self.play(FadeIn(word))
        self.wait()
        self.play(FadeOut(words))

    def show_signing_functions(self):
        sign = OldTexText(
            "Sign(", "Message", ", ", "sk", ") = ", "Signature",
            arg_separator = ""
        )
        sign.to_corner(UP+RIGHT)
        verify = OldTexText(
            "Verify(", "Message", ", ", "Signature", ", ", "pk", ") = ", "T/F",
            arg_separator = ""
        )
        for mob in sign, verify:
            mob.set_color_by_tex("sk", self.private_color)
            mob.set_color_by_tex("pk", self.public_color)
            mob.set_color_by_tex(
                "Signature", self.signature_color,
            )
            for name in "Message", "sk", "Signature", "pk":
                part = mob.get_part_by_tex(name)
                if part is not None:
                    setattr(mob, name.lower(), part)
        verify.next_to(sign, DOWN, MED_LARGE_BUFF, LEFT)
        VGroup(sign, verify).to_corner(UP+RIGHT)

        private_key = self.private_key_rects[0]
        public_key = self.public_keys[0]
        message = self.documents[0]
        signature = self.signatures[0]

        self.play(*[
            FadeIn(part)
            for part in sign
            if part not in [sign.message, sign.sk, sign.signature]
        ])
        self.play(ReplacementTransform(
            message.copy(), VGroup(sign.message)
        ))
        self.wait()
        self.play(ReplacementTransform(
            private_key.copy(), sign.sk
        ))
        self.wait()
        self.play(ReplacementTransform(
            VGroup(sign.sk, sign.message).copy(),
            VGroup(sign.signature)
        ))
        self.wait()
        self.play(Indicate(sign.sk))
        self.wait()
        self.play(Indicate(sign.message))
        self.wait()
        self.play(*[
            FadeIn(part)
            for part in verify
            if part not in [
                verify.message, verify.signature, 
                verify.pk, verify[-1]
            ]
        ])
        self.wait()
        self.play(
            ReplacementTransform(
                sign.message.copy(), verify.message
            ),
            ReplacementTransform(
                sign.signature.copy(), verify.signature
            )
        )
        self.wait()
        self.play(ReplacementTransform(
            public_key.copy(), VGroup(verify.pk)
        ))
        self.wait()
        self.play(Write(verify[-1]))
        self.wait()
