# ==============================================================================
# Scene:      WriteFullIntegrals
# Source:     videos/_2022/borwein/main.py (lines 407-440)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteFullIntegrals.py WriteFullIntegrals -w -m --fps 15
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


class WriteFullIntegrals(InteractiveScene):
    def construct(self):
        # Integrals
        ints = VGroup(*(
            get_multi_sinc_integral(range(1, n, 2), rhs=R"= \pi")
            for n in range(3, 19, 2)
        ))
        ints.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        ints.center().to_corner(UL)
        for inter in ints:
            inter[-1].scale(1.5, about_edge=LEFT)

        q_marks = OldTex("???", color=RED).scale(2)
        q_marks.next_to(ints[-1], RIGHT, buff=MED_LARGE_BUFF)
        correction = OldTex("- 0.0000000000462...").scale(1.25)
        correction.next_to(ints[-1], RIGHT, SMALL_BUFF)

        # Show all
        frame = self.camera.frame
        ds = ValueTracker(0)
        frame.add_updater(lambda m, dt: m.scale(1 + 0.02 * dt, about_edge=UL).shift(ds.get_value() * dt * DOWN))

        self.add(ints[0], ds)
        for i in range(len(ints) - 1):
            self.wait(2)
            # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
            anims = [TransformMatchingShapes(ints[i].copy(), ints[i + 1])]
            if i < 6:
                anims.append(ds.animate.increment_value(0.1))
            self.play(*anims)
        frame.clear_updaters()
        self.play(Write(q_marks), frame.animate.scale(1.1, about_edge=UL).shift(2 * DOWN), run_time=2)
        self.wait()
        self.play(FadeTransform(q_marks, correction))
        self.wait()
