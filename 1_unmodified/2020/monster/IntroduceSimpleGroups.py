# ==============================================================================
# Scene:      IntroduceSimpleGroups
# Source:     videos/_2020/monster.py (lines 3191-3365)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceSimpleGroups.py IntroduceSimpleGroups -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceSimpleGroups(Scene):
    def construct(self):
        # Setup
        bg_rect = FullScreenFadeRectangle(fill_color=GREY_E, fill_opacity=1)
        self.add(bg_rect)

        groups = OldTexText("Groups")
        groups.scale(2)
        groups.to_edge(UP)
        inf_groups = OldTexText("Infinite groups")
        fin_groups = OldTexText("Finite groups")
        children = VGroup(inf_groups, fin_groups)
        children.scale(1.5)
        children.arrange(RIGHT, buff=2)
        children.next_to(groups, DOWN, buff=2)
        child_lines = VGroup(*[
            Line(groups.get_bottom(), child.get_top(), buff=0)
            for child in children
        ])
        child_lines.set_stroke(WHITE, 2)
        s_rects = VGroup(*[
            ScreenRectangle(height=3).move_to(child)
            for child in children
        ])
        s_rects.next_to(children, DOWN)
        s_rects.set_fill(BLACK, 1)

        # Introductions
        self.add(groups)
        self.wait()
        self.play(
            ShowCreation(child_lines[0]),
            FadeIn(inf_groups, 2 * UR),
            FadeIn(s_rects[0])
        )
        self.wait(2)
        self.play(
            ShowCreation(child_lines[1]),
            FadeIn(fin_groups, 2 * UL),
            FadeIn(s_rects[1]),
        )
        self.wait()

        self.add(s_rects, fin_groups)
        self.play(
            Uncreate(child_lines),
            FadeOut(inf_groups, 3 * LEFT),
            FadeOut(s_rects[0], 3 * LEFT),
            FadeOut(groups, 2 * UP),
            fin_groups.move_to, groups,
            s_rects[1].replace, bg_rect,
            s_rects[1].set_stroke, {"width": 0},
            run_time=2,
        )
        self.remove(s_rects, bg_rect)

        # Comparison titles
        bg_rects = VGroup(*[
            Rectangle(
                height=FRAME_HEIGHT,
                width=FRAME_WIDTH / 3,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            )
            for color in [GREY_D, GREY_E, BLACK]
        ])
        bg_rects.arrange(RIGHT, buff=0)
        bg_rects.center()

        fin_groups.generate_target()
        titles = VGroup(
            OldTexText("Integers").scale(1.5),
            OldTexText("Molecules").scale(1.5),
            fin_groups.target,
        )
        sub_titles = VGroup(*[
            OldTexText("break down into\\\\", word)
            for word in ("primes", "atoms", "simple groups")
        ])

        for rect, title, sub_title in zip(bg_rects, titles, sub_titles):
            title.move_to(rect, UP)
            title.shift(0.5 * DOWN)
            sub_title.next_to(title, DOWN)
            sub_title[1].set_color(BLUE)
            sub_title.align_to(sub_titles[0], UP)

        # Comparison diagrams
        H_sphere = Sphere()
        H_sphere.set_height(0.5)
        H_sphere.set_color(RED)
        H_atom = Group(
            H_sphere,
            OldTexText("H").scale(0.5).move_to(H_sphere)
        )
        O_sphere = Sphere()
        O_sphere.set_height(1)
        O_sphere.set_color(BLUE)
        O_atom = Group(
            O_sphere,
            OldTexText("O").scale(0.75).move_to(O_sphere)
        )
        H2O = Group(
            O_atom.copy(),
            H_atom.copy().move_to([-0.45, 0.35, 0]),
            H_atom.copy().move_to([0.45, 0.35, 0]),
        )

        trees = Group(
            VGroup(
                Integer(60),
                VGroup(*map(Integer, [2, 2, 3, 5])),
            ),
            Group(
                H2O,
                Group(H_atom.copy(), H_atom.copy(), O_atom.copy())
            ),
            VGroup(
                OldTex("S_4"),
                VGroup(*[
                    OldTex(
                        "C_" + str(n),
                        fill_color=(RED_B if n == 2 else BLUE)
                    )
                    for n in [2, 2, 2, 3]
                ]),
            )
        )
        for tree, rect in zip(trees, bg_rects):
            root, children = tree
            children.arrange(RIGHT, buff=0.35)
            children.next_to(root, DOWN, buff=1.2)
            lines = VGroup()
            for child in children:
                lines.add(Line(root.get_bottom(), child.get_top(), buff=0.1))
            tree.add(lines)
            tree.move_to(rect)
            tree.shift(DOWN)

        # Slice screen
        self.add(bg_rects, fin_groups)
        for rect in bg_rects:
            rect.save_state()
            rect.shift(LEFT)
            rect.set_fill(BLACK, 1)
        self.play(
            MoveToTarget(fin_groups),
            LaggedStartMap(Restore, bg_rects, lag_ratio=0.3)
        )

        # Breakdowns
        for title, sub_title, tree in zip(titles, sub_titles, trees):
            root, children, lines = tree
            self.play(
                FadeIn(title),
                FadeIn(root),
            )
            globals()['root'] = root
            self.play(
                ShowCreation(lines),
                LaggedStart(*[
                    GrowFromPoint(child, root)
                    for child in children
                ]),
                FadeIn(sub_title)
            )
            self.wait()

        # Theorem
        theorem_name = OldTexText("(Jordan–Hölder Theorem)")
        theorem_name.scale(0.7)
        theorem_name.next_to(sub_titles[2], DOWN)
        self.play(Write(theorem_name, run_time=1))
        self.wait()
