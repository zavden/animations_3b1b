# ==============================================================================
# Scene:      StripClaim
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 461-553)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StripClaim.py StripClaim -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class StripClaim(InteractiveScene):
    def construct(self):
        # Add title
        title = Text("Desired Claim", font_size=72)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Underline(title)
        VGroup(title, underline).set_color(BLUE)
        self.add(title, underline)

        # Add claim
        claim = Text("""
            A Möbius strip cannot be embedded in 3D
            with its edge on the xy-plane without
            intersecting itself.
        """, alignment="LEFT")
        claim.next_to(title, DOWN, buff=MED_LARGE_BUFF)
        underline.match_width(claim)
        self.play(Write(claim, run_time=2, lag_ratio=0.05))

        # False!
        morty = Mortimer()
        morty.to_corner(DR)
        self.play(
            VFadeIn(morty),
            morty.says("False!", mode="surprised"),
        )
        self.play(
            morty.bubble.content.animate.set_color(RED),
            Blink(morty)
        )
        self.wait()

        # Change the title
        new_title = Text("Revised Claim", font_size=72)
        new_title.set_color(TEAL)
        new_title.move_to(title)
        dots = Text("...")
        dots.next_to(claim["lane"], RIGHT, SMALL_BUFF, aligned_edge=DOWN)

        self.play(
            TransformMatchingStrings(
                title, new_title,
                key_map={"Desired": "Revised"},
                run_time=1,
                lag_ratio=0.5
            ),
            FadeOut(VGroup(morty, morty.bubble)),
            FadeOut(claim["without"], DOWN),
            FadeOut(claim["intersecting itself."], DOWN),
            Write(dots),
        )

        # New claim
        new_claim = Text("""
            A Möbius strip cannot be embedded in 3D
            with its edge on the xy-plane, and with
            its interior entirely above the xy-plane
            without intersecting itself.
        """, alignment="LEFT")
        new_claim.move_to(claim, UL)

        part1 = claim["with its edge on the xy-plane"]
        part2 = new_claim["its interior entirely above the xy-plane"]

        self.play(
            FlashUnder(part1, color=YELLOW, time_width=1.5),
            part1.animate.set_color(YELLOW),
        )
        self.wait()
        self.play(
            FadeOut(dots),
            FadeIn(new_claim[", and with"]),
            FadeIn(part2),
        )
        self.play(
            FlashUnder(part2, time_width=1.5, color=BLUE, run_time=2),
            part2.animate.set_color(BLUE)
        )
        self.wait()
        self.play(
            Write(new_claim["without intersecting itself."])
        )
        self.wait()

        # This one is true
        morty = Mortimer(height=1.5).to_corner(DR)

        self.play(
            VFadeIn(morty),
            morty.says("This one\nis true", mode="tease")
        )
        self.play(Blink(morty))
        self.wait()
