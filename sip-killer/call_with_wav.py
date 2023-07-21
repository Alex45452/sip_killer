import pjsua2 as pj
from cfg import *

class MyCall(pj.Call):
    def __init__(self, acc, call_id = pj.PJSUA_INVALID_ID):
        pj.Call.__init__(self, acc, call_id)

    def onCallState(self, prm):
        print("Call is ", self.getInfo().stateText)
        print("Last code =", self.getInfo().lastStatusCode)
        print("(" + self.getInfo().lastReason + ")")

    def onCallMediaState(self, prm):
        if self.getMedia().type == pj.PJMEDIA_TYPE_AUDIO:
            aud_med = pj.AudioMedia.typecastFromMedia(self.getMedia())
            pj.Endpoint.instance().audDevManager().getCaptureDevMedia().startTransmit(aud_med)
            recorder = pj.AudioMediaRecorder()
            recorder.createRecorder('filename.wav')  # replace 'filename.wav' with your desired filename
            aud_med.startTransmit(recorder)

class MyAccount(pj.Account):
    def onIncomingCall(self, prm):
        call = MyCall(self, prm.callId)
        call.answer(pj.CallOpParam())

# Initialise library
ep = pj.Endpoint()
ep.libCreate()

# Initialise transport
ep.libInit(pj.EpConfig())

# Create UDP transport.
tp = ep.transportCreate(pj.TransportType.PJSIP_TRANSPORT_UDP, pj.TransportConfig(5060))

ep.libStart()

# create a SIP account
account_config = pj.AccountConfig()
account_config.idUri = f"sip:{sip_user}@{sip_domain}"
account_config.regConfig.registrarUri = f"sip:{sip_domain}"
account_config.sipConfig.authCreds.append(pj.AuthCred("digest", "*", sip_user, 0, sip_password))
acc = pj.create_account(account_config)

# Make call
call_prm = pj.CallOpParam(True)
call = MyAccount.makeCall(f'sip:{phone_number}', call_prm, MyCall(acc))

# Wait for ENTER before quitting
print("Press <ENTER> to quit")
input()

ep.libDestroy()