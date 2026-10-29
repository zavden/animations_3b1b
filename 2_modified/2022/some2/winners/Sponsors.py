# ==============================================================================
# Scene:      Sponsors
# Source:     videos/_2022/some2/winners.py (lines 1336-1383)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Sponsors.py Sponsors -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DOC_DIR (Grant's output folder in the original) -> os.path.join(get_directories()["data"], "2022/some2/winners/"), with the placeholder data in _lib/data/2022/some2/winners/
#
# Placeholder assets (not Grant's originals):
#   - sponsor_logos/ (Brilliant.png, RiscZero.png, ProtocolLabs.png, placeholder GoogleFonts.svg, in _lib/data/2022/some2/winners/; make_some2_assets.py)
# ==============================================================================

from manim_imports_ext import *

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DOC_DIR = os.path.join(get_directories()["data"], "2022/some2/winners/")


class Sponsors(InteractiveScene):
    def construct(self):
        # Images
        self.add(FullScreenFadeRectangle(fill_color=interpolate_color(GREY_A, WHITE, 0.5)))

        img_dir = os.path.join(DOC_DIR, "sponsor_logos")
        brilliant = ImageMobject(os.path.join(img_dir, "Brilliant"))
        risczero = ImageMobject(os.path.join(img_dir, "RiscZero"))
        google = SVGMobject(os.path.join(img_dir, "GoogleFonts"))
        google.set_stroke(width=0)
        pl = ImageMobject(os.path.join(img_dir, "ProtocolLabs"))

        logos = Group(brilliant, risczero, google, pl)
        for logo in logos:
            logo.set_width(5)

        logos.arrange(DOWN)
        logos[0].shift(0.35 * UP)
        logos[2:].shift(0.75 * DOWN)
        logos.center().to_corner(DL)
        logos.to_edge(DOWN, buff=0)

        # Contributions
        contributions = VGroup(
            Text("$1,000 for each winner").next_to(brilliant, RIGHT, buff=2.0),
            Text("$500 for each\nhonorable mention").next_to(logos[1:3], RIGHT, buff=2.0),
            Text("Operations costs").next_to(pl, RIGHT, buff=2.0),
        )
        contributions.set_fill(BLACK)
        contributions.set_stroke(BLACK, 0)
        brace = Brace(logos[1:3], RIGHT)
        brace.set_fill(BLACK, 1)
        arrows = VGroup()
        for logo, j in zip(logos, [0, 1, 1, 2]):
            arrows.add(Arrow(logo.get_right(), contributions[j].get_left(), color=BLACK))

        # Animations
        self.play(FadeIn(brilliant, 0.5 * DOWN))
        self.play(ShowCreation(arrows[0]), Write(contributions[0]))
        self.wait()

        self.play(LaggedStartMap(FadeIn, logos[1:3], shift=DOWN, lag_ratio=0.7))
        self.play(*map(ShowCreation, arrows[1:3]), Write(contributions[1]))
        self.wait()

        self.play(FadeIn(pl, DOWN))
        self.play(ShowCreation(arrows[3]), Write(contributions[2]))
        self.wait()
