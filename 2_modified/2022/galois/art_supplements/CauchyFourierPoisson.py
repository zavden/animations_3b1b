# ==============================================================================
# Scene:      CauchyFourierPoisson
# Source:     videos/_2022/galois/art_supplements.py (lines 152-186)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CauchyFourierPoisson.py CauchyFourierPoisson -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - Cauchy-Portrait-Cutoff.png, Fourier-Portrait.png, Poisson-Portrait-Outpainted.png (placeholder portraits, raster_images/; make_galois_assets.py)
# ==============================================================================

from manim_imports_ext import *

class CauchyFourierPoisson(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle(fill_color="#211F22", fill_opacity=1))
        folder = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2022/galois/artwork/chapter 1/Portraits/"
        images = Group(
            ImageMobject(os.path.join(folder, "Cauchy-Portrait-Cutoff")),
            ImageMobject(os.path.join(folder, "Fourier-Portrait")),
            ImageMobject(os.path.join(folder, "Poisson-Portrait-Outpainted")),
        )
        for image in images:
            image.set_width(4)
        images[0].set_width(3.5)
        images.arrange(RIGHT, aligned_edge=DOWN)
        images.set_width(FRAME_WIDTH - 1)
        images.to_edge(UP, buff=LARGE_BUFF)

        # Names
        names = VGroup(
            Text("Augustin Cauchy"),
            Text("Joseph Fourier"),
            Text("Siméon Poisson"),
        )
        for name, image in zip(names, images):
            name.next_to(image, DOWN)
            name.set_fill(GREY_A)
        names[1:].shift(SMALL_BUFF * RIGHT)

        # Animations
        kw = dict(lag_ratio=0.5, run_time=3)
        self.play(
            LaggedStart(*(FadeIn(image, 0.5 * UP, scale=1.1) for image in images), **kw),
            LaggedStart(*(Write(name, rate_func=squish_rate_func(smooth, 0, 0.85)) for name in names), **kw),
        )
        self.wait()
