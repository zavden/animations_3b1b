# ==============================================================================
# Scene:      MainBreakdown
# Source:     videos/_2017/256.py (lines 188-650)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MainBreakdown.py MainBreakdown -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - set_points with 4 points per cubic segment is not valid for GL quadratic curves: build the path with start_new_path/add_cubic_bezier_curve_to
#   - saved_state exists but is None until save_state() is called in GL
#   - the Google logo path has no sub-pieces in GL (IndexError); use the shape itself
# ==============================================================================

from manim_imports_ext import *

def get_google_logo():
    result = SVGMobject(
        file_name = "google_logo",
        height = 0.75
    )
    blue, red, yellow, green = [
        "#4885ed", "#db3236", "#f4c20d", "#3cba54"
    ]
    colors = [red, yellow, blue, green, red, blue]
    result.set_color_by_gradient(*colors)
    return result


class MainBreakdown(Scene):
    CONFIG = {
        "n_group_rows" : 8,
        "n_group_cols" : 8,
    }
    def construct(self):
        self.add_four_billions()
        self.gpu_packed_computer()
        self.kilo_google()
        self.half_all_people_on_earth()
        self.four_billion_earths()
        self.four_billion_galxies()
        self.show_time_scale()
        self.show_probability()

    def add_four_billions(self):
        top_line = VGroup()
        four_billions = VGroup()
        for x in range(8):
            mob = OldTexText(
                "$\\big($", "4 Billion", "$\\big)$",
                arg_separator = ""
            )
            top_line.add(mob)
            four_billions.add(mob[1])
        top_line.arrange(RIGHT, buff = SMALL_BUFF)
        top_line.set_width(FRAME_WIDTH - LARGE_BUFF)
        top_line.to_edge(UP)
        four_billions.set_color(YELLOW)
        self.add(top_line)

        self.top_line = top_line
        self.four_billions = four_billions

    def gpu_packed_computer(self):
        self.show_gpu()
        self.cram_computer_with_gpus()

    def show_gpu(self):
        gpu = SVGMobject(
            file_name = "gpu",
            height = 1,
            fill_color = GREY_B,
        )
        name = OldTexText("Graphics", "Processing", "Unit")
        for word in name:
            word[0].set_color(BLUE)
        name.to_edge(LEFT)
        gpu.next_to(name, UP)

        hash_names = VGroup(*[
            OldTexText("hash")
            for x in range(10)
        ])
        hash_names.arrange(DOWN, buff = MED_SMALL_BUFF)
        hash_names.next_to(name, RIGHT, buff = 2)

        paths = VGroup()
        for hash_name in hash_names:
            hash_name.add_background_rectangle(opacity = 0.5)
            path = VMobject()
            start_point = name.get_right() + SMALL_BUFF*RIGHT
            end_point = start_point + (4+hash_name.get_width())*RIGHT
            # CHANGE: set_points with 4 points per cubic segment is not valid for GL quadratic curves: build the path with start_new_path/add_cubic_bezier_curve_to
            path.start_new_path(start_point)
            path.add_cubic_bezier_curve_to(
                start_point+RIGHT, hash_name.get_left()+LEFT, hash_name.get_left(),
            )
            path.add_line_to(hash_name.get_right())
            path.add_cubic_bezier_curve_to(
                hash_name.get_right() + RIGHT, end_point + LEFT, end_point,
            )
            paths.add(path)
        paths.set_stroke(width = 3)
        paths.set_color_by_gradient(BLUE, GREEN)
        def get_passing_flash():
            return ShowPassingFlash(
                paths,
                lag_ratio = 0,
                time_width = 0.7,
                run_time = 2,
            )
        rate_words = OldTexText(
            "$<$ 1 Billion", "Hashes/sec"
        )
        rate_words.next_to(name, DOWN)

        self.play(FadeIn(name))
        self.play(DrawBorderThenFill(gpu))
        self.play(
            get_passing_flash(),
            FadeIn(hash_names)
        )
        for x in range(2):
            self.play(
                get_passing_flash(),
                Animation(hash_names)
            )
        self.play(
            Write(rate_words, run_time = 2),
            get_passing_flash(),
            Animation(hash_names)
        )
        self.play(get_passing_flash(), Animation(hash_names))
        self.play(*list(map(FadeOut, [name, hash_names])))

        self.gpu = gpu
        self.rate_words = rate_words

    def cram_computer_with_gpus(self):
        gpu = self.gpu
        gpus = VGroup(gpu, *[gpu.copy() for x in range(5)])

        rate_words = self.rate_words
        four_billion = self.four_billions[0]

        laptop = Laptop()
        laptop.next_to(rate_words, RIGHT)
        laptop.to_edge(RIGHT)
        new_rate_words = OldTexText("4 Billion", "Hashes/sec")
        new_rate_words.move_to(rate_words)
        new_rate_words[0].set_color(BLUE)

        hps, h_line, target_laptop = self.get_fraction(
            0, OldTexText("H/s"), Laptop()
        )
        hps.scale(0.7)

        self.play(FadeIn(laptop))
        self.play(
            gpus.arrange, RIGHT, SMALL_BUFF,
            gpus.next_to, rate_words, UP,
            gpus.to_edge, LEFT
        )
        self.play(
            Transform(
                four_billion.copy(), new_rate_words[0],
                remover = True,
            ),
            Transform(rate_words, new_rate_words)
        )
        self.wait()
        self.play(
            LaggedStartMap(
                ApplyFunction, gpus,
                lambda g : (
                    lambda m : m.scale(0.01).move_to(laptop),
                    g
                ),
                remover = True
            )
        )
        self.wait()
        self.play(
            Transform(
                rate_words[0], four_billion.copy().set_color(BLUE),
                remover = True,
            ),
            four_billion.set_color, BLUE,
            Transform(rate_words[1], hps),
        )
        self.play(
            Transform(laptop, target_laptop),
            ShowCreation(h_line),
        )
        self.wait()

    def kilo_google(self):
        self.create_four_billion_copies(1, Laptop())
        google = self.get_google_logo()
        google.next_to(
            self.group_of_four_billion_things, UP,
            buff = LARGE_BUFF,
            aligned_edge = LEFT
        )
        google.shift(RIGHT)
        millions = OldTexText("$\\sim$ Millions of servers")
        millions.next_to(google, RIGHT)
        plus_plus = OldTex("++")
        plus_plus.next_to(google, RIGHT, SMALL_BUFF)
        plus_plus.set_stroke(width = 2)
        kilo = OldTexText("Kilo")
        kilo.scale(1.5)
        kilo.next_to(google[-1], LEFT, SMALL_BUFF, DOWN)
        kilogoogle = VGroup(kilo, google, plus_plus)

        four_billion = self.four_billions[1]
        laptop, h_line, target_kilogoogle = self.get_fraction(
            1, Laptop(), self.get_kilogoogle()
        )

        self.revert_to_original_skipping_status()
        self.play(DrawBorderThenFill(google))
        self.wait(2)
        self.play(Write(millions))
        self.wait(2)
        self.play(LaggedStartMap(
            Indicate, self.group_of_four_billion_things,
            run_time = 4,
            rate_func = there_and_back,
            lag_ratio = 0.25,
        ))
        self.play(FadeOut(millions), FadeIn(plus_plus))
        self.play(Write(kilo))
        self.wait()
        self.play(
            four_billion.restore,
            FadeOut(self.group_of_four_billion_things)
        )
        self.play(
            Transform(kilogoogle, target_kilogoogle),
            FadeIn(laptop),
            FadeIn(h_line),
        )
        self.wait()

    def half_all_people_on_earth(self):
        earth = self.get_earth()
        people = OldTexText("7.3 Billion people")
        people.next_to(earth, RIGHT)
        group = VGroup(earth, people)
        group.next_to(self.four_billions, DOWN, MED_LARGE_BUFF)
        group.shift(RIGHT)

        kg, h_line, target_earth = self.get_fraction(
            2, self.get_kilogoogle(), self.get_earth(), 
        )

        self.play(
            GrowFromCenter(earth),
            Write(people)
        )
        self.wait()
        self.create_four_billion_copies(2, self.get_kilogoogle())
        self.wait()
        self.play(
            self.four_billions[2].restore,
            Transform(earth, target_earth),
            FadeIn(h_line),
            FadeIn(kg),
            FadeOut(self.group_of_four_billion_things),
            FadeOut(people)
        )
        self.wait()

    def four_billion_earths(self):
        self.create_four_billion_copies(
            3, self.get_earth()
        )
        milky_way = ImageMobject("milky_way")
        milky_way.set_height(3)
        milky_way.to_edge(LEFT, buff = 0)
        milky_way.shift(DOWN)

        n_stars_estimate = OldTexText("100 to 400 \\\\ billion stars")
        n_stars_estimate.next_to(milky_way, RIGHT)
        n_stars_estimate.shift(UP)

        earth, h_line, denom = self.get_fraction(
            3, self.get_earth(), self.get_galaxy()
        )

        self.revert_to_original_skipping_status()
        self.play(FadeIn(milky_way))
        self.play(Write(n_stars_estimate))
        self.wait()
        self.play(LaggedStartMap(
            Indicate, self.group_of_four_billion_things,
            rate_func = there_and_back,
            lag_ratio = 0.2,
            run_time = 3,
        ))
        self.wait()
        self.play(
            ReplacementTransform(
                self.group_of_four_billion_things,
                VGroup(earth)
            ),
            ShowCreation(h_line),
            FadeIn(denom),
            self.four_billions[3].restore,
            FadeOut(milky_way),
            FadeOut(n_stars_estimate),
        )
        self.wait()

    def four_billion_galxies(self):
        self.create_four_billion_copies(4, self.get_galaxy())
        num, h_line, denom = fraction = self.get_fraction(
            4, self.get_galaxy(), OldTexText("GGSC").set_color(BLUE)
        )

        name = OldTexText(
            "Giga", "Galactic \\\\", " Super", " Computer",
            arg_separator = ""
        )
        for word in name:
            word[0].set_color(BLUE)
        name.next_to(self.group_of_four_billion_things, UP)

        self.play(Write(name))
        self.wait()
        self.play(
            self.four_billions[4].restore,
            ReplacementTransform(
                self.group_of_four_billion_things, VGroup(num),
                run_time = 2,
                lag_ratio = 0.5
            ),
            ShowCreation(h_line),
            ReplacementTransform(
                name, denom
            ),
        )
        self.wait()

    def show_time_scale(self):
        fb1, fb2 = self.four_billions[5:7]
        seconds_to_years = OldTexText("seconds $\\approx$ 126.8 years")
        seconds_to_years.shift(LEFT)
        years_to_eons = OldTexText(
            "$\\times$ 126.8 years", "$\\approx$ 507 Billion years", 
        )
        years_to_eons.next_to(
            seconds_to_years, DOWN, 
            aligned_edge = LEFT,
        )
        universe_lifetimes = OldTexText("$\\approx 37 \\times$ Age of universe")
        universe_lifetimes.next_to(
            years_to_eons[1], DOWN, 
            aligned_edge = LEFT
        )

        for fb, words in (fb1, seconds_to_years), (fb2, years_to_eons):
            self.play(
                fb.scale, 1.3,
                fb.next_to, words, LEFT, 
                fb.set_color, BLUE,
                Write(words)
            )
            self.wait()
        self.play(Write(universe_lifetimes))
        self.wait()

    def show_probability(self):
        four_billion = self.four_billions[7]
        words = OldTexText(
            "1 in ", "4 Billion\\\\",
            "chance of success"
        )
        words.next_to(four_billion, DOWN, buff = MED_LARGE_BUFF)
        words.to_edge(RIGHT)
        words[1].set_color(BLUE)

        self.play(
            Write(VGroup(*words[::2])),
            Transform(four_billion, words[1])
        )
        self.wait()


    ############

    def create_four_billion_copies(self, index, mobject):
        four_billion = self.four_billions[index]
        four_billion.set_color(BLUE)
        four_billion.save_state()

        group = VGroup(*[
            VGroup(*[
                mobject.copy().set_height(0.25)
                for x in range(self.n_group_rows)
            ]).arrange(DOWN, buff = SMALL_BUFF)
            for y in range(self.n_group_cols-1)
        ])
        dots = OldTex("\\dots")
        group.add(dots)
        group.add(*[group[0].copy() for x in range(2)])
        group.arrange(RIGHT, buff = SMALL_BUFF)
        group.set_height(FRAME_Y_RADIUS)
        max_width = 1.25*FRAME_X_RADIUS
        if group.get_width() > max_width:
            group.set_width(max_width)
        group.to_corner(DOWN+RIGHT)
        group = VGroup(*it.chain(*group))

        brace = Brace(group, LEFT)

        self.play(
            four_billion.scale, 2,
            four_billion.next_to, brace, LEFT,
            GrowFromCenter(brace),
            LaggedStartMap(
                FadeIn, group,
                run_time = 3,
                lag_ratio = 0.2
            )
        )
        self.wait()

        group.add_to_back(brace)
        self.group_of_four_billion_things = group

    def get_fraction(self, index, numerator, denominator):
        four_billion = self.four_billions[index]
        # CHANGE: saved_state exists but is None until save_state() is called in GL
        if getattr(four_billion, "saved_state", None) is not None:
            four_billion = four_billion.saved_state

        space = LARGE_BUFF
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(four_billion.get_width())
        h_line.next_to(four_billion, DOWN, space)
        for mob in numerator, denominator:
            mob.set_height(0.75*space)
            max_width = h_line.get_width()
            if mob.get_width() > max_width:
                mob.set_width(max_width)
        numerator.next_to(h_line, UP, SMALL_BUFF)
        denominator.next_to(h_line, DOWN, SMALL_BUFF)
        fraction = VGroup(numerator, h_line, denominator)

        return fraction

    def get_google_logo(self):
        return get_google_logo()

    def get_kilogoogle(self):
        G = self.get_google_logo()[-1]
        kilo = OldTexText("K")
        kilo.scale(1.5)
        # CHANGE: the Google logo path has no sub-pieces in GL (IndexError); use the shape itself
        kilo.next_to(G[-1] if len(G.submobjects) > 0 else G, LEFT, SMALL_BUFF, DOWN)
        plus_plus = OldTex("++")
        plus_plus.set_stroke(width = 1)
        plus_plus.next_to(G, RIGHT, SMALL_BUFF)
        return VGroup(kilo, G, plus_plus)

    def get_earth(self):
        earth = SVGMobject(
            file_name = "earth",
            height = 1.5,
            fill_color = BLACK,
        )
        circle = Circle(
            stroke_width = 3,
            stroke_color = GREEN,
            fill_opacity = 1,
            fill_color = BLUE_C,
        )
        circle.replace(earth)
        earth.add_to_back(circle)
        return earth

    def get_galaxy(self):
        return SVGMobject(
            file_name = "galaxy",
            fill_opacity = 0,
            stroke_width = 3,
            stroke_color = WHITE,
            height = 1,
        )
