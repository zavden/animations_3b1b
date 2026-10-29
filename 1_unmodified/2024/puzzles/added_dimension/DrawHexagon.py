# ==============================================================================
# Scene:      DrawHexagon
# Source:     videos/_2024/puzzles/added_dimension.py (lines 390-416)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrawHexagon.py DrawHexagon -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_lozenge(side_length=1):
    verts = [math.sqrt(3) * LEFT, UP, math.sqrt(3) * RIGHT, DOWN]
    result = Polygon(*verts)
    result.scale(side_length / get_norm(verts[0] - verts[1]))
    return result


class IntroduceHexagonFilling(InteractiveScene):
    N = 15
    tile_color = GREY_C
    highlight_color = TEAL
    drag_to_pan = False

    def setup(self):
        super().setup()
        # Create hexagonal tiling
        lozenge = get_lozenge()
        lozenge.set_stroke(WHITE, 1)
        lozenge.set_fill(self.tile_color, 1)
        lozenge.move_to(ORIGIN, DOWN)
        lozenges = VGroup(lozenge.copy().rotate(theta, about_point=ORIGIN) for theta in np.arange(0, TAU, TAU / 3))

        tiling = VGroup()
        for template in lozenges:
            v1 = template.get_vertices()[0]
            v2 = template.get_vertices()[2]
            for x, y in it.product(*2 * [range(self.N)]):
                tiling.add(template.copy().shift(x * v1 + y * v2))

        self.add(tiling)
        self.tiling = tiling

        # Add hexagon
        hexagon = RegularPolygon(6, radius=self.N, start_angle=90 * DEGREES)
        hexagon.set_stroke(YELLOW, 3)
        self.add(hexagon)
        self.hexagon = hexagon

        self.selected_set = VGroup()

    def construct(self):
        # Just play around
        self.wait(10)
        pass

    def rotate_selection(self):
        trip = self.selected_set
        trip.target = trip.generate_target()
        trip.target.rotate(TAU / 6)
        trip.target.set_fill(self.tile_color)
        self.add(trip)
        self.play(MoveToTarget(trip, path_arc=TAU / 6))
        self.selected_set.clear()
        self.add(self.tiling)

        for tile in self.tiling:
            tile.refresh_bounding_box()

    def fill_with_current_tiles(self):
        # Populate
        starter = self.tiling[0].copy()
        starter.to_corner(UL)

        random_order = VGroup(*self.tiling)
        random_order.shuffle()

        self.remove(self.tiling)
        self.play(
            LaggedStart(
                (TransformFromCopy(starter, tile)
                for tile in random_order),
                lag_ratio=1.0 / len(self.tiling),
                run_time=5
            )
        )
        self.add(self.tiling)

    def on_mouse_release(
        self,
        point: Vect3,
        button: int,
        mods: int
    ) -> None:
        super().on_mouse_release(point, button, mods)
        if len(self.selected_set) == 3:
            return
        mouse_center = self.mouse_point.get_center()
        dists = [get_norm(tile.get_center() - mouse_center) for tile in self.tiling]
        tile = self.tiling[np.argmin(dists)]
        tile.set_fill(self.highlight_color)
        if tile in self.selected_set:
            tile.set_fill(self.tile_color)
            self.selected_set.remove(tile)
        else:
            self.selected_set.add(tile)

    def on_key_release(
        self,
        symbol: int,
        modifiers: int
    ) -> None:
        super().on_key_release(symbol, modifiers)
        if chr(symbol) == "p":
            self.fill_with_current_tiles()

        if len(self.selected_set) != 3:
            return

        if chr(symbol) == "r":
            self.rotate_selection()


class DrawHexagon(IntroduceHexagonFilling):
    def construct(self):
        self.remove(self.tiling)

        # Test
        tiles = self.tiling
        tiles.add(*tiles.copy().rotate(60 * DEGREES))
        tiles.set_fill(opacity=0)
        tiles.set_stroke(WHITE, 0.5, 0.5)
        frame = self.frame
        hexagon = self.hexagon
        brace = Brace(Line(ORIGIN, 4 * UP), RIGHT)
        brace.next_to(hexagon, RIGHT, SMALL_BUFF)
        brace_label = brace.get_text("4")

        self.play(
            ShowCreation(hexagon),
            VShowPassingFlash(hexagon.copy().set_stroke(width=5).insert_n_curves(20), time_width=2),
            run_time=2
        )
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(brace_label),
            FadeIn(tiles),
        )
        self.wait()
