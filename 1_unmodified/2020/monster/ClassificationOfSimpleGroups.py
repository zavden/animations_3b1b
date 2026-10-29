# ==============================================================================
# Scene:      ClassificationOfSimpleGroups
# Source:     videos/_2020/monster.py (lines 3722-4094)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ClassificationOfSimpleGroups.py ClassificationOfSimpleGroups -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MONSTER_SIZE = 808017424794512875886459904961710757005754368000000000


BABY_MONSTER_SIZE = 4154781481226426191177580544000000


def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


def get_baby_monster():
    return get_monster().stretch(0.7, 1)


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


class ClassificationOfSimpleGroups(Scene):
    def construct(self):
        # Title
        class_title = OldTexText("Classification of finite simple groups")
        class_title.set_width(FRAME_WIDTH - 4)
        class_title.add(Underline(class_title).set_color(GREY_B))
        class_title.to_edge(UP)
        self.add(class_title)

        # 18 families
        square_template = Square(side_length=0.3)
        square_template.set_stroke(GREY_B, 2)
        square_template.set_fill(BLUE_E, 0.5)
        families_grid = VGroup(*[
            VGroup(*[square_template.copy() for x in range(8)])
            for y in range(18)
        ])
        for family in families_grid:
            family.arrange(DOWN, buff=0)
            dots = OldTex("\\vdots")
            dots.next_to(family, DOWN)
            family.add(dots)
        families_grid.arrange(RIGHT, buff=MED_SMALL_BUFF)
        families_grid.to_edge(LEFT)
        families_grid.set_y(-1)

        families_title = OldTexText("18 infinite families")
        families_title.set_color(BLUE)
        families_title.next_to(families_grid, UP, MED_LARGE_BUFF)

        self.play(
            FadeIn(families_title),
            FadeIn(families_grid, lag_ratio=0.1, run_time=4),
        )
        self.wait()

        # Analogize to periodic table
        families_grid.generate_target()
        families_grid.save_state()
        families_grid.target.arrange(RIGHT, buff=0)
        families_grid.target.move_to(families_grid)
        faders = VGroup(*[
            column[:n]
            for column, n in zip(families_grid.target, [
                0, 1, *[3] * 10, *[1] * 5, 0,
            ])
        ])
        faders.set_opacity(0)

        self.play(MoveToTarget(families_grid, lag_ratio=0.001))
        self.wait(2)
        self.play(Restore(families_grid))

        # Sporadic
        sporadics = VGroup(*[square_template.copy() for x in range(26)])
        buff = 0.1
        sporadics[:20].arrange_in_grid(10, 2, buff=buff)
        sporadics[20:].arrange(DOWN, buff=buff)
        sporadics[20:].next_to(sporadics[:20], RIGHT, buff)
        sporadics.next_to(families_grid, RIGHT, buff=1.5, aligned_edge=UP)
        sporadics.set_fill(YELLOW_E)

        pre_sporadics_title = OldTexText("26", " leftovers")
        sporadics_title = OldTexText("26", " ``sporadic''\\\\groups")
        for title in pre_sporadics_title, sporadics_title:
            title.set_color(YELLOW)
            title.next_to(sporadics, UP, MED_LARGE_BUFF)
        sporadics_title.shift(MED_SMALL_BUFF * DOWN)

        self.play(
            FadeIn(pre_sporadics_title, DOWN),
            ShowIncreasingSubsets(sporadics, run_time=3),
        )
        self.wait()
        self.play(
            ReplacementTransform(pre_sporadics_title[0], sporadics_title[0]),
            FadeOut(pre_sporadics_title[1], UP),
            FadeIn(sporadics_title[1], DOWN),
        )
        self.wait()

        # Show prime cyclic groups
        families_grid.save_state()
        column = families_grid[0]

        def prepare_column(column):
            column.generate_target()
            column.target.set_height(FRAME_HEIGHT)
            column.target.move_to(5 * LEFT)
            column.target.to_edge(UP)
            column.target[-1].scale(0.5, about_point=column.target[-2].get_bottom())

        prepare_column(column)

        self.play(
            MoveToTarget(column),
            FadeOut(families_grid[1:], lag_ratio=0.1),
            FadeOut(families_title),
            FadeOut(class_title, UP),
            FadeOut(sporadics, 2 * RIGHT),
            FadeOut(sporadics_title, 2 * RIGHT),
        )

        # C5
        c_names = VGroup(*[
            OldTex(f"C_{{{p}}}")
            for p in [2, 3, 5, 7, 11, 13, 17, 19]
        ])

        def put_in_square(mob, square, factor=0.4):
            mob.set_height(factor * square.get_height())
            mob.move_to(square)

        def put_names_in_column(names, column):
            for name, square in zip(names, column):
                put_in_square(name, square)

        put_names_in_column(c_names, column)

        self.play(FadeIn(c_names, lag_ratio=0.1))
        self.wait()

        pentagon = RegularPolygon(5)
        pentagon.set_height(3)
        pentagon.set_fill(TEAL_E, 0.5)
        pentagon.set_stroke(WHITE, 1)
        pentagon.move_to(2 * RIGHT)
        c_names.save_state()
        c5 = c_names[2]
        c5.generate_target()
        c5.target.scale(2)
        c5.target.next_to(pentagon, UP, LARGE_BUFF)

        self.play(
            MoveToTarget(c5),
            DrawBorderThenFill(pentagon, run_time=1),
        )
        pcenter = center_of_mass(pentagon.get_vertices())
        for n in [1, -2, 2]:
            self.play(Rotate(pentagon, n * TAU / 5, about_point=pcenter))
            self.wait(0.5)
        self.play(
            Restore(c_names),
            FadeOut(pentagon)
        )

        c_names.generate_target()
        c_names.target.replace(families_grid.saved_state[0])
        c_names.target.scale(0.9)
        c_names.target.set_opacity(0)
        families_grid[1:].fade(1)

        self.play(
            Restore(families_grid),
            MoveToTarget(c_names, remover=True)
        )

        # Alternating
        column = families_grid[1]
        prepare_column(column)
        self.play(
            MoveToTarget(column),
            FadeOut(families_grid[0]),
            FadeOut(families_grid[2:], lag_ratio=0.1),
        )

        a_names = VGroup(*[
            OldTex(f"A_{{{n}}}")
            for n in range(5, 5 + len(column) - 1)
        ])
        put_names_in_column(a_names, column)
        self.play(FadeIn(a_names, lag_ratio=0.1))

        dots = VGroup(*[Dot() for x in range(5)])
        dots.set_height(0.5)
        dots.arrange(RIGHT, buff=MED_LARGE_BUFF)
        dots.set_submobject_colors_by_gradient(RED, YELLOW)
        dots.move_to(RIGHT)

        a5 = a_names[0]
        a5.save_state()
        a5.generate_target()
        a5.target.scale(2)
        a5.target.next_to(dots, UP, buff=1.5)

        self.play(
            FadeIn(dots, lag_ratio=0.1),
            MoveToTarget(a5),
        )
        for x in range(5):
            perm = list(range(5))
            swaps = 1  # Lie
            while swaps % 2 == 1:
                random.shuffle(perm)
                swaps = 0
                for i, j in it.combinations(perm, 2):
                    if j < i:
                        swaps += 1
            arrows = get_permutation_arrows(dots, perm)
            self.play(
                FadeIn(arrows),
                permutation_animation(dots, perm, lag_factor=0.1),
            )
            self.play(FadeOut(arrows))
        self.wait()

        self.play(
            FadeOut(dots, lag_ratio=0.1),
            Restore(a5),
        )
        self.wait()

        a_names.generate_target()
        a_names.target.replace(families_grid.saved_state[1])
        a_names.target.scale(0.9)
        a_names.target.fade(1)

        self.play(
            Restore(families_grid),
            MoveToTarget(a_names, remover=True),
            FadeIn(families_title),
            FadeIn(class_title),
        )

        # Others
        others_rect = SurroundingRectangle(families_grid[2:])
        others_rect.set_stroke(YELLOW, 2)
        others_name = OldTexText("Groups of\\\\Lie type")
        others_name.set_color(YELLOW)
        others_name.next_to(others_rect, RIGHT)
        self.play(ShowCreation(others_rect))
        self.play(FadeIn(others_name))
        self.wait()
        self.play(FadeOut(others_name), FadeOut(others_rect))

        # Back to sporadics
        self.play(
            ShowIncreasingSubsets(sporadics),
            FadeIn(sporadics_title),
        )
        self.wait()

        # Look closer at sporadics
        sporadics.generate_target()
        sporadics.target.rotate(PI, axis=UL)
        sporadics.target.set_width(FRAME_WIDTH - 1)
        sporadics.target.center().to_edge(DOWN)

        sporadics_title.save_state()
        sporadics.save_state()

        self.play(
            sporadics_title.scale, 1.25,
            sporadics_title.center,
            sporadics_title.to_edge, UP,
            MoveToTarget(sporadics),
            FadeOut(families_grid, LEFT),
            FadeOut(families_title, LEFT),
            FadeOut(class_title, UP),
        )

        # Monster
        monster = get_monster()
        put_in_square(monster, sporadics[0], 0.9)
        monster_name = OldTexText("Monster", " group")
        monster_name.next_to(sporadics[0], UP, LARGE_BUFF)
        monster_name.shift_onto_screen()
        monster_arrow = Arrow(monster_name.get_bottom(), monster.get_top())

        size_label = OldTexText("{:,}".format(MONSTER_SIZE))[0]
        size_label.scale(0.8)
        size_label.move_to(monster_name, LEFT)

        self.play(
            sporadics[0].set_fill, {"opacity": 0},
            FadeIn(monster)
        )
        self.play(
            Write(monster_name),
            GrowArrow(monster_arrow),
        )
        self.wait()

        # sporadics_title.generate_target()
        # sporadics_title.target.scale(1 / 1.5)
        # sporadics_title.target.to_corner(UR)
        self.play(
            monster_name.shift, 0.6 * UP,
            ShowIncreasingSubsets(size_label, run_time=2),
            # MoveToTarget(sporadics_title, run_time=2, rate_func=squish_rate_func(smooth, 0.5, 1))
        )
        self.wait()

        # Baby monster
        full_monster_label = VGroup(monster_name, size_label)
        full_monster_label.save_state()
        full_monster_label.generate_target()
        full_monster_label.target.to_edge(UP, buff=MED_SMALL_BUFF)
        full_monster_label.target.set_opacity(0.7)

        baby_name = OldTexText("Baby monster group")
        baby_name.move_to(size_label, LEFT)
        baby_arrow = Arrow(baby_name.get_bottom(), sporadics[1].get_corner(UR) + SMALL_BUFF * DL)
        baby_arrow.set_stroke(BLACK, 6, background=True)
        baby_size_label = OldTexText("{:,}".format(BABY_MONSTER_SIZE))[0]
        baby_size_label.scale(0.8)
        baby_size_label.move_to(baby_name, LEFT)

        baby_monster = get_baby_monster()
        baby_monster.set_width(0.9 * sporadics[1].get_width())
        baby_monster.move_to(sporadics[1])
        baby_monster.shift(SMALL_BUFF * DOWN)

        self.remove(monster_arrow)
        self.play(
            MoveToTarget(full_monster_label),
            TransformFromCopy(monster_arrow, baby_arrow),
            FadeIn(baby_name, DOWN),
            sporadics[1].set_fill, {"opacity": 0},
            FadeIn(baby_monster),
            FadeOut(sporadics_title, UP),
        )
        self.wait()
        self.play(
            baby_name.shift, 0.6 * UP,
            ShowIncreasingSubsets(baby_size_label, run_time=2)
        )
        self.wait()

        # 20 vs. 6
        top_20 = sporadics[:20]
        top_20.generate_target()
        top_20.target.shift(2 * UP)
        top_20.target[1:].set_fill(GREEN, 0.8)

        self.play(
            MoveToTarget(top_20),
            MaintainPositionRelativeTo(monster, sporadics[0]),
            MaintainPositionRelativeTo(baby_monster, sporadics[1]),
            UpdateFromAlphaFunc(baby_monster, lambda m, a: m.set_opacity(1 - a), remover=True),
            ApplyMethod(baby_arrow.scale, 0, {"about_point": baby_arrow.get_start()}, remover=True),
            FadeOut(baby_size_label, UP),
            FadeOut(baby_name, UP),
            full_monster_label.set_fill, WHITE, 1,
        )

        monster_name.generate_target()
        monster_name.target.arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        monster_name.target.next_to(sporadics[0], UP, SMALL_BUFF, aligned_edge=LEFT)

        happy_family_name = OldTexText("``Happy family''")
        happy_family_name.set_height(0.7)
        happy_family_name.to_edge(UP)
        happy_family_name.set_color(GREEN)

        self.play(
            MoveToTarget(monster_name),
            FadeOut(size_label, DOWN),
            FadeIn(happy_family_name, UP),
        )
        self.wait()

        pariahs = sporadics[20:]
        pariahs_name = OldTexText("``Pariahs''")
        pariahs_name.set_height(0.7)
        pariahs_name.next_to(pariahs, UP, MED_LARGE_BUFF)
        pariahs_name.set_color(YELLOW)

        self.play(
            FadeIn(pariahs_name, UP),
            pariahs.set_fill, YELLOW, 0.7,
        )
        self.wait()
