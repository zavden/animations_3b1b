# ==============================================================================
# Scene:      HoldUpBarberPoleVideos
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1317-1344)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HoldUpBarberPoleVideos.py HoldUpBarberPoleVideos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject used an absolute path in Grant's Dropbox (PrismThumbnail2, CleanThumbnail, Part2Thumbnail6); changed to the file name (placeholder image in raster_images)
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/PrismThumbnail2.png (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/CleanThumbnail.png (placeholder, make_optics_puzzles_assets.py)
#   - _lib/assets/raster_images/Part2Thumbnail6.png (placeholder, make_optics_puzzles_assets.py)
# ==============================================================================

from manim_imports_ext import *

def get_bordered_thumbnail(path, height=3, stroke_width=3):
    image = ImageMobject(path)
    thumbnail = Group(
        SurroundingRectangle(image, buff=0).set_stroke(WHITE, stroke_width),
        image,
    )
    thumbnail.set_height(height)
    return thumbnail


class HoldUpMainVideo(TeacherStudentsScene):
    def construct(self):
        # Show previous video
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        thumbnail = get_bordered_thumbnail("PrismThumbnail2")
        thumbnail.move_to(self.hold_up_spot, DOWN)

        morty = self.teacher
        self.play(
            morty.change("raise_left_hand"),
            FadeIn(thumbnail, UP),
            self.change_students("happy", "guilty", "erm", look_at=thumbnail),
        )
        self.wait(2)

        # Key points
        key_points = VGroup(
            Text("Key point #1: Phase kicks"),
            Text("Key point #2: Layer oscillations"),
            Text("Key point #3: Resonance"),
        )
        key_points.scale(1.25)
        key_points.set_backstroke(BLACK, 4)
        key_points.to_edge(UP)
        key_points[0].set_fill(BLUE)
        key_points[0].save_state()
        key_points.set_fill(WHITE)
        key_points.scale(0.7)
        key_points.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        key_points.set_y(2).to_edge(RIGHT)
        thumbnail.generate_target()
        thumbnail.target.next_to(key_points, LEFT, buff=0.75)

        self.play(
            MoveToTarget(thumbnail),
            morty.change("raise_right_hand", key_points),
            self.change_students("pondering", "hesitant", "pondering", look_at=thumbnail.target),
            LaggedStartMap(FadeIn, key_points, shift=0.5 * LEFT, lag_ratio=0.5)
        )
        self.wait(2)
        self.play(
            Restore(key_points[0]),
            LaggedStartMap(FadeOut, key_points[1:], shift=DOWN),
            LaggedStartMap(FadeOut, self.pi_creatures, shift=DOWN),
            FadeOut(thumbnail, scale=0.5, shift=DOWN),
        )
        self.wait()


class HoldUpBarberPoleVideos(HoldUpMainVideo):
    def construct(self):
        # Show thumbnails
        # CHANGE: the image lived in Grant's Dropbox (absolute path); now it is looked up by name in raster_images (placeholder)
        folder = ""
        thumbnails = Group(*(
            get_bordered_thumbnail(os.path.join(folder, name), stroke_width=2)
            for name in ["CleanThumbnail", "Part2Thumbnail6"]
        ))
        thumbnails.arrange(RIGHT, buff=1.0)
        thumbnails.set_height(2.5)
        thumbnails.move_to(self.hold_up_spot, DR)

        morty = self.teacher
        self.play(
            morty.change("raise_right_hand", thumbnails),
            LaggedStartMap(FadeIn, thumbnails, shift=0.5 * UP, lag_ratio=0.5),
            self.change_students("maybe", "erm", "happy", look_at=thumbnails),
        )
        self.wait()
        self.play(
            self.change_students("confused", "maybe"),
            morty.animate.look_at(self.students)
        )
        self.wait()
        self.play(
            self.students[2].change("tease", thumbnails)
        )
        self.wait(2)
