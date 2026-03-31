#! /usr/bin/env python
import rospy
import actionlib
import math
import time

from tortoisebot_waypoints.msg import (
    WaypointActionFeedback,
    WaypointActionResult,
    WaypointActionAction
)

from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations


class WaypointActionClass(object):

    def __init__(self):

        self._feedback = WaypointActionFeedback()
        self._result = WaypointActionResult()

        self._position = Point()
        self._yaw = 0.0
        self._des_pos = Point()

        self._state = "idle"

        self.dist_precision = 0.08
        self.yaw_precision = math.pi / 30

        self.Kv = 0.5
        self.Kw = 1.5

        self.max_lin = 0.18
        self.max_ang = 0.8

        self._as = actionlib.SimpleActionServer(
            "tortoisebot_as",
            WaypointActionAction,
            execute_cb=self.goal_callback,
            auto_start=False
        )
        self._as.start()

        self._rate = rospy.Rate(20)

        self._pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._sub_odom = rospy.Subscriber('/odom', Odometry, self._clbk_odom)

        rospy.loginfo("Action server started")

    def _clbk_odom(self, msg):

        self._position = msg.pose.pose.position

        quaternion = (
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w
        )

        euler = transformations.euler_from_quaternion(quaternion)
        self._yaw = euler[2]

    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def saturate(self, val, vmin, vmax):
        return max(min(val, vmax), vmin)

    def goal_callback(self, goal):

        rospy.loginfo("Goal received")

        self._des_pos = goal.position
        success = True

        twist = Twist()

        start_time = time.time()
        timeout = 30

        while not rospy.is_shutdown():

            if time.time() - start_time > timeout:
                rospy.logwarn("Timeout reached")
                success = False
                break

            if self._as.is_preempt_requested():
                self._as.set_preempted()
                success = False
                break

            dx = self._des_pos.x - self._position.x
            dy = self._des_pos.y - self._position.y

            rho = math.sqrt(dx**2 + dy**2)

            desired_yaw = math.atan2(dy, dx)
            alpha = self.normalize_angle(desired_yaw - self._yaw)

            # ======================
            # GOAL REACHED
            # ======================
            if rho < self.dist_precision:

                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self._pub_cmd_vel.publish(twist)

                self._state = "done"
                rospy.loginfo("Goal reached")
                break

            # ======================
            # CONTROL
            # ======================
            v = self.Kv * rho
            w = self.Kw * alpha

            v = self.saturate(v, 0.0, self.max_lin)
            w = self.saturate(w, -self.max_ang, self.max_ang)

            if abs(alpha) > 0.35:
                v = 0.0

            twist.linear.x = v
            twist.angular.z = w

            self._pub_cmd_vel.publish(twist)

            self._state = "moving"

            self._feedback.position = self._position
            self._feedback.state = self._state
            self._as.publish_feedback(self._feedback)

            self._rate.sleep()

        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self._pub_cmd_vel.publish(twist)

        if success:
            self._result.success = True
            self._as.set_succeeded(self._result)
        else:
            self._result.success = False
            self._as.set_aborted(self._result)


if __name__ == '__main__':
    rospy.init_node('tortoisebot_as')
    WaypointActionClass()
    rospy.spin()
