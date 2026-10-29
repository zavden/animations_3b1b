# ==============================================================================
# Scene:      USProcessAlt
# Source:     videos/_2019/windmill.py (lines 444-710)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl USProcessAlt.py USProcessAlt -w -m --fps 15
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


class USProcessAlt(IntroduceIMO):
    CONFIG = {
    }

    def construct(self):
        self.add_flag_and_label()
        self.show_tests()
        self.show_imo()

    def add_flag_and_label(self):
        flag = ImageMobject("flags/us")
        flag.set_height(1)
        flag.to_corner(UL)
        label = VGroup(*map(TexText, "USA"))
        label.arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        label.set_width(0.8 * flag.get_width())
        label.next_to(flag, DOWN, buff=0.2 * flag.get_height())

        self.add(flag, label)

        self.flag = flag

    def show_tests(self):
        tests = VGroup(
            self.get_test(
                ["American ", "Mathematics ", "Contest"],
                n_questions=25,
                time_string="75 minutes",
                hours=1.25,
                n_students=250000,
            ),
            self.get_test(
                ["American ", "Invitational ", "Math ", "Exam"],
                n_questions=15,
                time_string="3 hours",
                hours=3,
                n_students=12000,
            ),
            self.get_test(
                ["U", "S", "A ", "Math ", "Olympiad"],
                n_questions=6,
                time_string="$2 \\times 4.5$ hours",
                hours=4.5,
                n_students=500,
            ),
            self.get_test(
                ["Mathematical ", "Olympiad ", "Program"],
                n_questions=None,
                time_string="3 weeks",
                hours=None,
                n_students=60
            )
        )
        amc, aime, usamo, mop = tests
        arrows = VGroup()

        amc.to_corner(UR)
        top_point = amc.get_top()
        last_arrow = VectorizedPoint()
        last_arrow.to_corner(DL)
        next_anims = []

        self.force_skipping()
        for test in tests:
            test.move_to(top_point, UP)
            test.shift_onto_screen()
            self.play(
                Write(test.name),
                *next_anims,
                run_time=1,
            )
            self.wait()
            self.animate_name_abbreviation(test)
            self.wait()

            if isinstance(test.nq_label[0], Integer):
                int_mob = test.nq_label[0]
                n = int_mob.get_value()
                int_mob.set_value(0)
                self.play(
                    ChangeDecimalToValue(int_mob, n),
                    FadeIn(test.nq_label[1:])
                )
            else:
                self.play(FadeIn(test.nq_label))

            self.play(
                FadeIn(test.t_label)
            )
            self.wait()

            test.generate_target()
            test.target.scale(0.575)
            test.target.next_to(last_arrow, RIGHT, buff=SMALL_BUFF)
            test.target.shift_onto_screen()

            next_anims = [
                MoveToTarget(test),
                GrowArrow(last_arrow),
            ]
            last_arrow = Vector(0.5 * RIGHT)
            last_arrow.set_color(WHITE)
            last_arrow.next_to(test.target, RIGHT, SMALL_BUFF)
            arrows.add(last_arrow)
        self.play(*next_anims)

        self.revert_to_original_skipping_status()
        self.play(
            LaggedStartMap(
                FadeInFrom, tests,
                lambda m: (m, LEFT),
            ),
            LaggedStartMap(
                GrowArrow, arrows[:-1]
            ),
            lag_ratio=0.4,
        )
        self.wait()

        self.tests = tests

    def show_imo(self):
        tests = self.tests
        logo = ImageMobject("imo_logo")
        logo.set_height(1)
        name = OldTexText("IMO")
        name.scale(2)
        group = Group(logo, name)
        group.arrange(RIGHT)
        group.to_corner(UR)
        group.shift(2 * LEFT)

        students = VGroup(*[
            PiCreature()
            for x in range(6)
        ])
        students.arrange_in_grid(n_cols=3, buff=LARGE_BUFF)
        students.set_height(2)
        students.next_to(group, DOWN)
        colors = it.cycle([RED, GREY_B, BLUE])
        for student, color in zip(students, colors):
            student.set_color(color)
            student.save_state()
            student.move_to(tests[-1])
            student.fade(1)

        self.play(
            FadeInFromDown(group),
            LaggedStartMap(
                Restore, students,
                run_time=3,
                lag_ratio=0.3,
            )
        )
        self.play(
            LaggedStart(*[
                ApplyMethod(student.change, "hooray")
                for student in students
            ])
        )
        for x in range(3):
            self.play(Blink(random.choice(students)))
        self.wait()

    #
    def animate_name_abbreviation(self, test):
        name = test.name
        short_name = test.short_name
        short_name.move_to(name, LEFT)
        name.generate_target()
        for p1, p2 in zip(name.target, short_name):
            for letter in p1:
                letter.move_to(p2[0])
                letter.set_opacity(0)
            p1[0].set_opacity(1)
        self.add(test.rect, test.name, test.ns_label)
        self.play(
            FadeIn(test.rect),
            MoveToTarget(name),
            FadeIn(test.ns_label),
        )

        test.remove(name)
        test.add(short_name)
        self.remove(name)
        self.add(short_name)

    def get_test(self, name_parts, n_questions, time_string, hours, n_students):
        T_COLOR = GREEN_B
        Q_COLOR = YELLOW

        name = OldTexText(*name_parts)
        short_name = OldTexText(*[np[0] for np in name_parts])
        if n_questions:
            nq_label = VGroup(
                Integer(n_questions),
                OldTexText("questions")
            )
            nq_label.arrange(RIGHT)
        else:
            nq_label = OldTexText("Lots of training")
        nq_label.set_color(Q_COLOR)

        if time_string:
            t_label = OldTexText(time_string)
            t_label.set_color(T_COLOR)
        else:
            t_label = Integer(0).set_opacity(0)

        clock = Clock()
        clock.hour_hand.set_opacity(0)
        clock.minute_hand.set_opacity(0)
        clock.set_stroke(WHITE, 2)
        if hours:
            sector = Sector(
                start_angle=TAU / 4,
                angle=-TAU * (hours / 12),
                outer_radius=clock.get_width() / 2,
                arc_center=clock.get_center()
            )
            sector.set_fill(T_COLOR, 0.5)
            sector.set_stroke(T_COLOR, 2)
            clock.add(sector)
            if hours == 4.5:
                plus = OldTex("+").scale(2)
                plus.next_to(clock, RIGHT)
                clock_copy = clock.copy()
                clock_copy.next_to(plus, RIGHT)
                clock.add(plus, clock_copy)
        else:
            clock.set_opacity(0)
        clock.set_height(1)
        clock.next_to(t_label, RIGHT, buff=MED_LARGE_BUFF)
        t_label.add(clock)

        ns_label = OldTexText("$\\sim${:,} students".format(n_students))

        result = VGroup(
            name,
            nq_label,
            t_label,
            ns_label,
        )
        result.arrange(
            DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        rect = SurroundingRectangle(result, buff=MED_SMALL_BUFF)
        rect.set_width(
            result[1:].get_width() + MED_LARGE_BUFF,
            about_edge=LEFT,
            stretch=True,
        )
        rect.set_stroke(WHITE, 2)
        rect.set_fill(BLACK, 1)
        result.add_to_back(rect)

        result.name = name
        result.short_name = short_name
        result.nq_label = nq_label
        result.t_label = t_label
        result.ns_label = ns_label
        result.rect = rect
        result.clock = clock

        return result
