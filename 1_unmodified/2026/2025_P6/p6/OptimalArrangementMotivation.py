# ==============================================================================
# Scene:      OptimalArrangementMotivation
# Source:     videos/_2026/2025_P6/p6.py (lines 158-551)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OptimalArrangementMotivation.py OptimalArrangementMotivation -w -m --fps 15
# ==============================================================================

import tempfile
import os
import math
import random
from manim_imports_ext import *

class Tile(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, fill_opacity=0.9, fill_color=BLUE, stroke_width=8, stroke_color=WHITE, **kwargs)
        self.round_corners(0.05)
        self.set_scale_stroke_with_zoom(True)


class Hole(VGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = Square(
            side_length=1,
            fill_opacity=1,
            fill_color="#444444",
            stroke_width=0
        )
        self.cross = Cross(self.background, stroke_width=2).scale(0.95)
        points = [ORIGIN, RIGHT, UR, UP]
        self.border = VGroup(*[
            Line(points[i], points[(i + 1) % 4], stroke_width=4, stroke_color=YELLOW).scale(1.06)
            for i in range(len(points))
        ]).match_width(self.cross).scale(1.06).move_to(self.cross)
        self.add(self.background, self.cross, self.border)
        self.set_scale_stroke_with_zoom(False)


class OptimalArrangementMotivation(InteractiveScene):
    def construct(self):
        # Add a bunch of tiles
        self.camera.frame.save_state()
        self.camera.frame.scale(2)
        tiles = VGroup(
            Tile(4, 2),
            Tile(2, 3),
            Tile(4, 3),
            Tile(1, 5),
            Tile(3, 3)
        )
        tiles[0].shift(LEFT * 8 + UP * 4.5)
        tiles[1].shift(RIGHT * 8 + UP * 4.5)
        tiles[3].shift(LEFT * 8 + DOWN * 3.5)
        tiles[4].shift(RIGHT * 8 + DOWN * 4.5)

        for i, tile in enumerate(tiles):
            tile.w_val = tile.get_width()
            tile.h_val = tile.get_height()
            phase = random.uniform(0, 2 * math.pi)
            amplitude = math.radians(random.uniform(3, 6))
            frequency = random.uniform(1, 1.2)

            init_angle = amplitude * math.sin(phase)
            tile.angle_tracker = ValueTracker(init_angle)
            tile.current_angle = init_angle
            tile.rotate(init_angle)

            def make_tile_updater(p, amp, freq):
                def updater(m, dt):
                    t = self.time
                    target_angle = amp * math.sin(freq * t + p)
                    m.angle_tracker.set_value(target_angle)

                    d_theta = target_angle - m.current_angle
                    m.rotate(d_theta)
                    m.current_angle = target_angle
                return updater

            tile.add_updater(make_tile_updater(phase, amplitude, frequency))

        shuffled_tiles = list(tiles)
        random.shuffle(shuffled_tiles)

        self.play(
            AnimationGroup(
                *[GrowFromCenter(tile) for tile in shuffled_tiles],
                lag_ratio=0.25
            )
        )
        self.wait(3)

        # Add some holes sliding around the sides
        holes = VGroup()
        for tile in tiles:
            w_val = tile.w_val
            h_val = tile.h_val

            for side_idx in range(4):
                hole = Hole()
                hole.border[side_idx].set_color(WHITE)
                hole.phase = random.uniform(0, 2 * math.pi)
                hole.freq = random.uniform(0.8, 1.5)

                if side_idx == 0 or side_idx == 2:
                    L = max(0.1, (w_val - 1) / 2)
                else:
                    L = max(0.1, (h_val - 1) / 2)

                s = L * math.sin(hole.phase)
                if side_idx == 0:
                    local_pos = np.array([s, h_val / 2 + 0.5, 0])
                elif side_idx == 1:
                    local_pos = np.array([-w_val / 2 - 0.5, s, 0])
                elif side_idx == 2:
                    local_pos = np.array([s, -h_val / 2 - 0.5, 0])
                else:
                    local_pos = np.array([w_val / 2 + 0.5, s, 0])

                init_angle = tile.angle_tracker.get_value()
                world_pos = tile.get_center() + rotate_vector(local_pos, init_angle)

                hole.rotate(init_angle)
                hole.current_angle = init_angle
                hole.move_to(world_pos)

                def make_hole_updater(t_ref, s_idx, l_val, p_val, f_val, w_v, h_v):
                    def updater(h, dt):
                        t = self.time
                        s_t = l_val * math.sin(f_val * t + p_val)
                        if s_idx == 0:
                            loc = np.array([s_t, h_v / 2 + 0.5, 0])
                        elif s_idx == 1:
                            loc = np.array([-w_v / 2 - 0.5, s_t, 0])
                        elif s_idx == 2:
                            loc = np.array([s_t, -h_v / 2 - 0.5, 0])
                        else:
                            loc = np.array([w_v / 2 + 0.5, s_t, 0])

                        target_angle = t_ref.angle_tracker.get_value()
                        w_pos = t_ref.get_center() + rotate_vector(loc, target_angle)
                        d_theta = target_angle - h.current_angle
                        h.rotate(d_theta)
                        h.current_angle = target_angle
                        h.move_to(w_pos)
                    return updater

                hole.add_updater(make_hole_updater(tile, side_idx, L, hole.phase, hole.freq, w_val, h_val))
                holes.add(hole)

        shuffled_holes = list(holes)
        random.shuffle(shuffled_holes)
        self.play(AnimationGroup(*[FadeIn(hole) for hole in shuffled_holes], lag_ratio=0.05))
        self.wait(9)

        # Focus on one of the tiles
        tiles[2].clear_updaters()

        def make_tracker_listener():
            def updater(m, dt):
                target_angle = m.angle_tracker.get_value()
                d_theta = target_angle - m.current_angle
                m.rotate(d_theta)
                m.current_angle = target_angle
            return updater

        tiles[2].add_updater(make_tracker_listener())

        self.play(
            self.camera.frame.animate.scale(0.87),
            VGroup(tiles[:2], tiles[3:], holes[:8], holes[12:]).animate.set_opacity(0),
            tiles[2].angle_tracker.animate.set_value(0), run_time=2)
        self.remove(tiles[:2], tiles[3:], holes[:8], holes[12:])
        tile = tiles[2]
        holes = holes[8:12]

        # Let the holes naturally slide into a cleaned up position
        damp_tracker = ValueTracker(1.0)

        for side_idx, hole in enumerate(holes):
            w_val = tile.w_val
            h_val = tile.h_val

            if side_idx == 0 or side_idx == 2:
                L = max(0.1, (w_val - 1) / 2)
            else:
                L = max(0.1, (h_val - 1) / 2)

            hole.clear_updaters()

            def make_dampening_hole_updater(t_ref, s_idx, l_val, p_val, f_val, w_v, h_v):
                def updater(h, dt):
                    t = self.time
                    scale = damp_tracker.get_value()
                    s_t = scale * l_val * math.sin(f_val * t + p_val)

                    if s_idx == 0:
                        loc = np.array([s_t, h_v / 2 + 0.5, 0])
                    elif s_idx == 1:
                        loc = np.array([-w_v / 2 - 0.5, s_t, 0])
                    elif s_idx == 2:
                        loc = np.array([s_t, -h_v / 2 - 0.5, 0])
                    else:
                        loc = np.array([w_v / 2 + 0.5, s_t, 0])

                    target_angle = t_ref.angle_tracker.get_value()
                    w_pos = t_ref.get_center() + rotate_vector(loc, target_angle)
                    d_theta = target_angle - h.current_angle
                    h.rotate(d_theta)
                    h.current_angle = target_angle
                    h.move_to(w_pos)
                return updater

            hole.add_updater(make_dampening_hole_updater(tile, side_idx, L, hole.phase, hole.freq, w_val, h_val))

        self.play(damp_tracker.animate.set_value(0), run_time=3)
        tile.clear_updaters()
        holes.clear_updaters()

        # Add tiles above and below the hole
        right_hole = holes[3]
        right_hole.add_updater(lambda m: self.bring_to_front(m))
        tile_above = Tile(3, 5).align_to(right_hole.get_corner(UL), DL)
        tile_below = Tile(4, 5).align_to(right_hole.get_corner(DL), UL)
        self.add(tile_above, tile_below, holes)
        self.play(
            FadeIn(tile_above, shift=DOWN),
            FadeIn(tile_below, shift=UP),
            holes[:3].animate.set_opacity(0.2),
            VGroup(right_hole.border[0], right_hole.border[2]).animate.set_color(WHITE), run_time=2)
        self.wait(2)

        # Add holes to those tiles
        inner_holes_above = VGroup(*[
            Hole().next_to(tile_above, [LEFT, UP, RIGHT][i], buff=0).shift(UP * 0.8 if i == 0 else 0)
            for i in range(3)
        ])
        for i, hole in enumerate(inner_holes_above):
            for j in range(len(hole.border)):
                if (-j + 1) % 4 == i:
                    hole.border[j].set_color(WHITE)
        inner_holes_below = VGroup(*[
            Hole().next_to(tile_below, [LEFT, RIGHT, DOWN][i], buff=0).shift(DOWN * 0.8 if i == 0 else 0)
            for i in range(3)
        ])
        for i, hole in enumerate(inner_holes_below):
            for j in range(len(hole.border)):
                if (i == 0 and j == 1 or i == 1 and j == 3 or i == 2 and j == 2):
                    hole.border[j].set_color(WHITE)
        hole_above = inner_holes_above[0]
        hole_below = inner_holes_below[0]
        shuffled_inner_holes = list(inner_holes_above) + list(inner_holes_below)
        random.shuffle(shuffled_inner_holes)
        self.play(AnimationGroup(*[FadeIn(hole) for hole in shuffled_inner_holes], lag_ratio=0.2))
        self.wait(2)
        dashed_line = DashedLine(hole_below, hole_above, dash_length=0.2, stroke_width=6).set_color(PURE_RED)
        self.play(
            ShowCreation(dashed_line),
            inner_holes_above[1:].animate.set_opacity(0.2),
            inner_holes_below[1:].animate.set_opacity(0.2)
        )
        self.wait(3)

        # Slide the hole up and down the side of the tile
        extra_tiles_and_holes_group = VGroup(tile_above, tile_below, inner_holes_above, inner_holes_below, dashed_line)
        right_hole.clear_updaters()
        self.play(VGroup(extra_tiles_and_holes_group, right_hole).animate.shift(UP * 0.3), run_time=3)
        self.play(VGroup(extra_tiles_and_holes_group, right_hole).animate.shift(DOWN * 0.6), run_time=3)
        self.play(FadeOut(VGroup(holes[:3], inner_holes_above[1:], inner_holes_below[1:])))
        self.wait(1)
        holes_group = VGroup(right_hole, hole_above, hole_below, dashed_line)
        holes_group.generate_target()
        holes_group.target.shift(UP * (tile.get_top()[1] - right_hole.get_top()[1]))
        tile_above.generate_target()
        tile_above.target.align_to(holes_group.target[0].get_top(), DOWN)
        tile_below.generate_target()
        tile_below.target.align_to(holes_group.target[0].get_bottom(), UP)
        self.play(
            MoveToTarget(holes_group),
            MoveToTarget(tile_above),
            MoveToTarget(tile_below),
            self.camera.frame.animate.move_to(holes_group.target[0]), run_time=3)
        right_hole.add_updater(lambda m: self.bring_to_front(m))
        self.play(
            FadeOut(dashed_line, shift=LEFT * 1.7),
            VGroup(tile_above, hole_above).animate.shift(LEFT * (tile_above.get_right()[0] - right_hole.get_right()[0])), run_time=2.5)
        self.wait(2)
        new_tile = Tile(5, 3).align_to(right_hole.get_corner(DR), DL)
        self.play(FadeIn(new_tile, shift=LEFT), right_hole.border[1].animate.set_color(WHITE))
        right_hole.clear_updaters()

        # Add some extra holes around the outer tiles
        outer_tiles = VGroup(tile, tile_above, new_tile, tile_below)
        outer_tiles.add_updater(lambda m: self.bring_to_back(m))
        middle_hole = right_hole
        inner_holes = VGroup(*[
            Hole().align_to(outer_tile.get_corner(direction1), direction2)
            for outer_tile, direction1, direction2 in zip(outer_tiles, [DR, DL, UL, UR], [UR, DR, DL, UL])
        ])
        for i in range(len(inner_holes)):
            VGroup(inner_holes[i].border[(-i + 1) % 4], inner_holes[i].border[(-i + 2) % 4]).set_color(WHITE)
        self.play(
            ReplacementTransform(hole_below, inner_holes[0]),
            ReplacementTransform(hole_above, inner_holes[1]),
            AnimationGroup(*[
                FadeIn(hole, shift=direction)
                for hole, direction in zip(inner_holes[2:], [DL, UL])
            ], lag_ratio=0.1), run_time=1.5)
        outer_holes = VGroup(*[
            Hole().align_to(outer_tile.get_corner(direction1), direction2)
            for outer_tile, direction1, direction2 in zip(outer_tiles, [DL, UL, UR, DR], [DR, DL, UL, UR])
        ])
        for i in range(len(inner_holes)):
            for j in range(4):
                if (-j + 1) % 4 == i:
                    outer_holes[i].border[j].set_color(WHITE)
        self.play(AnimationGroup(*[FadeIn(hole) for hole in outer_holes], lag_ratio=0.1))
        self.wait(0.5)
        checkmarks = VGroup(*[
            Checkmark().scale(1.5).set_color(PURE_GREEN).move_to(hole)
            for hole in [middle_hole] + list(inner_holes) + list(outer_holes)
        ])
        self.play(AnimationGroup(*[GrowFromCenter(checkmark) for checkmark in checkmarks], lag_ratio=0.2))
        self.wait(2)
        self.play(FadeOut(checkmarks))

        # Change the tiles into squares
        square_tiles = VGroup(*[Tile(3, 3) for _ in range(4)])
        for square_tile, outer_tile, direction in zip(square_tiles, outer_tiles, [UR, DR, DL, UL]):
            square_tile.align_to(outer_tile, direction)
        for hole, square_tile, direction1, direction2 in zip(inner_holes, square_tiles, [DR, DL, UL, UR], [UR, DR, DL, UL]):
            hole.generate_target()
            hole.target.align_to(square_tile.get_corner(direction1), direction2)
        for hole, square_tile, direction1, direction2 in zip(outer_holes, square_tiles, [DL, UL, UR, DR], [DR, DL, UL, UR]):
            hole.generate_target()
            hole.target.align_to(square_tile.get_corner(direction1), direction2)
        middle_hole.add_updater(lambda m: self.bring_to_front(m))
        self.play(
            AnimationGroup(*[
                ReplacementTransform(outer_tile, square_tile)
                for outer_tile, square_tile in zip(outer_tiles, square_tiles)
            ]),
            AnimationGroup(*[
                MoveToTarget(hole)
                for hole in inner_holes
            ]),
            AnimationGroup(*[
                MoveToTarget(hole)
                for hole in outer_holes
            ]), run_time=2)
        middle_hole.clear_updaters()
        self.clear()
        self.add(square_tiles, middle_hole, inner_holes, outer_holes)
        self.wait(2)

        # Focus on one of the puzzle pieces
        puzzle_piece = VGroup(square_tiles[2], middle_hole, inner_holes[2], outer_holes[2], inner_holes[3])

        time_start = self.time
        single_phase = 0
        single_amplitude = math.radians(4.5)
        single_frequency = 1.1

        single_init_angle = single_amplitude * math.sin(single_phase)
        puzzle_piece.angle_tracker = ValueTracker(single_init_angle)
        puzzle_piece.current_angle = single_init_angle
        puzzle_piece.rotate(single_init_angle)

        def make_piece_updater(p, amp, freq):
            def updater(m, dt):
                t = self.time - time_start
                target_angle = amp * math.sin(freq * t + p)
                m.angle_tracker.set_value(target_angle)

                d_theta = target_angle - m.current_angle
                m.rotate(d_theta)
                m.current_angle = target_angle

                for i in range(len(m[1:])):
                    for j in range(4):
                        if (-j + 1) % 4 != i:
                            m[1:][i].border[j].set_color(interpolate_color(m[1:][i].border[j].get_color(), YELLOW, 0.03))

            return updater

        puzzle_piece.add_updater(make_piece_updater(single_phase, single_amplitude, single_frequency))
        self.play(
            FadeOut(
                VGroup(
                    square_tiles[:2], square_tiles[3],
                    inner_holes[:2],
                    outer_holes[:2], outer_holes[3]
                ),
                shift=DL * 2
            ),
            self.camera.frame.animate.scale(0.9).move_to(puzzle_piece),
            puzzle_piece.animate.shift(0), run_time=2)

        # Show floating copies of the puzzle piece
        self.camera.frame.center()
        puzzle_piece.center()

        puzzle_pieces = VGroup(puzzle_piece, *[puzzle_piece.copy() for _ in range(4)])
        puzzle_pieces[1].move_to(LEFT * 7.5 + UP * 4.5)
        puzzle_pieces[2].move_to(RIGHT * 7.5 + UP * 4.5)
        puzzle_pieces[3].move_to(LEFT * 7.5 + DOWN * 4.5)
        puzzle_pieces[4].move_to(RIGHT * 7.5 + DOWN * 4.5)

        for i in range(1, len(puzzle_pieces)):
            piece = puzzle_pieces[i]
            phase = random.uniform(0, 2 * math.pi)
            amplitude = math.radians(random.uniform(3, 6))
            frequency = random.uniform(1, 1.2)

            init_angle = amplitude * math.sin(phase)
            piece.angle_tracker = ValueTracker(init_angle)
            piece.current_angle = init_angle
            piece.rotate(init_angle)

            piece.add_updater(make_piece_updater(phase, amplitude, frequency))

        shuffled_pieces = list(puzzle_pieces)
        random.shuffle(shuffled_pieces)

        self.play(
            self.camera.frame.animate.scale(1.35),
            AnimationGroup(
                *[GrowFromCenter(piece) for piece in shuffled_pieces if piece != puzzle_piece],
                lag_ratio=0.25
            ),
            run_time=2.5
        )
        self.wait(10)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
