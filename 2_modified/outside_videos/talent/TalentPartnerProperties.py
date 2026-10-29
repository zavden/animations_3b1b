# ==============================================================================
# Scene:      TalentPartnerProperties
# Source:     videos/outside_videos/talent.py (lines 79-193)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TalentPartnerProperties.py TalentPartnerProperties -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/outside_videos/talent/company_building.svg
#   - _lib/assets/svg_images/company_building.svg
#
# Notes:
#   company_building.svg is a placeholder SVG generated with _lib/assets/generated/outside_videos/talent/make_talent_svgs.py and copied to _lib/assets/svg_images/ because the code calls SVGMobject('company_building').
# ==============================================================================

from manim_imports_ext import *

class TalentPartnerProperties(InteractiveScene):
    def construct(self):
        # Company seeking you
        company = SVGMobject("company_building")
        company.set_height(3)
        company.set_fill(GREY_B)
        company.set_shading(0.5, 0.5)
        company.to_edge(LEFT, buff=0.5)

        laptop = Laptop(width=2.5)
        laptop.rotate(80 * DEG, LEFT)
        laptop.rotate(80 * DEG, DOWN)
        laptop.center().to_edge(RIGHT, buff=1.0)
        randy = Randolph(mode="pondering", height=2.5)
        randy.next_to(laptop, LEFT, buff=0).shift(0.5 * DOWN)
        randy.align_to(company, DOWN)
        randy.look_at(laptop.screen)

        arrow = Arrow(randy.get_corner(DL), company.get_corner(DR), thickness=8, buff=0.5)
        arrow.match_y(randy)

        self.add(company)
        self.add(laptop)
        self.add(randy)
        for n in range(2):
            self.play(Blink(randy))
            self.wait()
        self.play(GrowArrow(arrow))
        self.play(randy.change("well", company))
        self.wait()
        self.play(Blink(randy))
        self.wait()

        # Others at the company
        others = VGroup(
            PiCreature(color=BLUE_D, mode="gracious"),
            PiCreature(color=BLUE_C, mode="tease"),
            PiCreature(color=BLUE_E, mode="well"),
        )
        others.set_height(0.8)
        others.arrange(RIGHT, buff=0.2)
        others.next_to(company, DOWN, buff=0.2)

        hearts = SuitSymbol("hearts").replicate(3)
        hearts.set_height(0.3)
        for heart, pi in zip(hearts, others):
            heart.move_to(pi.get_corner(UR))
            heart.shift(0.1 * RIGHT)
        hearts.shuffle()

        self.play(
            LaggedStartMap(FadeIn, others),
            randy.change("coin_flip_1", others),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, hearts, shift=0.25 * UP, lag_ratio=0.25),
            *(pi.animate.look_at(company) for pi in others)
        )
        self.play(Blink(others[1]))
        self.play(Blink(others[2]))
        self.wait()

        # Talking with them
        frame = self.frame

        morty = Mortimer().flip()
        morty.set_height(others.get_height() * 1.1)
        morty.next_to(others, LEFT, LARGE_BUFF, aligned_edge=DOWN)

        self.add(morty)
        self.play(
            FadeOut(randy, time_span=(0, 1)),
            frame.animate.reorient(0, 0, 0, (-6.75, -1.77, 0.0), 3.94),
            FadeOut(arrow),
            morty.change("well", others),
            FadeOut(hearts, lag_ratio=0.5),
            *(pi.animate.look_at(morty.eyes) for pi in others),
            run_time=3
        )
        bubble = morty.get_bubble("...", bubble_type=SpeechBubble)
        self.play(LaggedStart(
            Write(bubble),
            morty.change('speaking', others),
            others[0].change("tease"),
            others[1].change("happy"),
            others[1].change("happy"),
            lag_ratio=0.5
        ))
        self.play(Blink(morty))
        self.wait()

        # Response
        content = Text("...", font_size=12)
        new_bubble = others[0].get_bubble(
            content,
            bubble_type=SpeechBubble,
            direction=RIGHT
        )
        content.scale(3)
        self.play(
            others[0].change("hooray"),
            Write(new_bubble),
            FadeOut(bubble),
            morty.change('tease')
        )
        self.wait()
        self.play(Blink(others[0]))
        self.play(
            others[0].change("well", others[1].eyes),
            others[1].animate.look_at(others[0].eyes),
            FadeOut(new_bubble),
        )
        self.play(Blink(others[1]))
        self.wait()
