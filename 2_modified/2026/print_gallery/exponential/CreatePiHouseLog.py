# ==============================================================================
# Scene:      CreatePiHouseLog
# Source:     videos/_2026/print_gallery/exponential.py (lines 236-253)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CreatePiHouseLog.py CreatePiHouseLog -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_texture_folder() points to a 'textures' folder next to the file (the Dropbox path of Grant does not exist)
#   - UltraHighResPiHouse.png is a placeholder image: the Droste (x16) of the PiHouseLog strip computed with numpy
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/print_gallery/textures/UltraHighResPiHouse.png
#
# Notes:
#   The original images (the rectified 'Print Gallery' lithograph and the 'pi house') are private. Placeholder strips were generated with make_print_gallery_assets.py: they are periodic on both axes and have square cells in (log r, theta) space, with ln(scale):TAU proportion, so after exp or the Droste zoom the ring and sector structure is visible; it is not Escher's work.
# ==============================================================================

from manim_imports_ext import *

def get_texture_folder():
    # CHANGE: the textures lived in Grant's Dropbox; now they are in the "textures" folder next to
    # this file (procedurally generated placeholder images).
    return Path(__file__).parent / "textures"


class CreatePiHouseLog(InteractiveScene):
    def construct(self):
        # Read from rectified image as polar coordinates
        piece = TexturedSurface(
            Square3D(resolution=(1000, 1000)),
            Path(get_texture_folder(), "UltraHighResPiHouse.png"),
        )
        piece.set_height(FRAME_HEIGHT)
        piece.set_shading(0, 0, 0)

        def to_polar(u, v):
            z1 = np.exp(complex(-(1 - v) * np.log(16), TAU * u))
            z2 = (z1 + complex(1, 1)) / 2
            return (z2.real, z2.imag)

        piece.set_image_coords_by_uv_func(to_polar)
        piece.set_shape(FRAME_WIDTH, FRAME_HEIGHT)
        self.add(piece)
