# ==============================================================================
# Scene:      NonTransitive
# Source:     videos/_2021/bertrands_paradox.py (lines 750-817)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NonTransitive.py NonTransitive -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RandomChordScene(Scene):
    title = ""
    radius = 3.5
    n_samples = 1000
    long_color = BLUE
    short_color = WHITE
    chord_width = 0.5
    chord_opacity = 0.35
    run_time = 20
    include_triangle = True

    def construct(self):
        circle = self.circle = Circle(radius=self.radius)
        circle.set_stroke(GREY_B, 3)
        circle.to_edge(LEFT)

        chords = self.get_chords(circle)
        flash_chords = chords.copy()
        flash_chords.set_stroke(width=3, opacity=1)
        indicators = Group(*map(self.get_method_indicator, chords))

        title = Text(self.title)
        title.set_x(FRAME_WIDTH / 4).to_edge(UP)

        triangle = self.get_triangle(circle)

        if not self.include_triangle:
            triangle.set_opacity(0)

        self.add(circle, title, triangle)

        for s, rt in (slice(0, 16), 8), (slice(18, None), self.run_time):
            fraction = self.get_fraction([c.long for c in chords[s]])
            fraction.match_x(title)
            fraction.match_y(circle)
            self.add(fraction)
            self.remove(triangle)
            self.play(
                ShowIncreasingSubsets(chords[s]),
                ShowSubmobjectsOneByOne(flash_chords[s]),
                ShowSubmobjectsOneByOne(indicators[s]),
                Animation(triangle),
                fraction.alpha_update,
                rate_func=linear,
                run_time=rt,
            )
            self.remove(flash_chords)
            self.remove(indicators)
            self.remove(fraction)
        self.add(fraction)
        self.wait()

    def get_fraction(self, data):
        tex = OldTex(
            "{100", "\\over ", "100", "+", "100}", "= ", "0.500"
        )
        nl1 = Integer(100, edge_to_fix=ORIGIN)  # Number of long chords
        nl2 = Integer(100, edge_to_fix=RIGHT)
        ns = Integer(100, edge_to_fix=LEFT)  # Number of short chords
        ratio = DecimalNumber(0, num_decimal_places=4)
        fraction = VGroup(
            nl1.move_to(tex[0]),
            tex[1],
            nl2.move_to(tex[2]),
            tex[3],
            ns.move_to(tex[4]),
            tex[5],
            ratio.move_to(tex[6], LEFT),
        )

        def update_fraction(frac, alpha):
            subdata = data[:int(np.floor(alpha * len(data)))]
            n_long = sum(subdata)
            n_short = len(subdata) - n_long
            frac[0].set_value(n_long)
            frac[0].set_color(self.long_color)
            frac[2].set_value(n_long)
            frac[2].set_color(self.long_color)
            frac[4].set_value(n_short)
            frac[4].set_color(self.short_color)

            if len(subdata) == 0:
                frac[-2:].set_opacity(0)
            else:
                frac[-2:].set_opacity(1)
                frac[6].set_value(n_long / len(subdata))
            return frac

        fraction.alpha_update = UpdateFromAlphaFunc(
            fraction, update_fraction
        )
        return fraction

    def get_chords(self, circle, chord_generator=None):
        if chord_generator is None:
            chord_generator = self.get_random_chord
        tri_len = np.sqrt(3) * circle.get_width() / 2
        chords = VGroup(*(
            chord_generator(circle)
            for x in range(self.n_samples)
        ))
        for chord in chords:
            chord.long = (chord.get_length() > tri_len)
            chord.set_color(
                self.long_color if chord.long else self.short_color
            )
        chords.set_stroke(
            width=self.chord_width,
            opacity=self.chord_opacity
        )
        return chords

    def get_triangle(self, circle):
        verts = [circle.pfp(a) for a in np.arange(0, 1, 1 / 3)]
        triangle = Polygon(*verts)
        triangle.rotate(-PI / 6, about_point=circle.get_center())
        triangle.set_stroke(RED, 2, 1)
        return triangle

    def get_random_chord(self, circle):
        return NotImplemented

    def get_method_indicator(self, chord):
        return NotImplemented


class CenterPoint(RandomChordScene):
    title = "Random point in circle"

    @staticmethod
    def get_random_chord(circle):
        x = y = 1
        while x * x + y * y > 1:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
        return CenterPoint.chord_from_xy(x, y, circle)

    @staticmethod
    def chord_from_xy(x, y, circle):
        n2 = x * x + y * y
        temp_x = math.sqrt(n2)
        temp_y = math.sqrt(1 - n2)
        line = Line(
            [temp_x, -temp_y, 0],
            [temp_x, temp_y, 0],
        )
        line.rotate(angle_of_vector([x, y, 0]), about_point=ORIGIN)
        line.scale(circle.get_width() / 2, about_point=ORIGIN)
        line.shift(circle.get_center())
        return line

    @staticmethod
    def get_method_indicator(chord):
        dots = DotCloud([chord.get_center()])
        dots.set_glow_factor(2)
        dots.set_radius(0.25)
        dots.set_color(YELLOW)
        return dots


class RadialPoint(CenterPoint):
    title = "Random point along radial line"

    @staticmethod
    def get_random_chord(circle):
        angle = random.uniform(0, TAU)
        dist = random.uniform(0, 1)
        return CenterPoint.chord_from_xy(
            dist * math.cos(angle),
            dist * math.sin(angle),
            circle
        )

    @staticmethod
    def get_method_indicator(chord):
        dot = super().get_method_indicator(chord)
        line = Line(self.circle.get_center(), dot.get_center())
        line.set_length(self.radius, about_point=line.get_start())
        line.set_stroke(YELLOW, 1)
        return Group(dot, line)


class NonTransitive(Scene):
    def construct(self):
        circle = Circle(radius=3)
        circle.set_stroke(GREY_B, 2)

        words = OldTexText(
            "Rotational symmetries do \\emph{not} act\\\\"
            "transitively on the space of all chords",
            tex_to_color_map={"\\emph{not}": RED},
        )
        words.to_edge(UP, MED_SMALL_BUFF)
        circle.next_to(words, DOWN, MED_SMALL_BUFF)

        chord1 = Line(circle.pfp(0.4), circle.pfp(0.5))
        chord1.set_stroke(RED, 3)
        chord1_shadow = chord1.copy().set_stroke(opacity=0.5)
        chord2 = Line(circle.pfp(0.8), circle.pfp(0.25))
        chord2.set_stroke(BLUE, 3)

        left_words = Text("No action on\nthis chord...")
        right_words = Text("...will ever map\nto this chord.")
        left_words.to_edge(LEFT).shift(UP)
        right_words.to_edge(RIGHT).shift(DOWN)

        left_arrow = Arrow(left_words, chord1.get_center(), buff=0.1)
        right_arrow = Arrow(right_words.get_left(), chord2.get_center(), buff=0.1)

        VGroup(left_words, left_arrow).set_color(RED)
        VGroup(right_words, right_arrow).set_color(BLUE)

        chords = VGroup(*(
            RadialPoint.get_random_chord(circle)
            for x in range(100)
        ))
        chords.set_stroke(WHITE, 1, 0.5)

        group = VGroup(circle, chords)

        self.add(words)
        self.play(
            Rotate(group, TAU, about_point=circle.get_center(), run_time=6)
        )
        self.wait()

        self.add(chord1_shadow, chord1)
        self.play(
            FadeOut(chords),
            ShowCreation(chord1_shadow),
            ShowCreation(chord1),
            FadeIn(left_words),
            ShowCreation(left_arrow),
        )
        group = VGroup(circle, chord1)
        self.add(group, left_arrow)
        self.play(
            Rotate(
                group, TAU,
                about_point=circle.get_center(),
            ),
            FadeIn(
                VGroup(right_words, right_arrow, chord2),
                rate_func=squish_rate_func(smooth, 0.3, 0.4),
            ),
            run_time=10,
        )

        # Embed
        self.embed()
