# ==============================================================================
# Scene:      AskHowDigitalSignaturesArePossible
# Source:     videos/_2017/crypto.py (lines 966-996)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskHowDigitalSignaturesArePossible.py AskHowDigitalSignaturesArePossible -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_cursive_name(name):
    result = OldTexText("\\normalfont\\calligra %s"%name)
    result.set_stroke(width = 0.5)
    return result


class AskHowDigitalSignaturesArePossible(TeacherStudentsScene):
    def construct(self):
        signature = get_cursive_name("Alice")
        signature.scale(1.5)
        signature.set_color(BLUE_C)
        signature.to_corner(UP+LEFT)
        signature_copy = signature.copy()
        signature_copy.shift(3*RIGHT)

        bits = OldTex("01100001")
        bits.next_to(signature, DOWN)
        bits.shift_onto_screen()
        bits_copy = bits.copy()
        bits_copy.next_to(signature_copy, DOWN)


        self.student_says(
            "Couldn't you just \\\\ copy the signature?",
            target_mode = "confused",
            run_time = 1
        )
        self.play_student_changes("pondering", "confused", "erm")
        self.play(Write(signature))
        self.play(LaggedStartMap(FadeIn, bits, run_time = 1))
        self.wait()
        self.play(ReplacementTransform(
            bits.copy(), bits_copy,
            path_arc = np.pi/2
        ))
        self.play(Write(signature_copy))
        self.wait(3)
