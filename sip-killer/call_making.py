
from cfg import *


import pjsua2 as pj

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
call = pj.Call(acc)
dest_uri = f"sip:{phone_number}@{sip_domain}"
call.makeCall(dest_uri, call_prm)

# Wait for the call to end
while call.isActive():
    pj.Endpoint.instance().libHandleEvents(50)

# Clean up
acc.delete()
ep.libDestroy()