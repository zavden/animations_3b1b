# ==============================================================================
# Scene:      FamousMathematicians
# Source:     videos/_2021/shadows.py (lines 6321-6376)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FamousMathematicians.py FamousMathematicians -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/Fourier.jpg  (_lib/assets/generated/2021/shadows/make_shadows_assets.py)
#   - _lib/assets/raster_images/Riemann_cropped.jpeg  (_lib/assets/generated/2021/shadows/make_shadows_assets.py)
# ==============================================================================

from manim_imports_ext import *

class FamousMathematicians(Scene):
    im_height = 3.5

    def construct(self):
        # Portraits
        images = Group(
            ImageMobject("Newton"),
            ImageMobject("Euler"),
            ImageMobject("Gauss"),
            ImageMobject("Fourier"),
            ImageMobject("Riemann_cropped"),
            ImageMobject("Cauchy"),
            ImageMobject("Noether"),
            ImageMobject("Ramanujan"),
        )
        names = VGroup(
            Text("Isaac Newton"),
            Text("Leonhard Euler"),
            Text("Carl Friedrich Gauss"),
            Text("Joseph Fourier"),
            Text("Bernhard Riemann"),
            Text("Augustin Cauchy"),
            Text("Emmy Noether"),
            Text("Srinivasa Ramanujan"),
        )
        im_groups = Group()
        for im, name in zip(images, names):
            im.set_height(self.im_height)
            name.scale(0.6)
            name.set_color(GREY_A)
            name.next_to(im, DOWN)
            im_groups.add(Group(im, name))

        # im_groups.arrange(RIGHT, aligned_edge=UP, buff=LARGE_BUFF)
        im_groups.arrange_in_grid(2, 4, aligned_edge=UP, buff=LARGE_BUFF)
        im_groups.set_width(FRAME_WIDTH - 2)
        im_groups.to_edge(LEFT)
        dots = OldTex("\\dots", font_size=72).replicate(2)
        dots[0].next_to(images[-5], RIGHT, MED_LARGE_BUFF)
        dots[1].next_to(images[-1], RIGHT, MED_LARGE_BUFF)

        self.play(
            LaggedStart(*map(FadeIn, (*im_groups, dots)), lag_ratio=0.25),
            run_time=5
        )
        self.wait()

        self.play(
            im_groups[0].animate.set_height(6).center().to_edge(LEFT),
            LaggedStart(*(
                FadeOut(mob, DR)
                for mob in (*im_groups[1:], dots)
            ), lag_ratio=0.25),
            run_time=2,
        )
        self.wait()
