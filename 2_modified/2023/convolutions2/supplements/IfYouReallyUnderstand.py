# ==============================================================================
# Scene:      IfYouReallyUnderstand
# Source:     videos/_2023/convolutions2/supplements.py (lines 15-64)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IfYouReallyUnderstand.py IfYouReallyUnderstand -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - A bubble's content is now its child (manimgl, March 2024): only the body is transformed (the content is already transformed separately) and only the bubble is shifted, which used to move together with its content separately
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IfYouReallyUnderstand(TeacherStudentsScene):
    def construct(self):
        # Initial comments
        morty = self.teacher
        self.play(
            morty.says(TexText(R"If you \emph{really} \\ understand"), run_time=1.5),
            self.change_students("pondering", "confused", "erm", look_at=self.screen)
        )
        self.wait()

        old_bubble = morty.bubble
        old_words = morty.bubble.content
        new_bubble = morty.get_bubble(
            TexText(R"You'll understand \\ why normal distributions \\ are special"),
            bubble_type=SpeechBubble,
            width=5, height=4,
        )
        new_bubble.content.scale(1.2)
        # CHANGE: the content is now a child of the bubble; if it was also moved separately it was shifted twice
        new_bubble.shift(0.5 * RIGHT)
        self.play(
            # CHANGE: now the content is a child of the bubble; only the body is transformed (the content is already transformed below)
            Transform(old_bubble.body, new_bubble.body),
            Transform(old_words, new_bubble.content, run_time=1),
            morty.change("tease"),
        )
        self.remove(old_bubble, old_words)
        self.add(new_bubble, new_bubble.content)
        morty.bubble = new_bubble

        # Stare at it
        self.wait()
        self.play(self.change_students(None, "tease", "maybe", look_at=self.screen))
        self.wait(3)
        self.play(self.change_students("happy", "erm", "hesitant", look_at=self.screen, lag_ratio=0.2))
        self.wait(3)

        # The real lesson
        title = TexText("Today's lesson:", font_size=60)
        subtitle = Text("How to add random\nvariables, in general", font_size=48)
        title.set_x(FRAME_WIDTH / 4).to_edge(UP, buff=MED_SMALL_BUFF)
        subtitle.next_to(title, DOWN, buff=LARGE_BUFF)

        self.play(
            morty.debubble("raise_right_hand"),
            FadeIn(title, UP),
            self.change_students("pondering", "pondering", "hesitant", look_at=title),
        )
        self.play(FadeIn(subtitle, lag_ratio=0.1))
        self.wait(2)
        self.play(self.change_students("maybe", "hesitant", "well", look_at=self.screen))
        self.wait(4)
