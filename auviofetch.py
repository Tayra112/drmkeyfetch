import requests
from pywidevine import Cdm, Device, PSSH

# 1. Load your Android L3 CDM device
device = Device.load("my_cdm_device.wvd")
cdm = Cdm.from_device(device)

# 2. Open a session and prepare the challenge using the video stream's PSSH
session_id = cdm.open()
pssh = PSSH("")
challenge = cdm.get_license_challenge(session_id, pssh)

# 3. CRITICAL: Go back to Auvio, refresh, and get a fresh DASH URL
# Tokens on this platform expire rapidly!
lic_url = ""

# 4. Mirror your browser's security fingerprint
# Look at your browser network tab and fill these values in completely!
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://auvio.rtbf.be",
    "Referer": "https://auvio.rtbf.be/",
    # If your browser headers show an "Authorization" or "X-Playtoken" header, paste it here:
    # "Authorization": "Bearer eyJhbGci...",
}

# 5. Fire the authenticated request to the server
res = requests.post(lic_url, data=challenge, headers=headers)
if res.status_code == 200:
    cdm.parse_license(session_id, res.content)
    for key in cdm.get_keys(session_id):
        if key.type == "CONTENT":
            print(f"\nFOUND KEY -> 2f6103b38a9c42dca8c27e1261d4795f:{key.key.hex()}\n")
else:
    print(f"Error {res.status_code}: {res.text}")

cdm.close(session_id)
