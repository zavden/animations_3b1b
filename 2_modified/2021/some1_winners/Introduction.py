# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2021/some1_winners.py (lines 91-306)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument: Logo.add_pupil is redefined without sheen in the scene.
#   - LaggedStartMap(Anim, group, arg_creator, ...): the third argument `arg_creator` no longer exists; a lambda m: Anim(m, ...) is passed as anim_func.
#
# Placeholder assets (not Grant's originals):
#   - Placeholder Leios.png (512x512) in _lib/assets/raster_images/ (make_some1_assets.py)
#
# Notes:
#   No published video: with the current manimgl fork it fails in VMobject.insert_n_curves_to_point_list (align_points); it used to render. Known problem.
# ==============================================================================

from manim_imports_ext import *


# CHANGE: Logo (_lib/custom/logo.py) passes sheen=0.0 to Circle and manimgl no longer has that argument (TypeError); add_pupil is redefined without sheen
class Logo(Logo):
    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            stroke_color=BLACK,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)


class Introduction(TeacherStudentsScene):
    def construct(self):
        # Kill background
        self.clear()
        morty = self.teacher

        # Add title
        this_summer = Text("This Summer", font_size=72)
        this = this_summer.get_part_by_text("This")
        summer = this_summer.get_part_by_text("Summer")
        this_summer.to_edge(UP)
        some = Text("Summer of Math Exposition", font_size=72)
        some.to_edge(UP)
        some.shift(0.7 * RIGHT)
        this_summer.generate_target()
        this_summer.target.shift(some[0].get_left() - summer[0].get_left())

        logos = Group(
            ImageMobject("Leios"),
            Logo(),
        )
        for logo in logos:
            logo.set_height(1.0)
        logos.arrange(RIGHT, buff=2)
        logos.next_to(this_summer.target, RIGHT, buff=1.5)
        james_name = Text("James Schloss")
        james_name.set_color(GREY_A)
        james_name.next_to(logos[0], DOWN)

        logos.generate_target()
        logos.target.set_height(0.5)
        logos.target.arrange(RIGHT, buff=0.25)
        logos.target.replace(this_summer.target[:4], 0)

        self.add(this)
        self.wait(0.3)
        self.add(summer)
        self.wait(0.5)
        self.play(
            MoveToTarget(this_summer),
            FadeIn(james_name, lag_ratio=0.1),
            FadeIn(logos[0], LEFT),
        )
        self.play(
            Write(logos[1], lag_ratio=0.01, stroke_width=0.05, run_time=1),
            Animation(logos[1][-1].copy(), remover=True),
            FadeOut(james_name),
        )
        self.wait()
        self.play(
            FadeIn(some[len("Summer"):], lag_ratio=0.1),
            FadeOut(this),
            MoveToTarget(logos, path_arc=-PI / 3, run_time=2)
        )
        self.remove(this_summer)
        self.add(some)
        self.wait()

        title = Group(logos, some)

        # Mention blog post
        url = VGroup(
            Text("Full details: "),
            Text("https://3b1b.co/some1-results")
        )
        url[1].set_color(BLUE_C)
        url.arrange(RIGHT)
        url[0].shift(0.05 * UP)
        url.to_edge(UP)

        self.play(
            FadeOut(title, UP),
            FadeIn(url[0]),
            ShowIncreasingSubsets(url[1], rate_func=linear, run_time=2)
        )
        self.wait()

        # Key points
        dots = Dot().get_grid(3, 1)
        dots.arrange(DOWN, buff=1.5)
        dots.align_to(url, LEFT)
        dots.set_y(-0.5)

        points = VGroup(
            Text("Extremely open-ended"),
            Text("Promise to feature 4 to 5 winners"),
            Text("Brilliant offered $5k in cash prizes"),
        )
        colors = [GREEN_A, GREEN_B, GREEN_C]

        for dot, point, color in zip(dots, points, colors):
            point.next_to(dot, RIGHT)
            point.set_color(color)

        self.play(
            # CHANGE: LaggedStartMap no longer has the third argument arg_creator; a lambda is passed as anim_func
            LaggedStartMap(
                lambda m: FadeInFromPoint(m, url.get_bottom()), dots,
            ),
        )
        self.wait()

        for point in points:
            self.play(Write(point))
            if point is points[1]:
                self.play(
                    morty.change("hooray").look(ORIGIN),
                    FadeOut(BackgroundRectangle(morty, buff=0.25, fill_opacity=1))
                )
                self.play(Blink(morty))
                self.play(morty.change("tease", points[2]))
            else:
                self.wait()

        # Discuss winner
        winner_word = OldTexText("``Winners''", font_size=72)[0]
        winner_word.move_to(self.hold_up_spot, DOWN)
        pre_winner_word = points[1].get_part_by_text("winner").copy()

        self.students.flip().flip()

        self.add(self.background, pre_winner_word, *self.pi_creatures)
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                url, dots, points,
            )),
            FadeIn(self.background),
            morty.change("hesitant", winner_word),
            FadeTransform(pre_winner_word, winner_word[2:9]),
            LaggedStartMap(FadeIn, self.students),
        )
        self.play(
            Write(winner_word[:2]),
            Write(winner_word[-2:]),
            self.change_students("sassy", "raise_right_hand", "raise_left_hand"),
        )
        self.wait(4)

        # Spirit of the event (start at 25)
        salt = Text("Take with a grain of salt")
        salt.to_edge(UP)
        strange = Text("(what a strange phrase...)", font_size=20)
        strange.set_color(GREY_B)
        strange.next_to(salt, RIGHT)
        arrow = Arrow(salt, winner_word)

        self.play(
            FadeIn(salt, lag_ratio=0.1),
            ShowCreation(arrow),
            self.change_students(
                "pondering", "pondering", "erm",
                look_at=salt,
            )
        )
        self.play(
            Blink(self.students[2]),
            FadeIn(strange, lag_ratio=0.1),
        )
        self.play(FadeOut(strange))
        self.wait()

        spirit = Text("The spirit of the event")
        spirit.to_edge(UP)
        bubble = ThoughtBubble(height=3, width=3)
        bubble.pin_to(self.students[0])
        bubble.shift(SMALL_BUFF * UR)
        bubble.add_content(OldTex(
            r"|fg|_1 \leq |f|_p |g|_q",
            tex_to_color_map={
                "f": GREEN,
                "g": TEAL,
            }
        ))
        bubble.add(bubble.content)
        arrow.target = Arrow(spirit, bubble)
        video = VideoIcon()
        video.set_height(0.7)
        video.next_to(self.students, UP, MED_LARGE_BUFF).to_edge(LEFT)
        video.set_color(GREY_C)
        video.set_gloss(1)

        self.play(
            FadeOut(salt, 0.5 * UP),
            FadeIn(spirit, 0.5 * UP),
        )
        self.play(
            MoveToTarget(arrow),
            FadeIn(bubble),
            self.students[0].change("thinking", bubble),
            self.students[1].change("pondering", bubble),
            self.students[2].change("pondering", bubble),
            self.teacher.change("happy", bubble),
            winner_word.animate.scale(0.3).set_opacity(0.5).to_corner(UR),
        )
        self.play(
            self.students[0].change("raise_left_hand", video),
            FadeIn(video, 0.5 * UP),
        )
        self.wait()

        bubble_copies = bubble.replicate(2).scale(0.7)
        for bc, student in zip(bubble_copies, self.students[1:]):
            bc.move_to(student.get_corner(UR), DL)

        self.play(
            LaggedStart(*(
                TransformFromCopy(bubble, bc)
                for bc in bubble_copies
            ), lag_ratio=0.5),
            LaggedStart(*(
                student.change("thinking", UR)
                for student in self.students[1:]
            ), lag_ratio=0.5),
            run_time=2,
        )
        self.wait(3)
