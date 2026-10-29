# ==============================================================================
# Scene:      AskAboutFavoriteMegaNumber
# Source:     videos/_2020/monster.py (lines 264-318)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutFavoriteMegaNumber.py AskAboutFavoriteMegaNumber -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutFavoriteMegaNumber(TeacherStudentsScene):
    CONFIG = {
        "background_color": BLACK,
    }

    def construct(self):
        self.remove(self.pi_creatures)
        # YouTubers
        title = OldTexText("What's your favorite number $> 1{,}000{,}000$?")
        title.set_width(FRAME_WIDTH - 1)
        title.to_edge(UP)

        images = Group(
            ImageMobject("standupmaths"),
            ImageMobject("singingbanana"),
            ImageMobject("Ben Sparks"),
            ImageMobject("Zoe Griffiths"),
            ImageMobject("tomrocksmaths"),
            ImageMobject("James Tanton"),
            ImageMobject("blackpenredpen"),
            ImageMobject("Eddie Woo"),
        )
        images.arrange_in_grid(2, 4, buff=MED_LARGE_BUFF)
        images.set_width(FRAME_WIDTH - 2)
        images.next_to(title, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(title, DOWN),
            LaggedStartMap(
                FadeIn, images,
                lambda m: (m, -0.1 * m.get_center()),
                lag_ratio=0.3,
                run_time=5,
            )
        )
        self.wait()

        # Pi Creatures
        self.teacher_says(
            "And we want\\\\you to join!",
            target_mode="surprised",
            bubble_config={
                "height": 3,
                "width": 4,
            },
            added_anims=[
                VFadeIn(self.pi_creatures),
                images.scale, 0.2,
                images.space_out_submobjects, 10,
                images.set_opacity, 0,
            ],
        )
        self.remove(images)
        self.play_student_changes("guilty", "hooray", "wave_2")
        self.wait(5)
