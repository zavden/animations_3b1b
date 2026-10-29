# ==============================================================================
# Scene:      HeroAndVillain
# Source:     videos/_2018/pi_day.py (lines 552-596)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HeroAndVillain.py HeroAndVillain -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - raster_images/replacement images made by _lib/assets/generated/2018/pi_day/make_pi_day_assets.py (Handmann portrait copy, pixelated/revealed variants, placeholder printed pages)
#
# Notes:
#   Uses MEDIA_DIR (defined in cairo_compat) + file lookup by name in _lib/assets/raster_images.
# ==============================================================================

from manim_imports_ext import *

RESOURCE_DIR = os.path.join(MEDIA_DIR, "3b1b_videos", "π Day 2018", "images")


def get_image(name):
    return ImageMobject(os.path.join(RESOURCE_DIR, name))


class HeroAndVillain(Scene):
    CONFIG = {
        "camera_config" : {
            "background_opacity" : 1,
        } 
    }
    def construct(self):
        good_euler = get_image("Leonhard_Euler_by_Handmann")
        bad_euler_pixelated = get_image("Leonard_Euler_pixelated")
        bad_euler = get_image("Leonard_Euler_revealed")
        pictures = good_euler, bad_euler_pixelated, bad_euler
        for mob in pictures:
            mob.set_height(5)

        good_euler.move_to(FRAME_X_RADIUS*LEFT/2)
        bad_euler.move_to(FRAME_X_RADIUS*RIGHT/2)
        bad_euler_pixelated.move_to(bad_euler)

        good_euler_label = OldTexText("Leonhard Euler")
        good_euler_label.next_to(good_euler, DOWN)
        tau_words = OldTexText("Used 6.2831...")
        tau_words.next_to(good_euler, UP)
        tau_words.set_color(GREEN)

        bad_euler_label = OldTexText("Also Euler...")
        bad_euler_label.next_to(bad_euler, DOWN)
        pi_words = OldTexText("Used 3.1415...")
        pi_words.set_color(RED)
        pi_words.next_to(bad_euler, UP)

        self.play(
            FadeInFromDown(good_euler),
            Write(good_euler_label)
        )
        self.play(LaggedStartMap(FadeIn, tau_words))
        self.wait()
        self.play(FadeInFromDown(bad_euler_pixelated))
        self.play(LaggedStartMap(FadeIn, pi_words))
        self.wait(2)
        self.play(
            FadeIn(bad_euler),
            Write(bad_euler_label),
        )
        self.remove(bad_euler_pixelated)
        self.wait(2)
