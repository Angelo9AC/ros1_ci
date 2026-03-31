For the Task 1 (ROS 1), you need to navigate to ~simulation_ws/src/tortoisebot_waypoints and then you can try the different tests for a 
passing or failing result.



---> First, for the success result

On the tortoisebot_waypoints/test/test_waypoints.py file you need to be sure that the goal position is very low, for example:
        expected_x = 0.30
        expected_y = 0.0

This is located on the lines 58, 59, 81 and 82 of the code. This goal position was defined because it is a reachable position within the map.
So now, you can try the simulation with this test. Make sure the error margin is 0.20 or similar in line 63. You need to open 3 terminals.

On the terminal #1, you need to compile and start the simulation with:

source /opt/ros/noetic/setup.bash
cd ~simulation_ws
catkin_make
source ~/simulation_ws/devel/setup.bash
rosrun tortoisebot_waypoints tortoisebot_action_server.py

Then, when the simulation is running, open a second terminal. You need to navigate to the ~simulation_ws/ directory and then type the following commands:

source /opt/ros/noetic/setup.bash
source devel/setup.bash
rosrun tortoisebot_waypoints tortoisebot_action_server.py

The last command will start the Action server. Now, open a third terminal, navigate to the ~simulation_ws/ directory and then type:

source /opt/ros/noetic/setup.bash
source devel/setup.bash
rostest tortoisebot_waypoints waypoints_test.test --reuse-master

This command will start the test and you will see the robot moving in the simulation window.
You also will get this successful result:

SUMMARY
 * RESULT: SUCCESS
 * TESTS: 2
 * ERRORS: 0
 * FAILURES: 0



 ---> For the failling result

 On the tortoisebot_waypoints/test/test_waypoints.py file you need to modify the goal position to negative values, for example:
        expected_x = -0.30
        expected_y = 0.0

This is located on the lines 58, 59, 81 and 82 of the code. This goal position is negative, which makes the test fail.
But also, you need to modify the error_margin to a very low value, such as 0.0000001 in the line 63.
You can verify it in the simulation by openning 3 terminals.

Then, the process is the same:

Terminal #1:
source /opt/ros/noetic/setup.bash
cd ~simulation_ws
catkin_make
source ~/simulation_ws/devel/setup.bash
rosrun tortoisebot_waypoints tortoisebot_action_server.py

Terminal #2:
source /opt/ros/noetic/setup.bash
cd ~simulation_ws
source devel/setup.bash
rosrun tortoisebot_waypoints tortoisebot_action_server.py

Terminal #3:
source /opt/ros/noetic/setup.bash
cd ~simulation_ws
source devel/setup.bash
rostest tortoisebot_waypoints waypoints_test.test --reuse-master

You will get the failling result:

SUMMARY
 * RESULT: FAIL
 * TESTS: 2
 * ERRORS: 0
 * FAILURES: 2
