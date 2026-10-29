# ==============================================================================
# Scene:      ImagineShapesAsMetal
# Source:     videos/_2017/fractal_dimension.py (lines 763-800)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImagineShapesAsMetal.py ImagineShapesAsMetal -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def break_up(mobject, factor = 1.3):
    mobject.scale(factor)
    for submob in mobject:
        submob.scale(1./factor)
    return mobject


class FourSelfSimilarShapes(Scene):
    CONFIG = {
        "shape_width" : 2,
        "sierpinski_order" : 6,
    }
    def construct(self):
        titles = self.get_titles()
        shapes = self.get_shapes(titles)

        self.introduce_shapes(titles, shapes)
        self.show_self_similarity(shapes)
        self.mention_measurements()

    def get_titles(self):
        titles = VGroup(*list(map(TexText, [
            "Line", "Square", "Cube", "Sierpinski"
        ])))
        for title, x in zip(titles, np.linspace(-0.75, 0.75, 4)):
            title.shift(x*FRAME_X_RADIUS*RIGHT)
        titles.to_edge(UP)
        return titles

    def get_shapes(self, titles):
        line = VGroup(
            Line(LEFT, ORIGIN),
            Line(ORIGIN, RIGHT)
        )
        line.set_color(BLUE_C)

        square = VGroup(*[
            Square().next_to(ORIGIN, vect, buff = 0)
            for vect in compass_directions(start_vect = DOWN+LEFT)
        ])
        square.set_stroke(width = 0)
        square.set_fill(BLUE, 0.7)

        cube = OldTexText("TODO")
        cube.set_fill(opacity = 0)

        sierpinski = Sierpinski(order = self.sierpinski_order)

        shapes = VGroup(line, square, cube, sierpinski)
        for shape, title in zip(shapes, titles):
            shape.set_width(self.shape_width)
            shape.next_to(title, DOWN, buff = MED_SMALL_BUFF)
        line.shift(DOWN)

        return shapes

    def introduce_shapes(self, titles, shapes):
        line, square, cube, sierpinski = shapes

        brace = Brace(VGroup(*shapes[:3]), DOWN)
        brace_text = brace.get_text("Not fractals")

        self.play(ShowCreation(line))
        self.play(GrowFromCenter(square))
        self.play(FadeIn(cube))
        self.play(ShowCreation(sierpinski))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_text)
        )
        self.wait()
        self.play(*list(map(FadeOut, [brace, brace_text])))
        self.wait()

        for title in titles:
            self.play(Write(title, run_time = 1))
        self.wait(2)

    def show_self_similarity(self, shapes):
        shapes_copy = shapes.copy()
        self.shapes_copy = shapes_copy
        line, square, cube, sierpinski = shapes_copy

        self.play(line.shift, 3*DOWN)
        self.play(ApplyFunction(break_up, line))
        self.wait()
        brace = Brace(line[0], DOWN)
        brace_text = brace.get_text("1/2")
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        brace.add(brace_text)
        self.wait()

        self.play(square.next_to, square, DOWN, LARGE_BUFF)
        self.play(ApplyFunction(break_up, square))
        subsquare = square[0]
        subsquare.save_state()
        self.play(subsquare.replace, shapes[1])
        self.wait()
        self.play(subsquare.restore)
        self.play(brace.next_to, subsquare, DOWN)
        self.wait()

        self.wait(5)#Handle cube

        self.play(sierpinski.next_to, sierpinski, DOWN, LARGE_BUFF)
        self.play(ApplyFunction(break_up, sierpinski))
        self.wait()
        self.play(brace.next_to, sierpinski[0], DOWN)
        self.wait(2)
        self.play(FadeOut(brace))

    def mention_measurements(self):
        line, square, cube, sierpinski = self.shapes_copy

        labels = list(map(TexText, [
            "$1/2$ length",
            "$1/4$ area",
            "$1/8$ volume",
            "You'll see...",
        ]))
        for label, shape in zip(labels, self.shapes_copy):
            label.next_to(shape, DOWN)
            label.to_edge(DOWN, buff = MED_LARGE_BUFF)
            if label is labels[-1]:
                label.shift(0.1*UP) #Dumb

            self.play(
                Write(label, run_time = 1),
                shape[0].set_color, YELLOW
            )
            self.wait()


class ImagineShapesAsMetal(FourSelfSimilarShapes):
    def construct(self):
        titles = VGroup(*list(map(VGroup, self.get_titles())))
        shapes = self.get_shapes(titles)
        shapes.shift(DOWN)
        descriptions = VGroup(*[
            OldTexText(*words, arg_separator = "\\\\")
            for shape, words in zip(shapes, [
                ["Thin", "wire"],
                ["Flat", "sheet"],
                ["Solid", "cube"],
                ["Sierpinski", "mesh"]
            ])
        ])
        for title, description in zip(titles, descriptions):
            description.move_to(title, UP)
            title.target = description

        self.add(titles, shapes)
        for shape in shapes:
            shape.generate_target()
            shape.target.set_color(GREY_B)
        shapes[-1].target.set_color_by_gradient(GREY, WHITE)
        for shape, title in zip(shapes, titles):
            self.play(
                MoveToTarget(title),
                MoveToTarget(shape)
            )
            self.wait()
        self.wait()

        for shape in shapes:
            self.play(
                shape.scale, 0.5, shape.get_top(),
                run_time = 3,
                rate_func = there_and_back
            )
        self.wait()
