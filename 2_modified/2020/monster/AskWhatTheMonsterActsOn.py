# ==============================================================================
# Scene:      AskWhatTheMonsterActsOn
# Source:     videos/_2020/monster.py (lines 4122-4251)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AskWhatTheMonsterActsOn.py AskWhatTheMonsterActsOn -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - monster.svg (free replacement) has different point indices for the eyes: _eye_points finds them by geometry
# ==============================================================================

from manim_imports_ext import *

def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


def _eye_points(mob):
    # CHANGE: monster.svg is a free replacement and its eyes are not at points 498:528 / 582:612; they are found as the two small subpaths at the top
    pts = mob.get_points()
    ends = mob.get_subpath_end_indices_from_points(pts)
    starts = [0, *(ends[:-1] + 2)]
    cy = mob.get_center()[1]
    eyes = [
        pts[a:b + 1] for a, b in zip(starts, ends)
        if np.ptp(pts[a:b + 1, 0]) < 0.1 * mob.get_width() and pts[a:b + 1, 1].mean() > cy
    ]
    eyes.sort(key=lambda p: p[:, 0].mean())
    return eyes[:2]


def blink_monster(monster):
    monster.generate_target()
    left_eye_points, right_eye_points = _eye_points(monster.target[0])
    for points in left_eye_points, right_eye_points:
        points[:, 1] = points[0, 1]
    return MoveToTarget(monster, rate_func=squish_rate_func(there_and_back, 0.4, 0.6))


class AskWhatTheMonsterActsOn(Scene):
    def construct(self):
        # Setup
        question = OldTexText(
            "The monster group describes the symmetries of ",
            "$\\underline{\\qquad\\qquad\\qquad}$",
        )
        question[1].set_color(YELLOW)
        question.to_edge(UP)

        monster = get_monster()
        monster.set_height(5)
        monster.to_corner(DL)

        self.add(monster)
        self.play(FadeIn(question, DOWN))
        self.wait()

        # Dimension counts
        dim_words = VGroup(*[
            OldTexText(
                "Something in\\\\",
                "{:,}".format(n),
                " dimensions",
                "?"
            )
            for n in [2, 3, 4, 5, 196883]
        ])
        dim_words.scale(1.25)
        dim_words.to_edge(RIGHT, buff=LARGE_BUFF)
        dim_words.set_y(1.5)

        final_words = dim_words[-1]
        dim = Integer(196883, edge_to_fix=ORIGIN)
        dim.replace(final_words[1])
        dim.match_style(final_words[1])
        final_words.replace_submobject(1, dim)
        final_words[-1].set_opacity(0)

        cross = Cross(dim_words)
        cross.set_stroke(RED, 8)
        for dim_word in dim_words[:-1]:
            cross.replace(dim_word[1], stretch=True)
            self.add(dim_word)
            self.wait()
            self.play(ShowCreation(cross, run_time=0.5))
            self.wait(0.5)
            self.remove(dim_word, cross)

        penult = dim_words[-2]
        dim.set_value(0)
        for i in 0, 2:
            final_words[i].save_state()
            final_words[i].replace(penult[i])
        self.play(
            Restore(final_words[0]),
            Restore(final_words[2]),
            FadeOut(penult[3]),
            ChangingDecimal(
                dim,
                lambda a: interpolate(5, 196883, a),
                run_time=8,
                rate_func=rush_from,
            ),
            UpdateFromAlphaFunc(
                Mobject(),
                lambda m, a, fw=final_words: fw.set_color(interpolate_color(WHITE, YELLOW, a)),
                remover=True
            )
        )
        final_words.add(dim)
        self.add(final_words)
        self.wait()
        self.play(blink_monster(monster))
        self.wait()

        # Elements of the monster
        in_sym = OldTex("\\in")
        in_sym.scale(2.5)

        monster.generate_target()
        monster.target.center().to_edge(RIGHT)
        in_sym.next_to(monster.target, LEFT, MED_LARGE_BUFF)

        self.play(
            MoveToTarget(monster),
            FadeOut(question, 3 * RIGHT),
            FadeOut(final_words, 2 * RIGHT),
            FadeIn(in_sym, 3 * LEFT),
        )

        matrix = IntegerMatrix(
            np.random.randint(0, 2, size=(6, 6)),
            v_buff=0.8,
            h_buff=0.8,
        )
        matrix.set_height(4)
        matrix.next_to(in_sym, LEFT, MED_LARGE_BUFF)

        mob_matrix = matrix.get_mob_matrix()
        groups_to_dots = [
            (mob_matrix[4, :4], OldTex("\\vdots")),
            (mob_matrix[:4, 4], OldTex("\\ldots")),
            (VGroup(mob_matrix[4, 4]), OldTex("\\ddots")),
        ]
        for group, dots in groups_to_dots:
            for elem in group:
                dots_copy = dots.copy()
                dots_copy.move_to(elem)
                elem.set_submobjects(dots_copy)

        braces = VGroup(
            Brace(matrix.get_entries(), DOWN),
            Brace(matrix.get_entries(), LEFT),
        )
        braces[1].shift(MED_SMALL_BUFF * LEFT)
        for brace in braces:
            brace.add(brace.get_text("196{,}882"))
        braces.set_color(BLUE)

        gigs_label = OldTexText("Each element $\\approx$ 4.5 Gigabytes of data!")
        gigs_label.next_to(matrix, UP, MED_LARGE_BUFF)

        self.play(Write(matrix, run_time=1))
        self.play(
            LaggedStartMap(GrowFromCenter, braces, lag_ratio=0.5, run_time=1),
            FadeIn(gigs_label, DOWN)
        )
        self.play(blink_monster(monster))
        self.wait()
