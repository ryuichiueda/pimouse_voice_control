#!/usr/bin/env python
#encoding: utf8
import rospy, os, socket
from std_srvs.srv import Trigger         #追加
from pimouse_ros.srv import TimedMotion  #追加

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

        rospy.on_shutdown(self.shutdown)    #元のon_shutdownから書き換え
        ###以下3行追加###
        map(rospy.wait_for_service,['/timed_motion','/motor_on','/motor_off'])
        rospy.ServiceProxy('/motor_on', Trigger).call()
        self.tm = rospy.ServiceProxy('/timed_motion', TimedMotion)

    def get_line(self):
        line = ""
        while not rospy.is_shutdown():
            v = self.sock.recv(1)
            if v == '\n':
                return line
            line += v

    def shutdown(self):          #このメソッドを追加
        self.sock.close()
        rospy.ServiceProxy('/motor_off', Trigger).call()

    def score(self,line):        #get_commandにあった行を利用して実装
        return float(line.split('CM="')[-1].split('"')[0])

    def pub_command(self,th):    #get_commandメソッドを書き換え
        line = self.get_line()   
                                 
        if "WHYPO" not in line:   return None
        if self.score(line) < th: return None
                                 
        if   "左" in line: self.tm(-400,400,300) 
        elif "右" in line: self.tm(400,-400,300)
        elif "前" in line: self.tm(400,400,3000)
        elif "後" in line: self.tm(-400,-400,1500)

if __name__ == '__main__':
    rospy.init_node("voice_to_command")
    j = JuliusReceiver()
    while not rospy.is_shutdown():
        j.pub_command(0.999)        #whileの中はこの1行だけに

# Copyright 2016 Ryuichi Ueda
# Released under the MIT License.
# To make line numbers be identical with the book, this statement is written here. Don't move it to the header.
