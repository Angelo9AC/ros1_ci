#!/usr/bin/env python

import rospy
import unittest
import actionlib
import math

from tortoisebot_waypoints.msg import (
    WaypointActionAction,
    WaypointActionGoal
)

from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion


class TestWaypoints(unittest.TestCase):

    def setUp(self):

        rospy.init_node('test_waypoints_node')

        self.position = None
        self.yaw = None

        rospy.Subscriber("/odom", Odometry, self.odom_callback)

        self.client = actionlib.SimpleActionClient(
            'tortoisebot_as',
            WaypointActionAction
        )

        self.client.wait_for_server()

    def odom_callback(self, msg):

        self.position = msg.pose.pose.position

        q = msg.pose.pose.orientation
        quaternion = [q.x, q.y, q.z, q.w]

        (_, _, self.yaw) = euler_from_quaternion(quaternion)

    def send_goal(self, x, y):

        goal = WaypointActionGoal()
        goal.position.x = x
        goal.position.y = y
        goal.position.z = 0.0

        self.client.send_goal(goal)
        self.client.wait_for_result()

        rospy.sleep(1)

    def test_final_position(self):

        expected_x = -0.30 # Change to positive for success, change to negative for failling
        expected_y = 0.0

        self.send_goal(expected_x, expected_y)

        error_margin = 0.0000001 # Change to error_margin = 0.20 for success, change to error_margin = 0.0000001 for failling

        self.assertIsNotNone(self.position)

        self.assertAlmostEqual(
            self.position.x,
            expected_x,
            delta=error_margin
        )

        self.assertAlmostEqual(
            self.position.y,
            expected_y,
            delta=error_margin
        )

    def test_final_yaw(self):

        expected_x = -0.30 # Change to positive for success, change to negative for failling
        expected_y = 0.0

        self.send_goal(expected_x, expected_y)

        expected_yaw = 0.0
        error_margin = 0.30

        self.assertIsNotNone(self.yaw)

        self.assertAlmostEqual(
            self.yaw,
            expected_yaw,
            delta=error_margin
        )


if __name__ == '__main__':
    import rostest
    rostest.rosrun(
        'tortoisebot_waypoints',
        'test_waypoints',
        TestWaypoints
    )
