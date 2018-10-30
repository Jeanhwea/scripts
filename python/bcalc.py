#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse


def getbase(goal, change):
    base = goal / (1.0 + change)
    return base

def getgoal(base, change):
    goal = (1.0 + change) * base
    return goal

def getchange(base, goal):
    change = (goal - base) / base
    return change


def bcalc(base, goal, change):

    if (base != None) and (goal != None):
        change = getchange(base, goal)
    elif (base != None) and (change != None):
        goal = getgoal(base, change)
    elif (goal != None) and (change != None):
        base = getbase(goal, change)

    if (base != None) and (goal != None) and (change != None):
        print("base: %f, goal: %f, change: %.2f%%" % (base, goal, 100*change))
    else:
        print('missing parameter, at least give two parameters of "base", "goal", "change"')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="formula: change = (goal - base) / base")
    parser.add_argument("-b", "--base", type=float)
    parser.add_argument("-g", "--goal", type=float)
    parser.add_argument("-c", "--change", type=float)
    args = parser.parse_args()

    bcalc(args.base, args.goal, args.change)

