# ==============================================================================
# Scene:      CoinFlips
# Source:     videos/_2021/bertrands_paradox.py (lines 487-555)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CoinFlips.py CoinFlips -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - OldTex: the final ' = ' of the first string becomes its own string (a manimgl balance_braces bug misaligned the parts with isolate; the numbers came out giant and without '=' signs)
# ==============================================================================

from manim_imports_ext import *

class CoinFlips(Scene):
    CONFIG = {
        "random_seed": 2,
    }

    def construct(self):
        n_rows = 15
        n_cols = 40
        heads = [bool(random.randint(0, 1)) for x in range(n_rows * n_cols)]
        coins = VGroup(*(self.get_coin(h) for h in heads))
        coins.arrange_in_grid(n_rows, n_cols, buff=SMALL_BUFF)
        coins.set_width(FRAME_WIDTH - 0.5)
        coins.to_edge(DOWN)

        # CHANGE: the "=" is split into its own string: OldTex.balance_braces (manimlib/mobject/svg/old_tex_mobject.py)
        # prepends an extra "{" for each character that follows an unmatched "}", and the chunk " \over \#
        # \text{Flips}} = " came out with 6 glyphs instead of 8, misaligning all the parts
        eq = OldTex(
            "{\\# \\text{Heads} \\over \\# \\text{Flips}}", " = ",
            "{Num \\over Den}", "=", "0.500",
            isolate={"Num", "Den", "\\# \\text{Heads}"}
        )
        eq.set_color_by_tex("Heads", RED)
        num = Integer(100, edge_to_fix=ORIGIN)
        den = Integer(100, edge_to_fix=ORIGIN)
        dec = DecimalNumber(0.5, num_decimal_places=3, edge_to_fix=LEFT)
        num_i = eq.index_of_part_by_tex("Num")
        den_i = eq.index_of_part_by_tex("Den")
        dec_i = eq.index_of_part_by_tex("0.500")
        num.replace(eq[num_i], dim_to_match=1)
        den.replace(eq[den_i], dim_to_match=1)
        dec.replace(eq[dec_i], dim_to_match=1)
        eq.replace_submobject(num_i, num)
        eq.replace_submobject(den_i, den)
        eq.replace_submobject(dec_i, dec)
        eq.to_edge(UP)

        def update_eq(eq, alpha):
            n_flips = max(int(alpha * len(heads)), 1)
            n_heads = sum(heads[:n_flips])
            num.set_value(n_heads).set_color(RED)
            den.set_value(n_flips)
            dec.set_value(n_heads / n_flips)
            return eq

        for sm in eq:
            sm.add_updater(lambda m: m)

        words = OldTexText("What does\\\\this approach?", font_size=36)
        words.to_corner(UR)
        arrow = Arrow(words, dec)
        VGroup(words, arrow).set_color(YELLOW)

        self.add(coins, *eq)
        srf = squish_rate_func(smooth, 0.3, 0.4)
        self.play(
            ShowIncreasingSubsets(coins, rate_func=linear),
            UpdateFromAlphaFunc(Mobject(), update_eq, rate_func=linear),
            Write(words, rate_func=srf),
            ShowCreation(arrow, rate_func=srf),
            run_time=18
        )
        self.wait(2)

    def get_coin(self, heads=True, radius=0.25):
        circle = Dot(radius=radius)
        circle.set_fill(RED_E if heads else BLUE_E)
        circle.set_stroke(WHITE, 0.5, 0.5)
        symbol = OldTex("H" if heads else "T")
        symbol.set_height(radius)
        symbol.move_to(circle)
        return VGroup(circle, symbol)
