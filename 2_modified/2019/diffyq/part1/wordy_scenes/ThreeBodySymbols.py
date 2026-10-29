# ==============================================================================
# Scene:      ThreeBodySymbols
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 481-599)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ThreeBodySymbols.py ThreeBodySymbols -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the first glyph of OldTexText is now count_word[0] (in Cairo the glyphs were one level more nested); count_word[0][0] gave IndexError
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_vector_symbol(*texs, **kwargs):
    config = {
        "include_background_rectangle": True,
        "bracket_h_buff": SMALL_BUFF,
        "bracket_v_buff": SMALL_BUFF,
        "element_alignment_corner": ORIGIN,
    }
    config.update(kwargs)
    array = [[tex] for tex in texs]
    return Matrix(array, **config)



# ----- From _2019/diffyq/part1/wordy_scenes.py -----

class ThreeBodySymbols(Scene):
    def construct(self):
        self.init_coord_groups()
        self.introduce_coord_groups()
        self.count_coords()

    def init_coord_groups(self):
        kwargs = {
            "bracket_v_buff": 2 * SMALL_BUFF
        }
        positions = VGroup(*[
            get_vector_symbol(*[
                "{}_{}".format(s, i)
                for s in "xyz"
            ], **kwargs)
            for i in range(1, 4)
        ])
        velocities = VGroup(*[
            get_vector_symbol(*[
                "p^{}_{}".format(s, i)
                for s in "xyz"
            ], **kwargs)
            for i in range(1, 4)
        ])
        groups = VGroup(positions, velocities)
        colors = [GREEN, RED, BLUE]
        for group in groups:
            for matrix in group:
                matrix.coords = matrix.get_entries()
                for coord, color in zip(matrix.coords, colors):
                    coord.set_color(color)
            group.arrange(RIGHT)
        groups.arrange(DOWN, buff=LARGE_BUFF)
        groups.to_edge(LEFT)

        self.coord_groups = groups

    def introduce_coord_groups(self):
        groups = self.coord_groups
        x_group, p_group = groups
        x_word = OldTexText("Positions")
        p_word = OldTexText("Momenta")
        words = VGroup(x_word, p_word)
        for word, group in zip(words, groups):
            word.next_to(group, UP)

        rect_groups = VGroup()
        for group in groups:
            rect_group = VGroup(*[
                SurroundingRectangle(
                    VGroup(*[
                        tm.coords[i]
                        for tm in group
                    ]),
                    color=WHITE,
                    stroke_width=2,
                )
                for i in range(3)
            ])
            rect_groups.add(rect_group)

        self.play(
            *[
                LaggedStartMap(
                    FadeInFrom, group,
                    lambda m: (m, UP),
                    run_time=1,
                )
                for group in groups
            ],
            *map(FadeInFromDown, words),
        )
        for rect_group in rect_groups:
            self.play(
                ShowCreationThenFadeOut(
                    rect_group,
                    lag_ratio=0.5,
                )
            )
        self.wait()

    def count_coords(self):
        coord_copies = VGroup()
        for group in self.coord_groups:
            for tex_mob in group:
                for coord in tex_mob.coords:
                    coord_copy = coord.copy()
                    coord_copy.set_stroke(
                        WHITE, 2, background=True
                    )
                    coord_copies.add(coord_copy)

        count = Integer()
        count_word = OldTexText("18", "degrees \\\\ of freedom")[1]
        count_group = VGroup(count, count_word)
        count_group.arrange(
            RIGHT,
            aligned_edge=DOWN,
        )
        count_group.scale(1.5)
        count_group.next_to(
            self.coord_groups, RIGHT,
            aligned_edge=DOWN,
        )
        count.add_updater(
            lambda m: m.set_value(len(coord_copies))
        )
        count.add_updater(
            # CHANGE: the first glyph of OldTexText is now count_word[0] (in Cairo the glyphs were one level more nested); count_word[0][0] gave IndexError
            lambda m: m.next_to(count_word[0], LEFT, aligned_edge=DOWN)
        )

        self.add(count_group)
        self.play(
            # ChangeDecimalToValue(count, len(coord_copies)),
            ShowIncreasingSubsets(coord_copies),
            run_time=1.5,
            rate_func=linear,
        )
        self.play(FadeOut(coord_copies))
