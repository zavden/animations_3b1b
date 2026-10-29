# ==============================================================================
# Scene:      WriteMoreFullIntegrals
# Source:     videos/_2022/borwein/main.py (lines 443-479)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteMoreFullIntegrals.py WriteMoreFullIntegrals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (it requires a StringMobject and OldTex is not one); the key_map becomes matched_pairs with the rhs of each integral
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


class WriteMoreFullIntegrals(InteractiveScene):
    def construct(self):
        # Unfortunate copy pasting, but I'm in a rush
        # Integrals
        ints = VGroup(*(
            get_multi_sinc_integral(range(1, n, 2), rhs=R"= \pi")
            for n in range(3, 17, 2)
        ))
        ints.add(get_multi_sinc_integral(range(1, 17, 2), rhs=R"= (0.99999999998529)\pi"))
        ints.add(get_multi_sinc_integral(range(1, 19, 2), rhs=R"= (0.99999998807962)\pi"))
        ints.add(get_multi_sinc_integral(range(1, 21, 2), rhs=R"= (0.99999990662610)\pi"))
        ints.add(get_multi_sinc_integral(range(1, 23, 2), rhs=R"= (0.99999972286332)\pi"))

        ints.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        ints.center().to_corner(UL)
        for inter in ints:
            inter[-1].scale(1.5, about_edge=LEFT)

        # Show all
        frame = self.camera.frame
        ds = ValueTracker(0)
        frame.add_updater(lambda m, dt: m.scale(1 + 0.04 * dt, about_edge=UL).shift(ds.get_value() * dt * DOWN))

        key_map = dict(
            (ints[n][-1].get_tex(), ints[n + 1][-1].get_tex())
            for n in range(-4, -1, 1)
        )

        self.add(ints[0], ds)
        for i in range(len(ints) - 1):
            self.wait()
            src = ints[i].copy()
            # CHANGE: the original key_map (rhs of each integral -> rhs of the next one, for the last ones) becomes matched_pairs
            pairs = [(src[-1], ints[i + 1][-1])] if i >= len(ints) - 4 else []
            # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
            anims = [TransformMatchingShapes(src, ints[i + 1], matched_pairs=pairs)]
            if i < 6:
                anims.append(ds.animate.increment_value(0.1))
            self.play(*anims)
        self.wait(3)
        frame.clear_updaters()
