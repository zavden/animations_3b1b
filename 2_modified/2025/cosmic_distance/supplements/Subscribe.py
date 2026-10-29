# ==============================================================================
# Scene:      Subscribe
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1260-1317)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Subscribe.py Subscribe -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses generic placeholder SVG icons for youtube_logo, email, x_logo, bluesky_logo and rss_logo (in _lib/assets/svg_images/).
#
# Placeholder assets (not Grant's originals):
#   - svg_images/{youtube_logo,email,x_logo,bluesky_logo,rss_logo}.svg (generic placeholder icons, not imitating the real logos)
# ==============================================================================

from manim_imports_ext import *

class Subscribe(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer()
        morty.to_corner(DR)
        morty.body.insert_n_curves(100)
        title = Text("Follow @3blue1brown wherever you follow things")
        title.to_edge(UP)
        title.set_fill(border_width=1)

        logos = Group(
            SVGMobject("youtube_logo"),
            SVGMobject("email").set_fill(GREY_A),
            SVGMobject("x_logo").set_fill(GREY_C),
            ImageMobject("instagram_logo"),
            SVGMobject("bluesky_logo"),
            ImageMobject("facebook_logo"),
            SVGMobject("rss_logo"),
            Tex(R"\dots", font_size=72),
        )
        for logo in logos[:-1]:
            logo.set_height(0.75)
            if isinstance(logo, SVGMobject):
                logo.set_fill(border_width=1)
        logos.arrange(RIGHT, buff=0.75, aligned_edge=DOWN)
        logos.next_to(title, DOWN, buff=1)
        logos[-1].match_y(logos)

        self.add(title)
        self.play(morty.change("raise_right_hand"))
        self.play(LaggedStartMap(FadeIn, logos, shift=0.25 * DR, lag_ratio=0.25, run_time=2))
        self.play(Blink(morty))
        self.wait()

        # Highlight email
        mail = logos[1]
        url = Text("https://3b1b.co/mail", font="Consolas")
        url.next_to(mail, DOWN, buff=1.5)
        arrow = Arrow(mail, url, thickness=5, buff=0.2)

        self.play(
            GrowArrow(arrow),
            FadeIn(url, DOWN),
            morty.change("tease"),
        )
        self.play(Blink(morty))
        self.wait()

        # Organize
        n = len("Follow@3blue1brown")
        self.play(
            LaggedStart(FadeOut(arrow, LEFT), FadeOut(url, LEFT)),
            logos.animate.arrange_in_grid(2, 4, h_buff=0.25, v_buff=0.5).set_height(1.0).next_to(title, DOWN, 0.5).to_edge(LEFT, buff=0.5),
            title[:n].animate.to_edge(LEFT),
            FadeOut(title[n:], LEFT),
            run_time=2
        )
        self.wait()
