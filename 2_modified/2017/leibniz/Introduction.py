# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2017/leibniz.py (lines 170-269)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - typo in the original: radius = YELLOW was meant to be the dot color (a color is not a radius)
#   - Scene.show_frame() opened a preview window in Cairo; nothing to render
# ==============================================================================

from manim_imports_ext import *

class Introduction(PiCreatureScene):
    def construct(self):
        self.introduce_three_objects()
        self.show_screen()

    def introduce_three_objects(self):
        primes = self.get_primes()
        primes.to_corner(UP+RIGHT)
        primes.shift(DOWN)
        plane = self.get_complex_numbers()
        plane.shift(2*LEFT)
        pi_group = self.get_pi_group()
        pi_group.next_to(primes, DOWN, buff = MED_LARGE_BUFF)
        pi_group.shift_onto_screen()

        morty = self.get_primary_pi_creature()
        video = VideoIcon()
        video.set_color(TEAL)
        video.next_to(morty.get_corner(UP+LEFT), UP)

        self.play(
            morty.change_mode, "raise_right_hand",
            DrawBorderThenFill(video)
        )
        self.wait()
        self.play(
            Write(primes, run_time = 2),
            morty.change_mode, "happy",
            video.set_height, FRAME_WIDTH,
            video.center,
            video.set_fill, None, 0
        )
        self.wait()
        self.play(
            Write(plane, run_time = 2),
            morty.change, "raise_right_hand"
        )
        self.wait()
        self.remove(morty)
        morty = morty.copy()
        self.add(morty)
        self.play(
            ReplacementTransform(
                morty.body,
                pi_group.get_part_by_tex("pi"),
                run_time = 1
            ),
            FadeOut(VGroup(morty.eyes, morty.mouth)),
            Write(VGroup(*pi_group[1:]))
        )
        self.wait(2)
        self.play(
            plane.set_width, pi_group.get_width(),
            plane.next_to, pi_group, DOWN, MED_LARGE_BUFF
        )

    def show_screen(self):
        screen = ScreenRectangle(height = 4.3)
        screen.to_edge(LEFT)
        titles = VGroup(
            OldTexText("From zeta video"),
            OldTexText("Coming up")
        )
        for title in titles:
            title.next_to(screen, UP)
            title.set_color(YELLOW)
        self.play(
            ShowCreation(screen),
            FadeIn(titles[0])
        )
        # CHANGE: Scene.show_frame() opened a preview window in Cairo; nothing to render
        pass
        self.wait(2)
        self.play(Transform(*titles))
        self.wait(3)

    def get_primes(self):
        return OldTex("2, 3, 5, 7, 11, 13, \\dots")

    def get_complex_numbers(self):
        plane = ComplexPlane(
            x_radius = 3,
            y_radius = 2.5,
        )
        plane.add_coordinates()
        point = plane.number_to_point(complex(1, 2))
        # CHANGE: typo in the original: radius = YELLOW was meant to be the dot color (a color is not a radius)
        dot = Dot(point, color = YELLOW)
        label = OldTex("1 + 2i")
        label.add_background_rectangle()
        label.next_to(dot, UP+RIGHT, buff = SMALL_BUFF)
        label.set_color(YELLOW)
        plane.label = label
        plane.add(dot, label)
        return plane

    def get_pi_group(self):
        result = OldTex("\\pi", "=", "%.8f\\dots"%np.pi)
        pi = result.get_part_by_tex("pi")
        pi.scale(2, about_point = pi.get_right())
        pi.set_color(MAROON_B)
        return result
