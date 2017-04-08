#! /usr/bin/env python
import rospy
import roslib
import actionlib
import sys

from mir_yb_action_msgs.msg import PerceiveLocationAction, PerceiveLocationGoal
from mir_yb_action_msgs.msg import MoveBaseSafeAction, MoveBaseSafeGoal
# from mcr_perception_msgs import ObjectList
from mir_yb_action_msgs.msg import PickObjectAction, PickObjectGoal
from mir_yb_action_msgs.msg import StageObjectAction, StageObjectGoal
from mir_yb_action_msgs.msg import UnStageObjectAction, UnStageObjectGoal
from mir_yb_action_msgs.msg import PlaceObjectAction, PlaceObjectGoal


class MyMoveSafeClient:


	def initialize_clients(self):

		self.client_move = actionlib.SimpleActionClient('move_base_safe_server', MoveBaseSafeAction)
		self.client_move.wait_for_server()
		self.goal_move = MoveBaseSafeGoal()

		self.client_perceive = actionlib.SimpleActionClient('perceive_location_server', PerceiveLocationAction)
		self.client_perceive.wait_for_server()
		self.goal_perceive = PerceiveLocationGoal()

		self.client_pick = actionlib.SimpleActionClient('pick_object_server', PickObjectAction)
		self.client_pick.wait_for_server()
		self.goal_pick = PickObjectGoal()

		self.client_stage = actionlib.SimpleActionClient('stage_object_server', StageObjectAction)
		self.client_stage.wait_for_server()
		self.goal_stage = StageObjectGoal()

		self.client_unstage = actionlib.SimpleActionClient('unstage_object_server', UnStageObjectAction)
		self.client_unstage.wait_for_server()
		self.goal_unstage = UnStageObjectGoal()

		self.client_place = actionlib.SimpleActionClient('place_object_server', PlaceObjectAction)
		self.client_place.wait_for_server()
		self.goal_place = PlaceObjectGoal()


	def move_base(self,start, end):
		
		self.goal_move.arm_safe_position = 'barrier_tape'

		timeout = 120.0
		self.goal_move.source_location = start
		self.goal_move.destination_location = end

		self.client_move.send_goal(self.goal_move)
		self.client_move.wait_for_result(rospy.Duration.from_sec(int(timeout)))

		self.client_move.cancel_goal()
		print str(self.client_move.get_result()) + " move_base"
		return self.client_move.get_result()

	def perceive(self):
		
	    self.goal_perceive.location = "sh-03"
	    self.client_perceive.send_goal(self.goal_perceive)
	    self.client_perceive.wait_for_result(rospy.Duration.from_sec(15.0))
	    print str(self.client_perceive.get_result())+ "  perceive"

	def pick_objects(self,list_objects, platform):
		i = 0
		for object_ in list_objects:      
		    self.goal_pick.object = object_
		    timeout = 15.0

		    rospy.loginfo('Sending action lib goal to pick_object_server : ' + self.goal_pick.object)
		    self.client_pick.send_goal(self.goal_pick)
		    self.client_pick.wait_for_result(rospy.Duration.from_sec(int(timeout)))
		    print str(self.client_pick.get_result()) + "  pick_objects"
		    self.stage_object(platform[i])
		    i+=1
		
	def stage_object(self,platform):
		self.goal_stage.robot_platform = platform
		self.client_stage.send_goal(self.goal_stage)
		self.client_stage.wait_for_result(rospy.Duration.from_sec(15.0))
		print str(self.client_stage.get_result()) + "  stage_object"


	def unstage_object(self,platform):

	    self.goal_unstage.robot_platform = platform
	    self.client_unstage.send_goal(self.goal_unstage)
	    self.client_unstage.wait_for_result(rospy.Duration.from_sec(15.0))
	    print str(self.client_unstage.get_result()) + "  unstage_object"

	def place_objects(self,list_objects, location, platform):
		i=0
		for object_ in list_objects: 
			self.unstage_object(platform[i])
			i+=1
			self.goal_place.object = object_
			self.goal_place.location = location

			timeout = 15.0
			rospy.loginfo('Sending action lib goal to place_object_server: ' + self.goal_place.object + ' ' + self.goal_place.location)
			self.client_place.send_goal(self.goal_place)

			self.client_place.wait_for_result(rospy.Duration.from_sec(int(timeout)))
			print str(self.client_place.get_result())


if __name__ == '__main__':

	rospy.init_node('move_base_safe_client_tester')
	main_ = MyMoveSafeClient()
	main_.initialize_clients()

	objects_list = ['Bearing', 'Axis', 'S40_40_B']
	platform_list = ["platform_middle", "platform_left", "platform_right"]

	if (main_.move_base('START','WS05')):
	
		main_.perceive()
		main_.pick_objects(objects_list, platform_list)
		main_.move_base('WS05','WS05')
		main_.place_objects(objects_list,'WS05',platform_list)	
	else:
		print "Abort_Move_Base"



	# def callback(data):
	#     object_list = data.data

	# def listener():    
	    
	#     rospy.Subscriber("output_object_list", String, callback)
	   
	#     rospy.spin()