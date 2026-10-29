# ==============================================================================
# Scene:      ProblemSolvingPrinciplesWithPis
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 342-421)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProblemSolvingPrinciplesWithPis.py ProblemSolvingPrinciplesWithPis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProblemSolvingPrinciplesWithPis(TeacherStudentsScene):
    def construct(self):
        # Prep
        morty = self.teacher
        stds = self.students
        for pi in [morty, *stds]:
            pi.body.insert_n_curves(100)

        # Title
        title = Text("Problem-solving principles", font_size=72)
        title.to_edge(UP)
        underline = Underline(title, buff=-0.1)
        VGroup(title, underline).set_color(BLUE)
        title.set_backstroke(width=3)

        # Items
        items = BulletedList(
            "Try a simpler version of the problem",
            "Use the defining features of the problem",
            "List any equations that might be relevant",
            "Seek symmetry",
            "Compute something (anything) to build intuition",
            "Run simulations (if possible) to build intuition",
            "Draw pictures!",
        )
        items.next_to(title, DOWN, buff=0.35)
        items.to_edge(LEFT, buff=0.75)
        items.save_state()

        # Have students toss up examples
        np.random.seed(0)
        for y, item in enumerate(items):
            item.set_height(0.25)
            item.set_opacity(0.8)
            item[0].set_opacity(0)
            item.next_to(underline, DOWN)
            item.shift(np.random.uniform(-5, 5) * RIGHT)
            item.shift(0.5 * y * DOWN)

        self.play(
            morty.change("raise_right_hand", underline),
            self.change_students("pondering", "pondering", "pondering", look_at=underline),
            FadeIn(title, lag_ratio=0.1),
            ShowCreation(underline),
        )
        self.play(morty.change("tease", stds))
        self.wait()
        index_mode_pairs = [
            (0, "raise_right_hand"),
            (2, "raise_right_hand"),
            (1, "raise_right_hand"),
            (2, "raise_left_hand"),
            (0, "raise_left_hand"),
            (1, "raise_left_hand"),
            (2, "raise_right_hand"),
        ]
        for item, pair in zip(items, index_mode_pairs):
            index, mode = pair
            if mode == "raise_left_hand":
                item.shift(2 * LEFT).shift_onto_screen()
            self.play(
                stds[index].change(mode, item),
                FadeIn(item, scale=3, shift=item.get_center() - stds[index].get_center())
            )
        self.wait(3)

        # Return to position
        self.play(
            Restore(items, run_time=2, lag_ratio=1e-3),
            FadeOut(self.pi_creatures),
            FadeOut(self.background),
        )
        self.wait()

        # Isolate a few items
        for index in [2, 6, 3]:
            self.play(
                items.animate.fade_all_but(index),
            )
            self.wait()
