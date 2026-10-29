# ==============================================================================
# Scene:      RandomnessVsProportions
# Source:     videos/_2019/bayes/part1.py (lines 3811-3989)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomnessVsProportions.py RandomnessVsProportions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RandomnessVsProportions(Scene):
    def construct(self):
        prob_word = OldTexText("Probability")
        unc_word = OldTexText("Uncertainty")
        prop_word = OldTexText("Proportions")
        words = VGroup(prop_word, prob_word, unc_word)
        words.arrange(RIGHT, buff=LARGE_BUFF)
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(UP)
        arrows = VGroup()
        for w1, w2 in zip(words, words[1:]):
            arrow = OldTex("\\rightarrow")
            arrow.move_to(midpoint(w1.get_right(), w2.get_left()))
            arrows.add(arrow)

        random_dice = self.get_random_dice()
        random_dice.next_to(unc_word, DOWN, LARGE_BUFF)

        diagram = self.get_dice_diagram()
        diagram.next_to(prop_word, DOWN, LARGE_BUFF)
        diagram.shift_onto_screen()

        grid = diagram[0]
        border = grid[0][0].copy()
        border.set_stroke(BLACK, 3)
        border.set_fill(WHITE, opacity=0.2)
        border.scale(1.02)

        def update_border(border):
            r1, r2 = random_dice
            i = len(r1[1]) - 1
            j = len(r2[1]) - 1
            border.move_to(diagram[0][i][j])
        border.add_updater(update_border)

        example = VGroup(
            OldTexText("P(X = 5)", tex_to_color_map={"5": YELLOW}),
            Line(LEFT, RIGHT)
        )
        example.arrange(RIGHT)
        example.next_to(grid, RIGHT, LARGE_BUFF)
        example.align_to(random_dice, RIGHT)
        example.shift(0.5 * DOWN)
        grid_copy = grid.copy()
        five_part = VGroup(*[
            square
            for i, row in enumerate(grid_copy)
            for j, square in enumerate(row)
            if i + j == 3
        ])

        self.play(FadeInFromDown(prob_word))
        self.play(
            FadeIn(unc_word, LEFT),
            Write(arrows[1]),
        )
        self.add(random_dice)
        self.wait(9)
        self.play(
            FadeIn(prop_word, RIGHT),
            Write(arrows[0])
        )
        self.play(FadeIn(diagram))
        self.add(border)
        self.wait(2)

        self.play(FadeIn(example))
        self.add(grid_copy, diagram[1])
        self.play(
            grid_copy.set_width, 0.8 * example[1].get_width(),
            grid_copy.next_to, example[1], DOWN,
        )
        self.play(five_part.copy().next_to, example[1], UP)
        self.wait(6)

    def get_die_faces(self):
        dot = Dot()
        dot.set_width(0.15)
        dot.set_color(BLUE_B)

        square = Square()
        square.round_corners(0.25)
        square.set_stroke(WHITE, 2)
        square.set_fill(GREY_E, 1)
        square.set_width(0.6)

        edge_groups = [
            (ORIGIN,),
            (UL, DR),
            (UL, ORIGIN, DR),
            (UL, UR, DL, DR),
            (UL, UR, ORIGIN, DL, DR),
            (UL, UR, LEFT, RIGHT, DL, DR),
        ]

        arrangements = VGroup(*[
            VGroup(*[
                dot.copy().move_to(square.get_bounding_box_point(ec))
                for ec in edge_group
            ])
            for edge_group in edge_groups
        ])
        square.set_width(1)

        faces = VGroup(*[
            VGroup(square.copy(), arrangement)
            for arrangement in arrangements
        ])
        faces.arrange(RIGHT)

        return faces

    def get_random_dice(self):
        faces = list(self.get_die_faces())

        def get_random_pair():
            result = VGroup(*random.sample(faces, 2)).copy()
            result.arrange(RIGHT)
            for mob in result:
                mob.shift(random.random() * RIGHT * MED_SMALL_BUFF)
                mob.shift(random.random() * UP * MED_SMALL_BUFF)
            return result

        result = VGroup(*get_random_pair())
        result.time = 0
        result.iter_count = 0

        def update_result(group, dt):
            group.time += dt
            group.iter_count += 1
            if int(group.time) % 3 == 2:
                group.set_stroke(YELLOW)
                return group
            elif result.iter_count % 3 != 0:
                return group
            else:
                pair = get_random_pair()
                pair.move_to(group)
                group.submobjects = [*pair]

        result.add_updater(update_result)
        result.update()
        return result

    def get_dice_diagram(self):
        grid = VGroup(*[
            VGroup(*[
                Square() for x in range(6)
            ]).arrange(RIGHT, buff=0)
            for y in range(6)
        ]).arrange(DOWN, buff=0)
        grid.set_stroke(WHITE, 1)
        grid.set_height(5)

        colors = color_gradient([RED, YELLOW, GREEN, BLUE], 11)

        numbers = VGroup()
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                num = Integer(i + j + 2)
                num.set_height(square.get_height() - MED_LARGE_BUFF)
                num.move_to(square)
                # num.set_stroke(BLACK, 2, background=True)
                num.set_fill(GREY_D)
                square.set_fill(colors[i + j], 0.9)
                numbers.add(num)

        faces = VGroup()
        face_templates = self.get_die_faces()
        face_templates.scale(0.5)
        for face, row in zip(face_templates, grid):
            face.next_to(row, LEFT, MED_SMALL_BUFF)
            faces.add(face)
        for face, square in zip(faces.copy(), grid[0]):
            face.next_to(square, UP, MED_SMALL_BUFF)
            faces.add(face)

        result = VGroup(grid, numbers, faces)
        return result
