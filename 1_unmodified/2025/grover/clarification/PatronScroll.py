# ==============================================================================
# Scene:      PatronScroll
# Source:     videos/_2025/grover/clarification.py (lines 1475-1476)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl PatronScroll.py PatronScroll -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/qc_supplements.py -----

class PatronScroll(PatreonEndScreen):
    def construct(self):
        # Title
        title = Text("Special thanks to\nthese supporters")
        title.to_corner(UR).shift(LEFT)
        title.set_color(BLUE)
        underline = Underline(title)
        rect = BackgroundRectangle(VGroup(title, underline))
        rect.set_fill(BLACK, 1)
        rect.scale(2, about_edge=DOWN)

        morty = Mortimer(height=1)
        morty.next_to(title, LEFT)
        morty.flip()

        for mob in rect, title, underline, morty:
            mob.fix_in_frame()
            self.add(mob)

        # Names
        names = self.get_names()
        name_mobs = VGroup(Text(name) for name in names)
        name_mobs.scale(0.5)
        for mob in name_mobs:
            mob.set_max_width(4)
        name_mobs.arrange(DOWN, aligned_edge=LEFT)
        name_mobs.next_to(underline.get_left(), DR).shift(0.5 * RIGHT)
        name_mobs.set_z_index(-1)

        self.add(name_mobs)

        # Scroll
        frame = self.frame
        dist = - name_mobs.get_y(DOWN) - 1
        total_time = 37
        velocity = dist / total_time
        frame.clear_updaters()
        frame.add_updater(lambda m, dt: m.shift(velocity * dt * DOWN))

        self.play(morty.change("gracious", name_mobs).fix_in_frame())
        for x in range(total_time):
            if random.random() < 0.15:
                self.play(Blink(morty))
            else:
                self.wait()



# ----- From _2025/grover/clarification.py -----

class PatronScroll(PatreonEndScreen):
    pass
