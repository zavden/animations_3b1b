# ==============================================================================
# Scene:      CommentFlurry
# Source:     videos/outside_videos/short_links.py (lines 10-44)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CommentFlurry.py CommentFlurry -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - base_folder points to _lib/assets/raster_images/short_links/lower_link (it was a path in Grant's Dropbox)
#
# Placeholder assets (not Grant's originals):
#   - 46 placeholder comment screenshots in _lib/assets/raster_images/short_links/lower_link/<subfolder>/ (make_short_links_assets.py)
# ==============================================================================

from manim_imports_ext import *

def get_vertical_screen():
    screen = Rectangle(width=FRAME_HEIGHT * (9 / 16), height=FRAME_HEIGHT)
    screen.center()
    return screen


class CommentFlurry(InteractiveScene):
    # CHANGE: placeholder comment screenshots in _lib/assets/raster_images/short_links/lower_link (in the original, Grant's Dropbox)
    base_folder = Path(get_directories()["raster_images"], "short_links/lower_link/")
    sub_folder = ""
    random_seed = 4

    def construct(self):
        # Test
        folder = os.path.join(self.base_folder, self.sub_folder)
        images = Group()
        screen = get_vertical_screen()
        files = os.listdir(folder)

        for file in files:
            if not file.endswith(".png"):
                continue
            image = ImageMobject(os.path.join(folder, file))
            image.match_width(screen)
            image.scale(random.uniform(0.6, 0.8))
            image.move_to([
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(-2, 2),
                0
            ])
            images.add(image)

        groups = Group()
        for image in images:
            rect = BackgroundRectangle(image, buff=0.025)
            rect.set_fill(BLACK, 0.75)
            group = Group(rect, image)
            groups.add(group)

        self.play(LaggedStartMap(FadeIn, groups, lag_ratio=0.5, shift=0.25 * UP, run_time=4))

        self.wait()
