import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiohttp import ClientSession

# Replace with your SIP account information and the phone number you want to call
SIP_USERNAME = "823662"
SIP_PASSWORD = "cG24xD9f5qs5jZF"
SIP_SERVER = "sip.comtube.com"
PHONE_NUMBER = "89150994289"

async def main():
    # Create a new RTCPeerConnection
    peer_connection = RTCPeerConnection()

    @peer_connection.on("track")
    def on_track(track):
        print("Track received")

    # Use aiohttp to communicate with the SIP server
    async with ClientSession() as session:
        # Register the client with the SIP server
        response = await session.post(
            f"https://{SIP_SERVER}/register",
            json={
                "type": "register",
                "username": SIP_USERNAME,
                "password": SIP_PASSWORD,
            },
        )
        assert response.status == 200

        # Make the call
        response = await session.post(
            f"https://{SIP_SERVER}/call",
            json={
                "type": "call",
                "callee": PHONE_NUMBER,
                "sdp": (await peer_connection.createOffer()).sdp,
            },
        )
        assert response.status == 200
        data = await response.json()

        # Set the remote description for the call
        await peer_connection.setRemoteDescription(
            RTCSessionDescription(sdp=data["sdp"], type=data["type"])
        )

        # Wait for the call to be answered
        await asyncio.sleep(10)

        # Hang up the call
        await peer_connection.close()

asyncio.run(main())