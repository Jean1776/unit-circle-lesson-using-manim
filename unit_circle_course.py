from manim import *
import numpy as np

# Set per-part duration (seconds). Default 5 minutes = 300s
PART_DURATION = 300

class BaseUnitCircle(Scene):
    def setup_circle(self):
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            tips=True,
            axis_config={"include_numbers": False},
        )
        circle = Circle(radius=1, color=BLUE)
        circle.move_to(ORIGIN)
        return axes, circle

# Part 1: Intro — unit circle, angle, definitions
class Part1_IntroScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        title = Tex("Unit circle: definitions").to_edge(UP)
        theta = ValueTracker(PI / 6)
        dot = always_redraw(lambda: Dot(np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]), color=YELLOW))
        radial = always_redraw(lambda: Line(ORIGIN, dot.get_center(), color=YELLOW))
        angle_arc = always_redraw(lambda: Arc(radius=0.25, start_angle=0, angle=theta.get_value(), color=YELLOW))
        labels = VGroup(
            MathTex(r"(\cos\theta,\ \sin\theta)").next_to(dot, UR),
            MathTex(r"\text{Radius }=1").to_corner(UL)
        )
        self.add(axes, circle, title)
        self.play(FadeIn(dot), Create(radial), Create(angle_arc), Write(labels[0]))
        self.play(theta.animate.set_value(PI/2), run_time=3)
        self.wait(PART_DURATION)

# Part 2: Visualizing cos and sin as projections
class Part2_ProjectionsScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        theta = ValueTracker(PI/3)
        dot = always_redraw(lambda: Dot(np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]), color=YELLOW))
        proj_x = always_redraw(lambda: Line(dot.get_center(), np.array([np.cos(theta.get_value()), 0, 0]), color=GREEN))
        proj_y = always_redraw(lambda: Line(dot.get_center(), np.array([0, np.sin(theta.get_value()), 0]), color=RED))
        cos_label = always_redraw(lambda: MathTex(r"\cos\theta").next_to(proj_x.get_center(), DOWN))
        sin_label = always_redraw(lambda: MathTex(r"\sin\theta").next_to(proj_y.get_center(), LEFT))
        self.add(axes, circle, dot, proj_x, proj_y, cos_label, sin_label)
        self.play(theta.animate.set_value(-PI/4), run_time=4)
        self.play(theta.animate.set_value(PI), run_time=6)
        self.wait(PART_DURATION)

# Part 3: Special angles table + animated highlights
class Part3_SpecialAnglesScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        title = Tex("Special angles and coordinates").to_edge(UP)
        angles = [0, PI/6, PI/4, PI/3, PI/2]
        coords = [(np.cos(a), np.sin(a)) for a in angles]
        table = VGroup(*[
            VGroup(
                MathTex(f"{int(np.degrees(a))}^\\circ:").scale(0.8),
                MathTex(f"({np.round(c[0],3)},\\ {np.round(c[1],3)})").scale(0.8)
            ).arrange(RIGHT, buff=0.4)
            for a, c in zip(angles, coords)
        ]).arrange(DOWN).to_corner(UR)
        self.add(axes, circle, title, table)
        for a in angles:
            p = Dot(np.array([np.cos(a), np.sin(a), 0]), color=YELLOW)
            self.play(FadeIn(p), run_time=0.8)
            self.wait(0.6)
            self.play(FadeOut(p))
        self.wait(PART_DURATION)

# Part 4: Mapping angle -> sin/cos graphs
class Part4_GraphsScene(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-0.5, 8, 1], y_range=[-1.5, 1.5, 1], x_length=7, y_length=4)
        title = Tex("Sine and Cosine as functions of angle").to_edge(UP)
        graph_sin = plane.plot(lambda x: np.sin(x), x_range=[0, 2 * PI], color=RED)
        graph_cos = plane.plot(lambda x: np.cos(x), x_range=[0, 2 * PI], color=GREEN)
        sin_label = MathTex(r"\sin x", color=RED).next_to(graph_sin, UR)
        cos_label = MathTex(r"\cos x", color=GREEN).next_to(graph_cos, DR)
        self.add(plane, title)
        self.play(Create(graph_sin), Write(sin_label), run_time=3)
        self.play(Create(graph_cos), Write(cos_label), run_time=3)
        self.wait(PART_DURATION)

# Part 5: Tangent and secant, asymptotes
class Part5_TangentScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        theta = ValueTracker(PI / 4)
        dot = always_redraw(lambda: Dot(np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]), color=YELLOW))
        ray = always_redraw(lambda: Line(ORIGIN, dot.get_center(), color=YELLOW))
        tan_line = always_redraw(lambda: Line(np.array([1, -3, 0]), np.array([1, 3, 0]), color=ORANGE))
        tan_segment = always_redraw(lambda: Line(np.array([1, 0, 0]), np.array([1, np.tan(theta.get_value()), 0]), color=ORANGE))
        tan_label = always_redraw(lambda: MathTex(r"\tan\theta").next_to(tan_segment.get_center(), RIGHT))
        self.add(axes, circle, dot, ray, tan_line, tan_segment, tan_label)
        self.play(theta.animate.set_value(PI / 2 - 0.4), run_time=4)
        self.wait(PART_DURATION)

# Part 6: Inverse trig — finding angles from values
class Part6_InverseTrigScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        val = ValueTracker(0.5)  # sin value example
        y_line = always_redraw(lambda: Line(np.array([-1.4, val.get_value(), 0]), np.array([1.4, val.get_value(), 0]), color=RED))
        intersections = always_redraw(lambda: VGroup(
            Dot(np.array([np.sqrt(1 - val.get_value() ** 2), val.get_value(), 0]), color=YELLOW),
            Dot(np.array([-np.sqrt(1 - val.get_value() ** 2), val.get_value(), 0]), color=YELLOW)
        ))
        label = always_redraw(lambda: MathTex(r"\sin\theta=" + f"{val.get_value():.3f}").to_corner(UL))
        self.add(axes, circle, y_line, intersections, label)
        self.play(val.animate.set_value(0.866), run_time=3)
        self.wait(PART_DURATION)

# Part 7: Identities — Pythagorean visualization
class Part7_IdentitiesScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        theta = ValueTracker(PI / 4)
        dot = always_redraw(lambda: Dot(np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]), color=YELLOW))
        proj_x = always_redraw(lambda: Line(dot.get_center(), np.array([np.cos(theta.get_value()), 0, 0]), color=GREEN))
        proj_y = always_redraw(lambda: Line(dot.get_center(), np.array([0, np.sin(theta.get_value()), 0]), color=RED))
        eq = MathTex(r"\cos^2\theta+\sin^2\theta=1").to_edge(UP)
        self.add(axes, circle, dot, proj_x, proj_y, eq)
        self.play(theta.animate.set_value(PI / 3), run_time=3)
        self.wait(PART_DURATION)

# Part 8: Composition, double-angle demo and summary
class Part8_ApplicationsScene(BaseUnitCircle):
    def construct(self):
        axes, circle = self.setup_circle()
        theta = ValueTracker(PI / 6)
        dot = always_redraw(lambda: Dot(np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]), color=YELLOW))
        dot2 = always_redraw(lambda: Dot(np.array([np.cos(2 * theta.get_value()), np.sin(2 * theta.get_value()), 0]), color=TEAL))
        title = Tex("Applications: double-angle, rotations").to_edge(UP)
        self.add(axes, circle, dot, dot2, title)
        self.play(theta.animate.set_value(PI / 2), run_time=4)
        self.wait(PART_DURATION)
