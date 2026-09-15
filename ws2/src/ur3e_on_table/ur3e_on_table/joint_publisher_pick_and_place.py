import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np


def linear_interpolate(p1, p2, a):
    return (1 - a) * p1 + a * p2


class JointPublisherPickAndPlace(Node):
    def __init__(self):
        super().__init__('joint_publisher_pick_and_place')

        self.publisher_ = self.create_publisher(
            JointState,
            'joint_states',
            10
        )

        self.timer_period = 0.1
        self.timer = self.create_timer(
            self.timer_period,
            self.timer_callback
        )

        self.t = 0.0

        self.p1 = np.array([
            0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ])

        self.p2 = np.array([
            -1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0
        ])

    def timer_callback(self):
        # 0-5 seconds: hold at p1
        if self.t < 5.0:
            a = 0.0

        # 5-10 seconds: move from p1 to p2
        elif self.t < 10.0:
            a = (self.t - 5.0) / 5.0

        # 10-15 seconds: hold at p2
        elif self.t < 15.0:
            a = 1.0

        # 15-20 seconds: move from p2 back to p1
        else:
            a = 1.0 - (self.t - 15.0) / 5.0

        position = linear_interpolate(
            self.p1,
            self.p2,
            a
        ).tolist()

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.name = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

        msg.position = position
        msg.velocity = []
        msg.effort = []

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publishing position: "{msg.position}"'
        )

        self.t += self.timer_period

        if self.t >= 20.0:
            self.t = 0.0


def main(args=None):
    rclpy.init(args=args)

    joint_publisher_pick_and_place_node = (
        JointPublisherPickAndPlace()
    )

    rclpy.spin(joint_publisher_pick_and_place_node)

    joint_publisher_pick_and_place_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()