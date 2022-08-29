import asyncio
import datetime
from pjsip_boostupper import pj_set_accounts,pj_set_target,pj_set_wav

def init_info():
    target = input()  # + (country_code) XXXXXXXXXXXX (12X)
    threads = int(input("type how many threads"))
    speed = int(input("type how many seconds between calls"))
    ring_duration = int(input("type how many seconds is one call ringing"))
    attack_duration = datetime.time(int(input("type how long in minutes will be attack going")))  # check if attack less than 12 hours
    path_to_wav = input("type path to your wav file (if no wav press enter)")
    return target,threads,speed,ring_duration,attack_duration,path_to_wav
    
def main(target,threads,speed,ring_duration,attack_duration,path_to_wav):
    pj_set_target(target)
    pj_set_accounts()
    pj_set_ring_duration(ring_duration)
    if path_to_wav:
        pj_set_wav(path_to_wav)
    # in every thread
    while datetime.datetime.now() - start_time < attack_duration
    
    pass






if __name__ == "__main__":
    # make asyncio cycle
    main(init_info())
