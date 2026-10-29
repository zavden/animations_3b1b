# ==============================================================================
# Scene:      PiLookingAtPhone
# Source:     videos/outside_videos/short_links.py (lines 68-89)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PiLookingAtPhone.py PiLookingAtPhone -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - Placeholder iPhone.svg (phone silhouette) in _lib/assets/svg_images/ (make_short_links_assets.py); the code finds it by name, unchanged
# ==============================================================================

from manim_imports_ext import *

def get_vertical_screen():
    screen = Rectangle(width=FRAME_HEIGHT * (9 / 16), height=FRAME_HEIGHT)
    screen.center()
    return screen


class PiLookingAtPhone(InteractiveScene):
    def construct(self):
        # Test
        screen = get_vertical_screen()
        # self.add(screen)

        randy = Randolph(height=2)
        randy.move_to(screen, LEFT)
        randy.shift(DOWN + 0.2 * RIGHT)
        phone = SVGMobject("iPhone")
        phone.set_height(3)
        phone.stretch(1.2, 0)
        phone.set_fill(GREY_A)
        phone.next_to(randy.get_corner(UR), RIGHT)

        self.add(randy)
        self.add(phone)

        for mode in ["pondering", "confused", "maybe", "tease"]:
            self.play(randy.change(mode, phone))
            self.play(Blink(randy))
            self.wait()
