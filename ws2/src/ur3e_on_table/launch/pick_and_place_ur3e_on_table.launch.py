import os

from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_path = get_package_share_directory("ur3e_on_table")

    xacro_file = os.path.join(
        package_path,
        "urdf",
        "ur3e_on_table.urdf.xacro"
    )

    robot_description = {
        "robot_description": Command(["xacro ", xacro_file])
    }

    joint_publisher_node = Node(
        package="ur3e_on_table",
        executable="pick-and-place",
        output="both"
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="both"
    )

    return LaunchDescription([
        joint_publisher_node,
        robot_state_publisher_node,
        rviz_node
    ])