# ==============================================================================
# Scene:      EndOfGeometryProofiness
# Source:     videos/_2018/lost_lecture.py (lines 2126-2139)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EndOfGeometryProofiness.py EndOfGeometryProofiness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeometryProofLand(Scene):
    CONFIG = {
        "colors": [
            PINK, RED, YELLOW, GREEN, GREEN_A, BLUE,
            MAROON_E, MAROON_B, YELLOW, BLUE,
        ],
        "text": "Geometry proof land",
    }

    def construct(self):
        word = self.get_geometry_proof_land_word()
        word_outlines = word.deepcopy()
        word_outlines.set_fill(opacity=0)
        word_outlines.set_stroke(WHITE, 1)
        colors = list(self.colors)
        random.shuffle(colors)
        word_outlines.set_color_by_gradient(*colors)
        word_outlines.set_stroke(width=5)

        circles = VGroup()
        for letter in word:
            circle = Circle()
            # circle = letter.copy()
            circle.replace(letter, dim_to_match=1)
            circle.scale(3)
            circle.set_stroke(WHITE, 0)
            circle.set_fill(letter.get_color(), 0)
            circles.add(circle)
            circle.target = letter

        self.play(
            LaggedStartMap(MoveToTarget, circles),
            run_time=2
        )
        self.add(word_outlines, circles)
        self.play(LaggedStartMap(
            FadeIn, word_outlines,
            run_time=3,
            rate_func=there_and_back,
        ), Animation(circles))
        self.wait()

    def get_geometry_proof_land_word(self):
        word = OldTexText(self.text)
        word.rotate(-90 * DEGREES)
        word.scale(0.25)
        word.shift(3 * RIGHT)
        word.apply_complex_function(np.exp)
        word.rotate(90 * DEGREES)
        word.set_width(9)
        word.center()
        word.to_edge(UP)
        word.set_color_by_gradient(*self.colors)
        word.set_background_stroke(width=0)
        return word


class EndOfGeometryProofiness(GeometryProofLand):
    def construct(self):
        geometry_word = self.get_geometry_proof_land_word()
        orbital_mechanics = OldTexText("Orbital Mechanics")
        orbital_mechanics.scale(1.5)
        orbital_mechanics.to_edge(UP)
        underline = Line(LEFT, RIGHT)
        underline.match_width(orbital_mechanics)
        underline.next_to(orbital_mechanics, DOWN, SMALL_BUFF)

        self.play(LaggedStartMap(FadeOutAndShiftDown, geometry_word))
        self.play(FadeInFromDown(orbital_mechanics))
        self.play(ShowCreation(underline))
        self.wait()
