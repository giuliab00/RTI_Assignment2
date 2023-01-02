Assignment 2 of Research Track I
================================


How to run the solution
----------------------
To run it:
```bash
roscore
```

```bash
roslaunch ass2 ass2.launch
```
```bash
rosrun ass2 node_b.py 
```

```bash
rosrun ass2 node_c.py 
```
![My Image](my-image.jpg)

Additional Requirements
----------------------

## Pseudocode
```python
#Initialize constructors
pose_ = Pose()
twist_= Twist()

def coordinate():
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
  
#Node C  
def tgt(x,y):
	global pub_target
		  	
	target_info = Point()
	target_info.x = x
	target_info.y = y
	pub_target.publish(target_info)

#Node B
def get_info_goal(req):

	global reach_t, canc_t, service
	
	#Response of target.srv
	return targetResponse(reach_t,canc_t)
  
def main():
	
	#Defining global variable
	global pub_info, reach_t, canc_t, pub_target
	
	#Initialize pose object
	pose = PoseStamped()
	
	#Initialize counters (Node B)
	reach_t = 0
	canc_t = 0
	
	#Init node
	rospy.init_node('node_a')
		
	#Create a new client
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	
	#Publish (Node A)
	pub_info = rospy.Publisher('/bot_info', Info, queue_size=1)
	#Publish (Node C)
	pub_target = rospy.Publisher('/tgt', Point, queue_size=1)
	
	#Make sub to \odom
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
	
	#Service definition
	service = rospy.Service("goal_info",target, get_info_goal)
	
	#Wait for the server ready
	client.wait_for_server()
	
	while True:
		
		#Set the goal coordinate to reach from input console
		x,y =coordinate()
		
		#Publishing target coordinate (Node C)
		tgt(x,y)
		
		pose.pose.position.x = x
		pose.pose.position.y = y
		
		#Create object Planning goal and assign the goal
		goal = assignment_2_2022.msg.PlanningGoal(target_pose = pose)
		
		#Send goal to the server
		client.send_goal(goal)
			
		print("Do you want to cancel the goal? y/n")
			
		while True:
			
			#Taking keyboard input 
			input = select.select([sys.stdin], [], [], 1)[0]
			
			if input:
				
				reset = sys.stdin.readline().rstrip()
				               
				if reset=="y":
					#Cancel goal
					client.cancel_all_goals()
					#Take time to process
					time.sleep(1)
					#Check the state
					state = client.get_state()
					#State 2 corresponds to preempted
					if state == 2:
						canc_t +=1
					break
					
			else:
				#Check the state
				state = client.get_state()
				#State 3 corresponds to reached goal
				if (state == 3 ):
					reach_t +=1
					break
					
		#Wait for the result
		client.wait_for_result()
	  
if __name__ == "__main__":
	main()
```
