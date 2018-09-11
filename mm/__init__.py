#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.path.append( "../" )

import serket as srk
import numpy as np
import os
import random

class MarkovModel(srk.Module):
    def __init__(self, num_samp=100, name="mm" ):
        super(MarkovModel, self).__init__(name, True)
        self.__num_samp=num_samp
        
    def sample_idx( self, P):
        K = len(P)
        
        # 累積確率を計算
        acc_prob = np.zeros(K)
        acc_prob[0] = P[0]
        for k in range(1,K):
            acc_prob[k] = P[k] + acc_prob[k-1]
            
        # サンプリング
        rnd = acc_prob[K-1] * random.random()
        for k in range(K):
            if P[k] >= rnd:
                return k
    
        return -1

    def update(self):
        data = self.get_observations()
        Pdz = self.get_backward_msg() # P(z|d)

        N = len( data[0] )  # データ数
        K = len( data[0][0] )

        # backward messageがまだ計算されていないときは一様分布にする
        if Pdz is None:
            Pdz = np.ones( (N, K) ) / K

        data[0] = np.array( data[0], dtype=np.float32 )
        
        
        # 遷移確率を計算
        trans_prob = np.zeros( (K, K) ) + 0.1
        for _ in range(self.__num_samp):
            for n in range(N-1):
                k =  self.sample_idx( data[0][n] )
                kk = self.sample_idx( data[0][n+1] )
                trans_prob[k,kk] += 1
        #正規化
        trans_prob = (trans_prob.T / trans_prob.sum(1)).T
        
        # 確率（メッセージ）を計算
        msg = np.zeros( (N, K) )
        msg[0] = data[0][0]
        for n in range(1,N):
            # kkからkに遷移する確率
            for k in range(K):
                for kk in range(K):
                    msg[n][k] += data[0][n-1][kk] * trans_prob[kk][k] * Pdz[n][k]
            # 正規化
            msg[n] = msg[n] / msg[n].sum()

            

        # メッセージの送信
        self.set_forward_msg( msg )
        self.send_backward_msgs( [msg] )
        
        # データ保存
        if not os.path.exists( self.get_name() ):
            os.mkdir( self.get_name())
            
        np.savetxt( os.path.join( self.get_name(), "trans_prob.txt" ), trans_prob )
        np.savetxt( os.path.join( self.get_name(), "msg.txt" ), msg )
