# ==============================================================================
# Scene:      Outline
# Source:     videos/_2024/holograms/supplements.py (lines 151-345)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Outline.py Outline -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (HologramProcess.jpg, SimplestHologram.jpg, HologramEquation.png, ZonePlateExposure.png, DotReconstruction.png, MultipleDotHologram.png, DiffractionGrating.png) replaced with regenerable placeholders
#   - Error in the original: `arrow` is not defined in `LaggedStartMap(FadeOut, Group(low_title, low_rect, arrow))`; replaced with `in_arrow, up_arrow`
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/HologramProcess.jpg  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/SimplestHologram.jpg  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/HologramEquation.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/ZonePlateExposure.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/DotReconstruction.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/MultipleDotHologram.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/DiffractionGrating.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
# ==============================================================================

from manim_imports_ext import *

class Outline(InteractiveScene):
    def construct(self):
        # Add top part
        frame = self.frame
        frame.set_y(2)

        background = FullScreenRectangle()
        background.fix_in_frame()
        self.add(background)

        top_outlines = ScreenRectangle().replicate(3)
        top_outlines.arrange(RIGHT, buff=1.5)
        top_outlines.set_width(13)
        top_outlines.set_stroke(WHITE, 2)
        top_outlines.set_fill(BLACK, 1)
        top_outlines.to_edge(UP, buff=LARGE_BUFF)

        top_images = Group(
            ImageMobject("HologramProcess.jpg"),
            ImageMobject("SimplestHologram.jpg"),
            ImageMobject("HologramEquation.png"),
        )
        top_rects = Group(
            Group(outline, image.replace(outline))
            for outline, image in zip(top_outlines, top_images)
        )

        top_titles = VGroup(
            Text("The process"),
            Text("The simplest hologram"),
            Text("The general derivation"),
        )
        top_titles.scale(0.75)

        for rect, title in zip(top_rects, top_titles):
            title.next_to(rect, UP, SMALL_BUFF)
            self.play(
                FadeIn(rect),
                FadeIn(title, 0.25 * UP)
            )
            self.wait()

        # Highlight process
        self.play(
            FadeOut(top_rects[1:]),
            FadeOut(top_titles[1:]),
            frame.animate.set_height(4).move_to(top_rects[0]),
            run_time=2
        )
        self.wait()
        self.play(
            FadeIn(top_rects[1:]),
            FadeIn(top_titles[1:]),
            frame.animate.to_default_state().set_y(2),
            run_time=2
        )

        # Isolation animation
        def isolate(rects, titles, index, faded_opacity=0.15):
            return AnimationGroup(
                *(
                    title.animate.set_opacity(1 if i == index else faded_opacity)
                    for i, title in enumerate(titles)
                ),
                *(
                    rect.animate.set_opacity(1 if i == index else faded_opacity)
                    for i, rect in enumerate(rects)
                ),
            )

        self.play(isolate(top_rects, top_titles, 0))
        self.wait()
        self.play(isolate(top_rects, top_titles, 1))
        self.wait()

        # Break down middle step
        mid_outlines = top_outlines.copy()
        mid_outlines.set_opacity(1)
        mid_outlines.next_to(top_rects, DOWN, buff=1.5)
        outer_lines = VGroup(
            CubicBezier(
                top_rects[1].get_corner(DL),
                top_rects[1].get_corner(DL) + DOWN,
                mid_outlines[0].get_corner(UL) + 2 * UP,
                mid_outlines[0].get_corner(UL),
            ),
            CubicBezier(
                top_rects[1].get_corner(DR),
                top_rects[1].get_corner(DR) + DOWN,
                mid_outlines[2].get_corner(UR) + 2 * UP,
                mid_outlines[2].get_corner(UR),
            ),
        )
        mid_images = Group(
            ImageMobject("ZonePlateExposure"),
            ImageMobject("DotReconstruction"),
            ImageMobject("MultipleDotHologram"),
        )

        mid_rects = Group(
            Group(outline, image.replace(outline))
            for outline, image in zip(mid_outlines, mid_images)
        )

        mid_titles = VGroup(
            Text("Exposure pattern"),
            Text("Reconstruction"),
            Text("Added complexity"),
        )
        mid_titles.scale(0.75)
        for rect, title in zip(mid_rects, mid_titles):
            title.next_to(rect, UP, SMALL_BUFF)
            rect.save_state()
            rect.replace(top_rects[1])
            rect.set_opacity(0)

        self.play(
            LaggedStartMap(Restore, mid_rects),
            ShowCreation(outer_lines, lag_ratio=0),
            frame.animate.set_y(0),
            FadeIn(mid_titles, time_span=(1.5, 2.0), lag_ratio=0.025),
            run_time=2
        )
        self.wait()
        for index in range(3):
            self.play(isolate(mid_rects, mid_titles, index))
            self.wait()
        self.play(isolate(mid_rects, mid_titles, 0))
        self.wait()

        # Minilesson
        low_outline = mid_outlines[1].copy()
        low_outline.next_to(mid_rects[1], DOWN, buff=1.5)

        low_image = ImageMobject("DiffractionGrating")
        low_image.replace(low_outline)
        low_rect = Group(low_outline, low_image)
        low_rect.shift(1.5 * LEFT)

        in_arrow = Arrow(mid_rects[0].get_bottom() + LEFT, low_rect.get_left(), path_arc=PI / 2, thickness=5, buff=0.15)
        up_arrow = Arrow(low_rect, mid_rects[1], thickness=5, buff=0.15)

        low_title = Text("Mini-lesson on\nDiffraction Gratings")
        low_title.next_to(low_rect, DOWN)

        self.play(
            frame.animate.set_y(-4),
            FadeIn(low_rect, DOWN),
            FadeIn(low_title, DOWN),
            GrowArrow(in_arrow),
            run_time=2
        )
        self.play(GrowArrow(up_arrow))
        self.wait()

        # Zoom in on mini-lesson
        frame.save_state()
        self.play(
            frame.animate.set_height(4).move_to(Group(low_rect, low_title)),
            FadeOut(VGroup(in_arrow, up_arrow)),
            run_time=2,
        )
        self.wait()
        self.play(
            Restore(frame),
            FadeIn(VGroup(in_arrow, up_arrow)),
            run_time=2
        )
        self.wait()

        # Back to the middle
        self.play(
            # CHANGE: `arrow` does not exist in the original (left over from an earlier version); the two arrows, in_arrow and up_arrow, are removed
            LaggedStartMap(FadeOut, Group(low_title, low_rect, in_arrow, up_arrow), lag_ratio=0.1, run_time=1),
            frame.animate.set_y(0).set_anim_args(run_time=2),
        )
        self.wait()
        self.play(isolate(mid_rects, mid_titles, 2))
        self.wait()

        # Back to the top
        self.play(
            LaggedStart(
                (mid_rect.animate.replace(top_rects[1]).set_opacity(0)
                for mid_rect in mid_rects),
                lag_ratio=0.05,
                group_type=Group
            ),
            FadeOut(mid_titles),
            Uncreate(outer_lines, lag_ratio=0),
            frame.animate.set_y(2),
            run_time=2
        )
        self.wait()
        self.play(isolate(top_rects, top_titles, 2))
        self.wait()
