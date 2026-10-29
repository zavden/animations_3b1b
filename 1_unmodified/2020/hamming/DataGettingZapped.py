# ==============================================================================
# Scene:      DataGettingZapped
# Source:     videos/_2020/hamming.py (lines 1152-1220)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DataGettingZapped.py DataGettingZapped -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_bit_grid(n_rows, n_cols, bits=None, buff=MED_SMALL_BUFF, height=4):
    bit_pair = VGroup(Integer(0), Integer(1))
    bit_mobs = VGroup(*[
        bit_pair.copy()
        for x in range(n_rows * n_cols)
    ])
    bit_mobs.arrange_in_grid(n_rows, n_cols, buff=buff)
    bit_mobs.set_height(height)
    if bits is None:
        bits = np.random.randint(0, 2, len(bit_mobs))

    for bit_mob, bit in zip(bit_mobs, bits):
        bit_mob[1 - bit].set_opacity(0)

    bit_mobs.n_rows = n_rows
    bit_mobs.n_cols = n_cols
    return bit_mobs


class DataGettingZapped(Scene):
    CONFIG = {
        "random_seed": 1,
    }

    def construct(self):
        # Setup bit array
        # bits = get_bit_grid(50, 100)
        bits = get_bit_grid(25, 50)
        bits.set_color(GREY_B)
        bits.set_height(FRAME_HEIGHT - 0.25)

        image = ImageMobject("LowResMandelbrot")
        image.replace(bits, dim_to_match=0)

        threshold = 0.1
        for bit in bits:
            try:
                rgb = image.point_to_rgb(bit.get_center())
                if get_norm(rgb) > threshold:
                    value = 1
                else:
                    value = 0
                bit[value].set_opacity(1)
                bit[1 - value].set_opacity(0)
            except Exception:
                pass

        self.add(bits)

        # Zippity zap
        bolt = SVGMobject("lightning_bolt")
        bolt[0].add_line_to(bolt[0].get_start())
        bolt.set_fill(RED_B, 1)
        bolt.set_stroke(width=0)
        bolt.set_height(0.5)

        def strike_anim(bit, bolt=bolt, **kwargs):
            bolt = bolt.copy()
            bolt.move_to(bit.get_center(), DL)
            bits.remove(bit)
            bit.generate_target()
            bit.target.set_color(RED)
            bit.target.set_stroke(RED, 1)
            for sm in bit.target:
                sm.set_opacity(1 - sm.get_fill_opacity())

            outline = bolt.deepcopy()
            outline.set_stroke(RED_D, 2)
            outline.set_fill(opacity=0)

            return AnimationGroup(
                Succession(
                    GrowFromPoint(bolt, bolt.get_corner(UR), rate_func=rush_into),
                    FadeOut(bolt, run_time=0.5),
                ),
                Succession(
                    ShowCreation(outline),
                    FadeOut(outline),
                ),
                MoveToTarget(bit),
            )

        for count in range(20):
            self.play(LaggedStart(*[
                strike_anim(random.choice(bits))
                for x in range(int(random.expovariate(0.5)) + 1)
            ], lag_ratio=0.25))
            self.wait(random.expovariate(2))
