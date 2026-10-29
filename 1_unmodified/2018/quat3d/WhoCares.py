# ==============================================================================
# Scene:      WhoCares
# Source:     videos/_2018/quat3d.py (lines 236-360)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoCares.py WhoCares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhoCares(TeacherStudentsScene):
    def construct(self):
        quotes = Group(*[
            ImageMobject(
                "CoderQuaternionResponse_{}".format(d),
                height=2
            )
            for d in range(4)
        ])
        logos = Group(*[
            ImageMobject(name, height=0.5)
            for name in [
                "TwitterLogo",
                "HackerNewsLogo",
                "RedditLogo",
                "YouTubeLogo",
            ]
        ])
        for quote, logo in zip(quotes, logos):
            logo.move_to(quote.get_corner(UR))
            quote.add(logo)

        quotes.arrange_in_grid()
        quotes.set_height(4)
        quotes.to_corner(UL)

        self.student_says(
            "Um...who cares?",
            target_mode="sassy",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_student_changes("angry", "sassy", "sad")
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand"
        )
        # self.play(
        #     LaggedStartMap(
        #         FadeInFromDown, quotes,
        #         run_time=3
        #     ),
        #     self.change_students(*3 * ["pondering"], look_at=quotes)
        # )
        # self.wait(2)

        # # Show HN
        # hn_quote = quotes[1]
        # hn_context = OldTexText("news.ycombinator.com/item?id=17933908")
        # hn_context.scale(0.7)
        # hn_context.to_corner(UL)

        # vr_headsets = VGroup()
        # for pi in self.students:
        #     vr_headset = SVGMobject("VR_headset")
        #     vr_headset.set_fill(GREY_B, opacity=0.9)
        #     vr_headset.set_width(pi.eyes.get_width() + 0.3)
        #     vr_headset.move_to(pi.eyes)
        #     vr_headsets.add(vr_headset)

        # self.play(
        #     hn_quote.scale, 2, {"about_edge": DL},
        #     FadeOut(quotes[0], 5 * UP),
        #     FadeOut(quotes[2], UR),
        #     FadeOut(quotes[3], RIGHT),
        #     FadeInFromDown(hn_context),
        # )
        # hn_rect = Rectangle(
        #     height=0.1 * hn_quote.get_height(),
        #     width=0.6 * hn_quote.get_width(),
        #     color=RED
        # )
        # hn_rect.move_to(hn_quote, UL)
        # hn_rect.shift(0.225 * RIGHT + 0.75 * DOWN)
        # self.play(
        #     ShowCreation(hn_rect),
        #     self.change_students(
        #         "erm", "thinking", "confused",
        #         look_at=hn_quote,
        #     )
        # )
        # self.add_foreground_mobjects(vr_headsets)
        # self.play(
        #     LaggedStartMap(
        #         FadeInFrom, vr_headsets,
        #         lambda m: (m, UP),
        #     ),
        #     self.change_students(
        #         *3 * ["sick"],
        #         look_at=hn_quote,
        #         run_time=3
        #     )
        # )
        # self.wait(3)

        # Show Twitter
        t_quote = quotes[0]
        # t_quote.next_to(FRAME_WIDTH * LEFT / 2 + FRAME_WIDTH * UP / 2, UR)
        # t_quote.set_opacity(0)
        # self.play(
        #     FadeOut(hn_quote, 4 * LEFT),
        #     FadeOut(hn_rect, 4 * LEFT),
        #     FadeOut(hn_context, UP),
        #     FadeOut(vr_headsets),
        #     t_quote.set_opacity, 1,
        #     t_quote.scale, 2,
        #     t_quote.to_corner, UL,
        # )
        # self.remove_foreground_mobjects(vr_headsets)
        t_quote.fade(1)
        t_quote.to_corner(UL)
        self.play(
            self.change_students(*3 * ["pondering"], look_at=quotes),
            t_quote.set_opacity, 1,
            t_quote.scale, 2,
            t_quote.to_corner, UL,
        )
        self.wait(2)
        self.play_student_changes(
            "pondering", "happy", "tease",
            look_at=t_quote
        )
        self.wait(2)
        self.play(FadeOut(t_quote))
        self.wait(5)
