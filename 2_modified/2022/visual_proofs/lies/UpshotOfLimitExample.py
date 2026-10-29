# ==============================================================================
# Scene:      UpshotOfLimitExample
# Source:     videos/_2022/visual_proofs/lies.py (lines 1573-1654)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UpshotOfLimitExample.py UpshotOfLimitExample -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2022/visual_proofs/make_lies_images.py
#   - _lib/assets/raster_images/SquareApprox1.png
#   - _lib/assets/raster_images/SquareApprox2.png
#   - _lib/assets/raster_images/SquareApprox3.png
#   - _lib/assets/raster_images/SquareApprox4.png
#   - _lib/assets/raster_images/SquareApproxInf.png
#   - _lib/assets/raster_images/Fourier1.png
#   - _lib/assets/raster_images/Fourier2.png
#   - _lib/assets/raster_images/Fourier3.png
#   - _lib/assets/raster_images/Fourier4.png
#   - _lib/assets/raster_images/FourierInf.png
# ==============================================================================

from manim_imports_ext import *

class UpshotOfLimitExample(InteractiveScene):
    def construct(self):
        # Title
        title = Text("The takeaway", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Underline(title, buff=-0.05)
        underline.scale(1.2)
        underline.insert_n_curves(20)
        underline.set_stroke(WHITE, (1, 3, 3, 1))

        subtitle = Text(
            "What's true of a sequence may not be true of the limit",
            t2c={"sequence": BLUE, "limit": YELLOW},
        )
        subtitle.set_max_width(FRAME_WIDTH - 1)
        subtitle.next_to(title, DOWN, buff=MED_LARGE_BUFF)

        self.add(title, underline, subtitle)

        # Various limits
        n = 4
        numbers = VGroup(
            OldTex("1.4"),
            OldTex("1.41"),
            OldTex("1.414"),
            OldTex("1.4142"),
            OldTex("\\sqrt{2}")
        )
        numbers.scale(1.25)
        properties = VGroup(
            *Text("Rational", font_size=30).replicate(n),
            Text("Irrational", font_size=30)
        )

        folder = "/Users/grant/Dropbox/3Blue1Brown/videos/2022/visual_proofs/lies/images/"
        rational_example = VGroup(numbers, properties)
        circle_example = Group(
            Group(*(
                ImageMobject(os.path.join(folder, "SquareApprox" + end)).set_width(1.25)
                for end in ["1", "2", "3", "4", "Inf"]
            )),
            VGroup(
                *TexText("Len = 8").replicate(n),
                OldTexText("Len = $2\\pi$")
            )
        )
        fourier_example = Group(
            Group(*(
                ImageMobject(os.path.join(folder, "Fourier" + end)).set_width(1.25)
                for end in ["1", "2", "3", "4", "Inf"]
            )),
            VGroup(
                *TexText("Continuous").replicate(n),
                OldTexText("Discontinuous")
            )
        )
        examples = Group(rational_example, circle_example, fourier_example)

        for objs, descs in examples:
            arrow = OldTex("\\cdots \\, \\rightarrow", font_size=72)
            group = Group(*objs[:n], arrow, objs[n])
            for x, mob in enumerate(group):
                mob.move_to(2.75 * x * RIGHT)
            group.set_x(0)
            for desc, obj in zip(descs, objs):
                desc.set_max_width(1.25 * obj.get_width())
                desc.next_to(obj, DOWN)
            descs[:n].set_color(BLUE)
            descs[n].set_color(YELLOW)
            objs.insert_submobject(n, arrow)

        examples.arrange(DOWN, buff=LARGE_BUFF)
        examples.set_height(5.0)
        examples.to_edge(DOWN)

        for i in range(3):
            objs, descs = examples[i]
            self.play(
                LaggedStartMap(FadeIn, objs, lag_ratio=0.5, scale=2),
                LaggedStartMap(FadeIn, descs, lag_ratio=0.5, scale=2),
                run_time=2
            )
