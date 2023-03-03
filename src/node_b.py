#! /usr/bin/env python3
"""
.. module:: node_b
    :platform: Unix
    :synopsis: Python module for second assignment of RTI
    
.. moduleauthor:: Giulia Berettieri giulia.berettieri@gmail.com

Service node


 
"""
#Useful import
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
	"""
	Function to obtain and 
	"""
	#Wait until the service is available
	rospy.wait_for_service("goal_info")
	
	try:
		#Connect to target.srv
		handle = rospy.ServiceProxy("goal_info",target)
		
		#Saving the response given from Node A
		resp = handle()
		
		print("Target reached: ",resp.reached,"Target canceled: ",resp.canceled)
		
	except rospy.ServiceException as e:
		print("Service call failed: %s" % e)


if __name__ == "__main__":
	getInfoGoal()
