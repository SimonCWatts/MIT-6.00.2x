# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:57:24 2020

@author: simon
"""

####################
## Helper functions#
####################
import random

def PickBalls(bucket, n=3):
    '''
    picks 'n' coloured balls from a bucket without replacement.

    bucket (list): the colours of the balls in the bucket.
    returns: a list of the colours of the balls that were picked from the basket.
    '''
    hand = []                                           # the list of balls picked out of the basket
    temp_bucket = bucket[:]                             # copy the bucket so we dont mutate it
    for i in range(n):                                  # pick 'n' balls from the bucket
        ball = random.choice(temp_bucket)               # pick a ball at random
        hand.append(ball)                               # add the ball to hand
        temp_bucket.remove(ball)                        # remove the ball from the bucket
    return hand

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3
    balls of the same color were drawn.
    '''
    Bucket = ['r','r','r','g','g','g']                  # the bucket we are taking balls from
    Trial_Results = []                                  # a list results of all the simulation results
    matching_hands = 0                                        # counter for how many hands are all the same colour

    for i in range(numTrials):                          # simulate numTrials
        pick = PickBalls(Bucket)                        # pick three balls from the bucket
        Trial_Results.append(pick)                      # add the results to the list
        if pick.count('r') == 3 or pick.count('g') == 3:# check if each result contains balls of the same colour
            matching_hands += 1                         # if so add one to the counter

    return matching_hands / len(Trial_Results)          # return the fraction of results that were all the same colour


#####################
## Run Simulations ##
#####################
print('1 Sim:', noReplacementSimulation(1) * 100, '%')

print('10 Sim:', noReplacementSimulation(10) * 100, '%')

print('100 Sim:', noReplacementSimulation(100) * 100, '%')

print('1,000 Sim:', noReplacementSimulation(1000) * 100, '%')

print('10,000 Sim:', noReplacementSimulation(10000) * 100, '%')

print('100,000 Sim:', noReplacementSimulation(100000) * 100, '%')

print('1,000,000 Sim:', noReplacementSimulation(1000000) * 100, '%')
