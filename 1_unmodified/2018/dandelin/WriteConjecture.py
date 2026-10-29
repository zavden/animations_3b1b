# ==============================================================================
# Scene:      WriteConjecture
# Source:     videos/_2018/dandelin.py (lines 1055-1128)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteConjecture.py WriteConjecture -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteConjecture(Scene):
    CONFIG = {
        "image_name": "ConjectureLineEquivalenceBigSphere",
        "q_coords": 1.28 * UP + 0.15 * LEFT,
        "circle_point_coords": 0.84 * RIGHT + 0.05 * DOWN,
        "tangent_point_coords": 0.85 * UP + 1.75 * LEFT,
        "plane_line_color": GOLD,
        "text_scale_factor": 0.75,
        "shift_plane_word_down": False,
        "include_image": False,
    }

    def construct(self):
        if self.include_image:
            image = ImageMobject(self.image_name)
            image.set_height(FRAME_HEIGHT)
            self.add(image)

        title = OldTexText("Conjecture:")
        title.to_corner(UR)

        cone_line = Line(self.q_coords, self.circle_point_coords)
        plane_line = Line(self.q_coords, self.tangent_point_coords)
        plane_line.set_color(self.plane_line_color)
        lines = VGroup(cone_line, plane_line)

        cone_line_words = OldTexText("Cone line")
        plane_line_words = OldTexText("Plane line")
        plane_line_words.set_color(self.plane_line_color)
        words = VGroup(cone_line_words, plane_line_words)

        for word in words:
            word.add_to_back(word.copy().set_stroke(BLACK, 5))
            word.in_equation = word.copy()

        equation = VGroup(
            OldTex("||"),
            words[0].in_equation,
            OldTex("||"),
            OldTex("="),
            OldTex("||"),
            words[1].in_equation,
            OldTex("||"),
        )
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.scale(0.75)
        equation.next_to(title, DOWN, MED_LARGE_BUFF)
        equation.shift_onto_screen()
        title.next_to(equation, UP)

        for word, line in zip(words, lines):
            word.scale(self.text_scale_factor)
            word.next_to(ORIGIN, UP, SMALL_BUFF)
            if self.shift_plane_word_down and (word is plane_line_words):
                word.next_to(ORIGIN, DOWN, SMALL_BUFF)
            angle = line.get_angle()
            if abs(angle) > 90 * DEGREES:
                angle += PI
            word.rotate(angle, about_point=ORIGIN)
            word.shift(line.get_center())

        self.play(LaggedStartMap(
            FadeInFromDown,
            VGroup(title, equation),
            lag_ratio=0.7
        ))
        self.wait()
        for word, line in zip(words, lines):
            self.play(ShowCreation(line))
            self.play(WiggleOutThenIn(line))
            self.play(ReplacementTransform(
                word.in_equation.copy(), word
            ))
            self.wait()
