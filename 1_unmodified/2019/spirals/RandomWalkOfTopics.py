# ==============================================================================
# Scene:      RandomWalkOfTopics
# Source:     videos/_2019/spirals.py (lines 4442-4621)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomWalkOfTopics.py RandomWalkOfTopics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RandomWalkOfTopics(Scene):
    CONFIG = {
        "n_dots": 30,
        "n_edge_range": [2, 4],
        "super_dot_n_edges": 20,
        "isolated_threashold": 0.5,
    }

    def construct(self):
        self.setup_network()
        self.define_important()
        self.perform_walk()

    def setup_network(self):
        n_dots = self.n_dots
        dots = VGroup()

        while len(dots) < n_dots:
            point = np.random.uniform(-1, 1, size=3)
            point[2] = 0
            point[0] *= 7
            point[1] *= 3
            isolated = True
            for dot in dots:
                if get_norm(dot.get_center() - point) < self.isolated_threashold:
                    isolated = False
            if not isolated:
                continue
            dot = Dot(point)
            dot.edges = VGroup()
            dot.neighbors = VGroup()
            dots.add(dot)
        super_dot = dots[len(dots) // 2]

        all_edges = VGroup()

        def add_edge(d1, d2):
            if d1 is d2:
                return
            edge = Line(
                d1.get_center(), d2.get_center(),
                buff=d1.get_width() / 2
            )
            d1.edges.add(edge)
            d2.edges.add(edge)
            d1.neighbors.add(d2)
            d2.neighbors.add(d1)
            all_edges.add(edge)

        for dot in dots:
            # others = list(dots[i + 1:])
            others = [d for d in dots if d is not dot]
            others.sort(key=lambda d: get_norm(d.get_center() - dot.get_center()))
            n_edges = np.random.randint(*self.n_edge_range)
            for other in others[:n_edges]:
                if dot in other.neighbors:
                    continue
                add_edge(dot, other)

        for dot in dots:
            if len(super_dot.neighbors) > self.super_dot_n_edges:
                break
            elif dot in super_dot.neighbors:
                continue
            add_edge(super_dot, dot)

        dots.sort(lambda p: p[0])

        all_edges.set_stroke(WHITE, 2)
        dots.set_fill(GREY_B, 1)

        VGroup(dots, all_edges).to_edge(DOWN, buff=MED_SMALL_BUFF)

        self.dots = dots
        self.edges = all_edges
        self.super_dot = super_dot

    def define_important(self):
        sd = self.super_dot
        dots = self.dots
        edges = self.edges

        sd.set_color(RED)
        for mob in [*dots, *edges]:
            mob.save_state()
            mob.set_opacity(0)

        sd.set_opacity(1)
        sd.edges.set_opacity(1)
        sd.neighbors.set_opacity(1)

        # angles = np.arange(0, TAU, TAU / len(sd.neighbors))
        # center = 0.5 * DOWN
        # sd.move_to(center)
        # for dot, edge, angle in zip(sd.neighbors, sd.edges, angles):
        #     dot.move_to(center + rotate_vector(2.5 * RIGHT, angle))
        #     if edge.get_length() > 0:
        #         edge.put_start_and_end_on(
        #             sd.get_center(),
        #             dot.get_center()
        #         )
        #     rad = dot.get_width() / 2
        #     llen = edge.get_length()
        #     edge.scale((llen - 2 * rad) / llen)

        title = VGroup(
            OldTexText("Important"),
            OldTex("\\Leftrightarrow"),
            OldTexText("Many connections"),
        )
        title.scale(1.5)
        title.arrange(RIGHT, buff=MED_LARGE_BUFF)
        title.to_edge(UP)

        arrow_words = OldTexText("(in my view)")
        arrow_words.set_width(2 * title[1].get_width())
        arrow_words.next_to(title[1], UP, SMALL_BUFF)

        title[0].save_state()
        title[0].set_x(0)

        self.add(title[0])
        self.play(
            FadeInFromLarge(sd),
            title[0].set_color, RED,
        )
        title[0].saved_state.set_color(RED)
        self.play(
            Restore(title[0]),
            GrowFromCenter(title[1]),
            FadeIn(arrow_words),
            FadeIn(title[2], LEFT),
            LaggedStartMap(
                ShowCreation, sd.edges,
                run_time=3,
            ),
            LaggedStartMap(
                GrowFromPoint, sd.neighbors,
                lambda m: (m, sd.get_center()),
                run_time=3,
            ),
        )
        self.wait()
        self.play(*map(Restore, [*dots, *edges]))
        self.wait()

    def perform_walk(self):
        # dots = self.dots
        # edges = self.edges
        sd = self.super_dot

        path = VGroup(sd)
        random.seed(1)
        for x in range(3):
            new_choice = None
            while new_choice is None or new_choice in path:
                new_choice = random.choice(path[0].neighbors)
            path.add_to_back(new_choice)

        for d1, d2 in zip(path, path[1:]):
            self.play(Flash(d1.get_center()))
            self.play(
                ShowCreationThenDestruction(
                    Line(
                        d1.get_center(),
                        d2.get_center(),
                        color=YELLOW,
                    )
                )
            )

        self.play(Flash(sd))
        self.play(LaggedStart(*[
            ApplyMethod(
                edge.set_stroke, YELLOW, 5,
                rate_func=there_and_back,
            )
            for edge in sd.edges
        ]))
        self.wait()
