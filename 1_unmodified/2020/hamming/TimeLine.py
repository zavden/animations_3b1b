# ==============================================================================
# Scene:      TimeLine
# Source:     videos/_2020/hamming.py (lines 961-1072)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TimeLine.py TimeLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TimeLine(Scene):
    def construct(self):
        # Time line
        decades = list(range(1920, 2030, 10))
        timeline = NumberLine(
            (decades[0], decades[-1], 2),
            big_tick_numbers=decades,
            width=13
        )
        timeline.add_numbers(
            decades,
            group_with_commas=False,
            height=0.2,
        )
        timeline.numbers.set_stroke(BLACK, 4, background=True)

        # Events
        def get_event(timeline, date, words, direction=UP):
            arrow = Vector(-direction)
            arrow.set_fill(GREY_A, 0.75)
            arrow.shift(timeline.n2p(date) - arrow.get_end())
            arrow.shift(SMALL_BUFF * direction)

            label = OldTexText(words)
            label.scale(0.7)
            label.next_to(arrow.get_start(), np.sign(direction[1]) * UP, SMALL_BUFF)
            label.set_color(GREY_A)
            label.set_stroke(BLACK, 4, background=True)

            event = VGroup(label, arrow)
            return event

        events = VGroup(
            get_event(timeline, 1947, "Hamming codes", 1.5 * UP),
            get_event(timeline, 1948, "Shannon's paper\\\\on information theory", DOWN + 0.2 * LEFT),
            # get_event(timeline, 1949, "Gorlay codes", 0.7 * UP),
            get_event(timeline, 1960, "Reed-Solomon\\\\codes", 0.7 * UP),
            get_event(timeline, 1993, "Turbo codes", UP),
            get_event(timeline, 1995, "Shor codes\\\\(quantum)", DOWN),
        )

        # Title
        title = OldTexText("Error correction codes")
        title.set_color(YELLOW)
        title.set_height(0.5)
        title.to_edge(UP)
        title_underline = Underline(title)
        title_underline.match_color(title)
        title.add(title_underline)
        title.fix_in_frame()

        # Introduce time line
        frame = self.camera.frame
        frame.save_state()
        frame.scale(0.5, about_point=timeline.n2p(1945))
        frame.shift(0.5 * UP)

        self.play(
            Write(timeline),
            Write(timeline.numbers.copy(), remover=True),
            LaggedStart(
                *[Animation(Mobject()) for x in range(1)],
                *[
                    AnimationGroup(
                        Write(event[0], run_time=1),
                        GrowArrow(event[1]),
                    )
                    for event in events
                ],
                lag_ratio=0.75,
            ),
            FadeIn(title, DOWN),
            Restore(frame, run_time=6),
        )
        self.wait(2)

        # Isolate Hamming
        hamming_word = events[0][0]
        rs_word = events[2][0]
        self.play(
            hamming_word.scale, 2, {"about_edge": DL},
            hamming_word.set_fill, WHITE,
            LaggedStart(*[
                ApplyMethod(mob.set_opacity, 0.5)
                for mob in events[1:]
            ]),
            FadeOut(VGroup(title, title_underline))
        )

        invent_words = OldTexText("How to invent")
        invent_words.match_height(hamming_word[0][0])
        invent_words.next_to(events[0], UP, buff=0.3)
        invent_words.set_color(BLUE)

        self.play(Write(invent_words))
        self.wait()

        hamming_word.generate_target()
        hamming_word.target.scale(0.5, about_edge=UL)
        hamming_word.target.set_opacity(0.5)
        hamming_arrow = events[0][1]

        self.play(
            MoveToTarget(hamming_word),
            FadeOut(invent_words),
            hamming_arrow.put_start_and_end_on, hamming_word.target.get_bottom(), hamming_arrow.get_end(),
            hamming_arrow.set_opacity, 0.5,
            rs_word.scale, 1.5, {"about_edge": DOWN},
            rs_word.set_opacity, 1,
            events[2][1].set_opacity, 1,
        )
        self.wait()
