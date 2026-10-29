# ==============================================================================
# Scene:      NoteThe256
# Source:     videos/_2026/print_gallery/exponential.py (lines 188-233)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NoteThe256.py NoteThe256 -w -m --fps 15
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


class NoteThe256(InteractiveScene):
    def construct(self):
        # Set up Droste
        frame = self.frame
        droste_image = get_rectified_print_gallery()
        droste_image.scale(256).center()

        drost_image_ghost = droste_image.copy().set_opacity(0.3)

        frame_exp_tracker = ValueTracker(0)
        box_exp_tracker = ValueTracker(0)
        frame.add_updater(lambda m: m.set_height(FRAME_HEIGHT * np.exp(-frame_exp_tracker.get_value())))

        box = ScreenRectangle()
        box.set_height(FRAME_HEIGHT)
        box.set_stroke(RED, 4)
        droste_image.always.clip_to_box(box)

        self.add(drost_image_ghost, droste_image)
        self.wait()

        # Set up box label
        box_label = Tex(R"\times 256.0")
        dec = box_label.make_number_changeable("256.0", font_size=72)

        def get_scale_factor():
            return np.exp(box_exp_tracker.get_value())

        def update_box_label(box_label):
            box_label[1].set_value(np.exp(box_exp_tracker.get_value()))
            box_label.set_width(box.get_width() * 0.5)
            box_label.next_to(box, UP, buff=0.1 * box.get_height())

        box_label.add_updater(update_box_label)
        dec.f_always.set_value(get_scale_factor)
        box.add_updater(lambda m: m.set_height((1 / get_scale_factor()) * FRAME_HEIGHT))

        box_exp_tracker.set_value(0)
        self.add(box, box_label, droste_image)
        self.play(
            box_exp_tracker.animate.set_value(math.log(256)).set_anim_args(time_span=(0, 10)),
            frame_exp_tracker.animate.set_value(math.log(256) - 1.5).set_anim_args(time_span=(4, 12)),
        )
        self.wait()
        self.play(frame_exp_tracker.animate.set_value(0), run_time=2)
        self.wait()
