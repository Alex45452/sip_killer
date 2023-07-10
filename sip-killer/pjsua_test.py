import pjsua2 as pj
import time

# Subclass to extend the Account and get notifications etc.
class Account(pj.Account):
    def onRegState(self, prm):
        print("***OnRegState: " + prm.reason)

class MyCall(pj.Call):
    def __init__(self,acc,call_id = pj.PJSUA_INVALID_ID):
        super().__init__(acc, call_id)

    def onCallState(self, prm):
        pass

    def onCallMediaState(self, prm):
        pass
    



# pjsua2 test function
def pjsua2_test():
    # Create and initialize the library
    ep_cfg = pj.EpConfig()
    ep_cfg.logConfig.level = 6
    ep = pj.Endpoint()
    ep.libCreate()
    ep.libInit(ep_cfg)
    try:
        # Create SIP transport. Error handling sample is shown
        sipTpConfig = pj.TransportConfig()
        sipTpConfig.port = 5060
        sipTpConfig.outbound_proxy = "sip:sip.comtube.com"
        ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sipTpConfig)
        # Start the library
        ep.libStart()


        acfg = pj.AccountConfig()
        acfg.idUri = "sip823662:@sip.comtube.com"
        acfg.regConfig.registrarUri = "sip:sip.comtube.com"
        acfg.regConfig.retryIntervalSec = 1
        cred = pj.AuthCredInfo("digest", "*", "823622", 0, "cG24xD9f5qs5jZF")
        acfg.sipConfig.authCreds.append( cred )
        # Create the account
        acc = Account()
        acc.create(acfg)
        # Here we don't have anything else to do..

        main_call = MyCall(acc, call_id=0)
        prm = pj.CallOpParam(True)
        try:
            main_call.makeCall("tel:+79150994289",prm)
            input("close coversation? (press enter to close)")
        except Exception as ex:
            print(f"err occured : {ex}")
    except:
        ep.libDestroy()
    ep.libDestroy()

if __name__ == "__main__":
    pjsua2_test()