import pjsua2 as pj
import sys
import time

# Subclass to extend the Account and get notifications etc.
class Account(pj.Account):
    def onRegState(self, prm):
        print("***OnRegState: " + prm.reason)

class MyCall(pj.Call):
    def __init__(self,acc,call_id = pj.PJSUA_INVALID_ID):
        super().__init__(acc, call_id)

    def onCallState(prm):
        pass

    def onCallMediaState(prm):
        pass
    



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
    acfg.idUri = "sip823662:@sip.comtube.com";
    acfg.regConfig.registrarUri = "sip:sip.comtube.com";
    cred = pj.AuthCredInfo("digest", "sip.comtube.com", "823622", 0, "cG24xD9f5qs5jZF");
    acfg.sipConfig.authCreds.append( cred );
    # Create the account
    acc = Account();
    acc.create(acfg);
    # Here we don't have anything else to do..

    # Destroy the library
    # pj.pj_thread_register()

    main_call = MyCall(acc)
    prm = pj.CallOpParam(True)
    try:
        main_call.makeCall("sip:79150994289",prm)
        time.sleep(10);
    except Exception as ex:
        print(f"err occured : {ex}")

    ep.libDestroy()


def main():
    pass

if __name__ == "__main__":
    pjsua2_test()