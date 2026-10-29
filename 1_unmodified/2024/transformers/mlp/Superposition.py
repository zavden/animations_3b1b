# ==============================================================================
# Scene:      Superposition
# Source:     videos/_2024/transformers/mlp.py (lines 1924-2133)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl Superposition.py Superposition -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def get_vector_pair(angle_in_degrees=90, length=1.0, colors=(BLUE, BLUE)):
    angle = angle_in_degrees * DEGREES
    v1 = Vector(length * RIGHT)
    v2 = v1.copy().rotate(angle, about_point=ORIGIN)
    v1.set_color(colors[0])
    v2.set_color(colors[1])
    arc = Arc(radius=0.2, angle=angle)
    arc.set_stroke(WHITE, 2)
    label = Tex(Rf"180^\circ", font_size=24)
    num = label.make_number_changeable("180")
    num.set_value(angle_in_degrees)
    label.next_to(arc.pfp(0.5), normalize(arc.pfp(0.5)), buff=SMALL_BUFF)

    return VGroup(v1, v2, arc, label)



# ----- From _2024/transformers/mlp.py -----

class Superposition(InteractiveScene):
    def construct(self):
        # Add undulating bubble to encompass N-dimensional space
        frame = self.frame
        bubble = self.undulating_bubble()
        bubble_label = TexText(R"$N$-dimensional\\ Space")
        bubble_label.set_height(1)
        bubble_label["$N$"].set_color(YELLOW)
        bubble_label.next_to(bubble, LEFT)

        self.add(bubble)
        self.add(bubble_label)

        # Preview some ideas
        ideas = VGroup(Text("Latin"), Text("Microphone"), Text("Basketball"), Text("The 1920s"))
        ideas.scale(0.75)
        vectors = VGroup()
        idea_vects = VGroup()
        vect = DOWN
        colors = [PINK, GREEN, ORANGE, BLUE]
        for idea, color in zip(ideas, colors):
            vect = rotate_vector(vect, 80 * DEGREES)
            vector = Vector(1.25 * normalize(vect))
            idea.next_to(vector.get_end(), vector.get_vector(), buff=SMALL_BUFF)
            idea_vect = VGroup(vector, idea)
            idea_vect.set_color(color)
            idea_vect.shift(bubble.get_center())
            idea_vects.add(idea_vect)

        frame.save_state()
        frame.scale(0.75)
        frame.move_to(VGroup(bubble, bubble_label))
        self.play(
            Restore(frame, run_time=7),
            LaggedStartMap(VFadeInThenOut, idea_vects, lag_ratio=0.5, run_time=5)
        )

        # Written conditions and answer
        conditions = [
            R"$90^\circ$ apart",
            R"between $89^\circ$ and $91^\circ$ apart"
        ]
        task1, task2 = tasks = VGroup(
            TexText(Rf"Choose multiple vectors,\\ each pair {phrase}", font_size=42, alignment="")
            for phrase in conditions
        )
        task1[R"90^\circ"].set_color(RED)
        task2[R"$89^\circ$ and $91^\circ$"].set_color(BLUE)
        task1.center().to_edge(UP)
        task2.move_to(task1, UL)

        maximum1, maximum2 = maxima = VGroup(
            TexText(fR"Maximum \# of vectors: {answer}", font_size=42)
            for answer in ["$N$", R"$\approx \exp(\epsilon \cdot N)$"]
        )
        for maximum in maxima:
            maximum.next_to(tasks, DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        maximum1["N"].set_color(YELLOW)
        maximum2["N"].set_color(YELLOW)

        # Add 3 vectors such that each pair is 90-degrees
        perp_vectors = VGroup(*map(Vector, [RIGHT, UP, OUT]))
        perp_vectors.set_shading(0.25, 0.25, 0.25)
        perp_vectors.set_submobject_colors_by_gradient(RED, GREEN, BLUE)
        elbows = VGroup(
            Elbow(width=0.1).rotate(angle, axis, about_point=ORIGIN).set_stroke(WHITE, 2)
            for angle, axis in [(0, UP), (-PI / 2, UP), (PI / 2, RIGHT)]
        )
        elbows.set_stroke(GREY_A, 2)

        perp_group = VGroup(perp_vectors, elbows)
        perp_group.rotate(-10 * DEGREES, UP)
        perp_group.rotate(20 * DEGREES, RIGHT)
        perp_group.scale(2)
        perp_group.move_to(bubble)

        self.play(
            FadeIn(task1),
            LaggedStartMap(GrowArrow, perp_vectors[:2], lag_ratio=0.5)
        )
        self.play(ShowCreation(elbows[0]))
        self.play(
            GrowArrow(perp_vectors[2]),
            LaggedStartMap(ShowCreation, elbows[1:3], lag_ratio=0.5),
        )
        self.play(
            Rotate(perp_group, -50 * DEGREES, axis=perp_vectors[1].get_vector(), run_time=15),
            Write(maximum1, time_span=(2, 4)),
        )

        # Relax the assumption
        ninety_part = task1[conditions[0]]
        cross = Cross(ninety_part)
        crossed_part = VGroup(ninety_part, cross)
        new_cond = task2[conditions[1]]
        new_cond.align_to(ninety_part, LEFT)

        pairs = VGroup(get_vector_pair(89), get_vector_pair(91))
        pairs.arrange(RIGHT)
        pairs.to_corner(UL)

        self.play(
            FadeOut(maximum1),
            ShowCreation(cross),
        )
        self.play(
            crossed_part.animate.shift(0.5 * DOWN).set_fill(opacity=0.5),
            Write(new_cond),
            LaggedStartMap(FadeIn, pairs, lag_ratio=0.25),
        )
        self.play(
            Rotate(perp_group, 50 * DEGREES, axis=perp_vectors[1].get_vector(), run_time=10)
        )

        # Struggle with 3 vectors (Sub out the title)
        three_d_label = TexText(R"3-dimensional\\ Space")
        three_d_label["3"].set_color(BLUE)
        three_d_label.move_to(bubble_label, UL)
        bubble_label.save_state()

        pv = perp_vectors
        pv.save_state()
        alt_vects = pv.copy()
        origin = pv[0].get_start()
        for vect in alt_vects:
            vect.rotate(5 * DEGREES, axis=normalize(np.random.random(3)), about_point=origin)

        new_vects = VGroup()
        for (v1, v2) in it.combinations(pv, 2):
            new_vects.add(Arrow(ORIGIN, v1.get_length() * normalize(v1.get_vector() + v2.get_vector()), buff=0).shift(origin))
        new_vects.set_color(YELLOW)
        new_vect = new_vects[0]

        def shake(vect):
            self.play(
                vect.animate.rotate(5 * DEGREES, RIGHT, about_point=origin),
                rate_func=lambda t: wiggle(t, 9)
            )

        self.play(
            FadeIn(three_d_label, DOWN),
            bubble_label.animate.to_edge(DOWN).set_opacity(0.5)
        )
        self.play(
            GrowArrow(new_vect),
            Transform(perp_vectors, alt_vects)
        )
        shake(new_vect)
        self.play(
            Restore(perp_vectors),
            Transform(new_vect, new_vects[1])
        )
        shake(new_vect)
        self.play(
            Transform(perp_vectors, alt_vects),
            Transform(new_vect, new_vects[2])
        )
        shake(new_vect)
        self.wait()
        self.play(
            new_vect.animate.scale(0, about_point=origin),
            ApplyMethod(perp_group.scale, 0, dict(about_point=origin), lag_ratio=0.25),
            Restore(bubble_label),
            FadeOut(three_d_label, UP),
            run_time=2
        )
        self.remove(new_vect, perp_group)

        # Stack on many vectors
        dodec = Dodecahedron()
        vertices = [face.get_center() for face in dodec]
        vectors = VGroup(Vector(vert) for vert in vertices)
        vectors.set_flat_stroke(True)
        vectors.rotate(30 * DEGREES, UR)
        for vector in vectors:
            vector.always.set_perpendicular_to_camera(self.frame)
            vector.set_color(random_bright_color(hue_range=(0.5, 0.7)))
        vectors.move_to(bubble)

        self.wait(6)
        self.play(
            FadeOut(crossed_part),
            Write(maximum2),
            Rotating(vectors, TAU, axis=UP, run_time=20),
            LaggedStartMap(VFadeIn, vectors, lag_ratio=0.5, run_time=8)
        )
        self.wait()

        # Somehow communicate exponential scaling

    def undulating_bubble(self):
        bubble = ThoughtBubble(filler_shape=(6, 3))[0][-1]
        bubble.set_stroke(WHITE, 1)
        bubble.set_fill(GREY)
        bubble.set_shading(0.5, 0.5, 0)
        bubble.to_edge(DOWN)

        points = bubble.get_points().copy()
        points -= np.mean(points, 0)

        def update_bubble(bubble):
            center = bubble.get_center()
            angles = np.apply_along_axis(angle_of_vector, 1, points)
            stretch_factors = 1.0 + 0.05 * np.sin(6 * angles + self.time)
            bubble.set_points(points * stretch_factors[:, np.newaxis])
            # bubble.move_to(center)
            bubble.set_x(0).to_edge(DOWN)

        bubble.add_updater(update_bubble)
        return bubble
