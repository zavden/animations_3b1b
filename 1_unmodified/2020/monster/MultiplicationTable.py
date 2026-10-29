# ==============================================================================
# Scene:      MultiplicationTable
# Source:     videos/_2020/monster.py (lines 2044-2216)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultiplicationTable.py MultiplicationTable -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_rot_icon(degrees, mobject, mini_mob_height=1.25):
    mini_mob = mobject.copy()
    temp_height = 1.75
    mini_mob.set_height(temp_height)
    mini_mob.set_stroke(width=0)
    mini_mob.center()
    angle = min(degrees * DEGREES, 170 * DEGREES)
    arc1 = Arrow(
        RIGHT, rotate_vector(RIGHT, angle),
        path_arc=angle,
        buff=0
    )
    arc2 = arc1.copy().rotate(PI, about_point=ORIGIN)
    label = Integer(degrees, unit="^\\circ")
    label.set_height(0.25)
    half_vect = rotate_vector(RIGHT, angle / 2)
    label.next_to(half_vect, half_vect, buff=MED_SMALL_BUFF)
    icon = VGroup(mini_mob, arc1, arc2, label)
    icon.scale(mini_mob_height / temp_height)
    return icon


def get_flip_icon(angle, mobject, opacity=0.75, mini_mob_height=1.25):
    mini_mob = mobject.copy()
    mini_mob.set_stroke(width=0)
    mini_mob.set_fill(opacity=opacity)
    mini_mob.set_height(mini_mob_height)
    mini_mob.center()
    sym_line = DashedLine(LEFT, RIGHT)
    sym_line.set_stroke(WHITE, 2)
    sym_line.set_width(1.2 * mini_mob_height)
    sym_line.rotate(angle)
    sym_line.move_to(mini_mob)
    back_line = sym_line.copy()
    back_line.set_stroke(BLACK, 5)
    return VGroup(mini_mob, back_line, sym_line)


class MultiplicationTable(Scene):
    def construct(self):
        # Grid
        grid = VGroup(*[Square() for x in range(64)])
        grid.arrange_in_grid(8, 8, buff=0)
        grid.set_stroke(WHITE, 2)
        grid.set_height(6.5)
        grid.to_edge(DOWN, buff=0.5)
        self.add(grid)

        # Action icons
        square = Square()
        square.rotate(45 * DEGREES)
        square.set_height(1)
        square.set_fill(BLUE_D, 1)
        icons = VGroup(
            *[
                get_rot_icon(deg, square)
                for deg in [0, 90, 180, -90]
            ] + [
                get_flip_icon(angle, square, opacity=1)
                for angle in np.arange(0, PI, PI / 4)
            ]
        )
        icons[0].remove(icons[0][-1])
        icons.match_height(grid[0])
        icons.scale(0.8)
        for icon in icons:
            icon[0].rotate(-45 * DEGREES)

        left_icons = icons.copy()
        top_icons = icons.copy()

        for icon_group, grid_group, vect in [(left_icons, grid[0::8], LEFT), (top_icons, grid[:8], UP)]:
            for gs, icon in zip(grid_group, icon_group):
                icon.shift(gs.get_edge_center(vect) - icon[0].get_center())
                icon.shift(0.6 * gs.get_width() * vect)

        for icon in top_icons:
            icon[0].set_fill(GREY_BROWN)

        self.add(left_icons, top_icons)

        # Figure out full table
        def pmult(perm1, perm2):
            return [perm1[i] for i in perm2]

        r = [1, 2, 3, 0]
        s = [3, 2, 1, 0]
        r2 = pmult(r, r)
        r3 = pmult(r2, r)
        perms = [
            list(range(4)), r, r2, r3,
            s,
            pmult(r, s),
            pmult(r2, s),
            pmult(r3, s),
        ]

        table = np.zeros((8, 8), dtype=int)
        table_icons = VGroup()
        for n, square in enumerate(grid):
            i = n // 8
            j = n % 8
            perm = pmult(perms[i], perms[j])
            index = perms.index(perm)
            table[i, j] = index
            icon = icons[index].copy()
            icon[0].set_color(BLUE_E)
            icon.set_opacity(1)
            icon.shift(square.get_center() - icon[0].get_center())

            pre_icon = VGroup(icon.copy(), icon.copy())
            pre_icon.save_state()
            pre_icon.set_opacity(0)
            pre_icon[0].move_to(left_icons[i])
            pre_icon[1].move_to(top_icons[j])
            icon.pre_icon = pre_icon

            table_icons.add(icon)

        # Show all product
        sorted_icons = list(table_icons)

        frame = self.camera.frame
        frame.save_state()
        frame.scale(0.6)
        frame.move_to(top_icons.get_top() + MED_SMALL_BUFF * UL, UP)

        turn_animation_into_updater(Restore(frame, run_time=20, rate_func=bezier([0, 0, 1, 1])))
        self.add(frame)

        for sorted_index, icon in enumerate(sorted_icons):
            n = table_icons.submobjects.index(icon)
            i = n // 8
            j = n % 8
            rects = VGroup(
                SurroundingRectangle(left_icons[i]),
                SurroundingRectangle(top_icons[j]),
                grid[n].copy().set_fill(GREEN_E, 0.5)
            )
            rects.set_stroke(YELLOW, 2)
            self.add(rects, *self.mobjects)
            self.add(icon)
            if sorted_index < 8:
                pass  # Don't wait
            elif sorted_index < 24:
                self.wait(1)
            else:
                self.wait(0.15)
            self.remove(rects)
        self.add(table_icons)
        self.wait(2)

        # Symbolically
        symbols = VGroup(
            OldTex("1"),
            OldTex("r"),
            OldTex("r^2"),
            OldTex("r^3"),
            OldTex("s"),
            OldTex("rs"),
            OldTex("r^2 s"),
            OldTex("r^3 s"),
        )
        symbols.set_height(0.4 * grid[0].get_height())

        left_symbols = symbols.copy()
        top_symbols = symbols.copy()
        for symbol_group, icon_group in [(left_symbols, left_icons), (top_symbols, top_icons)]:
            for symbol, icon in zip(symbol_group, icon_group):
                symbol.move_to(icon[0], DOWN)

        table_symbols = VGroup()
        for n, icon in enumerate(table_icons):
            i = n // 8
            j = n % 8
            symbol = symbols[table[i, j]].copy()
            symbol.move_to(icon[0], DOWN)
            table_symbols.add(symbol)

        self.play(
            LaggedStart(*[
                ApplyMethod(mob.scale, 0, remover=True)
                for mob in [*left_icons, *top_icons, *table_icons]
            ]),
            LaggedStart(*[
                GrowFromCenter(mob)
                for mob in [*left_symbols, *top_symbols, *table_symbols]
            ]),
        )
        self.wait()

        # Show some products
        last_rects = VGroup()
        for x in range(10):
            n = random.randint(0, 63)
            i = n // 8
            j = n % 8
            rects = VGroup(
                SurroundingRectangle(left_symbols[i]),
                SurroundingRectangle(top_symbols[j]),
                grid[n].copy().set_stroke(YELLOW, 4).set_fill(YELLOW, 0.5)
            )
            self.add(rects, *self.mobjects)
            self.play(
                FadeOut(last_rects),
                FadeIn(rects),
            )
            self.wait(2)
            last_rects = rects
        self.play(FadeOut(last_rects))
        self.wait()
