import pjsua2 as pj

class MyAccountCallback(pj.AccountCallback):
    def init(self, account=None):
        pj.AccountCallback.init(self, account)

    def onIncomingCall(self, call):
        call.answer(180) # answer call with 180 Ringing
        call_cb = MyCallCallback(call)
        call.setCallback(call_cb)

    def onRegState(self, prm):
        print("Account onRegState:", prm.reason)

class MyCallCallback(pj.CallCallback):
    def init(self, call=None):
        pj.CallCallback.init(self, call)

    def onCallState(self, prm):
        print("Call with", self.getInfo().remoteUri,
              "is", prm.state_text, "last code =", prm.last_code,
              "(" + prm.last_reason + ")")

def make_call(dest_uri):
    # Create library instance
    lib = pj.Lib()

    # Init library with default config
    lib.init()

    # Create transport config
    tcfg = pj.TransportConfig()
    tcfg.port = 5060

    # Start the library
    lib.start()


# acfg.idUri = ""
#         acfg.regConfig.registrarUri = ""
#         acfg.regConfig.retryIntervalSec = 1
#         cred = pj.AuthCredInfo("digest", "sip.comtube.com", "", 0, "cG24xD9f5qs5jZF")
    # Create SIP account
    acc_cfg = pj.AccountConfig()
    acc_cfg.idUri = "sip823662:@sip.comtube.com"
    acc_cfg.regConfig.registrarUri = "sip:sip.comtube.com"
    acc_cfg.sipConfig.authCreds.append(pj.AuthCredInfo("digest", "*", "823622", 0, "cG24xD9f5qs5jZF"))
    acc = lib.createAccount(acc_cfg)

    # Create call
    call = lib.createCall(acc, dest_uri, MyCallCallback())

    # Make the call
    call.makeCall()

    # Wait for the call to complete
    input("Press Enter to hangup...")

    # Hangup the call
    call.hangup()

    # Destroy the library
    lib.destroy()

# Replace with your destination URI
dest_uri = "tel:+79150994289"
make_call(dest_uri)