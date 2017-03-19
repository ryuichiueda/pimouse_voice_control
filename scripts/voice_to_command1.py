#!/usr/bin/env python
#encoding: utf8
import rospy, os, socket

class JuliusReceiver:
    def __init__(self):   #socketの準備だけ
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("localhost",10500))
                break
            except:
                rate.sleep()

        rospy.on_shutdown(self.sock.close)

    def get_line(self):
        line = ""
        while not rospy.is_shutdown():
            v = self.sock.recv(1)
            if v == '\n':
                return line
            line += v

if __name__ == '__main__': 
    rospy.init_node("voice_to_command")
    j = JuliusReceiver()
    while not rospy.is_shutdown():
        print j.get_line()

# Copyright 2016 Ryuichi Ueda
# Released under the MIT License.
# To make line numbers be identical with the book, this statement is written here. Don't move it to the header.
