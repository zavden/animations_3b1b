# ==============================================================================
# Scene:      RevealingTiles
# Source:     videos/_2021/some1_winners.py (lines 484-661)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RevealingTiles.py RevealingTiles -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - LaggedStartMap(Anim, group, arg_creator, ...): the third argument `arg_creator` no longer exists; a lambda m: Anim(m, ...) is passed as anim_func.
#
# Placeholder assets (not Grant's originals):
#   - raster_images/some1_thumbnails/<slug>.jpg: 90 placeholder thumbnails (30 WINNERS/HONORABLE_MENTIONS videos with their title and author + 60 synthetic entries) in _lib/assets/ (make_some1_assets.py); the scene would download them from YouTube with urllib
# ==============================================================================

from manim_imports_ext import *
from manimlib.logger import log
import urllib.request

WINNERS = [
    ("That weird light at the bottom of a mug — ENVELOPES", "Paralogical", "fJWnA4j0_ho"),
    ("Hiding Images in Plain Sight: The Physics Of Magic Windows", "Matt Ferraro", "CatInCausticImage"),
    ("The Beauty of Bézier Curves", "Freya Holmér", "aVwxzDHniEw"),
    ("What Is The Most Complicated Lock Pattern?", "Dr. Zye", "PKjbBQ0PBCQ"),
    ("Pick's theorem: The wrong, amazing proof", "spacematt", "uh-yRNqLpOg"),
]


HONORABLE_MENTIONS = [
    ("Dirac's belt trick, Topology, and Spin ½ particles", "Noah Miller", "ACZC_XEyg9U"),
    ("Galois-Free Guarantee! | The Insolubility of the Quintic", "Carl Turner", "BSHv9Elk1MU"),
    ("The Two Envelope Problem - a Mystifying Probability Paradox", "Formant", "_NGPncypY68"),
    ("The Math Behind Font Rasterization | How it Works", "GamesWithGabe", "LaYPoMPRSlk"),
    ("What is a Spinor?", "Mia Hughes", "SpinorArticle"),
    ("Understanding e", "Veli Peltola", "e_comic"),
    ("Ancient Multiplication Trick", "Inigo Quilez", "CsMrHzp850M"),
    ("对称多项式基本定理自我探究", "凡人忆拾", "FiveIntsTheorem"),
    ("Lehmer Factor Stencils", "Proof of Concept", "QzohwKT6TNA"),
    ("What is the limit of a sequence of graphs?", "Spectral Collective", "7Gj9BH4IZ-4"),
    ("Steiner's Porism: proving a cool animation", "Joseph Newton", "fKAyaP8IzlE"),
    ("Wait, Probabilities can be Negative?!", "Steven G", "std9EBbtOC0"),
    ("This random graph fact will blow your mind", "Snarky Math", "3QjZ31lj974"),
    ("Why is pi here? Estimating π by Buffon's n̶e̶e̶d̶l̶e noodle!", "Mihai Nica", "e-RUyCs9B08"),
    ("Introduction to Waves", "Rob Schlub", "IntroToWaves"),
    ("ComplexFunctions", "Treena", "Treena"),
    ("I spent an entire summer to find this spiral", "Sort of School", "n-e9C8g5x68"),
    ("HACKENBUSH: a window to a new world of math", "Owen Maitzen", "ZYj4NkeGPdM"),
    ("The Tale of the Lights Puzzle", "Throw Math At It", "9aZsABF-Vj4"),
    ("The BEST Way to Find a Random Point in a Circle", "nubDotDev", "4y_nmpv-9lI"),
    ("Secrets of the Fibonacci Tiles", "Eric Severson", "Ct7oltmdJrM"),
    ("The Tale of Three Triangles", "Robin Truax", "5nuYD2M2AX8"),
    ("How Karatsuba's algorithm gave us new ways to multiply", "Nemean", "cCKOl5li6YM"),
    ("Can you change a sum by rearranging its numbers? --- The Riemann Series Theorem", "Morphocular", "U0w0f0PDdPA"),
    ("Neural manifolds - The Geometry of Behaviour", "Artem Kirsanov", "QHj9uVmwA_0"),
]


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


class RevealingTiles(Scene):
    def construct(self):
        self.five_winners()
        self.honorable_mentions()

    def five_winners(self):
        # title = Text("SoME1 Winners", font_size=72)
        title = OldTexText("Summer of Math Exposition\\\\", "Winners", font_size=72)
        title[1].scale(2, about_edge=UP)
        title[1].set_color(YELLOW)
        title.to_edge(UP, buff=0.2)
        # 
        # title.to_edge(UP)
        subtitle = Text("(in no particular order)", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.2)
        subtitle.set_color(GREY_B)

        self.add(title)

        tiles = self.get_mystery_tile().replicate(5)
        colors = color_gradient([BLUE_B, BLUE_D], 5)
        for tile, color in zip(tiles, colors):
            # tile[0].set_stroke(color, 1)
            tile[0].set_stroke(YELLOW, 2)
        tiles.set_height(2)
        tiles.arrange_in_grid(2, 3, buff=MED_SMALL_BUFF)
        tiles[3:].match_x(tiles[:3])
        tiles.set_width(FRAME_WIDTH - 2)
        # tiles.to_edge(DOWN, buff=1)
        tiles.to_edge(DOWN, buff=0.25)

        reorder = list(range(5))
        random.seed(1)
        random.shuffle(reorder)

        # Animations
        self.play(
            Write(title),
            LaggedStartMap(GrowFromCenter, tiles, lag_ratio=0.15)
        )
        self.wait()
        self.play(
            FadeIn(subtitle, lag_ratio=0.2),
            LaggedStart(*(
                ApplyMethod(
                    tile.move_to, tiles[reorder[i]],
                    path_arc=PI / 2
                )
                for i, tile in enumerate(tiles)
            ), lag_ratio=0.25, run_time=2)
        )
        self.wait()

        #
        for tile, triple in zip(tiles, WINNERS):
            self.reveal_tile(tile, *triple)

        self.title = title
        self.subtitle = subtitle
        self.tiles = tiles

    def honorable_mentions(self):
        tiles = self.tiles

        new_title = OldTexText("Others you'll enjoy", font_size=72)
        new_title.to_edge(UP, buff=MED_SMALL_BUFF)

        tiles.generate_target()
        new_tile = self.get_mystery_tile()
        new_tile.replace(tiles[0])
        new_tiles = Group(
            *tiles.target,
            *new_tile.replicate(len(HONORABLE_MENTIONS))
        )
        new_tiles.arrange_in_grid(5, 6, buff=0.25)
        new_tiles.set_height(6.5)
        new_tiles.next_to(new_title, DOWN)

        self.play(
            FadeTransform(self.title, new_title),
            FadeOut(self.subtitle),
            MoveToTarget(tiles),
            # CHANGE: LaggedStartMap no longer has the third argument arg_creator; a lambda is passed as anim_func
            LaggedStartMap(
                lambda m: FadeInFromPoint(m, ORIGIN), new_tiles[5:],
                lag_ratio=0.1,
                run_time=5,
            )
        )
        self.wait()

        reorder_tail = list(range(5, len(new_tiles)))
        random.shuffle(reorder_tail)
        reorder = [*range(5), *reorder_tail]
        centers = [nt.get_center().copy() for nt in new_tiles]
        for i, tile in enumerate(new_tiles):
            tile.move_to(centers[reorder[i]])

        for tile, triple in zip(new_tiles[5:], HONORABLE_MENTIONS):
            self.reveal_tile(tile, *triple)

    def reveal_tile(self, tile, title, author, image_name):
        # Flip tile
        try:
            image_path = get_full_raster_image_path(image_name)
        except IOError:
            # Try to redownload best YT slug
            save_thumbnail_locally(image_name)
            image_path = yt_slug_to_image_file(image_name)
        # Trim to be 16x9
        arr = np.array(Image.open(image_path))
        h, w, _ = arr.shape
        nh = w * 9 // 16
        if nh < h:
            trimmed_arr = arr[(h - nh) // 2:(h - nh) // 2 + nh, :, :]
            Image.fromarray(trimmed_arr).save(image_path)

        image = ImageMobject(image_path)
        image.rotate(PI, RIGHT)
        image.replace(tile, dim_to_match=1)
        image.set_max_width(tile.get_width())

        self.play(
            Rotate(image, PI, RIGHT),
            Rotate(tile, PI, RIGHT),
            UpdateFromAlphaFunc(
                tile, lambda m, a: m.set_opacity(1 if a < 0.5 else 0),
            ),
            UpdateFromAlphaFunc(
                image, lambda m, a: m.set_opacity(0 if a < 0.5 else 1),
            ),
        )
        tile.remove(tile[1])
        tile[0].set_fill(BLACK, 1)
        tile.add(image)

        # Expand
        full_rect = FullScreenRectangle()
        full_rect.set_fill(GREY_E)

        title = Text(title)
        title.set_max_width(FRAME_WIDTH - 1)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        byline = Text(f"by {author}", font_size=30)
        byline.set_color(GREY_B)
        byline.next_to(title, DOWN, buff=0.2)

        tile.save_state()
        tile.generate_target()
        tile.target.set_height(6)
        tile.target.next_to(byline, DOWN)
        tile.saved_state[0].set_stroke(opacity=1)

        self.add(full_rect, tile)
        self.play(
            FadeIn(full_rect),
            MoveToTarget(tile, run_time=2),
            FadeInFromPoint(title, tile.get_top(), run_time=2),
        )
        self.play(FadeIn(byline, 0.25 * DOWN))
        self.wait()
        self.play(
            Restore(tile),
            FadeOut(full_rect),
            FadeOut(title, 0.75 * UP),
            FadeOut(byline, 1.0 * UP),
        )

    def get_mystery_tile(self):
        rect = ScreenRectangle(height=1)
        rect.set_stroke(BLUE_D, 1)
        rect.set_fill(GREY_D, 1)
        q_marks = OldTex("???")
        q_marks.flip().flip()
        q_marks.set_fill(GREY_A)
        q_marks.move_to(rect)
        q_marks.shift(1e-3 * OUT)
        return Group(rect, q_marks)
