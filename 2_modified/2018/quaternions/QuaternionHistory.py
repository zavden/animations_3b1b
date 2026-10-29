# ==============================================================================
# Scene:      QuaternionHistory
# Source:     videos/_2018/quaternions.py (lines 635-967)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl QuaternionHistory.py QuaternionHistory -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject.pixel_array does not exist in GL; mirror the image left-right with flip(UP)
#   - original bug: images_with_quotes is a local of another method (NameError in Cairo too); fade out the group returned by get_dissenter_images_quotes_and_names instead
# ==============================================================================

from manim_imports_ext import *

class QuaternionHistory(Scene):
    CONFIG = {
        "names_and_quotes": [
            (
                "Oliver Heaviside",
                """\\huge ``As far as the vector analysis I required was
                concerned, the quaternion was not only not
                required, but was a positive evil of no
                inconsiderable magnitude.''"""
            ),
            (
                "Lord Kelvin",
                """\\huge ``Quaternions... though beautifully \\\\ ingenious,
                have been an unmixed evil to those who have
                touched them in any way, including Clerk Maxwell.''"""
            ),
        ]
    }

    def construct(self):
        self.show_dot_product_and_cross_product()
        self.teaching_students_quaternions()
        self.show_anti_quaternion_quote()
        self.mad_hatter()

    def show_dot_product_and_cross_product(self):
        date = OldTex("1843")
        date.scale(2)
        date.to_edge(UP)

        t2c = self.t2c = {
            "x_1": GREEN,
            "x_2": GREEN,
            "y_1": RED,
            "y_2": RED,
            "z_1": BLUE,
            "z_2": BLUE,
        }

        def get_colored_tex_mobject(tex):
            return OldTex(tex, tex_to_color_map=t2c)

        v1, v2 = [
            Matrix([
                ["{}_{}".format(c, i)]
                for c in "xyz"
            ], element_to_mobject=get_colored_tex_mobject)
            for i in (1, 2)
        ]
        dot_rhs = get_colored_tex_mobject(
            "x_1 x_2 + y_1 y_2 + z_1 z_2",
        )
        cross_rhs = Matrix([
            ["y_1 z_2 - z_1 y_2"],
            ["z_1 x_2 - x_1 z_2"],
            ["x_1 y_2 - y_1 x_2"],
        ], element_to_mobject=get_colored_tex_mobject)

        dot_product = VGroup(
            v1.copy(), OldTex("\\cdot").scale(2),
            v2.copy(), OldTex("="),
            dot_rhs
        )
        cross_product = VGroup(
            v1.copy(), OldTex("\\times"),
            v2.copy(), OldTex("="),
            cross_rhs
        )
        for product in dot_product, cross_product:
            product.arrange(RIGHT, buff=2 * SMALL_BUFF)
            product.set_height(1.5)
        dot_product.next_to(date, DOWN, buff=MED_LARGE_BUFF)
        dot_product.to_edge(LEFT, buff=LARGE_BUFF)
        cross_product.next_to(
            dot_product, DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )

        self.play(FadeIn(dot_product, 2 * RIGHT))
        self.play(FadeIn(cross_product, 2 * LEFT))
        self.wait()
        self.play(FadeInFromDown(date))
        self.play(ApplyMethod(dot_product.fade, 0.7))
        self.play(ApplyMethod(cross_product.fade, 0.7))
        self.wait()
        self.play(
            FadeOut(dot_product, 2 * LEFT),
            FadeOut(cross_product, 2 * RIGHT),
        )

        self.date = date

    def teaching_students_quaternions(self):
        hamilton = ImageMobject("Hamilton")
        hamilton.set_height(4)
        # CHANGE: ImageMobject.pixel_array does not exist in GL; mirror the image left-right with flip(UP)
        hamilton.flip(UP)
        hamilton.to_corner(UR)
        hamilton.shift(MED_SMALL_BUFF * DOWN)

        colors = color_gradient([BLUE_E, GREY_BROWN, BLUE_B], 7)
        random.shuffle(colors)
        students = VGroup(*[
            PiCreature(color=color)
            for color in colors
        ])
        students.set_height(2)
        students.arrange(RIGHT)
        students.set_width(FRAME_WIDTH - hamilton.get_width() - 1)
        students.to_corner(DL)

        equation = OldTex("""
            (x_1 i + y_1 j + z_1 k)
            (x_2 i + y_2 j + z_2 k)
            =
            (-x_1 x_2 - y_1 y_2 - z_1 z_2) +
            (y_1 z_2 - z_1 y_2)i +
            (z_1 x_2 - x_1 z_2)j +
            (x_1 y_2 - y_1 x_2)k
        """, tex_to_color_map=self.t2c)
        equation.set_width(FRAME_WIDTH - 1)
        equation.to_edge(UP, buff=MED_SMALL_BUFF)

        images = Group()
        image_labels = VGroup()
        images_with_labels = Group()
        names = ["Peter Tait", "Robert Ball", "Macfarlane Alexander"]
        for name in names:
            image = ImageMobject(name)
            image.set_height(3)
            label = OldTexText(name)
            label.scale(0.5)
            label.next_to(image, DOWN)
            image.label = label
            image_labels.add(label)
            images.add(image)
            images_with_labels.add(Group(image, label))
        images_with_labels.arrange(RIGHT)
        images_with_labels.next_to(hamilton, LEFT, LARGE_BUFF)
        images_with_labels.shift(MED_LARGE_BUFF * DOWN)
        society_title = OldTexText("Quaternion society")
        society_title.next_to(images, UP, MED_LARGE_BUFF, UP)

        def blink_wait(n_loops):
            for x in range(n_loops):
                self.play(Blink(random.choice(students)))
                self.wait(random.random())

        self.play(
            FadeInFromDown(hamilton),
            Write(
                self.date,
                rate_func=lambda t: smooth(1 - t),
                remover=True
            )
        )
        self.play(LaggedStartMap(
            FadeInFrom, students,
            lambda m: (m, LEFT),
        ))
        self.play(
            LaggedStartMap(
                ApplyMethod, students,
                lambda pi: (
                    pi.change,
                    random.choice(["confused", "maybe", "erm"]),
                    3 * LEFT + 2 * UP,
                ),
            ),
            Write(equation),
        )
        blink_wait(3)
        self.play(
            LaggedStartMap(FadeInFromDown, images),
            LaggedStartMap(FadeInFromLarge, image_labels),
            Write(society_title)
        )
        blink_wait(3)
        self.play(
            FadeOut(hamilton, RIGHT),
            LaggedStartMap(
                FadeOutAndShift, images_with_labels,
                lambda m: (m, UP)
            ),
            FadeOut(students, DOWN),
            FadeOut(society_title),
            run_time=1
        )

        self.equation = equation

    def show_anti_quaternion_quote(self):
        group = self.get_dissenter_images_quotes_and_names()
        images, quotes, names = group
        self.play(
            LaggedStartMap(FadeInFromDown, images),
            LaggedStartMap(FadeInFromLarge, names),
            lag_ratio=0.75,
            run_time=2,
        )
        for quote in quotes:
            self.play(LaggedStartMap(
                FadeIn, VGroup(*quote.family_members_with_points()),
                lag_ratio=0.3
            ))
            self.wait()
        # CHANGE: original bug: images_with_quotes is a local of another method (NameError in Cairo too); fade out the group returned by get_dissenter_images_quotes_and_names instead
        self.play(FadeOut(group))

    def mad_hatter(self):
        title = OldTexText(
            "Lewis Carroll's", "``Alice in wonderland''"
        )
        title.to_edge(UP, buff=LARGE_BUFF)
        author_brace = Brace(title[0], DOWN)
        aka = OldTexText("a.k.a. Mathematician Charles Dodgson")
        aka.scale(0.8)
        aka.set_color(BLUE)
        aka.next_to(author_brace, DOWN)

        quote = OldTexText(
            """
                ``Why, you might just as well say that\\\\
                ‘I see what I eat’ is the same thing as\\\\
                ‘I eat what I see’!''
            """,
            tex_to_color_map={
                "I see what I eat": BLUE,
                "I eat what I see": YELLOW,
            },
            alignment=""
        )
        quote.to_edge(UP, buff=LARGE_BUFF)

        hatter = PiCreature(color=RED, mode="surprised")
        hat = SVGMobject(file_name="hat")
        hat_back = hat.copy()
        hat_back[0].remove(*[
            sm for sm in hat_back[0] if sm.is_subpath
        ])
        hat_back.set_fill(GREY_D)
        hat.add_to_back(hat_back)
        hat.set_height(1.25)
        hat.next_to(hatter.body, UP, buff=-MED_SMALL_BUFF)
        hatter.add(hat)
        hatter.look(DL)
        hatter.pupils[1].save_state()
        hatter.look(UL)
        hatter.pupils[1].restore()
        hatter.set_height(2)

        hare = SVGMobject(file_name="bunny")
        mouse = SVGMobject(file_name="mouse")
        for mob in hare, mouse:
            mob.set_color(GREY_B)
            mob.set_sheen(0.2, UL)
            mob.set_height(1.5)

        characters = VGroup(hatter, hare, mouse)
        for mob, p in zip(characters, [UP, DL, DR]):
            mob.move_to(p)
        hare.shift(MED_SMALL_BUFF * LEFT)

        characters.space_out_submobjects(1.5)
        characters.to_edge(DOWN)

        def change_single_place(char, **kwargs):
            i = characters.submobjects.index(char)
            target = characters[(i + 1) % 3]
            return ApplyMethod(
                char.move_to, target,
                path_arc=-90 * DEGREES,
                **kwargs
            )

        def get_change_places():
            return LaggedStartMap(
                change_single_place, characters,
                lag_ratio=0.6
            )

        self.play(
            Write(title),
            LaggedStartMap(FadeInFromDown, characters)
        )
        self.play(
            get_change_places(),
            GrowFromCenter(author_brace),
            FadeIn(aka)
        )
        for x in range(4):
            self.play(get_change_places())
        self.play(
            FadeOut(VGroup(title, author_brace, aka)),
            FadeInFromDown(quote),
        )
        self.play(get_change_places())
        self.play(
            get_change_places(),
            VFadeOut(characters, run_time=2)
        )
        self.remove(characters)
        self.wait()

    #
    def get_dissenter_images_quotes_and_names(self):
        names_and_quotes = self.names_and_quotes
        images = Group()
        quotes = VGroup()
        names = VGroup()
        images_with_quotes = Group()
        for name, quote_text in names_and_quotes:
            image = Group(ImageMobject(name))
            image.set_height(4)
            label = OldTexText(name)
            label.next_to(image, DOWN)
            names.add(label)
            quote = OldTexText(
                quote_text,
                tex_to_color_map={
                    "positive evil": RED,
                    "unmixed evil": RED,
                },
                alignment=""
            )
            quote.scale(0.3)
            quote.next_to(image, UP)
            images.add(image)
            quotes.add(quote)
            images_with_quotes.add(Group(image, label, quote))

        images_with_quotes.arrange(RIGHT, buff=LARGE_BUFF)
        images_with_quotes.to_edge(DOWN, MED_LARGE_BUFF)
        return Group(images, quotes, names)
