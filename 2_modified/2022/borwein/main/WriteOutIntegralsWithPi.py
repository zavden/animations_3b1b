# ==============================================================================
# Scene:      WriteOutIntegralsWithPi
# Source:     videos/_2022/borwein/main.py (lines 529-585)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteOutIntegralsWithPi.py WriteOutIntegralsWithPi -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex requires a StringMobject and OldTex is not one; it matches glyphs by shape)
# ==============================================================================

from manim_imports_ext import *

SUB_ONE_FACTOR = "0.99999999998529"


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


class WriteOutIntegrals(InteractiveScene):
    def construct(self):
        # Integrals
        ints = self.get_integrals()

        ints.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=RIGHT)
        ints.set_height(FRAME_HEIGHT - 1)
        ints[-1][:-2].align_to(ints[:-1], RIGHT)
        ints[-1][-2:].next_to(ints[-1][:-2], RIGHT, SMALL_BUFF)
        ints[3].shift(SMALL_BUFF * LEFT)
        ints.center()

        # Show all
        self.add(ints[0])
        ints[-1][-2].set_opacity(0)
        ints[-1][-1].save_state()
        ints[-1][-1].move_to(ints[-1][-2], LEFT)
        for i in range(4):
            if i < 3:
                src = ints[i].copy()
            else:
                src = ints[i + 1].copy()

            if i < 2:
                target = ints[i + 1]
            elif i == 2:
                target = VGroup(*ints[i + 1], *ints[i + 2])
            else:
                target = ints[i + 2]
            # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
            self.play(TransformMatchingShapes(src, target))
            self.wait(0.5)

        ints[-1][-2].set_opacity(1)
        self.play(Write(ints[-1][-2]), ints[-1][-1].animate.restore())
        self.wait()

    def get_integrals(self):
        return VGroup(
            get_multi_sinc_integral([1], rhs=R"= \pi"),
            get_multi_sinc_integral([1, 3], rhs=R"= \pi"),
            get_multi_sinc_integral([1, 3, 5], rhs=R"= \pi"),
            OldTex(R"\vdots"),
            get_multi_sinc_integral([1, 3, 5, 7, 13], dots_at=7, rhs=R"= \pi"),
            get_multi_sinc_integral([1, 3, 5, 7, 13, 15], dots_at=7, rhs=Rf"= ({SUB_ONE_FACTOR}\dots)\pi"),
        )


class WriteOutIntegralsWithPi(WriteOutIntegrals):
    def get_integrals(self):
        t2c = {
            R"\sin": BLUE,
            "x/3": TEAL,
            "x/5": GREEN_B,
            "x/7": GREEN_C,
            "x/9": interpolate_color(GREEN, YELLOW, 1 / 3),
            "x/11": interpolate_color(GREEN, YELLOW, 2 / 3),
            "x/13": YELLOW,
            "x/15": RED_B,
        }
        result = VGroup(
            OldTex(
                R"\int_{-\infty}^\infty",
                R"\frac{\sin(\pi x)}{\pi x}",
                R"dx = ", "1.0"
            ),
            OldTex(
                R"\int_{-\infty}^\infty",
                R"\frac{\sin(\pi x)}{\pi x}",
                R"\frac{\sin(\pi x/3)}{\pi x/3}",
                R"dx = ", "1.0"
            ),
            OldTex(
                R"\int_{-\infty}^\infty",
                R"\frac{\sin(\pi x)}{\pi x}",
                R"\frac{\sin(\pi x/3)}{\pi x/3}",
                R"\frac{\sin(\pi x/5)}{\pi x/5}",
                R"dx = ", "1.0"
            ),
            OldTex(R"\vdots"),
            OldTex(
                R"\int_{-\infty}^\infty",
                R"\frac{\sin(\pi x)}{\pi x}",
                R"\frac{\sin(\pi x/3)}{\pi x/3}",
                # R"\frac{\sin(\pi x/5)}{\pi x/5}",
                R"\dots",
                R"\frac{\sin(\pi x/13)}{\pi x/13}",
                R"dx = ", "1.0"
            ),
            OldTex(
                R"\int_{-\infty}^\infty",
                R"\frac{\sin(\pi x)}{\pi x}",
                R"\frac{\sin(\pi x/3)}{\pi x/3}",
                # R"\frac{\sin(\pi x/5)}{\pi x/5}",
                R"\dots",
                R"\frac{\sin(\pi x/13)}{\pi x/13}",
                R"\frac{\sin(\pi x/15)}{\pi x/15}",
                R"dx = ", fR"{SUB_ONE_FACTOR}\dots", "."
            ),
        )
        result[-1][-1].scale(0)
        for mob in result:
            for tex, color in t2c.items():
                mob.set_color_by_tex(tex, color)
        return result
