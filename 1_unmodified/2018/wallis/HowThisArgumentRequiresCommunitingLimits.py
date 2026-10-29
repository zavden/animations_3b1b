# ==============================================================================
# Scene:      HowThisArgumentRequiresCommunitingLimits
# Source:     videos/_2018/wallis.py (lines 4073-4259)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowThisArgumentRequiresCommunitingLimits.py HowThisArgumentRequiresCommunitingLimits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


class HowThisArgumentRequiresCommunitingLimits(PiCreatureScene):
    def construct(self):
        mathy, morty = self.pi_creatures

        scale_val = 0.7
        factors = OldTex(
            "{|L_1 - K|", "\\over", "|L_1 - S|}", "\\cdot",
            "{|L_{-1} - K|", "\\over", "|L_{-1} - S|}", "\\cdot",
            "{|L_2 - K|", "\\over", "|L_2 - S|}", "\\cdot",
            "{|L_{-2} - K|", "\\over", "|L_{-2} - S|}", "\\cdot",
            "{|L_3 - K|", "\\over", "|L_3 - S|}", "\\cdot",
            "{|L_{-3} - K|", "\\over", "|L_{-3} - S|}", "\\cdots",
        )
        factors.set_color_by_tex_to_color_map({
            "K": BLUE,
            "S": YELLOW,
        })
        equals = OldTex("=")
        result = OldTex(
            "{N", "{\\text{distance} \\choose \\text{between obs.}}",
            "\\over", "2}"
        )

        top_line = VGroup(factors, equals, result)
        top_line.arrange(RIGHT, buff=SMALL_BUFF)
        result.shift(SMALL_BUFF * UP)
        top_line.scale(scale_val)
        top_line.to_edge(UP)

        fractions = VGroup(*[
            factors[i:i + 3]
            for i in range(0, len(factors), 4)
        ])
        fraction_limit_arrows = VGroup(*[
            Vector(0.5 * DOWN).next_to(fraction, DOWN)
            for fraction in fractions
        ])
        fraction_limit_arrows.set_color(WHITE)

        wallis_product = get_wallis_product(6)
        fraction_limits = VGroup(*[
            wallis_product[i:i + 3]
            for i in range(0, 4 * 6, 4)
        ])
        for lf, arrow in zip(fraction_limits, fraction_limit_arrows):
            lf.next_to(arrow, DOWN, MED_SMALL_BUFF)

        result_limit_arrow = fraction_limit_arrows[0].copy()
        result_limit_arrow.next_to(result, DOWN)
        result_limit_arrow.align_to(fraction_limit_arrows[0])

        result_limit = wallis_product[-3:]
        result_limit.next_to(result_limit_arrow, DOWN, MED_SMALL_BUFF)

        lower_equals = OldTex("=")
        lower_equals.next_to(result_limit, LEFT)

        mult_signs = VGroup()
        for f1, f2 in zip(fraction_limits, fraction_limits[1:]):
            mult_sign = OldTex("\\times")
            mult_sign.move_to(VGroup(f1, f2))
            mult_signs.add(mult_sign)
        cdots = OldTex("\\cdots")
        cdots.move_to(VGroup(fraction_limits[-1], lower_equals))
        mult_signs.add(cdots)

        # Pi creatures react
        self.play(
            PiCreatureSays(
                mathy,
                "Whoa whoa whoa \\\\ there buddy",
                look_at=morty.eyes,
                target_mode="sassy",
            ),
            morty.change, "guilty", mathy.eyes,
        )
        self.wait(2)

        # Write out commutative diagram
        self.play(
            RemovePiCreatureBubble(
                mathy,
                target_mode="raise_right_hand",
                look_at=factors,
            ),
            morty.change, "pondering", factors,
            LaggedStartMap(FadeIn, factors),
        )
        self.wait()
        self.play(
            FadeIn(equals),
            Write(result)
        )
        self.wait()
        self.play(
            LaggedStartMap(GrowArrow, fraction_limit_arrows),
            LaggedStartMap(
                FadeInFrom, fraction_limits,
                direction=UP
            ),
            run_time=4,
            lag_ratio=0.25,
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, mult_signs),
            FadeIn(lower_equals),
            mathy.change, "sassy",
        )
        self.play(
            GrowArrow(result_limit_arrow),
            FadeIn(result_limit, direction=UP),
            morty.change, "confused",
        )
        self.wait(2)

        # Write general limit rule
        limit_rule = OldTex(
            "\\left( \\lim_{N \\to \\infty} a_N^{(1)} \\right)",
            "\\left( \\lim_{N \\to \\infty} a_N^{(2)} \\right)",
            "\\cdots", "=",
            "\\lim_{N \\to \\infty} \\left( a_N^{(1)} a_N^{(2)} \\cdots \\right)"
        )
        limit_rule.next_to(self.pi_creatures, UP)
        q_marks = OldTex("???")
        q_marks.set_color(YELLOW)
        limit_equals = limit_rule.get_part_by_tex("=")
        q_marks.next_to(limit_equals, UP, SMALL_BUFF)

        index_of_equals = limit_rule.index_of_part(limit_equals)
        lhs_brace = Brace(limit_rule[:index_of_equals], UP)
        rhs_brace = Brace(limit_rule[index_of_equals + 1:], UP)

        self.play(
            FadeInFromDown(limit_rule),
            mathy.change, "angry",
            morty.change, "erm",
        )
        self.play(GrowFromCenter(lhs_brace))
        self.wait()
        self.play(ReplacementTransform(lhs_brace, rhs_brace))
        self.wait(2)
        self.play(FadeOut(rhs_brace), Write(q_marks))
        limit_rule.add(q_marks)
        self.wait(2)
        self.play(morty.change, "pondering")
        self.play(mathy.change, "tease")
        self.wait(3)
        self.play(
            Animation(limit_rule),
            morty.change, "pondering",
            mathy.change, "pondering",
        )
        self.wait(3)

        # Write dominated convergence
        mover = VGroup(
            top_line, fraction_limits, fraction_limit_arrows,
            mult_signs, lower_equals,
            result_limit, result_limit_arrow,
        )
        self.play(
            mover.next_to, FRAME_HEIGHT * UP / 2, UP,
            limit_rule.to_edge, UP,
        )
        dominated_convergence = OldTexText("``Dominated convergence''")
        dominated_convergence.set_color(BLUE)
        dominated_convergence.next_to(limit_rule, DOWN, LARGE_BUFF)

        see_blog_post = OldTexText("(See supplementary blog post)")
        see_blog_post.next_to(dominated_convergence, DOWN)

        self.play(
            FadeInFromDown(dominated_convergence),
            mathy.change, "raise_right_hand",
        )
        self.play(morty.change, "thinking")
        self.wait()
        self.play(Write(see_blog_post))
        self.wait(4)

    def create_pi_creatures(self):
        group = VGroup(PiCreature(color=GREY), Mortimer())
        group.set_height(2)
        group.arrange(RIGHT, buff=4)
        group.to_edge(DOWN)
        return group
