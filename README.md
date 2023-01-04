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
```python
Initialize constructors

def coordinate():

	while True:
		take x as keyboard input 
		take y as keyboard input

	return(x,y)


def clbk_odom(msg):
	
	Taking value needed to publish from Pose 
	
	Initialize Info object
	Passing values to Info	

	if not shutdown:
	        publish Info
  
def tgt(x,y):
			  	
	Initialize Point object
	Passing values to Target	
	publish target

def get_info_goal(req):

	return counters value to target service
  
def main():
	
	Initialize Pose object
	Initialize counter for reached and cancelled target
	Initialize Node A
	Create a new client
	Publish Node A
	Publish Node C
	Make sub to odom
	Service definition
	Wait for the server ready
	
	while True:
		
		Set the goal coordinate to reach from input console	
		Publishing target coordinate
				
		passing the input value to Pose object
		
		Create object Planning goal 
		Assign the goal		
		Send goal to the server
			
		while True:
			
			Taking keyboard input 

			if input is given:
				    
				if input = yes:
					Cancel goal
					Take time to process
					Check the state

					if state preempted:
						update counter canceled goal
					break
			else:
				Check the state
				if state == reached goal:
					update counter reached goal
					break

		Wait for the result
```
