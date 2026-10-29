# ==============================================================================
# Scene:      HumanitysLastStand
# Source:     videos/_2026/2025_P6/p6.py (lines 4338-4405)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HumanitysLastStand.py HumanitysLastStand -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/AI Evolution Timeline images/alphago.png  (placeholder: AlphaGo vs Lee Sedol (900x600))
#   - _lib/assets/raster_images/AI Evolution Timeline images/dota.png  (placeholder: OpenAI Five vs Dota 2 champions (960x540))
#   - _lib/assets/raster_images/AI Evolution Timeline images/gpt.png  (placeholder: GPT-3 (800x600))
#   - _lib/assets/raster_images/AI Evolution Timeline images/sedol.jpg  (placeholder: Lee Sedol (800x1000))
#
# Notes:
#   The 4 images in 'AI Evolution Timeline images/' are placeholders (Grant's Dropbox) and are in _lib/assets/raster_images/AI Evolution Timeline images/, found by relative name without changing code. IMO_logo: the code asks for 'IMO_logo' (case does not matter on macOS) and the actual file in the repo is imo_logo.png; _lib/manim_imports_ext.py retries the lookup ignoring case, so the real logo is used.
# ==============================================================================

from PIL import Image
import tempfile
import os
from manim_imports_ext import *

_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)


_source_array_cache = {}  # source_path -> float64 rgb(a) array, decoded once per source


def desaturate_from_source(source_path: str, alpha: float, position_ref: ImageMobject) -> ImageMobject:
    alpha = round(float(np.clip(alpha, 0.0, 1.0)), 2)

    if source_path not in _source_array_cache:
        _source_array_cache[source_path] = np.array(Image.open(source_path)).astype(np.float64)
    arr = _source_array_cache[source_path]

    has_alpha_channel = arr.shape[-1] == 4
    rgb = arr[..., :3]
    gray = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    gray_rgb = np.stack([gray, gray, gray], axis=-1)
    blended_rgb = (1 - alpha) * rgb + alpha * gray_rgb
    blended = (
        np.concatenate([blended_rgb, arr[..., 3:4]], axis=-1)
        if has_alpha_channel else blended_rgb
    )
    blended = np.clip(blended, 0, 255).astype(np.uint8)

    base_name = os.path.splitext(os.path.basename(source_path))[0]
    out_path = os.path.join(_desaturate_cache_dir, f"{base_name}_{alpha:.2f}.png")
    if not os.path.exists(out_path):
        Image.fromarray(blended).save(out_path)

    new_image_mobject = ImageMobject(out_path)
    new_image_mobject.replace(position_ref)
    return new_image_mobject


class Timeline(Group):
    def __init__(self, start_year, end_year, initial_year, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_year = start_year
        self.end_year = end_year
        self.number_line = NumberLine(
            x_range=(self.start_year, self.end_year, 1 / 12),
            unit_size=2.6,
            tick_size=0.1,
            longer_tick_multiple=2,
            big_tick_spacing=1
        )
        self.add(self.number_line)
        self.year_labels = self.number_line.add_numbers(
            range(self.start_year, self.end_year),
            group_with_commas=False,
        )

        def update_year_label(label):
            year = label.get_value()
            label.next_to(self.number_line.n2p(year), DOWN, 0.4)
            focal_value = np.exp(-0.1 * label.get_x()**2)
            label.set_height(0.25 + 0.25 * focal_value, about_edge=UP)
            label.set_fill(opacity=(0.5 + 0.5 * focal_value), color=interpolate_color(WHITE, YELLOW, focal_value**2))
        for label in self.year_labels:
            label.add_updater(update_year_label)

        self.images = Group()
        self.add(self.images)
        self._image_entries = []
        self.images.add_updater(self._refresh_images)

        self.center().set_y(-2)
        self.year_tracker = ValueTracker(initial_year)
        self.add_updater(
            lambda tl: tl.shift(tl.number_line.n2p(tl.year_tracker.get_value())[0] * LEFT)
        )

        self.markers = Group()

    def _refresh_images(self, images_group):
        for entry in self._image_entries:
            img = entry["current"]
            focal_value = np.exp(-0.1 * img.get_x() ** 2)
            new_img = desaturate_from_source(entry["source_path"], 1 - focal_value**2, img)
            new_img.set_width(1.6 + focal_value**0.7 * 2.35, about_edge=DOWN)
            new_img.set_opacity(focal_value**0.5)
            images_group.remove(img)
            images_group.add(new_img)
            entry["current"] = new_img

    def add_image(self, file_path, year):
        image = ImageMobject(file_path).align_to(DOWN, DOWN).set_x(self.number_line.n2p(year)[0])
        self.images.add(image)
        self._image_entries.append({"current": image, "source_path": image.image_path})
        self._refresh_images(self.images)  # avoid a 1-frame flash of the raw original

    def center_on_year(self, year):
        return self.shift(self.number_line.n2p(year)[0] * LEFT)

    def get_year_label(self, year):
        return self.year_labels[year - self.start_year]

    def get_marker(self, marker_text, year, image, font_size=60, shift=0, image_position=UP, image_shift=0):
        text = TexText(marker_text, font_size=font_size).next_to(self.number_line.n2p(year), UP).shift(UP * 2.5 + shift)
        ul = Underline(text)
        heading = VGroup(text, ul)
        image.next_to(heading, image_position).shift(image_shift)

        dot = Dot(radius=0.12).move_to(self.number_line.n2p(year)).set_z_index(1)
        line = Line(dot.get_center(), ul.get_center(), buff=0, stroke_width=3)

        marker = Group(dot, line, heading, image)
        marker.create = AnimationGroup(
            AnimationGroup(
                FadeIn(dot),
                ShowCreation(line),
                Write(text),
                GrowFromPoint(ul, ul.get_left()), lag_ratio=0.2),
            FadeIn(image, shift=image_position * 0.2), lag_ratio=0.5)
        marker.year_tracker = ValueTracker(year)
        marker.add_updater(lambda m: m.shift(self.number_line.n2p(m.year_tracker.get_value()) - dot.get_center()))
        self.markers.add(marker)

        marker.text = text
        marker.ul = ul
        marker.heading = heading
        marker.image = image
        marker.dot = dot
        marker.line = line

        return marker


class HumanitysLastStand(InteractiveScene):
    def construct(self):
        # Add the timeline
        timeline = Timeline(2010, 2040, 2030.7).set_y(-3)
        self.add(timeline)

        # Add impressive results in games and natural language
        alphago_marker = timeline.get_marker(
            R"AlphaGo beats Lee Sedol \\ every game except game 4 (of 5)",
            2016 + 3 / 12 + 15 / 365,
            ImageMobject("AI Evolution Timeline images/alphago.png").set_height(2),
            shift=UP * 2.3 + RIGHT * 3,
            image_position=RIGHT
        )
        alphago_marker.text["game 4"].set_color(GREEN)
        dota_marker = timeline.get_marker(
            "OpenAI 5 beats Dota 2 champs",
            2019 + 4 / 12 + 15 / 365,
            ImageMobject("AI Evolution Timeline images/dota.png").set_height(2),
            shift=UP * 0.5 + RIGHT * 2,
            image_position=RIGHT,
            image_shift=UP * 0.3
        )
        gpt_marker = timeline.get_marker(
            "GPT-3 released",
            2020 + 5 / 12 + 29 / 365,
            ImageMobject("AI Evolution Timeline images/gpt.png").set_height(2),
            shift=DOWN * 1.3 + RIGHT * 2.6,
            image_position=RIGHT,
            image_shift=DOWN * 0.2
        )
        self.add(alphago_marker, dota_marker, gpt_marker)

        # Add imo marker and shift the camera back
        imo_marker = timeline.get_marker(
            "IMO Gold?",
            2030.7,
            ImageMobject("IMO_logo").set_height(2),
            shift=UP + RIGHT * 0.3
        )
        self.add(imo_marker)
        self.camera.frame.scale(2, about_point=[0, timeline.get_y(), 0]).shift(RIGHT * 11)
        self.camera.frame.save_state()
        self.camera.frame.scale(0.7, about_point=[0, timeline.get_y(), 0]).shift(LEFT * 14)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    imo_marker.year_tracker.animate.set_value(2026.6),
                    timeline.year_tracker.animate.set_value(2016),
                    self.camera.frame.animate.restore()
                ),
                FadeOut(Group(dota_marker, gpt_marker)), lag_ratio=0.6), run_time=6)

        # Show the game
        alphago_marker.image.generate_target()
        alphago_marker.image.target.scale(2)
        vs = TexText("VS", font_size=100)
        sedol_image = ImageMobject("AI Evolution Timeline images/sedol.jpg").set_height(5)
        Group(sedol_image, vs, alphago_marker.image.target).arrange(buff=0.5).next_to(alphago_marker.text, UP, buff=1.3)

        self.play(
            AnimationGroup(
                FadeIn(sedol_image, shift=RIGHT),
                Write(vs),
                MoveToTarget(alphago_marker.image, path_arc=PI * 0.3),
                lag_ratio=0.1
            )
        )
