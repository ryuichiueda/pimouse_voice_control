#!/usr/bin/env python
import rospy, os
def kill():
    os.system("killall julius")
os.chdir(os.path.dirname(__file__) + "/../etc")
rospy.init_node("julius")
rospy.on_shutdown(kill)
os.system("julius -C command.jconf -input mic")
rospy.spin()

# Copyright 2016 Ryuichi Ueda
# Released under the MIT License.
# To make line numbers be identical with the book, this statement is written here. Don't move it to the header.
