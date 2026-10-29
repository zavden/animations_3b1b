# ==============================================================================
# Scene:      ContrastChapters1And2
# Source:     videos/_2019/diffyq/part2/staging.py (lines 262-366)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastChapters1And2.py ContrastChapters1And2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContrastChapters1And2(Scene):
    def construct(self):
        c1_frame, c2_frame = frames = VGroup(*[
            ScreenRectangle(height=3.5)
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)

        c1_title, c2_title = titles = VGroup(
            OldTexText("Chapter 1"),
            OldTexText("Chapter 2"),
        )
        titles.scale(1.5)

        ode, pde = des = VGroup(
            OldTexText(
                "Ordinary",
                "Differential Equations\\\\",
                "ODEs",
            ),
            OldTexText(
                "Partial",
                "Differential Equations\\\\",
                "PDEs",
            ),
        )
        ode[0].set_color(BLUE)
        pde[0].set_color(YELLOW)
        for de in des:
            de[-1][0].match_color(de[0])
            de[-1].scale(1.5, about_point=de.get_top())

        for title, frame, de in zip(titles, frames, des):
            title.next_to(frame, UP)
            de.match_width(frame)
            de.next_to(frame, DOWN)

        lt = OldTex("<")
        lt.move_to(Line(ode.get_right(), pde.get_left()))
        lt.scale(2, about_edge=UP)

        c1_words = OldTexText(
            "They're", "really\\\\", "{}",
            "freaking", "hard\\\\",
            "to", "solve\\\\",
        )
        c1_words.set_height(0.5 * c1_frame.get_height())
        c1_words.move_to(c1_frame)

        c2_words = OldTexText(
            "They're", "really", "\\emph{really}\\\\",
            "freaking", "hard\\\\",
            "to", "solve\\\\",
        )
        c2_words.set_color_by_tex("\\emph", YELLOW)
        c2_words.move_to(c2_frame)
        edit_shift = MED_LARGE_BUFF * RIGHT
        c2_edits = VGroup(
            OldTexText("sometimes").next_to(
                c2_words[1:3], UP,
                aligned_edge=LEFT,
            ),
            Line(
                c2_words[1].get_left(),
                c2_words[2].get_right(),
                stroke_width=8,
            ),
            OldTexText("not too").next_to(
                c2_words[3], LEFT,
            ),
            Line(
                c2_words[3].get_left(),
                c2_words[3].get_right(),
                stroke_width=8,
            ),
        )
        c2_edits.set_color(RED)
        c2_edits[2:].shift(edit_shift)

        self.add(titles)
        self.add(frames)
        self.add(des)

        self.wait()
        self.play(LaggedStartMap(
            FadeInFromDown, c1_words,
            lag_ratio=0.1,
        ))
        self.wait()
        # self.play(FadeIn(ode))
        self.play(
            # TransformFromCopy(ode, pde),
            TransformFromCopy(c1_words, c2_words),
            Write(lt)
        )
        self.wait()
        self.play(
            Write(c2_edits[:2], run_time=1),
        )
        self.play(
            c2_words[3:5].shift, edit_shift,
            Write(c2_edits[2:]),
            run_time=1,
        )
        self.wait()
