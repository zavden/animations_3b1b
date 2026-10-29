# ==============================================================================
# Scene:      ChordsInSpaceWithCircle
# Source:     videos/_2021/bertrands_paradox.py (lines 558-708)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChordsInSpaceWithCircle.py ChordsInSpaceWithCircle -w -m --fps 15
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


class ChordsInSpaceWithCircle(RandomChordScene):
    def construct(self):
        # Introduce chords
        n_lines = 500
        big_circle = Circle(radius=FRAME_WIDTH + FRAME_HEIGHT)
        lines = VGroup(*(
            RadialPoint.get_random_chord(big_circle)
            for x in range(n_lines)
        ))
        lines.set_stroke(WHITE, 0.5, 0.5)

        circle = Circle(radius=2)
        circle.set_stroke(WHITE, 2)

        triangle = Polygon(*(circle.pfp(a) for a in np.arange(0, 1, 1 / 3)))
        triangle.rotate(-PI / 6, about_point=circle.get_center())
        triangle.set_stroke(YELLOW, 3)
        triangle = VGroup(
            triangle.copy().set_stroke(BLACK, 8),
            triangle.copy(),
        )

        self.play(Write(lines, lag_ratio=(1 / n_lines), run_time=6))
        self.wait()

        def get_chords():
            return VGroup(*(
                self.line_to_chord(line, circle)
                for line in lines
            ))

        chords = get_chords()
        chords.save_state(RED)
        chords.set_stroke(WHITE, 1)
        self.play(
            ShowCreation(circle),
            VFadeIn(chords),
        )
        self.wait()
        self.play(ShowCreation(triangle, lag_ratio=0))
        circle.add(triangle)
        self.wait()

        # Show colors
        key = OldTexText(
            "Blue $\\Rightarrow$ Chord > \\text{Triangle side}\\\\"
            "Red $\\Rightarrow$ Chord < \\text{Triangle side}\\\\",
            tex_to_color_map={
                "Blue": BLUE,
                "Red": RED,
            }
        )
        key.to_edge(UP)
        key.set_backstroke(width=5)
        key[len(key) // 2:].align_to(key[:len(key) // 2], RIGHT)

        self.play(
            Restore(chords),
            FadeIn(key),
        )
        self.wait(2)

        # Move around
        chords.add_updater(lambda m: m.become(get_chords()))
        self.add(chords, circle)
        self.play(circle.animate.to_edge(RIGHT), run_time=6)
        self.play(circle.animate.to_edge(LEFT), run_time=6)
        self.wait()
        self.play(
            circle.animate.set_height(7, about_edge=LEFT),
            FadeOut(key, rate_func=squish_rate_func(smooth, 0, 0.5)),
            run_time=4
        )
        self.play(circle.animate.set_height(4, about_edge=RIGHT), run_time=4)

        # Show center point method
        big_circle = Circle(radius=3.25)
        big_circle.set_stroke(GREY_B, 2)
        big_circle.to_edge(DOWN)

        title = Text("Random center point method")
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        chords.clear_updaters()
        self.play(
            FadeOut(chords),
            FadeOut(lines),
            FadeIn(big_circle),
            FadeIn(title),
            circle.animate.set_height(0.5).to_corner(DR),
        )
        triangle.set_stroke(width=2)

        n_lines = 1000
        lines.become(VGroup(*(
            CenterPoint.get_random_chord(big_circle)
            for x in range(n_lines)
        )))
        lines.set_stroke(WHITE, self.chord_width, self.chord_opacity)
        flash_lines = lines.copy()
        flash_lines.set_stroke(width=3, opacity=1)
        indicators = Group(*map(CenterPoint.get_method_indicator, lines))

        self.play(
            ShowIncreasingSubsets(lines),
            ShowSubmobjectsOneByOne(flash_lines),
            ShowSubmobjectsOneByOne(indicators),
            rate_func=linear,
            run_time=8,
        )
        self.play(
            FadeOut(indicators[-1]),
            FadeOut(flash_lines[-1]),
        )
        self.wait()

        # Put circle back inside
        self.play(
            circle.animate.set_height(2).move_to(big_circle),
            run_time=1
        )
        chords.become(get_chords().set_stroke(opacity=0.7))
        self.add(chords, circle)
        self.play(VFadeIn(chords))
        self.wait()
        chords.add_updater(lambda m: m.become(get_chords().set_stroke(opacity=0.7)))
        self.play(
            circle.animate.move_to(big_circle, RIGHT),
            run_time=10,
            rate_func=there_and_back,
        )
        self.wait()

    def line_to_chord(self, line, circle, stroke_width=1):
        r = circle.get_radius()
        tangent = normalize(line.get_vector())
        normal = rotate_vector(tangent, PI / 2)
        center = circle.get_center()
        d1 = np.dot(line.get_start() - center, normal)
        if d1 > r:
            return VectorizedPoint(center + r * normal)
        d2 = np.sqrt(r**2 - d1**2)
        chord = Line(
            center + d1 * normal - d2 * tangent,
            center + d1 * normal + d2 * tangent,
        )
        chord.set_stroke(
            (BLUE if chord.get_length() > math.sqrt(3) * r else RED),
            width=stroke_width,
        )
        return chord
