import pjsua2 as pj
import time
from cfg import *

class MyCall(pj.Call):
    def __init__(self, acc, call_id = pj.PJSUA_INVALID_ID):
        pj.Call.__init__(self, acc, call_id)

    def onCallState(self, prm):
        pj.Call.onCallState(self, prm)
        ci = self.getInfo()
        print("Call is ", ci.stateText)

        if ci.state == pj.PJSIP_INV_STATE_CONFIRMED:
            # Create a media player and recorder
            player = pj.AudioMediaPlayer()
            recorder = pj.AudioMediaRecorder()

            # Open the files for the player and recorder
            player.createPlayer(wav_path, pj.PJMEDIA_FILE_NO_LOOP)
            recorder.createRecorder(record_path)

            # Connect the call's audio media to the player and recorder
            media_port = self.getAudioMedia(-1)
            player.startTransmit(media_port)
            time.sleep(0.1)
            player.startTransmit(recorder)
            time.sleep(0.1)
            media_port.startTransmit(recorder)

            # Wait for the audio file to finish playing
            if self.isActive():
                for _ in range(25):
                    time.sleep(1)

            player.stopTransmit(media_port)
            player.stopTransmit(recorder)
            hangup_prm = pj.CallOpParam()
            hangup_prm.statusCode = 603
            hangup_prm.reason = "hangup"
            self.hangup(hangup_prm)

# Create an endpoint
ep = pj.Endpoint()
ep.libCreate()

# Initialize the library
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

# Wait for the call to end
while call.isActive():
    pj.Endpoint.instance().libHandleEvents(50)

# Clean up
acc.shutdown()
ep.libDestroy()
