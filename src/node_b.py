#! /usr/bin/env python3

import rospy
import actionlib
import actionlib.msg
import ass2.msg
from ass2.srv import target, targetResponse
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
import assignment_2_2022.msg
from ass2.msg import Info
from nav_msgs.msg import Odometry

def getInfoGoal():
	rospy.wait_for_service("goal_info")
	try:
		#funzione richiesta
		handle = rospy.ServiceProxy("goal_info",target)
		resp = handle()
		print("Target reached: ", resp.reached,"Target canceled: ", resp.canceled)
		
	except rospy.ServiceException as e:
		print("Service call failed: %s" % e)


if __name__ == "__main__":
	getInfoGoal()
