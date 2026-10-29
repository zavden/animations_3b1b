# ==============================================================================
# Scene:      FeelConfidentWithVerification
# Source:     videos/_2017/crypto.py (lines 1334-1399)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FeelConfidentWithVerification.py FeelConfidentWithVerification -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - assigning into result.submobjects leaves the family cache stale in GL: build the list and use set_submobjects
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


class FeelConfidentWithVerification(PiCreatureScene):
    def construct(self):
        self.show_verification()
        self.show_secret_key()

    def show_verification(self):
        verify = OldTexText(
            "Verify(", "Message", ", ", 
            "256 bit Signature", ", ", "pk", ")",
            arg_separator = ""
        )
        signature_word = verify.get_part_by_tex("Signature")
        verify.set_color_by_tex("Signature", BLUE)
        verify.set_color_by_tex("pk", GREEN)
        brace = Brace(signature_word, UP)
        signature = sha256_tex_mob("Signature")
        signature.next_to(brace, UP)
        signature.set_color(BLUE_C)

        rhs = OldTexText("=", "True")
        rhs.set_color_by_tex("True", YELLOW)
        rhs.next_to(verify, RIGHT)

        pk = verify.get_part_by_tex("pk")
        sk = OldTexText("sk")
        sk.set_color(RED)
        arrow = OldTex("\\Updownarrow")
        arrow.next_to(pk, DOWN)
        sk.next_to(arrow, DOWN)
        sk_group = VGroup(arrow, sk)
        lock_box = SurroundingRectangle(sk_group, buff = SMALL_BUFF)
        lock_box.set_color(RED)
        lock = SVGMobject(
            file_name = "lock", 
            fill_color = GREY_B,
            height = 0.5,
        )
        lock.next_to(lock_box, LEFT, SMALL_BUFF)

        self.add(verify)
        self.play(
            GrowFromCenter(brace),
            Write(signature),
            self.pi_creature.change, "pondering"
        )
        self.play(ReplacementTransform(
            verify.copy(), rhs
        ))
        self.wait()
        self.play(self.pi_creature.change, "happy")
        self.play(Write(sk_group))
        self.play(
            ShowCreation(lock_box),
            DrawBorderThenFill(lock, run_time = 1)
        )
        self.wait(2)


    def show_secret_key(self):
        pass


    #####

    def create_pi_creature(self):
        return Randolph().to_corner(DOWN+LEFT)
