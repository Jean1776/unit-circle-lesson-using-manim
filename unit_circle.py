from manim import *
import numpy as np

class UnitCircleScene(Scene):
    def construct(self):
        theta = ValueTracker(PI/6)  # start angle

        axes = Axes(x_range=[-1.5,1.5,1], y_range=[-1.5,1.5,1], tips=False)
        circle = Circle(radius=1, color=BLUE)

        # moving point on unit circle
        point = always_redraw(lambda:
            Dot(np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]), color=YELLOW)
        )

        # radial line
        radial = always_redraw(lambda:
            Line(ORIGIN, point.get_center(), color=YELLOW)
        )

        # projections to axes
        proj_x = always_redraw(lambda:
            Line(point.get_center(), np.array([np.cos(theta.get_value()), 0, 0]), color=GREEN)
        )
        proj_y = always_redraw(lambda:
            Line(point.get_center(), np.array([0, np.sin(theta.get_value()), 0]), color=RED)
        )

        # small angle arc at origin
        angle_arc = always_redraw(lambda:
            Arc(radius=0.35, start_angle=0, angle=theta.get_value(), color=YELLOW)
        )

        # numeric labels for cos and sin
        cos_num = DecimalNumber(np.cos(theta.get_value()), num_decimal_places=3)
        cos_num.add_updater(lambda m: m.set_value(np.cos(theta.get_value())))
        cos_label = MathTex(r"\cos\theta=").next_to(cos_num, LEFT)
        cos_group = VGroup(cos_label, cos_num).to_corner(UL)

        sin_num = DecimalNumber(np.sin(theta.get_value()), num_decimal_places=3)
        sin_num.add_updater(lambda m: m.set_value(np.sin(theta.get_value())))
        sin_label = MathTex(r"\sin\theta=").next_to(sin_num, LEFT)
        sin_group = VGroup(sin_label, sin_num).next_to(cos_group, DOWN, aligned_edge=LEFT)

        # theta text (degrees)
        theta_deg = DecimalNumber(np.degrees(theta.get_value()), num_decimal_places=1)
        theta_deg.add_updater(lambda m: m.set_value(np.degrees(theta.get_value())))
        theta_label = VGroup(MathTex(r"\theta="), theta_deg, MathTex(r"^\circ")).arrange(RIGHT).to_corner(UR)

        # tangent length at x=1 (line from (1,0) up to intersection with ray)
        tan_segment = always_redraw(lambda:
            Line(np.array([1, 0, 0]), np.array([1, np.tan(theta.get_value()), 0]), color=ORANGE)
        )
        tan_label = always_redraw(lambda:
            MathTex(r"\tan\theta").next_to(tan_segment.get_center(), RIGHT)
        )

        title = Tex("Unit circle: cos, sin, and tan").to_edge(UP)

        # add static elements
        self.add(axes, circle, title)
        # add dynamic elements
        self.add(point, radial, proj_x, proj_y, angle_arc, cos_group, sin_group, theta_label, tan_segment, tan_label)

        # animate theta sweeping
        self.play(theta.animate.set_value(PI*5/6), run_time=6, rate_func=smooth)
        self.play(theta.animate.set_value(-PI/3), run_time=4, rate_func=there_and_back)
        self.wait(1)
