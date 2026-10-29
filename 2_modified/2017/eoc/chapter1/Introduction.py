# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2017/eoc/chapter1.py (lines 271-440)
# Category:   2 · Renders with modifications
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

class Introduction(TeacherStudentsScene):
    def construct(self):
        goals = OldTexText(
            "Goals: ",
            "1) Learn derivatives", 
            ", 2) Avoid paradoxes.",
            arg_separator = ""
        )
        goals[1].set_color(MAROON_B)
        goals[2].set_color(RED)
        goals[2][0].set_color(WHITE)
        goals.to_edge(UP)
        self.add(*goals[:2])

        self.student_says(
            "What is a derivative?",
            run_time = 2
        )
        self.play(self.get_teacher().change_mode, "happy")
        self.wait()
        self.teacher_says(
            "It's actually a \\\\",
            "very subtle idea",
            target_mode = "well"
        )
        self.play_student_changes(None, "pondering", "thinking")
        self.play(Write(goals[2], run_time = 2))
        self.play_student_changes("erm")
        self.student_says(
            "Instantaneous rate of change", "?",
            index = 0,
        )
        self.wait()

        bubble = self.get_students()[0].bubble
        phrase = bubble.content[0]
        bubble.content.remove(phrase)
        self.play(
            FadeOut(bubble),
            FadeOut(bubble.content),
            FadeOut(goals),
            phrase.center,
            phrase.scale, 1.5,
            phrase.to_edge, UP,
            *it.chain(*[
                [
                    pi.change_mode, mode,
                    pi.look_at, FRAME_Y_RADIUS*UP
                ]
                for pi, mode in zip(self.get_pi_creatures(), [
                    "speaking", "pondering", "confused", "confused",
                ])
            ])
        )
        self.wait()
        change = VGroup(*phrase[-len("change"):])
        instantaneous = VGroup(*phrase[:len("instantaneous")])
        change_brace = Brace(change)
        change_description = change_brace.get_text(
            "Requires multiple \\\\ points in time"
        )
        instantaneous_brace = Brace(instantaneous)
        instantaneous_description = instantaneous_brace.get_text(
            "One point \\\\ in time"
        )
        clock = Clock()
        clock.next_to(change_description, DOWN)
        def get_clock_anim(run_time = 3):
            return ClockPassesTime(
                clock,
                hours_passed = 0.4*run_time,
                run_time = run_time,
            )
        self.play(FadeIn(clock))
        self.play(
            change.set_color_by_gradient, BLUE, YELLOW,
            GrowFromCenter(change_brace),
            Write(change_description),
            get_clock_anim()
        )
        self.play(get_clock_anim(1))
        stopped_clock = clock.copy()
        stopped_clock.next_to(instantaneous_description, DOWN)
        self.play(
            instantaneous.set_color, BLUE,
            GrowFromCenter(instantaneous_brace),
            Transform(change_description.copy(), instantaneous_description),
            clock.copy().next_to, instantaneous_description, DOWN,
            get_clock_anim(3)
        )
        self.play(get_clock_anim(12))



# ----- From _2017/eoc/chapter1.py -----

class Introduction(TeacherStudentsScene):
    def construct(self):
        self.show_series()
        self.show_many_facts()
        self.invent_calculus()

    def show_series(self):
        series = VideoSeries()
        series.to_edge(UP)
        this_video = series[0]
        this_video.set_color(YELLOW)
        this_video.save_state()
        this_video.set_fill(opacity = 0)
        this_video.center()
        this_video.set_height(FRAME_HEIGHT)
        self.this_video = this_video


        words = OldTexText(
            "Welcome to \\\\",
            "Essence of calculus"
        )
        words.set_color_by_tex("Essence of calculus", YELLOW)

        self.teacher.change_mode("happy")
        self.play(
            FadeIn(
                series,
                lag_ratio = 0.5,
                run_time = 2
            ),
            Blink(self.get_teacher())
        )
        self.teacher_says(words, target_mode = "hooray")
        self.play_student_changes(
            *["hooray"]*3,
            look_at = series[1].get_left(),
            added_anims = [
                ApplyMethod(this_video.restore, run_time = 3),
            ]
        )
        self.play(*[
            ApplyMethod(
                video.shift, 0.5*video.get_height()*DOWN,
                run_time = 3,
                rate_func = squish_rate_func(
                    there_and_back, alpha, alpha+0.3
                )
            )
            for video, alpha in zip(series, np.linspace(0, 0.7, len(series)))
        ]+[
            Animation(self.teacher.bubble),
            Animation(self.teacher.bubble.content),
        ])

        essence_words = words.get_part_by_tex("Essence").copy()
        self.play(
            FadeOut(self.teacher.bubble),
            FadeOut(self.teacher.bubble.content),
            essence_words.next_to, series, DOWN,
            *[
                ApplyMethod(pi.change_mode, "pondering")
                for pi in self.get_pi_creatures()
            ]
        )
        self.wait(3)

        self.series = series
        self.essence_words = essence_words

    def show_many_facts(self):
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        rules = list(it.starmap(OldTex, [
            ("{d(", "x", "^2)", "\\over \\,", "dx}", "=", "2", "x"),
            (
                "d(", "f", "g", ")", "=", 
                "f", "dg", "+", "g", "df",
            ),
            (
                "F(x)", "=", "\\int_0^x", 
                "\\frac{dF}{dg}(t)\\,", "dt"
            ),
            (
                "f(x)", "=", "\\sum_{n = 0}^\\infty",
                "f^{(n)}(a)", "\\frac{(x-a)^n}{n!}"
            ),
        ]))
        video_indices = [2, 3, 7, 10]
        tex_to_color = [
            ("x", BLUE),
            ("f", BLUE),
            ("df", BLUE),
            ("g", YELLOW),
            ("dg", YELLOW),
            ("f(x)", BLUE),
            ( "f^{(n)}(a)", BLUE),
        ]

        for rule in rules:
            for tex, color in tex_to_color:
                rule.set_color_by_tex(tex, color, substring = False)
            rule.next_to(self.teacher.get_corner(UP+LEFT), UP)
            rule.shift_onto_screen()

        index = 1
        student = self.get_students()[index]
        self.play_student_changes(
            "pondering", "sassy", "pondering",
            look_at = self.teacher.eyes,
            added_anims = [
                self.teacher.change_mode, "plain"
            ]
        )
        self.wait(2)
        self.play(
            Write(rules[0]),
            self.teacher.change_mode, "raise_right_hand",
        )
        self.wait()
        alt_rules_list = list(rules[1:]) + [VectorizedPoint(self.teacher.eyes.get_top())]
        for last_rule, rule, video_index in zip(rules, alt_rules_list, video_indices):
            video = self.series[video_index]
            self.play(
                last_rule.replace, video,
                FadeIn(rule),
            )
            self.play(Animation(rule))
            self.wait()
        self.play(
            self.teacher.change_mode, "happy",
            self.teacher.look_at, student.eyes
        )

    def invent_calculus(self):
        student = self.get_students()[1]
        creatures = self.get_pi_creatures()
        creatures.remove(student)
        creature_copies = creatures.copy()
        self.remove(creatures)
        self.add(creature_copies)

        calculus = VGroup(*self.essence_words[-len("calculus"):])
        calculus.generate_target()
        invent = OldTexText("Invent")
        invent_calculus = VGroup(invent, calculus.target)
        invent_calculus.arrange(RIGHT, buff = MED_SMALL_BUFF)
        invent_calculus.next_to(student, UP, 1.5*LARGE_BUFF)
        invent_calculus.shift(RIGHT)
        arrow = Arrow(invent_calculus, student)

        fader = Rectangle(
            width = FRAME_WIDTH,
            height = FRAME_HEIGHT,
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.5,
        )

        self.play(
            FadeIn(fader),
            Animation(student),
            Animation(calculus)
        )
        self.play(
            Write(invent),
            MoveToTarget(calculus),
            student.change_mode, "erm",
            student.look_at, calculus
        )
        self.play(ShowCreation(arrow))
        self.wait(2)
