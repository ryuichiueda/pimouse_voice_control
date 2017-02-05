#!/usr/bin/env python
import rospy, os
def kill():
    os.system("killall julius")
os.chdir(os.path.dirname(__file__) + "/../etc")
rospy.init_node("julius")
rospy.on_shutdown(kill)
os.system("julius -C command.jconf -input mic")
rospy.spin()
