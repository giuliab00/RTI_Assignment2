#! /usr/bin/env python3
"""
.. module:: node_c
    :platform: Unix
    :synopsis: Python  module for second assignment of RTI
    
.. moduleauthor:: Giulia Berettieri giulia.berettieri@gmail.com

Node C  subscribes to the message published by node A updating the robot velocity and the target's distance. 
All the informations are then printed with a frequency set in the ros parrameter (in the launch file) as freq_c

Subscriber:
	/bot_info
	/tgt
	
Ros parameter:
	freq_c
 
"""
#Useful import
import rospy
import math
import actionlib
import actionlib.msg
import ass2.msg
from ass2.srv import target, targetResponse
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
import assignment_2_2022.msg
from ass2.msg import Info
from nav_msgs.msg import Odometry

#Global useful variable
global avg_vx, avg_vy 


def clbk_info(msg):
	"""
	Callback function to calculate distance from the target and average velocities
	
    	Args: msg Message
	"""
	global rx, ry, avg_vx, avg_vy, sample, rate, dist
	
	dist = math.sqrt( pow((rx - msg.x ),2) + pow((ry - msg.y),2))
	sample +=1
	avg_vx = (avg_vx + msg.vel_x)/sample
	avg_vy = (avg_vy + msg.vel_y)/sample
		
	
def clbk_tgt(msg):
	"""
	Callback function to obtain target info
	
    	Args: msg Message
	"""
	global rx, ry
	
	rx = msg.x
	ry = msg.y
	
def main():
	"""
	Main function to: 
		-Initialize the node;
		-Set publishing rate;
		-Subscribes to the robot information and target
		-Print all the informations
	"""

	global rx, ry, rate, sample, avg_vx, avg_vy, dist
	
	#Initializing useful variables
	sample= 0
	rx=0
	ry=0
	avg_vx=0
	avg_vy=0
	dist = 0
	
	#Init node
	rospy.init_node('node_c')
	
	#Setting rate of publishing choosen in launch file
	freq= rospy.get_param("freq_c")
	rate= rospy.Rate(freq)
	
	#Make subscription
	sub_info = rospy.Subscriber('/bot_info', Info, clbk_info)
	sub_tgt = rospy.Subscriber('/tgt', Point, clbk_tgt)
	
	while True:
		print("Average velocity x: ", avg_vx)
		print("Average velocity y: ", avg_vy)
		print("Distance from target: ", dist)
		rate.sleep()
	

if __name__ == "__main__":
	main()
