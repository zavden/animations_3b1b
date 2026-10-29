# ==============================================================================
# Scene:      ExtractFramesFromFootage
# Source:     videos/_2024/holograms/model.py (lines 7-81)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExtractFramesFromFootage.py ExtractFramesFromFootage -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The private mp4 from Grant's Dropbox was replaced with a placeholder video in _lib/data/2024/holograms/data/
#   - Installed opencv-python-headless (the scene does import cv2)
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/2024/holograms/data/MultiplePOVs.2.mp4  (placeholder video 1080x1080, 16 s, rotating wireframe cube; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#
# Extra packages installed in the venv: opencv-python-headless 5.0.0.93 (--no-deps)
# ==============================================================================

import cv2
from pathlib import Path
from manim_imports_ext import *

class ExtractFramesFromFootage(InteractiveScene):
    # CHANGE: the video from Grant's Dropbox was replaced by a placeholder mp4 in _lib/data (see make_holograms_assets.py)
    video_file = str(Path(get_directories()["data"], "2024/holograms/data/MultiplePOVs.2.mp4"))
    image_dir = "/tmp/"
    frequency = 0.25
    start_time = 0
    end_time = 14
    small_image_size = (1080, 1080)
    n_cols = 8

    def setup(self):
        super().setup()
        # Open the video file
        self.video = cv2.VideoCapture(self.video_file)
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
        self.video_duration = self.video.get(cv2.CAP_PROP_FRAME_COUNT) / self.video_fps

    def tear_down(self):
        super().tear_down()
        self.video.release()

    def construct(self):
        video_box = Square()
        video_box.set_height(4)
        video_box.to_edge(LEFT)
        video_box.set_stroke(WHITE, 0.0)
        self.add(video_box)

        # Collect images
        start_time = self.start_time
        end_time = min(self.end_time, self.video_duration)
        times = np.arange(start_time, end_time, self.frequency)
        images = Group()
        for time in ProgressDisplay(times, desc="Loading images"):
            image = self.image_from_timestamp(time)
            if image is not None:
                border = SurroundingRectangle(image, buff=0)
                border.set_stroke(WHITE, 1)
                images.add(Group(border, image))

        # Show clip extraction
        images.arrange_in_grid(n_cols=self.n_cols, buff=0.1 * images[0].get_width())
        images.set_width(FRAME_WIDTH - video_box.get_width() - 1.5)
        images.to_corner(UR, buff=0.25)
        flash = video_box.copy()
        flash.set_fill(WHITE, 0.25)

        for image in images:
            self.add(image)
            self.play(FadeOut(flash, run_time=self.frequency / 2))
            self.wait(self.frequency / 2)

        # Add still
        still_image = images[-1].copy()
        still_image.replace(video_box)
        self.add(still_image)
        self.wait()

        # Do something to zoom in on example frames

    def image_from_timestamp(self, time):
        video_name = Path(self.video_file).stem
        file_name = Path(self.image_dir, f"{video_name}_{time}.png")

        frame_number = int(time * self.video_fps)
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.video.read()
        if not ret:
            print(f"Failed to capture at {time}")
            return
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        small_image = pil_image.resize(self.small_image_size, Image.LANCZOS)
        small_image.save(file_name)

        return ImageMobject(file_name)
