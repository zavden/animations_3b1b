# ==============================================================================
# Scene:      SimpleVelocityGraph
# Source:     videos/_2017/dominos/domino_play.py (lines 8-155)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleVelocityGraph.py SimpleVelocityGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleVelocityGraph(GraphScene):
    CONFIG = {
        # "frame_rate" : 4000,
        # "domino_thickness" : 7.5438,
        # "domino_spacing" : 8.701314282,
        "data_files" : [
            "data07.txt",
            "data13.txt",
            # "data11.txt",
        ],
        "colors" : [WHITE, BLUE, YELLOW, GREEN, MAROON_B],
        "x_axis_label" : "$t$",
        "y_axis_label" : "$v$",
        "x_min" : 0,
        "x_max" : 1.8,
        "x_tick_frequency" : 0.1,
        "x_labeled_nums" : np.arange(0, 1.8, 0.2),
        "y_tick_frequency" : 100,
        "y_min" : 0,
        "y_max" : 1000,
        "y_labeled_nums" : list(range(0, 1000, 200)),
        "x_axis_width" : 12,
        "graph_origin" : 2.5*DOWN + 5*LEFT,
        "trailing_average_length" : 20,
        "include_domino_thickness" : False,
    }
    def construct(self):
        self.setup_axes()
        # self.save_all_images()
        for data_file, color in zip(self.data_files, self.colors):
            self.init_data(data_file)
            self.draw_dots(color)
            self.add_label_to_last_dot(
                "%s %s %.2f"%(
                    data_file[4:6], 
                    "hard" if self.friction == "low" else "felt",
                    self.domino_spacing,
                ),
                color
            )
            self.draw_lines(color)

    def save_all_images(self):
        indices = list(range(1, 20))
        for i1, i2 in it.combinations(indices, 2):
            to_remove = VGroup()
            for index in i1, i2:
                index_str = ("%.2f"%float(0.01*index))[-2:]
                data_file = "data%s.txt"%index_str
                self.init_data(data_file)
                color = WHITE if self.friction == "low" else BLUE
                self.draw_dots(color)
                self.add_label_to_last_dot(
                    "%s %s %.2f"%(
                        data_file[4:6], 
                        "hard" if self.friction == "low" else "felt",
                        self.domino_spacing,
                    ),
                    color
                )
                self.draw_lines(color)
                to_remove.add(self.dots, self.lines, self.label)
            self.save_image("dominos_%d_vs_%d"%(i1, i2))
            self.remove(to_remove)

    def init_data(self, data_file):
        file_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "dominos",
            data_file
        )

        file = open(file_name, "r")
        frames, notes = [], []
        for line in file:
            line = line.replace("  ", ",")
            line = line.replace("\n", "")
            entries = [s for s in line.split(",") if s is not ""]
            if len(entries) == 0:
                continue

            if entries[0] == "framerate":
                frame_rate = float(entries[1])
            elif entries[0] == "domino spacing":
                domino_spacing = float(entries[1])
            elif entries[0] == "domino thickness":
                domino_thickness = float(entries[1])
            elif entries[0] == "friction":
                self.friction = entries[1]
            else:
                try:
                    frames.append(int(entries[0]))
                except:
                    continue #How to treat?
                    # frames.append(frames[-1] + (frames[-1] - frames[-2]))
                if len(entries) > 1:
                    notes.append(entries[1])
                else:
                    notes.append("")
        frames = np.array(frames)

        self.times = (frames - frames[0])/float(frame_rate)
        delta_times = self.times[1:] - self.times[:-1]
        if self.include_domino_thickness:
            distance = domino_spacing+domino_thickness
        else:
            distance = domino_spacing
        self.velocities = distance/delta_times
        self.notes = notes

        n = self.trailing_average_length
        self.velocities = np.array([
            np.mean(self.velocities[max(0, i-n):i])
            for i in range(len(self.velocities))
        ])
        self.domino_spacing = domino_spacing
        self.domino_thickness = domino_thickness

    def draw_dots(self, color = WHITE):
        dots = VGroup()
        for time, v, note in zip(self.times, self.velocities, self.notes):
            dot = Dot(color = color)
            dot.scale(0.5)
            dot.move_to(self.coords_to_point(time, v))
            self.add(dot)
            dots.add(dot)
            if note == "twist":
                dot.set_color(RED)
        self.dots = dots

    def add_label_to_last_dot(self, label, color = WHITE):
        dot = self.dots[-1]
        label = OldTexText(label)
        label.scale(0.75)
        label.next_to(dot, UP, buff = MED_SMALL_BUFF)
        label.set_color(color)
        label.shift_onto_screen()
        self.label = label
        self.add(label)

    def draw_lines(self, color = WHITE, stroke_width = 2):
        lines = VGroup()
        for d1, d2 in zip(self.dots, self.dots[1:]):
            line = Line(d1.get_center(), d2.get_center())
            lines.add(line)
        lines.set_stroke(color, stroke_width)
        self.add(lines, self.dots)
        self.lines = lines
