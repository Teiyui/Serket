#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function,unicode_literals, absolute_import
import sys
sys.path.append("../../")

import serket as srk
import serket_ros as srkros
import mlda
import CNN
import rospy
from serket.utils import Buffer

def main():
    rospy.init_node( "image_categorization" )

    obs = srkros.ObservationImg( "image" )
    cnn = CNN.CNNFeatureExtractor( fileames=None )
    cnn_buf = Buffer()
    mlda1 = mlda.MLDA( 3, [1000] )

    cnn.connect( obs )
    cnn_buf.connect( cnn )
    mlda1.connect( cnn_buf )

    n = 0
    for i in range(6):
        print("***", n , "***")
        obs.update()
        cnn.update()
        cnn_buf.update()
        mlda1.update()
        n += 1

if __name__=="__main__":
    main()
    
    