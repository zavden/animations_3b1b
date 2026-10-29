# ==============================================================================
# Scene:      NudgeSideLengthOfCube
# Source:     videos/_2017/eoc/chapter3.py (lines 799-1191)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NudgeSideLengthOfCube.py NudgeSideLengthOfCube -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
# ==============================================================================

from manim_imports_ext import *

class NudgeSideLengthOfCube(Scene):
    CONFIG = {
        "x_color" : BLUE,
        "dx_color" : GREEN,
        "df_color" : YELLOW,
        "use_morty" : False,
        "x" : 3,
        "dx" : 0.2,
        "alt_dx" : 0.02,
        "offset_vect" : OUT,
        "pose_angle" : np.pi/12,
        "pose_axis" : UP+RIGHT,
        "small_piece_scaling_factor" : 0.7,
        "allow_recursion" : True,
    }
    def construct(self):
        self.states = dict()
        if self.allow_recursion:
            # CHANGE: in Cairo Scene.__init__ ran construct(); GL needs cairo_nested_scene(Class, **kw) to build a scene inside another
            self.alt_scene = cairo_nested_scene(self.__class__,
                skip_animations = True,
                allow_recursion = False,
                dx = self.alt_dx,
            )

        self.add_title()
        self.introduce_cube()
        self.write_df_equation()
        self.write_derivative()

    def add_title(self):
        title = OldTex("f(x) = x^3")
        title.shift(FRAME_X_RADIUS*LEFT/2)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()

    def introduce_cube(self):
        cube = self.get_cube()
        cube.to_edge(LEFT, buff = 2*LARGE_BUFF)
        cube.shift(DOWN)

        dv_pieces = self.get_dv_pices(cube)
        original_dx = self.dx
        self.dx = 0
        alt_dv_pieces = self.get_dv_pices(cube)
        self.dx = original_dx
        alt_dv_pieces.set_fill(opacity = 0)

        x_brace = Brace(cube, LEFT, buff = SMALL_BUFF)
        dx_brace = Brace(
            dv_pieces[1], LEFT, buff = SMALL_BUFF,
        )
        dx_brace.stretch_in_place(1.5, 1)
        for brace, tex in (x_brace, "x"), (dx_brace, "dx"):
            brace.scale(0.95)
            brace.rotate(-np.pi/96)
            brace.shift(0.3*(UP+LEFT))
            brace.add(brace.get_text("$%s$"%tex))


        cube_group = VGroup(cube, dv_pieces, alt_dv_pieces)
        self.pose_3d_mobject(cube_group)

        self.play(DrawBorderThenFill(cube))
        self.play(GrowFromCenter(x_brace))
        self.wait()
        self.play(Transform(alt_dv_pieces, dv_pieces))
        self.remove(alt_dv_pieces)
        self.add(dv_pieces)
        self.play(GrowFromCenter(dx_brace))
        self.wait()
        for piece in dv_pieces:
            piece.on_cube_state = piece.copy()
        self.play(*[
            ApplyMethod(
                piece.shift, 
                0.5*(piece.get_center()-cube.get_center())
            )
            for piece in dv_pieces
        ]+[
            ApplyMethod(dx_brace.shift, 0.7*UP)
        ])
        self.wait()

        self.cube = cube
        self.dx_brace = dx_brace
        self.faces, self.bars, self.corner_cube = [
            VGroup(*[
                piece 
                for piece in dv_pieces
                if piece.type == target_type
            ])
            for target_type in ("face", "bar", "corner_cube")
        ]

    def write_df_equation(self):
        df_equation = VGroup(
            OldTex("df"),
            OldTex("="),
            self.organize_faces(self.faces.copy()),
            OldTex("+"),
            self.organize_bars(self.bars.copy()),
            OldTex("+"),
            self.corner_cube.copy()
        )
        df, equals, faces, plus1, bars, plus2, corner_cube = df_equation
        df.set_color(self.df_color)
        for three_d_mob in faces, bars, corner_cube:
            three_d_mob.scale(self.small_piece_scaling_factor)
            # self.pose_3d_mobject(three_d_mob)
        faces.set_fill(opacity = 0.3)
        df_equation.arrange(RIGHT)
        df_equation.next_to(ORIGIN, RIGHT)
        df_equation.to_edge(UP)

        faces_brace = Brace(faces, DOWN)
        derivative = faces_brace.get_tex("3x^2", "\\, dx")
        extras_brace = Brace(VGroup(bars, corner_cube), DOWN)
        ignore_text = extras_brace.get_text(
            "Multiple \\\\ of $dx^2$"
        )
        ignore_text.scale(0.7)
        x_squared_dx = OldTex("x^2", "\\, dx")


        self.play(*list(map(Write, [df, equals])))
        self.grab_pieces(self.faces, faces)
        self.wait()
        self.shrink_dx("Faces are introduced")
        face = self.faces[0]
        face.save_state()
        self.play(face.shift, FRAME_X_RADIUS*RIGHT)
        x_squared_dx.next_to(face, LEFT)
        self.play(Write(x_squared_dx, run_time = 1))
        self.wait()
        for submob, sides in zip(x_squared_dx, [face[0], VGroup(*face[1:])]):
            self.play(
                submob.set_color, RED,
                sides.set_color, RED,
                rate_func = there_and_back
            )
            self.wait()
        self.play(
            face.restore,
            Transform(
                x_squared_dx, derivative,
                replace_mobject_with_target_in_scene = True
            ),
            GrowFromCenter(faces_brace)
        )
        self.wait()
        self.grab_pieces(self.bars, bars, plus1)
        self.grab_pieces(self.corner_cube, corner_cube, plus2)
        self.play(
            GrowFromCenter(extras_brace),
            Write(ignore_text)
        )
        self.wait()
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in [
                plus1, bars, plus2, corner_cube, 
                extras_brace, ignore_text
            ]
        ])
        self.wait()

        self.df_equation = df_equation
        self.derivative = derivative

    def write_derivative(self):
        df, equals, faces, plus1, bars, plus2, corner_cube = self.df_equation
        df = df.copy()
        equals = equals.copy()        
        df_equals = VGroup(df, equals)        

        derivative = self.derivative.copy()
        dx = derivative[1]

        extra_stuff = OldTex("+(\\dots)", "dx^2")
        dx_squared = extra_stuff[1]

        derivative.generate_target()
        derivative.target.shift(2*DOWN)
        extra_stuff.next_to(derivative.target)
        self.play(
            MoveToTarget(derivative),
            df_equals.next_to, derivative.target[0], LEFT,
            df_equals.shift, 0.07*DOWN
        )
        self.play(Write(extra_stuff))
        self.wait()

        frac_line = OldTex("-")
        frac_line.replace(df)
        extra_stuff.generate_target()
        extra_stuff.target.next_to(derivative[0])
        frac_line2 = OldTex("-")
        frac_line2.stretch_to_fit_width(
            extra_stuff.target[1].get_width()
        )
        frac_line2.move_to(extra_stuff.target[1])
        extra_stuff.target[1].next_to(frac_line2, UP, buff = SMALL_BUFF)
        dx_below_dx_squared = OldTex("dx")
        dx_below_dx_squared.next_to(frac_line2, DOWN, buff = SMALL_BUFF)
        self.play(
            FadeIn(frac_line),
            FadeIn(frac_line2),
            df.next_to, frac_line, UP, SMALL_BUFF,
            dx.next_to, frac_line, DOWN, SMALL_BUFF,
            MoveToTarget(extra_stuff),
            Write(dx_below_dx_squared),
            path_arc = -np.pi
        )
        self.wait()
        inner_dx = VGroup(*dx_squared[:-1])
        self.play(
            FadeOut(frac_line2),
            FadeOut(dx_below_dx_squared),
            dx_squared[-1].set_color, BLACK,
            inner_dx.next_to, extra_stuff[0], RIGHT, SMALL_BUFF
        )
        self.wait()
        self.shrink_dx("Derivative is written", restore = False)
        self.play(*[
            ApplyMethod(mob.fade, 0.7)
            for mob in (extra_stuff, inner_dx)
        ])
        self.wait(2)

        anims = []
        for mob in list(self.faces)+list(self.bars)+list(self.corner_cube):
            vect = mob.get_center()-self.cube.get_center()
            anims += [
                mob.shift, -(1./3)*vect
            ]
        anims += self.dx_brace.shift, 0.7*DOWN
        self.play(*anims)
        self.wait()

    def grab_pieces(self, start_pieces, end_pices, to_write = None):
        for piece in start_pieces:
            piece.generate_target()
            piece.target.rotate(
                np.pi/12, piece.get_center()-self.cube.get_center()
            )
            piece.target.set_color(RED)
        self.play(*list(map(MoveToTarget, start_pieces)), rate_func = wiggle)
        self.wait()
        added_anims = []
        if to_write is not None:
            added_anims.append(Write(to_write))
        self.play(
            Transform(start_pieces.copy(), end_pices),
            *added_anims
        )

    def shrink_dx(self, state_name, restore = True):
        mobjects = self.get_mobjects()
        mobjects_with_points = [
            m for m in mobjects
            if m.get_num_points() > 0
        ]
        #Alt_scene will reach this point, and save copy of self
        #in states dict
        self.states[state_name] = [
            mob.copy() for mob in mobjects_with_points
        ] 
        if not self.allow_recursion:
            return
        if restore:
            movers = self.states[state_name]
            for mob in movers:
                mob.save_state()
            self.remove(*mobjects)
        else:
            movers = mobjects_with_points
        self.play(*[
            Transform(*pair)
            for pair in zip(
                movers,
                self.alt_scene.states[state_name]
            )
        ])
        self.wait()
        if restore:
            self.play(*[m.restore for m in movers])
            self.remove(*movers)
            self.mobjects = mobjects

    def get_cube(self):
        cube = self.get_prism(self.x, self.x, self.x)
        cube.set_fill(color = BLUE, opacity = 0.3)
        cube.set_stroke(color = WHITE, width = 1)
        return cube

    def get_dv_pices(self, cube):
        pieces = VGroup()
        for vect in it.product([0, 1], [0, 1], [0, 1]):
            if np.all(vect == ORIGIN):
                continue
            args = [
                self.x if bit is 0 else self.dx
                for bit in vect
            ]
            piece = self.get_prism(*args)
            piece.next_to(cube, np.array(vect), buff = 0)
            pieces.add(piece)
            if sum(vect) == 1:
                piece.type = "face"
            elif sum(vect) == 2:
                piece.type = "bar"
            else:
                piece.type = "corner_cube"

        return pieces

    def organize_faces(self, faces):
        self.unpose_3d_mobject(faces)
        for face in faces:
            dimensions = [
                face.length_over_dim(dim)
                for dim in range(3)
            ]
            thin_dim = np.argmin(dimensions)
            if thin_dim == 0:
                face.rotate(np.pi/2, DOWN)
            elif thin_dim == 1:
                face.rotate(np.pi/2, RIGHT)
        faces.arrange(OUT, buff = LARGE_BUFF)
        self.pose_3d_mobject(faces)
        return faces

    def organize_bars(self, bars):
        self.unpose_3d_mobject(bars)
        for bar in bars:
            dimensions = [
                bar.length_over_dim(dim)
                for dim in range(3)
            ]
            thick_dim = np.argmax(dimensions)
            if thick_dim == 0:
                bar.rotate(np.pi/2, OUT)
            elif thick_dim == 2:
                bar.rotate(np.pi/2, LEFT)
        bars.arrange(OUT, buff = LARGE_BUFF)
        self.pose_3d_mobject(bars)
        return bars

    def get_corner_cube(self):
        return self.get_prism(self.dx, self.dx,  self.dx)

    def get_prism(self, width, height, depth):
        color_kwargs = {
            "fill_color" : YELLOW,
            "fill_opacity" : 0.4,
            "stroke_color" : WHITE,            
            "stroke_width" : 0.1,
        }
        front = Rectangle(
            width = width,
            height = height,
            **color_kwargs
        )
        face = VGroup(front)
        for vect in LEFT, RIGHT, UP, DOWN:
            if vect is LEFT or vect is RIGHT:
                side = Rectangle(
                    height = height, 
                    width = depth, 
                    **color_kwargs
                )
            else:
                side = Rectangle(
                    height = depth,
                    width = width, 
                    **color_kwargs
                )
            side.next_to(front, vect, buff = 0)
            side.rotate(
                np.pi/2, rotate_vector(vect, -np.pi/2),
                about_point = front.get_edge_center(vect)
            )
            face.add(side)
        return face

    def pose_3d_mobject(self, mobject):
        mobject.rotate(self.pose_angle, self.pose_axis)
        return mobject

    def unpose_3d_mobject(self, mobject):
        mobject.rotate(-self.pose_angle, self.pose_axis)
        return mobject
