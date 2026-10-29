# ==============================================================================
# Scene:      ZoomWithColors
# Source:     videos/_2026/print_gallery/exponential.py (lines 132-185)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ZoomWithColors.py ZoomWithColors -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_texture_folder() points to a 'textures' folder next to the file (the Dropbox path of Grant does not exist)
#   - The PrintGalleryLog/PiHouseLog(Small) textures are procedural placeholder images: periodic strips with picture frames / houses with pi creatures (_lib/assets/generated/2026/print_gallery/make_print_gallery_assets.py)
#   - Paul's outlines (person, frame, building, arcade) are read from the 'outlines' folder next to the file; they are placeholder outlines that do not match the placeholder image
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/print_gallery/textures/PrintGalleryLog.png
#   - _lib/assets/generated/2026/print_gallery/textures/PiHouseLog.png
#   - _lib/assets/generated/2026/print_gallery/textures/PiHouseLogSmall.png
#   - _lib/assets/generated/2026/print_gallery/outlines/PersonOutline.png
#   - _lib/assets/generated/2026/print_gallery/outlines/PersonMask.png
#   - _lib/assets/generated/2026/print_gallery/outlines/Frame.png
#   - _lib/assets/generated/2026/print_gallery/outlines/Building.png
#   - _lib/assets/generated/2026/print_gallery/outlines/Arcade.png
#
# Notes:
#   The original images (the rectified 'Print Gallery' lithograph and the 'pi house') are private. Placeholder strips were generated with make_print_gallery_assets.py: they are periodic on both axes and have square cells in (log r, theta) space, with ln(scale):TAU proportion, so after exp or the Droste zoom the ring and sector structure is visible; it is not Escher's work. The ZoomWithColors outlines (person/frame/building/arcade silhouettes) are also placeholders and are placed at the original's coordinates, but they do not match the placeholder paintings.
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


class ZoomWithColors(InteractiveScene):
    def construct(self):
        # Add Droste image and zoom in two iterations
        droste_image = get_rectified_print_gallery()
        droste_image.scale(256).center()
        droste_image.set_opacity(0.25)
        self.disable_interaction(droste_image)
        self.add(droste_image)

        exp_tracker = ValueTracker(0.5)
        frame = self.frame
        frame.add_updater(lambda m: m.set_height(FRAME_HEIGHT * np.exp(exp_tracker.get_value())))

        dec = DecimalNumber()
        dec.fix_in_frame()
        dec.to_corner(DL)
        dec.f_always.set_value(exp_tracker.get_value)

        # Add outlines
        # CHANGE: Paul's outlines lived in Grant's Dropbox; now they are in the "outlines" folder
        # next to this file (procedurally generated placeholder outlines).
        root = Path(__file__).parent / "outlines"
        person_outline, person_mask, frame, building, arcade = images = Group(
            ImageMobject(str(Path(root, name + ".png")))
            for name in ["PersonOutline", "PersonMask", "Frame", "Building", "Arcade"]
        )
        person = Group(
            person_mask.set_opacity(0.2),
            person_outline,
        )
        person.set_height(8.8).move_to(np.array([-2.41928692, -5.89659999, 0.]))
        frame.set_height(7.599240).move_to(np.array([-0.65032366, -0.76692351, 0.]))
        building.set_height(1.2807975113391876).move_to(np.array([-0.75733024, 0.36813092, 0.]))
        arcade.set_height(0.24800574034452438).move_to(np.array([0.0865169, 0.01073422, 0.]))
        small_person = person.copy().scale(1 / 256, about_point=ORIGIN)

        self.add(frame)
        self.add(person)
        self.add(building)
        self.add(arcade)
        self.add(small_person)

        # Test
        exp_tracker.set_value(1)
        self.play(
            exp_tracker.animate.set_value(1 - 1 * math.log(256)).set_anim_args(rate_func=linear),
            FadeOut(person, time_span=(0, 2)),
            FadeIn(frame, time_span=(0, 5), rate_func=there_and_back_with_pause),
            FadeIn(building, time_span=(3, 10), rate_func=there_and_back_with_pause),
            FadeIn(arcade, time_span=(7, 12), rate_func=there_and_back_with_pause),
            FadeIn(small_person, time_span=(9, 12)),
            run_time=12
        )
