# ==============================================================================
# Scene:      ThumbnailProgression
# Source:     videos/_2023/SoME3/main.py (lines 9-203)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThumbnailProgression.py ThumbnailProgression -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The blurred PNG is saved with save(blur_path) instead of opening the file in text mode ('w')
#
# Placeholder assets (not Grant's originals):
#   - 31 placeholder thumbnails <title>.png at the root of _lib/assets/raster_images/ (make_some3_assets.py); the scenes ask for them by Grant's Dropbox path and manim_imports_ext finds them by name
# ==============================================================================

from manim_imports_ext import *
from PIL import ImageFilter

class ThumbnailProgression(InteractiveScene):
    def construct(self):
        # Make grid
        thumbnail_dir = "/Users/grant/3Blue1Brown Dropbox/3Blue1Brown/videos/2023/SoME3/EntryThumbnails"
        names = [
            "Pixel Art Anti Aliasing",
            "The Math of Saving The Enola Gay",
            "Making a Pitch Shifter",
            "Cayley Graphs and Pretty Things",
            "The Longest Increasing Subsequence",
            "The Matrix Arcade: A Visual Explorable of Matrix Transformations",
            "Watching Neural Networks Learn",
            "Functions are Vectors",
            "The Art of Linear Programming",
            "The Mosaic Problem - How and Why to do Math for Fun",
            "Affording a Planet With Geometry",
            "When CAN'T Math Be Generalized?",
            "Rotation + Translation = Rotation. Animated proof",
            "Rethinking the real line",
            "How did the Ancient Egyptians find this volume without Algebra?",
            "A Subtle Aspect of Circular Motion",
            "Minimal Surfaces & the Calculus of Variations",
            "How does a computer-calculator compute logarithms?",
            "What Happens If We Add Fractions Incorrectly?",
            "Can you guess this shape from its shadows?",
            "Chasing Fixed Points: Greedy Gremlin's Trade-Off",
            "How Computers Use Numbers",
            "Mathematical Magic Mirrorball",
            "The Mathematics of String Art",
            "How Infinity Works",
        ]

        thumbnails = Group(*(
            ImageMobject(os.path.join(thumbnail_dir, name))
            for name in names
        ))
        framed_thumbnails = Group(*(
            Group(
                SurroundingRectangle(tn, buff=0).set_stroke(WHITE, 3),
                tn
            )
            for tn in thumbnails
        ))
        framed_thumbnails.set_height(2)
        framed_thumbnails.arrange_in_grid(h_buff=0.5, v_buff=0.25)
        framed_thumbnails.set_height(FRAME_HEIGHT - 1)

        # Covers
        covers = Group()
        cover_labels = VGroup()
        for thumbnail in thumbnails:
            folder, name = os.path.split(thumbnail.image_path)
            new_folder = guarantee_existence(os.path.join(folder, "blurred"))
            blur_path = os.path.join(new_folder, name)
            pil_img = thumbnail.image
            blurry_pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=75))
            # CHANGE: the file was opened in text mode ('w') and PIL writes bytes; it is saved directly to the path
            blurry_pil_img.save(blur_path)
            blurry_image = ImageMobject(blur_path)
            blurry_image.replace(thumbnail)
            cover = Group(
                SurroundingRectangle(blurry_image, buff=0).set_stroke(WHITE, 3),
                blurry_image
            )
            label = Tex("?").move_to(cover)
            cover.add(label)
            covers.add(cover)
            cover_labels.add(label)

        # Shuffle them up and add labels
        indices = list(range(1, 25))
        # random.shuffle(indices)
        indices = [0, *indices]

        for n, cover in enumerate(covers):
            cover.save_state()
            cover.move_to(thumbnails[indices[n]])
            label = Integer(indices[n] + 1, font_size=60)
            label.set_height(0.6 * cover.get_height())
            label.move_to(cover)
            label.set_fill(WHITE)
            label.set_backstroke(BLACK, 7)
            cover[-1].become(label)
        cover_labels.set_stroke(background=True)

        # Show entries
        self.play(LaggedStart(*(
            FadeIn(covers[indices.index(n)])
            for n in range(len(indices))
        ), run_time=4, lag_ratio=0.1))

        self.wait()
        cover_labels.set_backstroke(BLACK, 12)

        # Highlight one
        fave = Text("(My personal\nFavorite)")
        fave.replace(framed_thumbnails[23], dim_to_match=0)
        fave.scale(0.8)
        fave.set_backstroke(BLACK, 3)

        self.play(FadeOut(cover_labels), FadeIn(fave))
        self.wait()
        self.play(FadeOut(fave), FadeIn(cover_labels))

        # Reveal first
        self.reveal(framed_thumbnails[0], names[0], covers[0])
        self.wait()

        # Shuffle remaining
        for cover in covers:
            cover.saved_state[-1].set_opacity(0)

        self.play(LaggedStart(*(
            Restore(cover, path_arc=30 * DEGREES)
            for cover in covers[1:]
        )), lag_ratio=0.01, run_time=2)

        # Reveal one by one
        for image, name, cover in list(zip(framed_thumbnails, names, covers))[1:]:
            self.reveal(image, name, cover)

        # Reveal winners
        winners = [
            "The Mathematics of String Art",
            "Minimal Surfaces & the Calculus of Variations",
            "Rethinking the real line",
            "Pixel Art Anti Aliasing",
            "How Computers Use Numbers",
        ]

        winner_ftns = Group(*(
            framed_thumbnails[names.index(winner)]
            for winner in winners
        ))
        to_fade = Group(*(
            ftn
            for ftn in framed_thumbnails
            if ftn not in winner_ftns
        ))
        winner_ftns.target = winner_ftns.generate_target()
        winner_ftns.target.scale(2)
        winner_ftns.target.arrange_in_grid(2, 3, h_buff=0.5, v_buff=1.5)
        winner_ftns.target[3:].match_x(winner_ftns.target[:3])
        winner_ftns.target.set_width(FRAME_WIDTH - 1)
        winner_ftns.target.to_edge(DOWN)
        for ftn in winner_ftns.target:
            ftn.scale(0.5)

        self.play(FadeOut(to_fade, lag_ratio=0.1, run_time=2))
        self.play(MoveToTarget(winner_ftns, run_time=2))
        self.wait()

        # Add winner names
        winner_names = VGroup(*(
            Text(name, font_size=36)
            for name in [
                "The Mathematics\nof String Art",
                "Minimal Surfaces & \n Calculus of Variations",
                "Rethinking the\nReal Line",
                "Pixel Art\nAnti-aliasing",
                "How Computers\nUse Numbers",
            ]
        ))
        for name, ftn in zip(winner_names, winner_ftns):
            ftn.target = ftn.generate_target()
            ftn.target.scale(2)
            name.next_to(ftn.target, UP)
            self.play(
                FadeIn(name, lag_ratio=0.1),
                MoveToTarget(ftn),
            )
            self.wait()

    def reveal(self, image, name, cover):
        fade_rect = FullScreenRectangle()
        fade_rect.set_fill(BLACK, opacity=0)
        image.save_state()
        title = Text(name, font_size=60)
        title.set_max_width(FRAME_WIDTH - 1)
        title.to_edge(UP)

        self.add(fade_rect, image, cover)
        self.play(FadeOut(cover))
        self.remove(cover)
        self.play(
            fade_rect.animate.set_fill(opacity=1.0),
            image.animate.set_height(6).next_to(title, DOWN),
            FadeInFromPoint(title, image.get_top()),
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
            Restore(image),
            FadeOutToPoint(title, image.saved_state.get_top()),
        )
