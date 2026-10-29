# ==============================================================================
# Scene:      TryGuessingDigitalSignature
# Source:     videos/_2017/crypto.py (lines 1272-1311)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TryGuessingDigitalSignature.py TryGuessingDigitalSignature -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - OldTex(...).submobjects[-i-1] is the whole string group in GL (IndexError); flip the glyph in place with become()
# ==============================================================================

from manim_imports_ext import *

class TryGuessingDigitalSignature(Scene):
    def construct(self):
        verify = OldTexText(
            "Verify(", "Message", ", ", 
            "256 bit Signature", ", ", "pk", ")",
            arg_separator = ""
        )
        verify.scale(1.5)
        verify.shift(DOWN)
        signature = verify.get_part_by_tex("Signature")
        verify.set_color_by_tex("Signature", BLUE)
        verify.set_color_by_tex("pk", GREEN)
        brace = Brace(signature, UP)

        zeros_row = OldTex("0"*32)
        zeros = VGroup(*[zeros_row.copy() for x in range(8)])
        zeros.arrange(DOWN, buff = SMALL_BUFF)
        zeros.next_to(brace, UP)

        self.add(verify)
        self.play(
            GrowFromCenter(brace),
            FadeIn(
                zeros,
                lag_ratio = 0.5,
                run_time = 3
            )
        )
        self.wait()
        for n in range(2**10):
            last_row = zeros[-1]
            binary = bin(n)[2:]
            for i, bit_str in enumerate(reversed(binary)):
                # CHANGE: OldTex(...).submobjects[-i-1] is the whole string group in GL (IndexError); flip the glyph in place with become()
                curr_bit = last_row.split()[-i-1]
                new_bit = OldTex(bit_str)
                new_bit.replace(curr_bit, dim_to_match = 1)
                curr_bit.become(new_bit.split()[0])
            self.add(last_row)
            self.wait(1./30)
