# ==============================================================================
# Scene:      HammingAtBell
# Source:     videos/_2020/hamming.py (lines 1325-1396)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HammingAtBell.py HammingAtBell -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def zap_anim(bit, bolt_height=0.75):
    bolt = SVGMobject("lightning_bolt")
    bolt[0].add_line_to(bolt[0].get_start())
    bolt.set_fill(RED_B, 1)
    bolt.set_stroke(width=0)
    bolt.set_height(bolt_height)

    bolt.move_to(bit.get_center(), DL)

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
        run_time=1,
    )


class HammingAtBell(Scene):
    def construct(self):
        # Setup
        hamming_image = ImageMobject("Richard_Hamming")
        hamming_name = OldTexText("Richard Hamming")
        hamming_name.match_width(hamming_image)
        hamming_name.next_to(hamming_image, DOWN, MED_SMALL_BUFF)
        hamming = Group(hamming_image, hamming_name)
        hamming.to_corner(DR)
        hamming.shift(2 * LEFT)

        bell_logo = ImageMobject("BellSystemLogo")
        bell_logo.set_height(3)
        bell_logo.next_to(hamming, LEFT, buff=2)
        bell_logo.to_edge(UP)

        bell_logo_outline = SVGMobject("BellSystemLogo")
        bell_logo_outline.match_height(bell_logo)
        bell_logo_outline.set_stroke(GREY_B, 1)
        bell_logo_outline.set_fill(BLACK, 0)
        bell_logo_outline.move_to(bell_logo)

        punchcard = SVGMobject("punchcard")
        punchcard.set_stroke(width=0)
        punchcard.set_fill(GREY_B, 1)
        punchcard.next_to(bell_logo, DOWN, LARGE_BUFF)
        punchcard.remove(*punchcard[23:])

        years = OldTexText("1940s")
        years.scale(2)
        years.to_edge(UP)

        # Introductions
        self.play(Write(years))
        self.play(FadeIn(hamming[0], RIGHT))
        self.play(Write(hamming[1]))
        self.play(
            FadeOut(years),
            ShowCreationThenFadeOut(bell_logo_outline, lag_ratio=0.1, run_time=4),
            FadeIn(bell_logo, run_time=3),
        )

        self.play(
            FadeIn(punchcard[0]),
            Write(punchcard[1:], lag_ratio=0.5, run_time=4)
        )
        self.add(punchcard)
        self.wait()

        # Zap some bits
        random.seed(3)
        bits = random.sample(list(punchcard[1:]), 4)
        for bit in bits:
            bit.generate_target()
            bit.target.set_color(RED)
            if random.random() < 0.5:
                bit.target.stretch(0.2, 1, about_edge=DOWN)
            else:
                bit.target.shift(1.2 * bit.get_width() * LEFT)
            self.play(
                MoveToTarget(bit),
                zap_anim(bit)
            )
        self.wait()

        # Frustration
        curse = OldTexText("\\$*@\\#*!!?!")[0]
        curse.set_color(RED)
        curse.next_to(hamming, UP)

        self.play(ShowIncreasingSubsets(curse))
        self.wait()
