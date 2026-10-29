# ==============================================================================
# Scene:      Describe2011IMO
# Source:     videos/_2019/windmill.py (lines 713-1032)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Describe2011IMO.py Describe2011IMO -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
#   - Add factual IMO data regenerated with make_windmill_data.py and checked against the official results.
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/2019/windmill/2011_imo_countries.json
#   - _lib/data/2019/windmill/2019_imo_countries.json
#   - _lib/data/2019/windmill/country_codes.json
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject
import json

class IntroduceIMO(Scene):
    CONFIG = {
        "num_countries": 130,
        "use_real_images": True,
        # "use_real_images": False,
        "include_labels": False,
        "camera_config": {"background_color": GREY_E},
        "random_seed": 6,
        "year": 2019,
        "n_flag_rows": 10,
        "reorganize_students": True,
    }

    def construct(self):
        self.add_title()
        self.show_flags()
        self.show_students()
        self.move_title()
        self.isolate_usa()

    def add_title(self):
        title = OldTexText(
            "International ", "Mathematical ", "Olympiad",
        )
        title.scale(1.25)
        logo = ImageMobject("imo_logo")
        logo.set_height(1)

        group = Group(logo, title)
        group.arrange(RIGHT)
        group.to_edge(UP, buff=MED_SMALL_BUFF)

        self.add(title, logo)
        self.title = title
        self.logo = logo

    def show_flags(self):
        flags = self.get_flags()
        flags.set_height(6)
        flags.to_edge(DOWN)
        random_flags = Group(*flags)
        random_flags.shuffle()

        self.play(
            LaggedStartMap(
                FadeInFromDown, random_flags,
                run_time=2,
                lag_ratio=0.03,
            )
        )
        self.remove(random_flags)
        self.add(flags)
        self.wait()

        self.flags = flags

    def show_students(self):
        flags = self.flags

        student_groups = VGroup()
        all_students = VGroup()
        for flag in flags:
            group = self.get_students(flag)
            student_groups.add(group)
            for student in group:
                student.preimage = VectorizedPoint()
                student.preimage.move_to(flag)
                all_students.add(student)
        all_students.shuffle()

        student_groups.generate_target()
        student_groups.target.arrange_in_grid(
            n_rows=self.n_flag_rows,
            buff=SMALL_BUFF,
        )
        # student_groups.target[-9:].align_to(student_groups.target[0], LEFT)
        student_groups.target.match_height(flags)
        student_groups.target.match_y(flags)
        student_groups.target.to_edge(RIGHT, buff=0.25)

        self.play(LaggedStart(
            *[
                ReplacementTransform(
                    student.preimage, student
                )
                for student in all_students
            ],
            run_time=2,
            lag_ratio=0.2,
        ))
        self.wait()
        if self.reorganize_students:
            self.play(
                MoveToTarget(student_groups),
                flags.space_out_submobjects, 0.75,
                flags.to_edge, LEFT, MED_SMALL_BUFF,
            )
            self.wait()

        self.student_groups = student_groups

    def move_title(self):
        title = self.title
        logo = self.logo

        new_title = OldTexText("IMO")
        new_title.match_height(title)

        logo.generate_target()
        group = Group(logo.target, new_title)
        group.arrange(RIGHT, buff=SMALL_BUFF)
        group.match_y(title)
        group.match_x(self.student_groups, UP)

        title.generate_target()
        for word, letter in zip(title.target, new_title[0]):
            for nl in word:
                nl.move_to(letter)
            word.set_opacity(0)
            word[0].set_opacity(1)
            word[0].become(letter)

        self.play(
            MoveToTarget(title),
            MoveToTarget(logo),
        )
        self.wait()

    def isolate_usa(self):
        flags = self.flags
        student_groups = self.student_groups

        us_flag = flags[0]
        random_flags = Group(*flags[1:])
        random_flags.shuffle()

        old_height = us_flag.get_height()
        us_flag.label.set_width(0.8 * us_flag.get_width())
        us_flag.label.next_to(
            us_flag, DOWN,
            buff=0.2 * us_flag.get_height(),
        )
        us_flag.label.set_opacity(0)
        us_flag.add(us_flag.label)
        us_flag.generate_target()
        us_flag.target.scale(1 / old_height)
        us_flag.target.to_corner(UL)
        us_flag.target[1].set_opacity(1)

        self.remove(us_flag)
        self.play(
            LaggedStart(
                *[
                    FadeOut(flag, DOWN)
                    for flag in random_flags
                ],
                lag_ratio=0.05,
                run_time=1.5
            ),
            MoveToTarget(us_flag),
            student_groups[1:].fade, 0.9,
        )
        self.wait()

    #
    def get_students(self, flag):
        dots = VGroup(*[Dot() for x in range(6)])
        dots.arrange_in_grid(n_cols=2, buff=SMALL_BUFF)
        dots.match_height(flag)
        dots.next_to(flag, RIGHT, SMALL_BUFF)
        dots[flag.n_students:].set_opacity(0)

        if isinstance(flag, ImageMobject):
            rgba = random.choice(random.choice(flag.pixel_array))
            if np.all(rgba < 100):
                rgba = interpolate(rgba, 256 * np.ones(len(rgba)), 0.5)
            color = rgba_to_color(rgba / 256)
        else:
            color = random_bright_color()
        dots.set_color(color)
        dots.set_stroke(WHITE, 1, background=True)

        return dots

    def get_flags(self):
        year = self.year
        file = "{}_imo_countries.json".format(year)
        with open(os.path.join("assets", file)) as fp:
            countries_with_counts = json.load(fp)
        with open(os.path.join("assets", "country_codes.json")) as fp:
            country_codes = json.load(fp)
            country_to_code2 = dict([
                (country.lower(), code2.lower())
                for country, code2, code3 in country_codes
            ])
            country_to_code3 = dict([
                (country.lower(), code3.lower())
                for country, code2, code3 in country_codes
            ])

        images = Group()
        for country, count in countries_with_counts:
            country = country.lower()

            alt_names = [
                ("united states of america", "united states"),
                ("people's republic of china", "china"),
                ("macau", "macao"),
                ("syria", "syrian arab republic"),
                ("north macedonia", "macedonia, the former yugoslav republic of"),
                ("tanzania", "united republic of tanzania"),
                ("vietnam", "viet nam"),
                ("ivory coast", "cote d'ivoire")
            ]
            for n1, n2 in alt_names:
                if country == n1:
                    country = n2

            if country not in country_to_code2:
                print("Can't find {}".format(country))
                continue
            short_code = country_to_code2[country]
            try:
                image = ImageMobject(os.path.join("flags", short_code))
                image.set_width(1)
                label = VGroup(*[
                    OldTexText(l)
                    for l in country_to_code3[country].upper()
                ])
                label.arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
                label.set_height(0.25)
                if not self.use_real_images:
                    rect = SurroundingRectangle(image, buff=0)
                    rect.set_stroke(WHITE, 1)
                    image = rect
                image.label = label
                image.n_students = count
                images.add(image)
            except OSError:
                print("Failed on {}".format(country))

        n_rows = self.n_flag_rows
        images.arrange_in_grid(
            n_rows=n_rows,
            buff=1.25,
        )
        images[-(len(images) % n_rows):].align_to(images[0], LEFT)
        sf = 1.7
        images.stretch(sf, 0)
        for i, image in enumerate(images):
            image.set_height(1)
            image.stretch(1 / sf, 0)
            image.label.next_to(image, DOWN, SMALL_BUFF)
            if self.include_labels:
                image.add(image.label)

        images.set_width(FRAME_WIDTH - 1)
        if images.get_height() > FRAME_HEIGHT - 1:
            images.set_height(FRAME_HEIGHT - 1)
        images.center()
        return images


class Describe2011IMO(IntroduceIMO):
    CONFIG = {
        "year": 2011,
        "use_real_images": True,
        "n_flag_rows": 10,
        "student_data": [
            [1, "Lisa Sauermann", "de", [7, 7, 7, 7, 7, 7]],
            [2, "Jeck Lim", "sg", [7, 5, 7, 7, 7, 7]],
            [3, "Lin Chen", "cn", [7, 3, 7, 7, 7, 7]],
            [4, "Jun Jie Joseph Kuan", "sg", [7, 7, 7, 7, 7, 1]],
            [4, "David Yang", "us", [7, 7, 7, 7, 7, 1]],
            [6, "Jie Jun Ang", "sg", [7, 7, 7, 7, 7, 0]],
            [6, "Kensuke Yoshida", "jp", [7, 6, 7, 7, 7, 1]],
            [6, "Raul Sarmiento", "pe", [7, 7, 7, 7, 7, 0]],
            [6, "Nipun Pitimanaaree", "th", [7, 7, 7, 7, 7, 0]],
        ],
    }

    def construct(self):
        self.add_title()
        self.add_flags_and_students()
        self.comment_on_primality()
        self.show_top_three_scorers()

    def add_title(self):
        year = OldTex("2011")
        logo = ImageMobject("imo_logo")
        imo = OldTexText("IMO")
        group = Group(year, logo, imo)
        group.scale(1.25)
        logo.set_height(1)
        group.arrange(RIGHT)
        group.to_corner(UR, buff=MED_SMALL_BUFF)
        group.shift(LEFT)

        self.add(group)
        self.play(FadeIn(year, RIGHT))

        self.title = group

    def add_flags_and_students(self):
        flags = self.get_flags()
        flags.space_out_submobjects(0.8)
        sf = 0.8
        flags.stretch(sf, 0)
        for flag in flags:
            flag.stretch(1 / sf, 0)
        flags.set_height(5)
        flags.to_corner(DL)

        student_groups = VGroup(*[
            self.get_students(flag)
            for flag in flags
        ])
        student_groups.arrange_in_grid(
            n_rows=self.n_flag_rows,
            buff=SMALL_BUFF,
        )
        student_groups[-1].align_to(student_groups, LEFT)
        student_groups.set_height(6)
        student_groups.next_to(self.title, DOWN)
        flags.align_to(student_groups, UP)

        all_students = VGroup(*it.chain(*[
            [
                student
                for student in group
                if student.get_fill_opacity() > 0
            ]
            for group in student_groups
        ]))

        # Counters
        student_counter = VGroup(
            Integer(0),
            OldTexText("Participants"),
        )
        student_counter.set = all_students
        student_counter.next_to(self.title, LEFT, MED_LARGE_BUFF)
        student_counter.right_edge = student_counter.get_right()

        def update_counter(counter):
            counter[0].set_value(len(counter.set))
            counter.arrange(RIGHT)
            counter[0].align_to(counter[1][0][0], DOWN)
            counter.move_to(counter.right_edge, RIGHT)

        student_counter.add_updater(update_counter)

        flag_counter = VGroup(
            Integer(0),
            OldTexText("Countries")
        )
        flag_counter.set = flags
        flag_counter.next_to(student_counter, LEFT, buff=0.75)
        flag_counter.align_to(student_counter[0], DOWN)
        flag_counter.right_edge = flag_counter.get_right()
        flag_counter.add_updater(update_counter)

        self.add(student_counter)
        self.play(
            ShowIncreasingSubsets(all_students),
            run_time=3,
        )
        self.wait()
        self.add(flag_counter)
        self.play(
            ShowIncreasingSubsets(flags),
            run_time=3,
        )
        self.wait()

        self.student_counter = student_counter
        self.flag_counter = flag_counter
        self.all_students = all_students
        self.student_groups = student_groups
        self.flags = flags

    def comment_on_primality(self):
        full_rect = FullScreenFadeRectangle(opacity=0.9)
        numbers = VGroup(
            self.title[0],
            self.student_counter[0],
            self.flag_counter[0],
        )
        lines = VGroup(*[
            Line().match_width(number).next_to(number, DOWN, SMALL_BUFF)
            for number in numbers
        ])
        lines.set_stroke(TEAL, 2)

        randy = Randolph()
        randy.to_corner(DL)
        randy.look_at(numbers)

        words = VGroup(*[
            OldTexText("Prime").next_to(line, DOWN)
            for line in reversed(lines)
        ])
        words.match_color(lines)

        self.add(full_rect, numbers)
        self.play(
            FadeIn(full_rect),
            randy.change, "sassy",
            VFadeIn(randy),
        )
        self.play(
            ShowCreation(lines),
            randy.change, "pondering",
        )
        self.play(Blink(randy))
        self.play(
            randy.change, "thinking",
            LaggedStart(*[
                FadeIn(word, UP)
                for word in words
            ], run_time=3, lag_ratio=0.5)
        )
        self.play(Blink(randy))
        self.play(
            FadeOut(randy),
            FadeOut(words),
        )
        self.play(FadeOut(full_rect), FadeOut(lines))

    def show_top_three_scorers(self):
        student_groups = self.student_groups
        all_students = self.all_students
        flags = self.flags
        student_counter = self.student_counter
        flag_counter = self.flag_counter

        student = student_groups[10][0]
        flag = flags[10]

        students_to_fade = VGroup(*filter(
            lambda s: s is not student,
            all_students
        ))
        flags_to_fade = Group(*filter(
            lambda s: s is not flag,
            flags
        ))

        grid = self.get_score_grid()
        grid.shift(3 * DOWN)
        title_row = grid.rows[0]
        top_row = grid.rows[1]

        self.play(
            LaggedStartMap(FadeOutAndShiftDown, students_to_fade),
            LaggedStartMap(FadeOutAndShiftDown, flags_to_fade),
            ChangeDecimalToValue(student_counter[0], 1),
            FadeOut(flag_counter),
            run_time=2
        )
        student_counter[1][0][-1].fade(1)
        self.play(
            Write(top_row[0]),
            ReplacementTransform(student, top_row[1][1]),
            flag.replace, top_row[1][0],
        )
        self.remove(flag)
        self.add(top_row[1])
        self.play(
            LaggedStartMap(FadeIn, title_row[2:]),
            LaggedStartMap(FadeIn, top_row[2:]),
        )
        self.wait()
        self.play(
            LaggedStart(*[
                FadeIn(row, UP)
                for row in grid.rows[2:4]
            ]),
            LaggedStart(*[
                ShowCreation(line)
                for line in grid.h_lines[:2]
            ]),
            lag_ratio=0.5,
        )
        self.wait()
        self.play(
            ShowCreationThenFadeAround(
                Group(title_row[3], grid.rows[3][3]),
            )
        )
        self.wait()
        student_counter.clear_updaters()
        self.play(
            FadeOut(self.title, UP),
            FadeOut(student_counter, UP),
            grid.rows[:4].shift, 3 * UP,
            grid.h_lines[:3].shift, 3 * UP,
        )
        remaining_rows = grid.rows[4:]
        remaining_lines = grid.h_lines[3:]
        Group(remaining_rows, remaining_lines).shift(3 * UP)
        self.play(
            LaggedStartMap(
                FadeInFrom, remaining_rows,
                lambda m: (m, UP),
            ),
            LaggedStartMap(ShowCreation, remaining_lines),
            lag_ratio=0.3,
            run_time=2,
        )
        self.wait()

    def get_score_grid(self):
        data = self.student_data

        ranks = VGroup(*[
            Integer(row[0])
            for row in data
        ])

        # Combine students with flags
        students = VGroup(*[
            OldTexText(row[1])
            for row in data
        ])
        flags = Group(*[
            ImageMobject("flags/{}.png".format(row[2])).set_height(0.3)
            for row in data
        ])
        students = Group(*[
            Group(flag.next_to(student, LEFT, buff=0.2), student)
            for flag, student in zip(flags, students)
        ])

        score_rows = VGroup(*[
            VGroup(*map(Integer, row[3]))
            for row in data
        ])
        colors = color_gradient([RED, YELLOW, GREEN], 8)
        for score_row in score_rows:
            for score in score_row:
                score.set_color(colors[score.get_value()])

        titles = VGroup(*[
            VectorizedPoint(),
            VectorizedPoint(),
            *[
                OldTexText("P{}".format(i))
                for i in range(1, 7)
            ]
        ])
        titles.arrange(RIGHT, buff=MED_LARGE_BUFF)
        titles[2:].shift(students.get_width() * RIGHT)
        rows = Group(titles, *[
            Group(rank, student, *score_row)
            for rank, flag, student, score_row in zip(
                ranks, flags, students, score_rows
            )
        ])
        rows.arrange(DOWN)
        rows.to_edge(UP)
        for row in rows:
            for i, e1, e2 in zip(it.count(), titles, row):
                if i < 2:
                    e2.align_to(e1, LEFT)
                else:
                    e2.match_x(e1)
        ranks.next_to(students, LEFT)

        h_lines = VGroup()
        for r1, r2 in zip(rows[1:], rows[2:]):
            line = Line()
            line.set_stroke(WHITE, 0.5)
            line.match_width(r2)
            line.move_to(midpoint(r1.get_bottom(), r2.get_top()))
            line.align_to(r2, LEFT)
            h_lines.add(line)

        grid = Group(rows, h_lines)
        grid.rows = rows
        grid.h_lines = h_lines

        return grid
