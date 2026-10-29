# ==============================================================================
# Scene:      IntroduceGroupTheory
# Source:     videos/_2020/monster.py (lines 448-743)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceGroupTheory.py IntroduceGroupTheory -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_snowflake(height=2):
    snowflake = SVGMobject("snowflake")
    snowflake.set_fill(GREY_C, 1)
    snowflake.set_gloss(1)
    snowflake.set_shadow(0.2)
    snowflake.set_stroke(WHITE, 1)
    snowflake.set_height(height)
    return snowflake


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


class IntroduceGroupTheory(Scene):
    def construct(self):
        # Title
        over_title = OldTexText("An introduction\\\\to")
        over_title.scale(2.5)
        over_title.move_to(ORIGIN, DOWN)

        title = OldTexText("Group theory")
        title.scale(2.5)
        title.next_to(over_title, DOWN, buff=0.5)

        arrows = VGroup(Vector(DOWN), Vector(UP))
        arrows.arrange(RIGHT, buff=SMALL_BUFF)
        arrows.scale(2)
        arrows.next_to(title, DOWN, buff=MED_LARGE_BUFF)

        sym_amb = SVGMobject("symmetry_ambigram")
        sym_amb.set_stroke(width=0)
        sym_amb.set_fill(BLUE, 1)
        sym_amb.match_width(title)
        sym_amb.next_to(arrows, DOWN)
        sym_amb_ghost = sym_amb.copy()
        sym_amb_ghost.set_fill(WHITE, 0.2)

        self.add(over_title, title)
        self.wait()
        self.play(
            title.scale, 2.0 / 2.5,
            title.to_edge, UP,
            FadeOut(over_title, UP)
        )

        self.play(FadeIn(title, DOWN))
        self.play(
            LaggedStartMap(GrowArrow, arrows, run_time=1),
            Write(sym_amb, run_time=2)
        )
        self.add(sym_amb_ghost, sym_amb)
        self.play(Rotate(sym_amb, PI, run_time=2))
        self.remove(sym_amb_ghost)
        self.wait()

        # Symmetries of a face
        face = ImageMobject("average_face")
        face.set_height(5)

        sym_word = OldTexText("Symmetric")
        sym_word.scale(2)
        sym_word.to_edge(UP)
        face.next_to(sym_word, DOWN, buff=MED_LARGE_BUFF)
        sym_word.save_state()
        sym_word.replace(sym_amb)
        sym_word.set_opacity(0)

        face_citation = OldTexText("``Average face'' from the Face Research Lab\\\\DeBruine, Lisa \\& Jones, Benedict (2017)")
        face_citation.set_height(0.4)
        face_citation.next_to(face, DOWN)
        face_citation.to_corner(DL)

        sym_line = DashedLine(face.get_top(), face.get_bottom())
        sym_line.scale(1.05)
        sym_line.set_stroke(WHITE, 2)

        self.play(
            FadeIn(face, DOWN),
            FadeIn(face_citation),
            LaggedStartMap(FadeOut, VGroup(*arrows, title), lambda m: (m, UP)),
            sym_amb.replace, sym_word.saved_state, {"stretch": True},
            sym_amb.set_opacity, 0,
            Restore(sym_word),
        )
        self.remove(sym_amb)
        self.wait()
        self.play(ShowCreation(sym_line), FadeOut(face_citation))
        sym_line.rotate(PI)
        self.play(ApplyMethod(face.stretch, -1, 0, run_time=2))
        self.wait()

        sym_to_action = OldTexText("Symmetry", " $\\Rightarrow$ ", "\\emph{Action}")
        sym_to_action.set_color_by_tex("Action", YELLOW)
        sym_to_action.replace(sym_word, dim_to_match=1)
        self.play(
            ReplacementTransform(sym_word[0], sym_to_action[0]),
            Write(sym_to_action[1]),
            FadeIn(sym_to_action[2], LEFT),
        )
        self.play(ApplyMethod(face.stretch, -1, 0, run_time=2))
        self.wait()

        # Symmetries of a snowflake
        snowflake = get_snowflake()
        snowflake.set_height(5)
        snowflake.next_to(sym_to_action, DOWN, MED_LARGE_BUFF)
        self.play(
            FadeOut(face),
            Uncreate(sym_line),
            ShowCreationThenFadeOut(snowflake.copy().set_stroke(WHITE, 2).set_fill(opacity=0)),
            FadeIn(snowflake, run_time=2),
        )

        def get_flake_rot_icon(degrees, snowflake=snowflake):
            return get_rot_icon(degrees, snowflake)

        def get_flake_flip_icon(angle, snowflake=snowflake):
            return get_flip_icon(angle, snowflake)

        rot_icons = VGroup(
            get_flake_rot_icon(60),
            get_flake_rot_icon(120),
        )
        flip_icons = VGroup(
            get_flake_flip_icon(60 * DEGREES),
            get_flake_flip_icon(30 * DEGREES),
        )
        for icons, vect in [(rot_icons, LEFT), (flip_icons, RIGHT)]:
            icons.arrange(DOWN, buff=MED_LARGE_BUFF)
            icons.to_edge(vect)

        self.play(
            FadeIn(rot_icons[0]),
            Rotate(snowflake, 60 * DEGREES)
        )
        self.wait()
        self.play(
            FadeIn(rot_icons[1]),
            Rotate(snowflake, 120 * DEGREES)
        )
        self.wait()

        sym_line = DashedLine(snowflake.get_bottom(), snowflake.get_top())
        sym_line.scale(1.1)
        sym_line.set_stroke(WHITE, 2)
        sym_line.set_angle(60 * DEGREES)
        sym_line.move_to(snowflake)
        self.play(
            ShowCreation(sym_line),
            FadeIn(flip_icons[0]),
        )
        self.play(
            Rotate(snowflake, PI, axis=rotate_vector(RIGHT, 60 * DEGREES)),
        )
        self.play(
            sym_line.set_angle, 30 * DEGREES,
            sym_line.move_to, snowflake,
            FadeIn(flip_icons[1]),
        )
        self.play(
            Rotate(snowflake, PI, axis=rotate_vector(RIGHT, 30 * DEGREES)),
        )

        # Collection of all snowflake symmetries
        rot_icons.generate_target()
        flip_icons.generate_target()
        d6_group = VGroup(
            get_flake_rot_icon(0),
            rot_icons.target[0],
            rot_icons.target[1],
            get_flake_rot_icon(180),
            get_flake_rot_icon(-120),
            get_flake_rot_icon(-60),
            get_flake_flip_icon(0),
            flip_icons.target[1],
            flip_icons.target[0],
            get_flake_flip_icon(90 * DEGREES),
            get_flake_flip_icon(120 * DEGREES),
            get_flake_flip_icon(150 * DEGREES),
        )
        d6_group.arrange_in_grid(2, 6)
        d6_group.set_width(FRAME_WIDTH - 2)
        d6_group.set_gloss(0)
        d6_group.set_shadow(0)
        for mob in d6_group.get_family():
            if isinstance(mob, SVGMobject):
                mob.set_fill(GREY_C, 1)
                mob.set_stroke(WHITE, 0.25)

        self.play(
            MoveToTarget(rot_icons),
            MoveToTarget(flip_icons),
            ApplyMethod(snowflake.scale, 0, remover=True),
            ApplyMethod(sym_line.scale, 0, remover=True),
        )
        self.play(LaggedStartMap(FadeIn, d6_group))
        self.remove(rot_icons, flip_icons)
        self.wait()

        # Name groups
        group_name = OldTexText("Group", "$^*$")
        group_name.scale(2)
        group_name.to_edge(UP)
        footnote = OldTexText("$^*$er...kind of.  Keep watching")
        footnote.set_height(0.3)
        footnote.to_corner(UR)
        footnote.add(group_name[1])
        footnote.set_color(YELLOW)
        group_name.remove(group_name[1])
        d6_rect = SurroundingRectangle(d6_group)
        d6_rect.set_stroke(BLUE, 2)

        self.play(
            FadeOut(sym_to_action, UP),
            FadeIn(group_name, DOWN),
            ShowCreation(d6_rect),
        )
        self.play(
            FadeIn(
                footnote,
                rate_func=there_and_back_with_pause,
                run_time=3,
                remover=True
            )
        )
        self.wait()

        anims = []
        for icon, deg in zip(d6_group[1:], [60, 120, 180, -120, -60]):
            anims.append(Rotate(icon[0], deg * DEGREES))
        for icon, deg in zip(d6_group[6:], range(0, 180, 30)):
            anims.append(Rotate(icon[0], PI, axis=rotate_vector(RIGHT, deg * DEGREES)))
        random.shuffle(anims)
        self.play(LaggedStart(*anims, lag_ratio=0.3, run_time=5))
        self.play(LaggedStart(*reversed(anims), lag_ratio=0.3, run_time=5))

        # Identity
        id_rect = SurroundingRectangle(d6_group[0])
        id_words = OldTexText("The do-nothing", "\\\\action", alignment="")
        id_words.to_corner(UL)
        id_arrow = Arrow(id_words[1].get_bottom(), id_rect.get_top(), buff=0.2)
        id_arrow.match_color(id_rect)
        self.play(
            ShowCreation(id_rect)
        )
        self.play(
            FadeIn(id_words, lag_ratio=0.1),
            GrowArrow(id_arrow),
        )
        self.wait()

        # Count d6
        rects = VGroup(id_rect, *map(SurroundingRectangle, d6_group[1:]))
        counter = Integer(0)
        counter.set_height(0.8)
        counter.next_to(d6_rect, DOWN, MED_LARGE_BUFF)
        counter.set_color(YELLOW)
        counter.add_updater(lambda m, rects=rects: m.set_value(len(rects)))

        self.add(counter)
        self.play(
            FadeOut(id_words),
            FadeOut(id_arrow),
            ShowIncreasingSubsets(rects, int_func=np.ceil, run_time=2),
            UpdateFromAlphaFunc(counter, lambda m, a: m.set_opacity(a))
        )
        self.wait()

        d6_name = OldTex("D_6")
        d6_name.scale(2)
        d6_name.move_to(counter)
        d6_name.set_color(BLUE)
        self.play(
            FadeOut(rects, lag_ratio=0.1),
            FadeOut(counter, 0.2 * UP),
            FadeIn(d6_name, 0.2 * DOWN),
        )
        self.wait()

        # Name C2
        face_group = Group(face, face.deepcopy())
        face_group.set_height(4)
        face_group.arrange(RIGHT, buff=LARGE_BUFF)
        face_group.next_to(group_name, DOWN, MED_LARGE_BUFF)
        sym_line = DashedLine(2 * UP, 2 * DOWN)
        sym_line.set_stroke(WHITE, 2)
        sym_line.move_to(face_group[1])
        sym_line.set_height(face_group[1].get_height() * 1.1)
        face_group[1].add(sym_line)

        self.play(
            d6_rect.replace, face_group, {"stretch": True},
            d6_rect.scale, 1.1,
            FadeOut(d6_group),
            FadeOut(d6_name, DOWN),
            *[
                FadeIn(f, -0.5 * f.get_center())
                for f in face_group
            ],
        )
        self.play(face_group[1].stretch, -1, 0)
        self.wait()

        z2_name = OldTex("C_2")
        z2_name.match_color(d6_name)
        z2_name.match_height(d6_name)
        z2_name.next_to(d6_rect, DOWN, MED_LARGE_BUFF)
        self.play(Write(z2_name))
        self.wait()
