import operator 
from turtle import position


def a2(couple):
    #couple: (P1 +· · · +Pk, n)
    #position split: 用1d 里写的
    position_list = game.split(couple[1])
    position_list.sort(key=len)
    nimsum = None
    for i in range(len(position_list)-1):
        nimber = a3(position_list[i])
        if nimsum == None:
            nimsum = nimber
        else:
            nimsum = operator.xor(nimsum,nimber)
    outcome = a1(position_list[-1], nimsum)
    return outcome
