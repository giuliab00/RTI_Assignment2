#! /usr/bin/env python3

import rospy
import actionlib
import actionlib.msg
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
import assignment_2_2022.msg
from ass2.msg import Info
from nav_msgs.msg import Odometry
import sys
import select
import time
from ass2.srv import target, targetResponse

#costruttore
pose_ = Pose()
twist_= Twist()

def coordinate():

#I want to insert from terminal the coordinates for the action()

	while True:
		try:
			x=eval(input("x position to reach:"))
			break
		except (SyntaxError, ValueError, NameError):
			print("Oops!  That was no valid number.  Try again...")
	while True:
		try:
			y=eval(input("y position to reach:"))
			break
		except (SyntaxError, ValueError, NameError):
			print("Oops!  That was no valid number.  Try again...")
	
	return(x,y)


def clbk_odom(msg):
	global pub_info
	
	x_=msg.pose.pose.position.x
	y_=msg.pose.pose.position.y
	vx_=msg.twist.twist.linear.x
	vy_=msg.twist.twist.linear.y
	
	msg_info = Info()
	
	msg_info.x= x_
	msg_info.y= y_
	msg_info.vel_x= vx_
	msg_info.vel_y= vy_
	
	if not rospy.is_shutdown():
	         pub_info.publish(msg_info)
  
  
def tgt(x,y):
	global pub_target
	  	
	target_info = Point()
	target_info.x = x
	target_info.y = y
	pub_target.publish(target_info)

def get_info_goal(req):
	#node b
	global reach_t, canc_t, service
	
	return targetResponse(reach_t,canc_t)
  
def main():
	
	global pub_info, reach_t, canc_t, pub_target
	
	#Initialize pose object
	pose = PoseStamped()
	reach_t = 0
	canc_t = 0
	
	#Init node
	rospy.init_node('node_a')
		
	#create a new client
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	
	#we need to publish
	pub_info = rospy.Publisher('/bot_info', Info, queue_size=1)
	pub_target = rospy.Publisher('/tgt', Point, queue_size=1)
	
	#make sub to \odom
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
	
	service = rospy.Service("goal_info",target, get_info_goal)
	
	#Wait for the server ready
	client.wait_for_server()
	
	while True:
		#Set the goal coordinate to reach from input console
		x,y =coordinate()
		
		tgt(x,y)
		
		pose.pose.position.x = x;
		pose.pose.position.y = y;
		
		#Create object Planning goal and assign the goal
		goal = assignment_2_2022.msg.PlanningGoal(target_pose = pose)
		
		#Send goal to the server
		client.send_goal(goal)
			
		print("Do you want to cancel the goal? y/n")
			
		#cancelling the goal
		while True:
			
			input = select.select([sys.stdin], [], [], 1)[0]
			
			if input:
				reset = sys.stdin.readline().rstrip()                 
				if reset=="y":
					client.cancel_all_goals()
					#the state is 2 corresponding to preempted therefor cancelled
					time.sleep(1)
					state = client.get_state()
					if state == 2:
						canc_t +=1
					break
					
			else:
				state = client.get_state()
				#print(state)
				#the goal is reached when state equals to 3	
				if (state == 3 ):
					reach_t +=1
					break
					
		#Wait for the result
		client.wait_for_result()
	  
if __name__ == "__main__":
	main()
