# ==============================================================================
# Scene:      WriteTwoCosPattern
# Source:     videos/_2022/borwein/main.py (lines 649-693)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteTwoCosPattern.py WriteTwoCosPattern -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex requires a StringMobject and OldTex is not one; it matches glyphs by shape)
# ==============================================================================

from manim_imports_ext import *

def get_sinc_tex(k=1):
    div_k = f"/ {k}" if k > 1 else ""
    return Rf"{{\sin(x {div_k}) \over x {div_k}}}"


def get_multi_sinc_integral(ks=[1], dots_at=None, rhs="", insertion=""):
    result = OldTex(
        R"\int_{-\infty}^\infty",
        insertion,
        *(
            get_sinc_tex(k) if k != dots_at else R"\dots"
            for k in ks
        ),
        "dx",
        rhs,
    )
    t2c = {
        R"\sin": BLUE,
        "x / 3": TEAL,
        "x / 5": GREEN_B,
        "x / 7": GREEN_C,
        "x / 9": interpolate_color(GREEN, YELLOW, 1 / 3),
        "x / 11": interpolate_color(GREEN, YELLOW, 2 / 3),
        "x / 13": YELLOW,
        "x / 15": RED_B,
    }
    for tex, color in t2c.items():
        result.set_color_by_tex(tex, color)
    return result


class WriteTwoCosPattern(InteractiveScene):
    def construct(self):
        # Integrals
        integrals = VGroup(
            *(
                get_multi_sinc_integral(range(1, n, 2), insertion=R"2\cos(x)", rhs=R"= \pi")
                for n in range(1, 7, 2)
            ),
            OldTex(R"\vdots"),
            get_multi_sinc_integral([1, 3, 5, 111], dots_at=5, insertion=R"2\cos(x)", rhs=R"= \pi"),
            get_multi_sinc_integral([1, 3, 5, 111, 113], dots_at=5, insertion=R"2\cos(x)", rhs=R"= \pi"),
        )
        integrals.scale(0.75)
        for inter in integrals:
            inter[-1].scale(1.5, about_edge=LEFT)

        integrals.arrange(DOWN, buff=0.8, aligned_edge=RIGHT)
        integrals.set_height(FRAME_HEIGHT - 1)
        integrals.move_to(2 * LEFT)

        integrals[-1][-3].set_color(RED)

        self.add(integrals[0])
        for i in [0, 1, 2, 4]:
            j = i + 2 if i == 2 else i + 1
            # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
            anims = [TransformMatchingShapes(integrals[i].copy(), integrals[j])]
            if i == 2:
                anims.append(Write(integrals[3], run_time=1))
            self.play(*anims)
            self.wait(0.5)
        self.add(integrals)

        # RHS
        text = Text("A tiny-but-definitely-positive number\nthat my computer couldn't evaluate\nin a reasonable amount of time")
        text.scale(0.5)
        parens = OldTex("()")[0]
        parens.match_height(text)
        parens[0].next_to(text, LEFT, SMALL_BUFF)
        parens[1].next_to(text, RIGHT, SMALL_BUFF)
        minus = OldTex("-").next_to(parens, LEFT)
        rhs = VGroup(minus, parens, text)

        rhs.next_to(integrals[-1], RIGHT, buff=SMALL_BUFF)
        self.play(Write(rhs))
        self.wait()
