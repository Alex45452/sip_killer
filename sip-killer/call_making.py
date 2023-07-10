import sys
import time
import pjsua2 as pj

# Replace with your SIP account information and the phone number you want to call
SIP_USERNAME = "YOUR_SIP_USERNAME"
SIP_PASSWORD = "YOUR_SIP_PASSWORD"
SIP_SERVER = "YOUR_SIP_SERVER"
PHONE_NUMBER = "PHONE_NUMBER"

class MyCallObserver(pj.Call):
    def onCallState(self, prm):
        ci = self.getInfo()
        print(f"Call with {ci.remoteUri} is {ci.stateText}, last code = {ci.lastStatusCode} ({ci.lastReason})")

        if ci.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            global call_ended
            call_ended = True

class MyAccount(pj.Account):
    def onIncomingCall(self, prm):
        print("Incoming call")

# Create the pjsua lib instance
lib = pj.Endpoint.instance()
lib.libCreate()

try:
    # Init the library
    lib.libInit(log_cfg=pj.LogConfig(level=3))

    # Add a UDP transport
    transport_cfg = pj.TransportConfig()
    transport_cfg.port = 5060
    transport_id = lib.transportCreate(pj.PJSIP_TRANSPORT_UDP, transport_cfg)

    # Start the library
    lib.libStart()

    # Create an account
    account_cfg = pj.AccountConfig(domain=SIP_SERVER, username=SIP_USERNAME, password=SIP_PASSWORD)
    account = MyAccount()
    account.create(account_cfg)

    # Make a call
    call = MyCallObserver(account)
    call_prm = pj.CallOpParam()
    call_prm.opt.audioCount = 1
    call_prm.opt.videoCount = 0
    call.makeCall(f"sip:{PHONE_NUMBER}@{SIP_SERVER}", call_prm)

    # Wait for the call to end
    call_ended = False
    while not call_ended:
        time.sleep(1)

    # Clean up
    lib.transportClose(transport_id)
    lib.libDestroy()

except pj.Error as e:
    print(f"Error: {e}")
    lib.libDestroy()
    sys.exit(1)
