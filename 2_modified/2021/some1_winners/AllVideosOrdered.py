# ==============================================================================
# Scene:      AllVideosOrdered
# Source:     videos/_2021/some1_winners.py (lines 428-481)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AllVideosOrdered.py AllVideosOrdered -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - self.camera.release_texture(...) is removed: Camera no longer has that method (the current renderer manages textures).
#
# Placeholder assets (not Grant's originals):
#   - raster_images/some1_thumbnails/<slug>.jpg: 90 placeholder thumbnails (30 WINNERS/HONORABLE_MENTIONS videos with their title and author + 60 synthetic entries) in _lib/assets/ (make_some1_assets.py); the scene would download them from YouTube with urllib
#   - _lib/data/some1_video_urls_ordered.txt: list of the 90 youtu.be URLs (make_some1_assets.py); in the original it was in Grant's data folder
# ==============================================================================

from manim_imports_ext import *
from manimlib.logger import log
import urllib.request

def get_youtube_slugs(file="some1_video_urls.txt"):
    full_path = os.path.join(get_directories()["data"], file)
    slugs = []
    prefix = "https://youtu.be/"
    with open(full_path, "r") as fp:
        for url in fp.readlines():
            if not url.startswith(prefix):
                continue
            slugs.append(url[len(prefix):-1])
    return remove_list_redundancies(slugs)


def save_thumbnail_locally(slug, rewrite=False):
    file = yt_slug_to_image_file(slug)
    if os.path.exists(file) and not rewrite:
        return file
    suffixes = ["maxresdefault", "hqdefault", "mqdefault", "sddefault"]
    urls = [
        *(
            f"https://img.youtube.com/vi/{slug}/{suffix}.jpg"
            for suffix in suffixes
        ),
        *(
            f"https://i.ytimg.com/vi/{slug}/{suffix}.jpg"
            for suffix in suffixes
        )
    ]
    for url in urls:
        try:
            urllib.request.urlretrieve(url, file)
            return file
        except urllib.request.HTTPError:
            pass
    log.warning(f"Thumbnail not found: {slug}")


def yt_slug_to_image_file(slug):
    return os.path.join(
        get_raster_image_dir(),
        "some1_thumbnails",
        slug + ".jpg"
    )


class AllVideosOrdered(Scene):
    slug_file = "some1_video_urls_ordered.txt"
    grid_size = 3
    time_per_image = 0.2

    def construct(self):
        n = self.grid_size
        N = n**2
        time_per_image = self.time_per_image
        buffer_size = 2 * N

        slugs = get_youtube_slugs(self.slug_file)
        random.shuffle(slugs)
        log.info(f"Number of slugs: {len(slugs)}")
        image_slots = ScreenRectangle().get_grid(n, n, buff=0.2)
        image_slots.set_height(FRAME_HEIGHT)
        image_slots.set_stroke(WHITE, 1)

        images = buffer_size * [None]

        self.add(image_slots)

        def update_image(image, dt):
            image.time += dt
            image.set_opacity(clip(5 * image.time / (N * time_per_image), 0, 1))

        k = 0
        for slug in ProgressDisplay(slugs):
            slot = image_slots[k % N]
            save_thumbnail_locally(slug)
            file = yt_slug_to_image_file(slug)
            if not os.path.exists(file):
                continue
            if k > buffer_size:
                old_image = images[k % buffer_size]
                # CHANGE: Camera no longer has release_texture (AttributeError); the texture is managed by the current renderer
                self.remove(old_image)

            image = ImageMobject(file)
            image.replace(slot, stretch=True)

            images[k % buffer_size] = image

            image.time = 0
            image.add_updater(update_image)
            self.add(image)
            self.wait(time_per_image)

            k += 1

            # Hack to keep OpenGL from tracking too many textures.
            # Should be fixed more intelligently in Camera
            if k % (buffer_size) == 0:
                self.camera.n_textures = buffer_size + 2
