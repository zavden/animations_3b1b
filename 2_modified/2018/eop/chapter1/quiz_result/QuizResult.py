# ==============================================================================
# Scene:      QuizResult
# Source:     videos/_2018/eop/chapter1/quiz_result.py (lines 5-267)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/independence.py, _2018/eop/reusables/histograms.py
#
# Run from this folder:
#     manimgl QuizResult.py QuizResult -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
#   - added PiCreatureClass (Cairo pi_class.py: width x height block of small pi creatures) locally; it does not exist in GL
#   - bar.height/init_points() replaced: zero-height bars are built with height 0.01 directly (GL Rectangle has no height attribute)
#   - added FlashThroughClass (Cairo pi_creature_animations) locally; PiCreatureClass stores width_in_pis/height_in_pis
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *

# CHANGE: PiCreatureClass (a width x height block of small pi creatures, Cairo for_3b1b_videos/pi_class.py) does not exist in ManimGL; defined here
class PiCreatureClass(VGroup):
    def __init__(self, width = 3, height = 2, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.width_in_pis = width
        self.height_in_pis = height
        for i in range(width):
            for j in range(height):
                pi = PiCreature().scale(0.3)
                pi.move_to(i * DOWN + j * RIGHT)
                self.add(pi)


# CHANGE: FlashThroughClass (Cairo for_3b1b_videos/pi_creature_animations.py) does not exist in ManimGL; defined here
class FlashThroughClass(Animation):
    def __init__(self, mobject, mode = "linear", highlight_color = GREEN, **kwargs):
        self.highlight_color = highlight_color
        self.indices = list(range(mobject.height_in_pis * mobject.width_in_pis))
        if mode == "random":
            np.random.shuffle(self.indices)
        Animation.__init__(self, mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        n = self.mobject.height_in_pis * self.mobject.width_in_pis
        index = int(np.floor(alpha * n))
        for pi in self.mobject:
            pi.set_color(BLUE_E)
        if index < n:
            self.mobject[self.indices[index]].set_color(self.highlight_color)


# ----- From _2018/eop/reusables/histograms.py -----

class Histogram(VMobject):

    CONFIG = {
        "start_color" : RED,
        "end_color" : BLUE,
        "x_scale" : 1.0,
        "y_scale" : 1.0,
        "x_labels" : "auto", # widths, mids, auto, none, [...]
        "y_labels" : "auto", # auto, none, [...]
        "y_label_position" : "top", # "center"
        "x_min" : 0,
        "bar_stroke_width" : 5,
        "outline_stroke_width" : 0,
        "stroke_color" : WHITE
    }

    def __init__(self, x_values, y_values, mode = "widths", **kwargs):
        # mode = "widths" : x_values means the widths of the bars
        # mode = "posts"  : x_values means the delimiters btw the bars 

        digest_config(self, kwargs)

        if mode == "widths" and len(x_values) != len(y_values):
            raise Exception("Array lengths do not match up!")
        elif mode == "posts" and len(x_values) != len(y_values) + 1:
            raise Exception("Array lengths do not match up!")


        self.y_values = y_values
        self.x_values = x_values
        self.mode = mode
        self.process_values()

        VMobject.__init__(self, **kwargs)
        

    def process_values(self):

         # preliminaries
        self.y_values = np.array(self.y_values)

        if self.mode == "widths":
            self.widths = self.x_values
            self.posts = np.cumsum(self.widths)
            self.posts = np.insert(self.posts, 0, 0)
            self.posts += self.x_min
            self.x_max = self.posts[-1]
        elif self.mode == "posts":
            self.posts = self.x_values
            self.widths = self.x_values[1:] - self.x_values[:-1]
            self.x_min = self.posts[0]
            self.x_max = self.posts[-1]
        else:
            raise Exception("Invalid mode or no mode specified!")

        self.x_mids = 0.5 * (self.posts[:-1] + self.posts[1:])

        self.widths_scaled = self.x_scale * self.widths
        self.posts_scaled = self.x_scale * self.posts
        self.x_min_scaled = self.x_scale * self.x_min
        self.x_max_scaled = self.x_scale * self.x_max

        self.y_values_scaled = self.y_scale * self.y_values



    def init_points(self):

        self.process_values()
        for submob in self.submobjects:
            self.remove(submob)

        def empty_string_array(n):
            arr = []
            for i in range(n):
                arr.append("")
            return arr

        def num_arr_to_string_arr(arr): # converts number array to string array
            ret_arr = []
            for x in arr:
                if x == np.floor(x):
                    new_x = int(np.floor(x))
                else:
                    new_x = x
                ret_arr.append(str(new_x))
            return ret_arr

        previous_bar = ORIGIN
        self.bars = VGroup()
        self.x_labels_group = VGroup()
        self.y_labels_group = VGroup()
        outline_points = []

        if self.x_labels == "widths":
            self.x_labels = num_arr_to_string_arr(self.widths)
        elif self.x_labels == "mids":
            self.x_labels = num_arr_to_string_arr(self.x_mids)
        elif self.x_labels == "auto":
            self.x_labels = num_arr_to_string_arr(self.x_mids)
        elif self.x_labels == "none":
            self.x_labels = empty_string_array(len(self.widths))

        if self.y_labels == "auto":
            self.y_labels = num_arr_to_string_arr(self.y_values)
        elif self.y_labels == "none":
            self.y_labels = empty_string_array(len(self.y_values))




        for (i,x) in enumerate(self.x_mids):

            # CHANGE: GL Rectangle has no .height attribute nor init_points(); give zero-height bars the 0.01 height from the start
            bar = Rectangle(
                width = self.widths_scaled[i],
                height = self.y_values_scaled[i] if self.y_values_scaled[i] != 0 else 0.01,
                stroke_width = self.bar_stroke_width,
                stroke_color = self.stroke_color,
            )

            t = float(x - self.x_min)/(self.x_max - self.x_min)
            bar_color = interpolate_color(
                self.start_color,
                self.end_color,
                t
            )
            bar.set_fill(color = bar_color, opacity = 1)
            bar.next_to(previous_bar,RIGHT,buff = 0, aligned_edge = DOWN)
            
            self.bars.add(bar)

            x_label = OldTexText(self.x_labels[i])
            x_label.next_to(bar,DOWN)
            self.x_labels_group.add(x_label)

            y_label = OldTexText(self.y_labels[i])
            if self.y_label_position == "top":
                y_label.next_to(bar, UP)
            elif self.y_label_position == "center":
                y_label.move_to(bar)
            else:
                raise Exception("y_label_position must be top or center")
            self.y_labels_group.add(y_label)

            if i == 0:
                # start with the lower left
                outline_points.append(bar.get_anchors()[-2])

            # upper two points of each bar
            outline_points.append(bar.get_anchors()[0])
            outline_points.append(bar.get_anchors()[1])

            previous_bar = bar
        # close the outline
            # lower right
        outline_points.append(bar.get_anchors()[2])
            # lower left
        outline_points.append(outline_points[0])

        self.outline = Polygon(*outline_points,
            stroke_width = self.outline_stroke_width,
            stroke_color = self.stroke_color)
        self.add(self.bars, self.x_labels_group, self.y_labels_group, self.outline)

        self.move_to(ORIGIN)

    def get_lower_left_point(self):
        return self.bars[0].get_anchors()[-2]


class FlashThroughHistogram(Animation):
    CONFIG = {
        "cell_color" : WHITE,
        "cell_opacity" : 0.8,
        "hist_opacity" : 0.2
    }

    def __init__(self, mobject,
        direction = "horizontal",
        mode = "random",
        **kwargs):

        digest_config(self, kwargs)

        self.cell_height = mobject.y_scale
        self.prototype_cell = Rectangle(
            width = 1,
            height = self.cell_height,
            fill_color = self.cell_color,
            fill_opacity = self.cell_opacity,
            stroke_width = 0,
        )

        x_values = mobject.x_values
        y_values = mobject.y_values

        self.mode = mode
        self.direction = direction

        self.generate_cell_indices(x_values,y_values)
        Animation.__init__(self,mobject,**kwargs)



    def generate_cell_indices(self,x_values,y_values):

        self.cell_indices = []
        for (i,x) in enumerate(x_values):

            nb_cells = int(np.floor(y_values[i]))
            for j in range(nb_cells):
                self.cell_indices.append((i, j))

        self.reordered_cell_indices = self.cell_indices
        if self.mode == "random":
            shuffle(self.reordered_cell_indices)


    def cell_for_index(self,i,j):

        if self.direction == "vertical":
            width = self.mobject.x_scale
            height = self.mobject.y_scale
            x = (i + 0.5) * self.mobject.x_scale
            y = (j + 0.5) * self.mobject.y_scale
            center = self.mobject.get_lower_left_point() + x * RIGHT + y * UP
        
        elif self.direction == "horizontal":
            width = self.mobject.x_scale / self.mobject.y_values[i]
            height = self.mobject.y_scale * self.mobject.y_values[i]
            x = i * self.mobject.x_scale + (j + 0.5) * width
            y = height / 2
            center = self.mobject.get_lower_left_point() + x * RIGHT + y * UP

        cell = Rectangle(width = width, height = height)
        cell.move_to(center)
        return cell


    def interpolate_mobject(self,t):

        if t == 0:
            self.mobject.add(self.prototype_cell)

        flash_nb = int(t * (len(self.cell_indices))) - 1
        (i,j) = self.reordered_cell_indices[flash_nb]
        cell = self.cell_for_index(i,j)
        self.prototype_cell.width = cell.get_width()
        self.prototype_cell.height = cell.get_height()
        self.prototype_cell.init_points()
        self.prototype_cell.move_to(cell.get_center())

        if t == 1:
           self.mobject.remove(self.prototype_cell)


    def clean_up_from_scene(self, scene = None):
        Animation.clean_up_from_scene(self, scene)
        self.update(1)
        if scene is not None:
            if self.is_remover():
                scene.remove(self.prototype_cell)
            else:
                scene.add(self.prototype_cell)
        return self



# ----- From _2018/eop/independence.py -----

def get_quiz(*questions):
    q_mobs = VGroup(*list(map(TexText, [
        "%d. %s"%(i+1, question)
        for i, question in enumerate(questions)
    ])))
    q_mobs.arrange(
        DOWN, 
        buff = MED_LARGE_BUFF,
        aligned_edge = LEFT, 
    )
    content = VGroup(
        OldTexText("Quiz").scale(1.5),
        Line(q_mobs.get_left(), q_mobs.get_right()),
        q_mobs
    )
    content.arrange(DOWN, buff = MED_SMALL_BUFF)
    rect = SurroundingRectangle(content, buff = MED_LARGE_BUFF)
    rect.shift(MED_SMALL_BUFF*DOWN)
    rect.set_color(WHITE)
    quiz = VGroup(rect, content)
    quiz.questions = q_mobs
    quiz.scale(0.7)
    return quiz


def get_slot_group(
    bool_list, 
    buff = MED_LARGE_BUFF, 
    include_qs = True,
    min_bool_list_len = 3,
    ):
    if len(bool_list) < min_bool_list_len:
        bool_list += [None]*(min_bool_list_len - len(bool_list))
    n = len(bool_list)

    lines = VGroup(*[
        Line(ORIGIN, MED_LARGE_BUFF*RIGHT)
        for x in range(n)
    ])
    lines.arrange(RIGHT, buff = buff)
    if include_qs:
        labels = VGroup(*[
            OldTexText("Q%d"%d) for d in range(1, n+1)
        ])
    else:
        labels = VGroup(*[VectorizedPoint() for d in range(n)])
    for label, line in zip(labels, lines):
        label.scale(0.7)
        label.next_to(line, DOWN, SMALL_BUFF)
    slot_group = VGroup()
    slot_group.lines = lines
    slot_group.labels = labels
    slot_group.content = VGroup()
    slot_group.digest_mobject_attrs()
    slot_group.to_edge(RIGHT)
    slot_group.bool_list = bool_list

    total_height = FRAME_Y_RADIUS
    base = 2.3

    for i, line in enumerate(lines):
        if i >= len(bool_list) or bool_list[i] is None:
            mob = VectorizedPoint()
        elif bool_list[i]:
            mob = OldTex("\\checkmark")
            mob.set_color(GREEN)
            slot_group.shift(total_height*DOWN / (base**(i+1)))
        else:
            mob = OldTex("\\times")
            mob.set_color(RED)
            slot_group.shift(total_height*UP / (base**(i+1)))
        mob.next_to(line, UP, SMALL_BUFF)
        slot_group.content.add(mob)
    return slot_group



# ----- From _2018/eop/chapter1/quiz_result.py -----

class QuizResult(PiCreatureScene):
    CONFIG = {
        "pi_creatures_start_on_screen" : False,
        "random_seed" : 0
    }
    def construct(self):


        def get_example_quiz():
            quiz = get_quiz(
                "Define ``Brachistochrone'' ",
                "Define ``Tautochrone'' ",
                "Define ``Cycloid'' ",
            )
            rect = SurroundingRectangle(quiz, buff = 0)
            rect.set_fill(color = BLACK, opacity = 1)
            rect.set_stroke(width = 0)
            quiz.add_to_back(rect)
            return quiz


        highlight_color = WHITE

        nb_students_x = 5
        nb_students_y = 3
        spacing_students_x = 2.0
        spacing_students_y = 2.2

        all_students = PiCreatureClass(
            width = nb_students_x, height = nb_students_y)# Defunct()
        student_points = []
        grades = []
        grades_count = []
        hist_y_values = np.zeros(4)
        for i in range(nb_students_x):
            for j in range(nb_students_y):
                x = i * spacing_students_x
                y = j * spacing_students_y
                #pi = PiCreature().scale(0.3)
                #pi.move_to([x,y,0])
                #all_students.add(pi)
                all_students[i*nb_students_y + j].move_to([x,y,0])
                q1 = np.random.choice([True, False])
                q2 = np.random.choice([True, False])
                q3 = np.random.choice([True, False])
                student_points.append([q1, q2, q3])
                grade = q1*1+q2*1+q3*1
                grades.append(grade)
                hist_y_values[grade] += 1
                # How many times has this grade already occured?
                grade_count = grades.count(grade)
                grades_count.append(grade_count)


        all_students.move_to(ORIGIN)
        self.pi_creatures = all_students
        self.play(FadeIn(all_students))

        all_quizzes = VGroup()

        quiz = get_example_quiz().scale(0.2)
        for pi in all_students:
            quiz_copy = quiz.copy()
            quiz_copy.next_to(pi, UP)
            all_quizzes.add(quiz_copy)

        master_quiz = get_example_quiz()
        self.play(Write(master_quiz), run_time = 2)
        self.wait()
        self.play(ReplacementTransform(
            VGroup(master_quiz), all_quizzes,
            run_time=2,
            lag_ratio=0.5
        ))
        self.wait(2)

        grades_mob = VGroup()
        for (pi, quiz, grade) in zip(all_students, all_quizzes, grades):
            grade_mob = OldTex(str(grade) + "/3")
            grade_mob.move_to(quiz)
            grades_mob.add(grade_mob)

        self.remove(master_quiz)
        self.wait()
        self.play(
            FadeOut(all_quizzes),
            FadeIn(grades_mob)
        )

        # self.play(
        #     all_students[2:].fade, 0.8,
        #     grades_mob[2:].fade, 0.8
        # )

        students_points_mob = VGroup()
        for (pi, quiz, points) in zip(all_students, all_quizzes, student_points):
            slot = get_slot_group(points, include_qs = False)
            slot.scale(0.5).move_to(quiz)
            students_points_mob.add(slot)

        self.wait()
        self.play(
            #all_students.fade, 0,
            FadeOut(grades_mob),
            FadeIn(students_points_mob)
        )

        all_students.save_state()
        students_points_mob.save_state()
        self.wait()
        randy = all_students[0]
        morty = all_students[nb_students_y]
        all_other_students = VGroup(*all_students)
        all_other_students.remove(randy, morty)
        randy_points = students_points_mob[0]
        morty_points = students_points_mob[nb_students_y]
        all_other_points = VGroup(*students_points_mob)
        all_other_points.remove(randy_points, morty_points)
        self.play(
            all_other_students.fade, 0.8,
            all_other_points.fade, 0.8,
        )
        self.wait()
        scale = 1.5
        self.play(randy_points.scale,scale)
        self.play(randy_points.scale,1.0/scale, morty_points.scale,scale)
        self.play(morty_points.scale,1.0/scale)

        self.wait()
        self.play(
            all_students.restore,
            students_points_mob.restore,
        )

        self.wait()
        anims = []
        for points in students_points_mob:
            anims.append(points.scale)
            anims.append(scale)
        self.play(*anims)

        self.wait()
        anims = []
        for points in students_points_mob:
            anims.append(points.scale)
            anims.append(1.0/scale)
        self.play(*anims)

        anims = []
        anchor_point = 3 * DOWN + 1 * LEFT
        for (pi, grade, grades_count) in zip(all_students, grades, grades_count):
            anims.append(pi.move_to)
            anims.append(anchor_point + grade * RIGHT + grades_count * UP)
        anims.append(FadeOut(students_points_mob))

        self.wait()
        self.play(*anims)

        grade_labels = VGroup()
        for i in range(4):
            grade_label = Integer(i, color = highlight_color)
            grade_label.move_to(i * RIGHT)
            grade_labels.add(grade_label)
        grade_labels.next_to(all_students, DOWN)
        out_of_label = OldTexText("out of 3", color = highlight_color)
        out_of_label.next_to(grade_labels, RIGHT, buff = MED_LARGE_BUFF)
        grade_labels.add(out_of_label)
        self.wait()
        self.play(Write(grade_labels))

        grade_hist = Histogram(
            np.ones(4),
            hist_y_values,
            mode = "widths",
            x_labels = "none",
            y_label_position = "center",
            bar_stroke_width = 0,
            outline_stroke_width = 5
        )
        grade_hist.move_to(all_students)

        self.wait()
        self.play(
            FadeIn(grade_hist),
            FadeOut(all_students)
        )


        nb_students_label = OldTexText("\# of students", color = highlight_color)
        nb_students_label.move_to(5 * RIGHT + 1 * UP)
        arrows = VGroup(*[
            Arrow(nb_students_label.get_left(), grade_hist.bars[i].get_center(),
                color = highlight_color)
            for i in range(4)
        ])
        self.wait()
        self.play(Write(nb_students_label), LaggedStartMap(GrowArrow,arrows))

        percentage_label = OldTexText("\% of students", color = highlight_color)
        percentage_label.move_to(nb_students_label)
        percentages = hist_y_values / (nb_students_x * nb_students_y) * 100
        anims = []
        for (label, percentage) in zip(grade_hist.y_labels_group, percentages):
            new_label = DecimalNumber(percentage,
                num_decimal_places = 1,
                unit = "\%",
                color = highlight_color
            )
            new_label.scale(0.7)
            new_label.move_to(label)
            anims.append(Transform(label, new_label))
        anims.append(ReplacementTransform(nb_students_label, percentage_label))
        self.wait()
        self.play(*anims)

        self.remove(all_quizzes)
        # put small copy of class in corner
        for (i,pi) in enumerate(all_students):
            x = i % 5
            y = i / 5
            pi.move_to(x * RIGHT + y * UP)
        all_students.scale(0.8)
        all_students.to_corner(DOWN + LEFT)
        self.wait()
        self.play(FadeIn(all_students))

        prob_label = OldTexText("probability", color = highlight_color)
        prob_label.move_to(percentage_label)
        self.wait()
        self.play(
            all_students[8].set_color, MAROON_E,
            #all_students[:8].fade, 0.6,
            #all_students[9:].fade, 0.6,
            ReplacementTransform(percentage_label, prob_label)
        )

        self.wait()
        self.play(
            FadeOut(prob_label),
            FadeOut(arrows)
        )

        flash_hist = FlashThroughHistogram(
                    grade_hist,
                    direction = "vertical",
                    mode = "random",
                    cell_opacity = 0.5,
                    run_time = 5,
                    rate_func = linear
                )

        flash_class = FlashThroughClass(
                    all_students,
                    mode = "random",
                    highlight_color = MAROON_E,
                    run_time = 5,
                    rate_func = linear
                )

        self.wait()
        for i in range(3):
            self.play(flash_hist, flash_class)
            self.remove(flash_hist.prototype_cell)
