# ==============================================================================
# Scene:      PermutationGroups
# Source:     videos/_2020/monster.py (lines 1045-1334)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PermutationGroups.py PermutationGroups -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - unlock_unit_normal no longer exists (normals are no longer locked)
# ==============================================================================

from manim_imports_ext import *

def get_permutation_arrows(mobs, permutation, arc=PI / 2):
    arrows = VGroup()
    for i in range(len(permutation)):
        j = permutation[i]
        u = -1 if mobs[i].get_x() < mobs[j].get_x() else 1
        arrow = Arrow(
            mobs[i].get_edge_center(u * UP),
            mobs[j].get_edge_center(u * UP),
            buff=SMALL_BUFF,
            path_arc=arc,
        )
        arrow.insert_n_curves(10)
        arrow.set_stroke(BLACK, 2, background=True)
        arrow.set_fill(BLUE, 0.8)
        arrows.add(arrow)
    return arrows


def permutation_animation(mobs, perm=None, arc=PI / 2, lag_factor=3, run_time=None):
    if perm is None:
        targets = list(mobs)
        random.shuffle(targets)
    else:
        targets = [mobs[i] for i in perm]

    kw = {"lag_ratio": lag_factor / len(mobs)}
    if run_time is not None:
        kw["run_time"] = run_time
    return LaggedStart(
        *[
            ApplyMethod(m1.move_to, m2, path_arc=arc)
            for m1, m2 in zip(mobs, targets)
        ],
        **kw
    )


class PermutationGroups(Scene):
    def construct(self):
        # Setup
        question = OldTexText("What about no structure?")
        question.scale(1.5)
        question.to_edge(UP)

        perm_words = OldTexText("All ", "permutations")
        perm_words.scale(1.5)
        perm_words.next_to(question, DOWN, buff=0.7)
        perm_words.set_color(BLUE)

        dots = VGroup(*[Dot() for x in range(6)])
        dots.set_fill(GREY_B)
        dots.set_height(0.5)
        dots.arrange(RIGHT, buff=LARGE_BUFF)
        dots.shift(DOWN)
        alt_dots = dots.copy()

        self.add(question)
        self.play(ShowIncreasingSubsets(dots))

        # Permutations
        def get_permutation(self=self, dots=dots, arc=PI / 2):
            perm = list(range(len(dots)))
            random.shuffle(perm)
            arrows = get_permutation_arrows(dots, perm, arc)
            for i, dot in enumerate(dots):
                dot.target = dots[perm[i]]

            arrows.set_opacity(0)
            return Succession(
                UpdateFromAlphaFunc(arrows, lambda m, a: m.set_opacity(a)),
                LaggedStartMap(MoveToTarget, dots, path_arc=arc, lag_ratio=0.15, run_time=2),
                UpdateFromAlphaFunc(arrows, lambda m, a: m.set_opacity(1 - a)),
            )

        permutations = Succession(*[
            get_permutation()
            for x in range(20)
        ])
        animated_perm_mob = cycle_animation(permutations)
        self.add(animated_perm_mob)
        self.wait(5)
        self.play(FadeIn(perm_words, UP))
        self.wait(10)

        # Count perms
        perm_count = OldTex("6!")
        perm_count.match_height(perm_words[0])
        perm_count.match_color(perm_words[0])
        perm_count.move_to(perm_words[0], RIGHT)
        full_count = Integer(720, edge_to_fix=RIGHT)
        full_count.match_height(perm_count)
        full_count.move_to(perm_count, DR)
        full_count.shift(0.7 * RIGHT)
        full_count.match_color(perm_count)
        equals = OldTex("=")
        equals.scale(1.5)
        equals.next_to(full_count, LEFT)
        equals.match_color(perm_count)
        perm_count.next_to(equals, LEFT)
        full_count.set_value(0)

        self.remove(animated_perm_mob)
        dots = alt_dots
        self.add(alt_dots)
        self.play(
            FadeIn(full_count, LEFT),
            FadeOut(perm_words[0], RIGHT),
            perm_words[1].shift, 0.7 * RIGHT,
        )

        all_perms = list(it.permutations(range(6)))
        arrows = VGroup()
        self.add(arrows)
        self.play(
            ChangeDecimalToValue(full_count, 720),
            UpdateFromAlphaFunc(
                arrows,
                lambda m, a, dots=dots, all_perms=all_perms: m.set_submobjects(
                    get_permutation_arrows(dots, all_perms[int(np.round(719 * a))])
                )
            ),
            run_time=20,
        )
        self.play(
            FadeIn(perm_count, RIGHT),
            Write(equals),
        )
        self.wait(2)

        perm_label = VGroup(perm_count, equals, full_count, perm_words[1])

        # Revisit snowflake symmetries
        dots.generate_target()
        for dot, point in zip(dots.target, compass_directions(6, UP)):
            dot.move_to(2 * point)

        self.play(
            FadeOut(arrows),
            FadeOut(perm_label, UP),
            FadeOut(question, 0.5 * UP),
            MoveToTarget(dots),
        )

        lines = VGroup()
        for d1, d2 in it.combinations(dots, 2):
            lines.add(Line(
                d1.get_center(),
                d2.get_center(),
                buff=d1.get_width() / 4,
            ))
        lines.set_stroke(WHITE, 2)
        hexy = VGroup(dots, lines)
        # CHANGE: unlock_unit_normal no longer exists (normals are no longer locked)
        pass

        self.play(LaggedStartMap(ShowCreation, lines))
        self.wait()
        self.play(Rotate(hexy, 60 * DEGREES))
        self.wait()
        self.play(Rotate(hexy, -120 * DEGREES))
        self.wait()
        self.play(Rotate(hexy, PI, axis=UP))
        self.wait()
        self.play(Rotate(hexy, PI, axis=rotate_vector(RIGHT, 60 * DEGREES)))
        self.wait()

        # Back to a row
        dots.generate_target()
        dots.target.arrange(RIGHT, buff=LARGE_BUFF)
        dots.target.move_to(0.5 * DOWN)
        for line in lines:
            line.generate_target()
            line.target.set_angle(0)
            line.target.set_stroke(WHITE, 0, 0)

        perm_label.to_edge(UP, buff=LARGE_BUFF)
        self.play(
            MoveToTarget(dots),
            FadeIn(perm_label),
            LaggedStartMap(MoveToTarget, lines, run_time=1.5)
        )

        # Bump it up to 12
        new_dots = dots.copy()
        new_dots.shift(1.5 * DOWN)

        new_perm_label = VGroup(
            OldTex("12!"),
            OldTex("="),
            Integer(math.factorial(12)),
            OldTexText("permutations")[0],
        )
        new_perm_label.arrange(RIGHT)
        new_perm_label.match_height(perm_label)
        new_perm_label.set_color(YELLOW)
        new_perm_label.move_to(perm_label)
        new_perm_label[0].align_to(perm_label[2][0], DOWN)

        old_full_count_center = full_count.get_center()
        self.play(
            ChangeDecimalToValue(
                perm_label[2], new_perm_label[2].get_value(),
                run_time=3
            ),
            UpdateFromAlphaFunc(
                perm_label[2], lambda m, a: m.move_to(interpolate(
                    old_full_count_center,
                    new_perm_label[2].get_center(),
                    a
                )).set_color(interpolate_color(BLUE, YELLOW, a))
            ),
            ShowIncreasingSubsets(new_dots),
            *[
                ReplacementTransform(perm_label[i], new_perm_label[i])
                for i in [0, 1, 3]
            ]
        )
        self.remove(perm_label)
        perm_label = new_perm_label
        self.add(perm_label)
        dots.add(*new_dots)

        self.wait()

        for x in range(5):
            perm = list(range(12))
            random.shuffle(perm)
            self.play(LaggedStart(*[
                Transform(dots[i], dots[perm[i]], path_arc=PI / 2)
                for i in range(12)
            ]))
            self.wait()

        # Show 101 dots
        new_perm_label = VGroup(
            OldTex("101!"),
            OldTex("\\approx"),
            OldTex("9.43 \\times 10^{159}"),
            OldTexText("permutations")[0]
        )
        new_perm_label.arrange(RIGHT)
        new_perm_label.match_height(perm_label)
        new_perm_label[2].align_to(new_perm_label[0], DOWN)
        new_perm_label[3].shift(SMALL_BUFF * DOWN)
        new_perm_label.move_to(perm_label, RIGHT)

        new_dots = VGroup(*[dots[0].copy() for x in range(101)])
        new_dots.arrange_in_grid(7, 13)
        new_dots.set_height(5)
        new_dots.to_edge(DOWN)

        self.play(
            FadeOut(perm_label),
            FadeIn(new_perm_label),
            ReplacementTransform(dots, new_dots[-len(dots):]),
            ShowIncreasingSubsets(new_dots[:-len(dots)], run_time=2)
        )
        self.add(new_dots)
        perm_label = new_perm_label
        dots = new_dots

        labels = VGroup()
        for i, dot in enumerate(new_dots):
            label = Integer(i + 1, fill_color=BLACK)
            label.replace(dot, dim_to_match=1)
            label.scale(0.3)
            labels.add(label)
        labels.set_stroke(width=0)

        self.play(FadeIn(labels))
        self.remove(labels)
        for dot, label in zip(dots, labels):
            dot.add(label)

        for x in range(6):
            self.play(permutation_animation(dots, lag_factor=1))
            self.wait(0.5)

        # Name S_n
        perm_label[3].generate_target()
        new_perm_label = VGroup(
            OldTex("n!").match_height(perm_label[0]),
            perm_label[3].target,
        )
        new_perm_label.arrange(RIGHT, buff=MED_LARGE_BUFF)
        new_perm_label[0].align_to(new_perm_label[1][-1], DOWN)
        new_perm_label.next_to(perm_label[0], RIGHT, MED_LARGE_BUFF)
        new_perm_label[0].save_state()
        new_perm_label[0].replace(perm_label[0], stretch=True)
        new_perm_label[0].set_opacity(0)

        Sn_name = OldTex("S_n")
        Sn_name.match_height(new_perm_label)
        Sn_name.next_to(new_perm_label, RIGHT, buff=LARGE_BUFF)
        Sn_name.set_color(YELLOW)

        self.play(
            perm_label[0].replace, new_perm_label[0], {"stretch": True},
            perm_label[0].set_opacity, 0,
            FadeOut(perm_label[1:3], RIGHT),
            MoveToTarget(perm_label[3]),
            Restore(new_perm_label[0]),
        )
        self.play(FadeIn(Sn_name, LEFT))

        self.remove(perm_label)
        perm_label = new_perm_label
        self.add(perm_label)

        self.play(permutation_animation(dots))

        # Down to a square
        new_dots = dots[:4]
        faders = dots[4:]
        new_dots.generate_target()
        for dot in new_dots.target:
            dot.set_height(0.8)
        new_dots.target.arrange_in_grid(2, 2, buff=LARGE_BUFF)
        new_dots.target.center()

        self.play(
            MoveToTarget(new_dots),
            FadeOut(faders),
        )
        dots = new_dots
        for x in range(2):
            self.play(permutation_animation(dots, [2, 0, 3, 1], lag_factor=0))
            self.wait()
