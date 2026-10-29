# ==============================================================================
# Scene:      TileToDoughnut
# Source:     videos/_2026/print_gallery/exponential.py (lines 3506-3549)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TileToDoughnut.py TileToDoughnut -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_texture_folder() points to a 'textures' folder next to the file (the Dropbox path of Grant does not exist)
#   - The PrintGalleryLog/PiHouseLog(Small) textures are procedural placeholder images: periodic strips with picture frames / houses with pi creatures (_lib/assets/generated/2026/print_gallery/make_print_gallery_assets.py)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/print_gallery/textures/PrintGalleryLog.png
#   - _lib/assets/generated/2026/print_gallery/textures/PiHouseLog.png
#   - _lib/assets/generated/2026/print_gallery/textures/PiHouseLogSmall.png
#
# Notes:
#   The original images (the rectified 'Print Gallery' lithograph and the 'pi house') are private. Placeholder strips were generated with make_print_gallery_assets.py: they are periodic on both axes and have square cells in (log r, theta) space, with ln(scale):TAU proportion, so after exp or the Droste zoom the ring and sector structure is visible; it is not Escher's work.
# ==============================================================================

from manim_imports_ext import *

def get_texture_folder():
    # CHANGE: the textures lived in Grant's Dropbox; now they are in the "textures" folder next to
    # this file (procedurally generated placeholder images).
    return Path(__file__).parent / "textures"


def get_print_gallery_log_image_path():
    return Path(get_texture_folder(), "PrintGalleryLog.png")


class TileToDoughnut(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        file = get_print_gallery_log_image_path()
        tile = TexturedSurface(Square3D(resolution=(101, 101)), file)
        tile.set_shape(math.log(256), TAU).center()
        tiles = tile.get_grid(11, 11, buff=0)
        tiles.set_opacity(0.8)
        borders = VGroup(
            SurroundingRectangle(piece, buff=0)
            for piece in tiles
        )
        borders.set_stroke(RED, 1)
        tile.shift(1e-2 * OUT)

        def uv_func(u: float, v: float) -> np.ndarray:
            r1 = 2
            r2 = 1
            P = np.array([math.cos(v), math.sin(v), 0])
            return (r1 - r2 * math.cos(u)) * P - r2 * math.sin(u) * OUT

        torus = TexturedSurface(
            ParametricSurface(uv_func, resolution=(101, 101), u_range=(0, TAU), v_range=(0, TAU)),
            file
        )
        torus.set_z(3)

        frame.set_height(12)
        self.add(tiles, borders)
        self.play(
            tiles.animate.set_opacity(0.5),
            FadeIn(tile)
        )
        self.play(
            tiles.animate.set_opacity(0.5).set_anim_args(run_time=4),
            ReplacementTransform(tile, torus, time_span=(1, 5)),
            frame.animate.reorient(16, 45, 0, (0.01, 0.08, 0.14), 13.11).set_anim_args(run_time=6),
        )
        self.play(
            frame.animate.reorient(-39, 47, 0, (0.01, 0.08, 0.14), 13.11),
            run_time=8
        )
        self.wait()
