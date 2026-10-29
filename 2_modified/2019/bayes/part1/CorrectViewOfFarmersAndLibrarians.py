# ==============================================================================
# Scene:      CorrectViewOfFarmersAndLibrarians
# Source:     videos/_2019/bayes/part1.py (lines 1271-1419)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CorrectViewOfFarmersAndLibrarians.py CorrectViewOfFarmersAndLibrarians -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class Steve(SVGMobject):
    CONFIG = {
        "file_name": "steve",
        "fill_color": GREY,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "stroke_width": 0,
        "height": 3,
        "include_name": True,
        "name": "Steve"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.include_name:
            self.add_name()

    def add_name(self):
        self.name = OldTexText(self.name)
        self.name.match_width(self)
        self.name.next_to(self, DOWN, SMALL_BUFF)
        self.add(self.name)


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class LibrarianIcon(SVGMobject):
    CONFIG = {
        "file_name": "book",
        "stroke_width": 0,
        "fill_color": GREY_B,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 0.75,
    }


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class FarmerIcon(SVGMobject):
    CONFIG = {
        "file_name": "farming",
        "stroke_width": 0,
        "fill_color": GREEN_E,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 1.5,
    }


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class Person(SVGMobject):
    CONFIG = {
        "file_name": "person",
        "height": 1.5,
        "stroke_width": 0,
        "fill_opacity": 1,
        "fill_color": GREY_B,
    }


class Librarian(Person):
    CONFIG = {
        "IconClass": LibrarianIcon,
        "icon_style": {
            "background_stroke_width": 5,
            "background_stroke_color": BLACK,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        icon = self.IconClass()
        icon.set_style(**self.icon_style)
        icon.match_width(self)
        icon.move_to(self.get_corner(DR), DOWN)
        self.add(icon)


class Farmer(Librarian):
    CONFIG = {
        "IconClass": FarmerIcon,
        "icon_style": {
            "background_stroke_width": 2,
        },
        "fill_color": GREEN,
    }


class CorrectViewOfFarmersAndLibrarians(Scene):
    def construct(self):
        # Match last scene
        steves = VGroup(Steve(), Steve())
        book = LibrarianIcon()
        farm = FarmerIcon()
        icons = VGroup(book, farm)

        for mob in icons:
            mob.set_height(1)
            mob.move_to(DOWN + 2 * LEFT)
        farm.shift(4 * RIGHT)

        steves.match_width(book)
        steves.move_to(book, DOWN)
        steves.shift(3 * UP)
        steve1, steve2 = steves
        steve2.match_x(farm)

        self.add(steves, book, farm)

        # Add arrows
        arrows = VGroup(*[
            Arrow(s.get_bottom(), m.get_top())
            for s, m in zip(steves, icons)
        ])
        words = VGroup(
            OldTexText("Stereotype"),
            OldTexText("Unexpected"),
        )
        for arrow, word, vect in zip(arrows, words, [LEFT, RIGHT]):
            word.scale(1.5)
            word.next_to(arrow, vect)
            self.play(
                GrowArrow(arrow),
                FadeIn(word, UP),
            )
        self.wait()

        # Show people proportions
        librarian = Librarian()
        farmer = Farmer()

        librarian.move_to(LEFT).to_edge(UP)
        farmer.move_to(RIGHT).to_edge(UP)
        farmer_ul = farmer.get_corner(UL)

        farmers = VGroup(farmer, *[farmer.copy() for x in range(19)])
        farmers.arrange_in_grid(n_rows=4)
        farmers.move_to(farmer_ul, UL)

        farmer_outlines = farmers.copy()
        farmer_outlines.set_fill(opacity=0)
        farmer_outlines.set_stroke(YELLOW, 1)

        farmer_count = Integer(1)
        farmer_count.scale(2)
        farmer_count.set_color(GREEN)
        farmer_count.next_to(farmers, LEFT, buff=LARGE_BUFF)
        farmer_count.add_updater(lambda m: m.set_value(len(farmer_outlines)))

        for person, icon in zip([librarian, farmer], icons):
            person.save_state()
            person[:-1].set_opacity(0)
            person.scale(
                icon.get_height() / person[-1].get_height()
            )
            person.move_to(icon, DR)

        self.remove(*icons)
        self.play(
            LaggedStartMap(FadeOut, VGroup(steves, arrows, words)),
            Restore(librarian),
            Restore(farmer),
            run_time=1,
        )
        self.play(
            LaggedStartMap(FadeIn, farmers[1:])
        )
        self.wait()
        self.add(farmer_count)
        self.play(
            ShowIncreasingSubsets(farmer_outlines),
            int_func=np.ceil,
            rate_func=linear,
            run_time=2,
        )
        self.play(FadeOut(farmer_outlines))
        self.wait()

        # Show higher number of farmers
        farmers.save_state()
        farmers.generate_target()
        farmers.target.scale(0.5, about_edge=UL)
        new_farmers = VGroup(*it.chain(*[
            farmers.target.copy().next_to(
                farmers.target, vect, buff=SMALL_BUFF,
            )
            for vect in [RIGHT, DOWN]
        ]))
        new_farmers[-10:].align_to(new_farmers, RIGHT)
        new_farmers[-10:].align_to(new_farmers[-20], UP)

        farmer_count.clear_updaters()
        self.play(
            MoveToTarget(farmers),
            ShowIncreasingSubsets(new_farmers),
            ChangeDecimalToValue(farmer_count, 60),
        )
        self.wait()
        self.play(
            FadeOut(new_farmers),
            Restore(farmers),
            ChangeDecimalToValue(farmer_count, 20),
        )
        self.wait()

        # Organize into a representative sample
        farmers.generate_target()
        librarian.generate_target()
        group = VGroup(librarian.target, *farmers.target)
        self.arrange_bottom_row(group)

        l_brace = self.get_count_brace(VGroup(librarian.target))
        f_brace = self.get_count_brace(farmers.target)

        self.play(
            MoveToTarget(librarian),
            MoveToTarget(farmers),
            ReplacementTransform(farmer_count, f_brace[-1]),
            GrowFromCenter(f_brace[:-1]),
        )
        self.play(GrowFromCenter(l_brace))
        self.wait()

    def get_count_brace(self, people):
        brace = Brace(people, UP, buff=SMALL_BUFF)
        count = Integer(len(people), edge_to_fix=DOWN)
        count.next_to(brace, UP, SMALL_BUFF)
        brace.add(count)
        brace.count = count
        return brace

    def arrange_bottom_row(self, group):
        group.arrange(RIGHT, buff=0.5)
        group.set_width(FRAME_WIDTH - 3)
        group.to_edge(DOWN)
        for person in group:
            person[-1].set_stroke(BLACK, 1, background=True)
