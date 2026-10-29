# ==============================================================================
# Scene:      ForcedOscillatorSolutionForm
# Source:     videos/_2025/laplace/exponentials.py (lines 1118-1334)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ForcedOscillatorSolutionForm.py ForcedOscillatorSolutionForm -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ForcedOscillatorSolutionForm(InteractiveScene):
    def construct(self):
        # Create linear combination
        exp_texs = [Rf"e^{{s_{n} t}}" for n in range(1, 5)]
        const_texs = [Rf"c_{n}" for n in range(1, 5)]
        terms = [" ".join(pair) for pair in zip(const_texs, exp_texs)]
        solution = Tex("x(t) = " + " + ".join(terms), isolate=[*exp_texs, *const_texs])
        solution.to_edge(RIGHT)

        solution[re.compile(r's_\w+')].set_color(YELLOW)
        solution[re.compile(r'c_\w+')].set_color(BLUE)

        cut_index = solution.submobjects.index(solution["+"][1][0])
        first_two = solution[:cut_index]
        last_two = solution[cut_index:]

        first_two.save_state()
        first_two.to_edge(RIGHT, buff=1.5)

        self.add(first_two)

        # Not this
        ex_mark = Exmark(font_size=72).set_color(RED)
        checkmark = Checkmark(font_size=72).set_color(GREEN)
        ex_mark.next_to(first_two, UP, MED_LARGE_BUFF, aligned_edge=LEFT)
        checkmark.next_to(first_two.saved_state, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        nope = Text("Nope!", font_size=60).set_fill(border_width=4)
        nope.match_color(ex_mark)
        nope.next_to(ex_mark, RIGHT)

        actually = Text("Actually...", font_size=60)
        actually.set_fill(border_width=2)
        actually.match_color(checkmark)
        actually.next_to(checkmark, RIGHT, SMALL_BUFF, aligned_edge=DOWN, index_of_submobject_to_align=0)

        self.play(Write(ex_mark), Write(nope))

        # Freely tune coefficients
        c_trackers = ValueTracker(0).replicate(2)

        def get_c_values():
            return [tracker.get_value() for tracker in c_trackers]

        number_lines = VGroup(
            NumberLine((-3, 3), width=2).rotate(90 * DEG).next_to(solution[c_tex], DOWN)
            for c_tex in const_texs[:2]
        )
        for line in number_lines:
            line.set_width(0.1, stretch=True)
            line.add_numbers(font_size=12, direction=LEFT, buff=0.1)

        tips = ArrowTip().rotate(PI).set_height(0.2).replicate(2)
        tips.set_color(BLUE)

        def update_tips(tips):
            for tip, line, value in zip(tips, number_lines, get_c_values()):
                tip.move_to(line.n2p(value), LEFT)
            return tips

        tips.add_updater(update_tips)

        c_labels = VGroup(DecimalNumber(0, font_size=24) for _ in range(2))

        def update_c_labels(c_labels):
            for label, tip, value in zip(c_labels, tips, get_c_values()):
                label.set_value(value)
                label.next_to(tip, RIGHT, SMALL_BUFF)

        c_labels.add_updater(update_c_labels)

        def random_tuning_animation(run_time=2, lag_ratio=0.25):
            return LaggedStart(
                *(
                    tracker.animate.set_value(random.uniform(-3, 3))
                    for tracker in c_trackers
                ),
                lag_ratio=lag_ratio,
                run_time=run_time,
            )

        self.play(
            FadeIn(number_lines),
            VFadeIn(tips),
            VFadeIn(c_labels),
            random_tuning_animation()
        )
        for _ in range(6):
            self.play(random_tuning_animation())
        self.wait()

        # Show four particulcar exponentials
        plane = ComplexPlane((-3, 3), (-2, 2))
        plane.set_height(3.25)
        plane.to_corner(UL)
        plane.add_coordinate_labels(font_size=16)
        plane.coordinate_labels[-1].set_opacity(0)

        s_values = [1.5j, -1.5j, -0.3 + 1.0j, -0.3 - 1.0j]
        s_dots = Group(
            GlowDot(plane.n2p(s))
            for s in s_values
        )
        s_labels = VGroup(
            Tex(Rf"s_{n}", font_size=24).set_color(YELLOW).next_to(dot, vect, buff=-0.1)
            for n, dot, vect in zip(it.count(1), s_dots, [RIGHT, RIGHT, LEFT, LEFT])
        )

        self.play(LaggedStart(
            FadeOut(number_lines, lag_ratio=0.1),
            FadeOut(tips, lag_ratio=0.1),
            FadeOut(c_labels, lag_ratio=0.1),
            FadeOut(VGroup(ex_mark, nope), LEFT),
            FadeIn(VGroup(checkmark, actually), LEFT),
            Restore(first_two),
            FadeIn(last_two, LEFT),
            run_time=2
        ))
        self.play(
            FadeIn(plane),
            LaggedStartMap(FadeIn, s_dots),
            LaggedStart(
                *(
                    FadeTransform(solution[f"s_{n + 1}"].copy(), s_labels[n])
                    for n in range(4)
                )
            ),
        )
        self.wait()

        # Comment on constants
        const_rects = VGroup(
            SurroundingRectangle(solution[c_tex], buff=0.075)
            for c_tex in const_texs
        )
        const_rects.set_stroke(BLUE, 2)

        underlines = VGroup(
            Line(c1.get_bottom(), c2.get_bottom(), path_arc=40 * DEG)
            for c1, c2 in it.combinations(const_rects, 2)
        )
        underlines.set_stroke(TEAL, 2)
        underlines.insert_n_curves(10)

        underlines = VGroup(
            Vector(0.75 * UP, thickness=4).next_to(rect, DOWN, buff=0)
            for rect in const_rects
        )
        underlines.set_fill(BLUE)

        constraint_words = TexText("Only specific $c_n$ work")
        constraint_words.set_fill(BLUE, border_width=1)
        constraint_words.match_width(underlines)
        constraint_words.next_to(underlines, DOWN, buff=SMALL_BUFF)

        self.play(
            FadeIn(constraint_words, lag_ratio=0.1),
            FadeOut(checkmark),
            FadeOut(actually),
            LaggedStartMap(ShowCreation, const_rects, lag_ratio=0.25),
            LaggedStartMap(GrowArrow, underlines),
        )
        self.play(FadeOut(const_rects, lag_ratio=0.1))

        # Add exponential parts
        if False:
            # For an insertion
            for term, s in zip(exp_texs, s_values):
                exp_diagram = self.get_exponential_diagram(solution[term], s)
                self.add(exp_diagram)
            self.wait(24)

        # Ask about each part
        term_rects = VGroup(
            SurroundingRectangle(solution[term], buff=0.1).set_stroke(TEAL, 2)
            for term in terms
        )
        s_rects = VGroup(
            SurroundingRectangle(solution[exp_tex][0][1:3], buff=0.05).set_stroke(YELLOW, 2)
            for exp_tex in exp_texs
        )

        moving_rects = const_rects.copy()
        self.remove(const_rects)

        anim_kw = dict(lag_ratio=0.25, run_time=1.5)
        self.play(
            FadeOut(constraint_words),
            FadeOut(underlines),
            Transform(moving_rects, term_rects, **anim_kw)
        )
        self.wait()
        self.play(Transform(moving_rects, s_rects, **anim_kw))
        self.wait()
        self.play(Transform(moving_rects, const_rects, **anim_kw))
        self.wait()
        self.play(FadeOut(moving_rects, **anim_kw))

    def get_exponential_diagram(self, term, s, c=1.0, color=PINK):
        plane = ComplexPlane((-1, 1), (-1, 1))
        plane.set_width(1.25)
        plane.next_to(term, UP)

        t_tracker = ValueTracker()
        get_t = t_tracker.get_value
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        vector = Vector(thickness=2, fill_color=color)
        vector.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(0),
            plane.n2p(c * np.exp(s * get_t())),
        ))

        tail = TracingTail(vector.get_end, stroke_color=color, time_traced=2, stroke_width=(0, 4))
        path = TracedPath(vector.get_end, stroke_color=color, stroke_width=1, stroke_opacity=0.75)

        return Group(plane, t_tracker, vector, tail, path)
