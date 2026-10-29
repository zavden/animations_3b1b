# ==============================================================================
# Scene:      MetaThumbnail
# Source:     videos/_2023/SoME3/main.py (lines 206-287)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MetaThumbnail.py MetaThumbnail -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - 31 placeholder thumbnails <title>.png at the root of _lib/assets/raster_images/ (make_some3_assets.py); the scenes ask for them by Grant's Dropbox path and manim_imports_ext finds them by name
# ==============================================================================

from manim_imports_ext import *

class MetaThumbnail(InteractiveScene):
    def construct(self):
        thumbnail_dir = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2023/SoME3/EntryThumbnails"
        names = [
            "The Mathematics of String Art",
            "Rethinking the real line",
            "The Longest Increasing Subsequence",
            "Chasing Fixed Points: Greedy Gremlin's Trade-Off",
            "How Infinity Works",
            "Pixel Art Anti Aliasing",
            "The Math of Saving The Enola Gay",
            "Making a Pitch Shifter",
            "Functions are Vectors",
            "Cayley Graphs and Pretty Things",
            "The Matrix Arcade: A Visual Explorable of Matrix Transformations",
            "Watching Neural Networks Learn",
            "The Art of Linear Programming",
            "The Mosaic Problem - How and Why to do Math for Fun",
            "Affording a Planet With Geometry",
            "When CAN'T Math Be Generalized?",
            "Rotation + Translation = Rotation. Animated proof",
            "How did the Ancient Egyptians find this volume without Algebra?",
            "A Subtle Aspect of Circular Motion",
            "Minimal Surfaces & the Calculus of Variations",
            "How does a computer-calculator compute logarithms?",
            "What Happens If We Add Fractions Incorrectly?",
            "Can you guess this shape from its shadows?",
            "How Computers Use Numbers",
            "Signed Distance Functions",
            "A Study In Greyscale",
            "Conservative matrix fields",
            "Are Elo Systems Overrated?",
            "The essence of multivariable calculus",
            "The Principle of Least Action",
        ]

        thumbnails = Group(*(
            ImageMobject(os.path.join(thumbnail_dir, name))
            for name in names
        ))
        ftns = Group(*(
            Group(
                SurroundingRectangle(tn, buff=0).set_stroke(GREY_A, 2),
                tn
            )
            for tn in thumbnails
        ))

        # Rows
        groups = Group(
            ftns[:2],
            ftns[2:6],
            ftns[6:14],
            ftns[14:30],
        )
        last = self.frame.get_top()
        for n, group in enumerate(groups):
            group.scale(2**-n)
            group.arrange(RIGHT, buff=0.1)
            group.set_width(FRAME_WIDTH - 0.5)
            group.next_to(last, DOWN, buff=0.2)
            last = group.get_bottom()

        self.add(ftns)
        return

        # Fractal
        last_rect = FullScreenRectangle().set_height(7.25)
        for trip in zip(ftns[0::3], ftns[1::3], ftns[2::3]):
            triad = self.create_triad(*trip, last_rect)
            last_rect = triad[-1]

        self.add(ftns)

    def create_triad(self, im1, im2, im3, to_replace):
        group = Group(im1, im2, im3)
        for im in group:
            im.set_height(4)
        group.add(ScreenRectangle(height=4).set_opacity(0))
        group.arrange_in_grid(buff=0.25)
        group.replace(to_replace)
        return group
