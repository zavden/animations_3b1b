# ==============================================================================
# Scene:      PrintGalleryZoomStages
# Source:     videos/_2026/print_gallery/exponential.py (lines 102-129)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PrintGalleryZoomStages.py PrintGalleryZoomStages -w -m --fps 15
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


def get_log_image(log_image_path, scale_factor, resolution=(51, 101)):
    log_image = TexturedSurface(
        Square3D(resolution=resolution),
        log_image_path,
    )
    log_image.set_shading(0, 0, 0)
    log_image.deactivate_depth_test()
    log_image.set_shape(math.log(scale_factor), TAU)
    return log_image


def get_droste_from_log_image_path(log_image_path, scale_factor=256, n_iterations=5, height=7.5):
    log_image = get_log_image(log_image_path, scale_factor)
    log_images = log_image.get_grid(1, n_iterations, buff=0)
    log_images.move_to(ORIGIN, DR)
    log_images.apply_complex_function(np.exp)
    log_images.set_height(height)
    return log_images


def get_rectified_print_gallery(**kwargs):
    return get_droste_from_log_image_path(get_print_gallery_log_image_path(), **kwargs)


class PrintGalleryZoomStages(InteractiveScene):
    def construct(self):
        # Add Droste image and zoom in two iterations
        droste_image = get_rectified_print_gallery()
        droste_image.scale(256).center()
        self.add(droste_image)

        exp_tracker = ValueTracker(0)
        frame = self.frame
        frame.add_updater(lambda m: m.set_height(FRAME_HEIGHT * np.exp(exp_tracker.get_value())))

        dec = DecimalNumber()
        dec.fix_in_frame()
        dec.to_corner(DL)
        dec.f_always.set_value(exp_tracker.get_value)

        exp_tracker.set_value(0.5)
        self.wait()
        for value in [-0.5, -1.87, -3.86, -5.0]:
            self.play(exp_tracker.animate.set_value(value), run_time=2)
            self.wait()

        # Full zoom
        exp_tracker.set_value(-5 + math.log(256))
        self.play(
            exp_tracker.animate.set_value(-5),
            run_time=10
        )
