# ==============================================================================
# Scene:      IntroduceTotientJargon
# Source:     videos/_2019/spirals.py (lines 2537-2775)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceTotientJargon.py IntroduceTotientJargon -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Disable draw_together only in this scene to avoid the misaligned GPU storage offsets of the fork.
# ==============================================================================

from manim_imports_ext import *

class IntroduceTotientJargon(TeacherStudentsScene):
    # CHANGE: avoid the fork's misaligned GPU offsets when batching mixed objects.
    default_camera_config = dict(TeacherStudentsScene.default_camera_config, draw_together=False)

    def construct(self):
        self.add_title()
        self.eliminate_non_coprimes()

    def add_title(self):
        self.teacher_says(
            "More jargon!",
            target_mode="hooray",
        )
        self.play_all_student_changes("erm")
        words = self.teacher.bubble.content

        words.generate_target()
        words.target.scale(1.5)
        words.target.center().to_edge(UP, buff=MED_SMALL_BUFF)
        words.target.set_color(BLUE)
        underline = Line(LEFT, RIGHT)
        underline.match_width(words.target)
        underline.next_to(words.target, DOWN, SMALL_BUFF)
        underline.scale(1.2)

        self.play(
            MoveToTarget(words),
            FadeOut(self.teacher.bubble),
            LaggedStart(*[
                FadeOut(pi, 4 * DOWN)
                for pi in self.pi_creatures
            ]),
            ShowCreation(underline)
        )

    def eliminate_non_coprimes(self):
        number_grid = VGroup(*[
            VGroup(*[
                Integer(n) for n in range(11 * k, 11 * (k + 1))
            ]).arrange(DOWN)
            for k in range(4)
        ]).arrange(RIGHT, buff=1)
        numbers = VGroup(*it.chain(*number_grid))
        numbers.set_height(6)
        numbers.move_to(4 * LEFT)
        numbers.to_edge(DOWN)

        evens = VGroup(*filter(
            lambda nm: nm.get_value() % 2 == 0,
            numbers
        ))
        div11 = VGroup(*filter(
            lambda nm: nm.get_value() % 11 == 0,
            numbers
        ))
        coprimes = VGroup(*filter(
            lambda nm: nm not in evens and nm not in div11,
            numbers
        ))

        words = OldTexText(
            "Which ones ", "don't\\\\",
            "share any factors\\\\",
            "with ", "44",
            alignment=""
        )
        words.scale(1.5)
        words.next_to(ORIGIN, RIGHT)

        ff = words.get_part_by_tex("44")
        ff.set_color(YELLOW)
        ff.generate_target()

        # Show coprimes
        self.play(
            ShowIncreasingSubsets(numbers, run_time=3),
            FadeIn(words, LEFT)
        )
        self.wait()
        for group in evens, div11:
            rects = VGroup(*[
                SurroundingRectangle(number, color=RED)
                for number in group
            ])
            self.play(LaggedStartMap(ShowCreation, rects, run_time=1))
            self.play(
                LaggedStart(*[
                    ApplyMethod(number.set_opacity, 0.2)
                    for number in group
                ]),
                LaggedStartMap(FadeOut, rects),
                run_time=1
            )
            self.wait()

        # Rearrange words
        dsf = words[1:3]
        dsf.generate_target()
        dsf.target.arrange(RIGHT)
        dsf.target[0].align_to(dsf.target[1][0], DOWN)

        example = numbers[35].copy()
        example.generate_target()
        example.target.match_height(ff)
        num_pair = VGroup(
            ff.target,
            OldTexText("and").scale(1.5),
            example.target,
        )
        num_pair.arrange(RIGHT)
        num_pair.move_to(words.get_top(), DOWN)
        dsf.target.next_to(num_pair, DOWN, MED_LARGE_BUFF)

        phrase1 = OldTexText("are ", "``relatively prime''")
        phrase2 = OldTexText("are ", "``coprime''")
        for phrase in phrase1, phrase2:
            phrase.scale(1.5)
            phrase.move_to(dsf.target)
            phrase[1].set_color(BLUE)
            phrase.arrow = OldTex("\\Updownarrow")
            phrase.arrow.scale(1.5)
            phrase.arrow.next_to(phrase, DOWN, 2 * SMALL_BUFF)
            phrase.rect = SurroundingRectangle(phrase[1])
            phrase.rect.set_stroke(BLUE)

        self.play(
            FadeOut(words[0]),
            FadeOut(words[3]),
            MoveToTarget(dsf),
            MoveToTarget(ff),
            GrowFromCenter(num_pair[1]),
        )
        self.play(
            MoveToTarget(example, path_arc=30 * DEGREES),
        )
        self.wait()
        self.play(
            dsf.next_to, phrase1.arrow, DOWN, SMALL_BUFF,
            GrowFromEdge(phrase1.arrow, UP),
            GrowFromCenter(phrase1),
            ShowCreation(phrase1.rect)
        )
        self.play(FadeOut(phrase1.rect))
        self.wait()
        self.play(
            VGroup(dsf, phrase1, phrase1.arrow).next_to,
            phrase2.arrow, DOWN, SMALL_BUFF,
            GrowFromEdge(phrase2.arrow, UP),
            GrowFromCenter(phrase2),
            ShowCreation(phrase2.rect)
        )
        self.play(FadeOut(phrase2.rect))
        self.wait()

        # Count through coprimes
        coprime_rects = VGroup(*map(SurroundingRectangle, coprimes))
        coprime_rects.set_stroke(BLUE, 2)
        example_anim = UpdateFromFunc(
            example, lambda m: m.set_value(coprimes[len(coprime_rects) - 1].get_value())
        )
        self.play(
            ShowIncreasingSubsets(coprime_rects, int_func=np.ceil),
            example_anim,
            run_time=3,
            rate_func=linear,
        )
        self.wait()

        # Show totient function
        words_to_keep = VGroup(ff, num_pair[1], example, phrase2)
        to_fade = VGroup(phrase2.arrow, phrase1, phrase1.arrow, dsf)

        totient = OldTex("\\phi", "(", "44", ")", "=", "20")
        totient.set_color_by_tex("44", YELLOW)
        totient.scale(1.5)
        totient.move_to(num_pair, UP)
        phi = totient.get_part_by_tex("phi")
        rhs = Integer(20)
        rhs.replace(totient[-1], dim_to_match=1)
        totient.submobjects[-1] = rhs

        self.play(
            words_to_keep.to_edge, DOWN,
            MaintainPositionRelativeTo(to_fade, words_to_keep),
            VFadeOut(to_fade),
        )
        self.play(FadeIn(totient))
        self.wait()

        # Label totient
        brace = Brace(phi, DOWN)
        etf = OldTexText("Euler's totient function")
        etf.next_to(brace, DOWN)
        etf.shift(RIGHT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(etf, UP)
        )
        self.wait()
        self.play(
            ShowIncreasingSubsets(coprime_rects),
            UpdateFromFunc(
                rhs, lambda m: m.set_value(len(coprime_rects)),
            ),
            example_anim,
            rate_func=linear,
            run_time=3,
        )
        self.wait()

        # Show totatives
        totient_group = VGroup(totient, brace, etf)
        for cp, rect in zip(coprimes, coprime_rects):
            cp.add(rect)

        self.play(
            coprimes.arrange, RIGHT, {"buff": SMALL_BUFF},
            coprimes.set_width, FRAME_WIDTH - 1,
            coprimes.move_to, 2 * UP,
            FadeOut(evens),
            FadeOut(div11[1::2]),
            FadeOutAndShiftDown(words_to_keep),
            totient_group.center,
            totient_group.to_edge, DOWN,
        )

        totatives = OldTexText("``Totatives''")
        totatives.scale(2)
        totatives.set_color(BLUE)
        totatives.move_to(ORIGIN)
        arrows = VGroup(*[
            Arrow(totatives.get_top(), coprime.get_bottom())
            for coprime in coprimes
        ])
        arrows.set_color(WHITE)

        self.play(
            FadeIn(totatives),
            LaggedStartMap(VFadeInThenOut, arrows, run_time=4, lag_ratio=0.05)
        )
        self.wait(2)
