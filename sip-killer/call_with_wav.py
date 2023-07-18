import pjsua2 as pj
from cfg import *
import time

class MyCall(pj.Call):
    def __init__(self, account):
        super().__init__(account)

    def onCallState(self, prm):
        ci = self.getInfo()
        print("Call state: ", ci.stateText)

        if ci.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            # End the call and clean up
            self.account.delete()
            pj.Endpoint.instance().libDestroy()

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        if ci.media[0].status == pj.PJSUA_CALL_MEDIA_ACTIVE:
            # The call is active, start playing the WAV file
            player = pj.AudioMediaPlayer()
            player.createPlayer("/home/aa/test_lida.wav")
            call_slot = self.getAudioMedia(-1).getPortId()
            player_slot = player.getPortId()
            pj.Endpoint.instance().audDevManager().getConfBridge().connectPorts(player_slot, call_slot, 0)

    

# Create an endpoint
ep = pj.Endpoint()
ep.libCreate()

# Initialize the library with default Endpoint configuration
ep_config = pj.EpConfig()
ep.libInit(ep_config)

# Create a SIP transport
transport = pj.TransportConfig()
transport.port = 5060  # Default SIP port
ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, transport)

# Start the library
ep.libStart()

# Configure the SIP account
acc_cfg = pj.AccountConfig()
acc_cfg.idUri = f"sip:{sip_user}@{sip_domain}"
acc_cfg.regConfig.registrarUri = f"sip:{sip_domain}"
cred_info = pj.AuthCredInfo("digest", "*", sip_user, 0, sip_password)
acc_cfg.sipConfig.authCreds.append(cred_info)

# Create the account
acc = pj.Account()
acc.create(acc_cfg)

# Make a call
call_prm = pj.CallOpParam()
call = MyCall(acc)
dest_uri = f"sip:{phone_number}@{sip_domain}"
call.makeCall(dest_uri, call_prm)

# Wait until the call is disconnected
while call.isActive():
    pj.Endpoint.instance().libHandleEvents(50)

# Clean up
acc.delete()
ep.libDestroy()