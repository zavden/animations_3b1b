# ==============================================================================
# Scene:      ShowTinyTao
# Source:     videos/_2019/windmill.py (lines 268-296)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowTinyTao.py ShowTinyTao -w -m --fps 15
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


class ShowTinyTao(IntroduceIMO):
    CONFIG = {
        "reorganize_students": False,
    }

    def construct(self):
        self.force_skipping()
        self.add_title()
        self.show_flags()
        self.show_students()
        self.revert_to_original_skipping_status()

        image = ImageMobject("TerryTaoIMO")
        label = OldTexText("Terence Tao at 12")
        label.match_width(image)
        label.next_to(image, DOWN, SMALL_BUFF)
        image.add(label)

        ausie = self.flags[17]
        image.replace(ausie)
        image.set_opacity(0)

        self.play(image.set_opacity, 1)
        self.play(
            image.set_height, 5,
            image.to_corner, DR, {"buff": MED_SMALL_BUFF},
        )
        self.wait()
        self.play(FadeOut(image))
