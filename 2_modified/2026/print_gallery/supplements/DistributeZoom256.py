# ==============================================================================
# Scene:      DistributeZoom256
# Source:     videos/_2026/print_gallery/supplements.py (lines 269-354)
# Category:   2 · Renders with modifications
# Includes code copied from: _2026/print_gallery/exponential.py
#
# Run from this folder:
#     manimgl DistributeZoom256.py DistributeZoom256 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_texture_folder() points to a 'textures' folder next to the file (the Dropbox path of Grant does not exist)
#   - PrintGalleryLog.png is a placeholder image (periodic strip with picture frames)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2026/print_gallery/textures/PrintGalleryLog.png
#
# Notes:
#   The original images (the rectified 'Print Gallery' lithograph and LogImage) are private. Placeholder images were generated with _lib/assets/generated/2026/print_gallery/make_print_gallery_assets.py: periodic strips with picture frames, with square cells in (log r, theta) space; after exp / Droste zoom the ring and sector structure is visible. It is not Escher's work.
# ==============================================================================

from manim_imports_ext import *


# ----- From _2026/print_gallery/exponential.py -----

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



# ----- From _2026/print_gallery/supplements.py -----

class DistributeZoom256(InteractiveScene):
    def construct(self):
        # Add frames
        frames = Square(side_length=6).replicate(2)
        frames.arrange(RIGHT, buff=1.5)
        frames.set_stroke(WHITE, 2)
        frames.set_fill(BLACK, 0)
        left_frame, right_frame = frames
        left_frame.set_stroke(BLACK)
        right_frame.set_stroke(opacity=0)

        self.add(left_frame)

        # Add droste
        droste_image = get_rectified_print_gallery()
        droste_image.scale(175)
        droste_image.move_to(left_frame)
        droste_image.clip_to_box(left_frame)

        droste_image_ghost = droste_image.copy()
        droste_image_ghost.set_opacity(0.5)

        self.add(droste_image_ghost, Point(), droste_image)

        # Add zoom arrows
        small_left = left_frame.copy()
        small_left.scale(1 / 256)
        corner_arrows = VGroup(
            Arrow(
                left_frame.get_corner(vect),
                small_left.get_corner(vect),
                buff=0.1,
                thickness=8
            )
            for vect in compass_directions(4, DL)
        )
        corner_arrows.set_color(TEAL)
        zoom_label = Tex(R"\times 256", font_size=72)
        zoom_label.move_to(corner_arrows[:2])

        self.play(
            *map(GrowArrow, corner_arrows),
            Transform(left_frame, small_left),
            Write(zoom_label),
            droste_image.animate.clip_to_box(small_left),
            run_time=2
        )
        self.wait()

        # Distributed
        top_equation = Tex(R"256 = 4 \times 4 \times 4 \times 4")
        top_equation.to_edge(UP, buff=0.25)

        corner_squares = Square(side_length=2).replicate(4)
        for corner, square in zip(compass_directions(4, DL), corner_squares):
            square.move_to(right_frame, corner)

        rot_arrows = VGroup(
            Arrow(s2, s1, buff=0.1, thickness=5, fill_color=TEAL)
            for s1, s2 in adjacent_pairs(corner_squares)
        )

        two_x_labels = VGroup(
            Tex(R"\times 4").next_to(arrow, np.round(rotate_vector(arrow.get_vector(), 90 * DEG)), buff=0)
            for arrow in rot_arrows
        )

        corner_arrow_ghosts = corner_arrows.copy().set_fill(opacity=0.35)
        zoom_label_ghost = zoom_label.copy().set_fill(opacity=0.35)

        self.play(
            Write(top_equation[3:]),
            TransformFromCopy(zoom_label["256"], top_equation["256"]),
            run_time=1
        )
        self.play(
            small_left.animate.set_stroke(opacity=0.35),
            FadeIn(right_frame),
            TransformFromCopy(corner_arrows, rot_arrows),
            *(
                FadeTransform(zoom_label.copy(), two_x_label)
                for two_x_label in two_x_labels
            ),
            run_time=2
        )
        self.wait()
