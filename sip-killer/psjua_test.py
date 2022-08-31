import pjsua2 as pj
import sys
import time


# pjsua2 test function
def pjsua2_test():
    # Create and initialize the library
    ep_cfg = pj.EpConfig()
    ep = pj.Endpoint()
    ep.libCreate()
    ep.libInit(ep_cfg)

    # Create SIP transport. Error handling sample is shown
    sipTpConfig = pj.TransportConfig();
    sipTpConfig.port = 5060;
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sipTpConfig);
    # Start the library
    ep.libStart();

    acfg = pj.AccountConfig();
    acfg.idUri = "sip239888:@sip.novofon.com";
    acfg.regConfig.registrarUri = "sip:sip.novofon.com";
    cred = pj.AuthCredInfo("digest", "sip.novofon.com", "239888", 0, "ziduMGNT64");
    acfg.sipConfig.authCreds.append( cred );
    # Create the account
    acc = Account();
    acc.create(acfg);
    # Here we don't have anything else to do..
    time.sleep(10);

    # Destroy the library
    ep.libDestroy()


LOG_LEVEL = 3
CALL_STATUS = {
    "quit": 0,            
    "start": 1,
    "ongoing": 2,         
    }
def log_cb(level, str, len):
    print(str)



class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    def on_state(self):
        global current_status
        print("Call is ", self.call.info().state_text)
        print("last code =", self.call.info().last_code) 
        print("(" + self.call.info().last_reason + ")")

        if self.call.info().state == pj.CallState.DISCONNECTED:
            print("Call again? y=yes, n=quit")
            input = sys.stdin.readline().rstrip("\r\n")
        if input == "y":
            current_status = CALL_STATUS["start"]
        else:        
            current_status = CALL_STATUS["quit"]

def pjsua1_test():

    lib = pj.Lib()
    lib.init(log_cfg = pj.LogConfig(
        level=LOG_LEVEL,
        callback=log_cb
        ))
    transport = lib.create_transport(pj.TransportType.UDP)         
    lib.start()
    acc = lib.create_account_for_transport(transport)   
    global current_status
    current_status = CALL_STATUS["start"]
    while True:
        if not current_status:
            print("Quitting...")
            break
        elif current_status == 1:
            call = acc.make_call("sip:79150994289:5060", MyCallCallback())
            current_status = CALL_STATUS["ongoing"]
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

# Subclass to extend the Account and get notifications etc.
class Account(pj.Account):
    def onRegState(self, prm):
        print("***OnRegState: " + prm.reason)

class MyCall(pj.Call):
    pass


def main():
    pass

if __name__ == "__main__":
    main()