import pjsua2 as pj
import time

# Subclass to extend the Account and get notifications etc.
class Account(pj.Account):
  def onRegState(self, prm):
      print("***OnRegState: " + prm.reason)

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


if __name__ == "__main__":
  pjsua2_test()
