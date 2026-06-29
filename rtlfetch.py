import base64
import json
import requests
from pywidevine import Cdm, Device, PSSH

# 1. Load your Android L3 CDM device
device = Device.load("my_cdm_device.wvd")
cdm = Cdm.from_device(device)

# 2. Prepare the challenge using the RTL Play PSSH
session_id = cdm.open()
pssh = PSSH("")
challenge = cdm.get_license_challenge(session_id, pssh)

# 3. Native DRMtoday license endpoint (Clean, no query flags)
lic_url = "https://lic.drmtoday.com/license-proxy-widevine/cenc/"

# 4. Update your headers with your FRESH token
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0",
    "Origin": "https://www.rtlplay.be",
    "Referer": "https://www.rtlplay.be/",
    "Content-Type": "application/octet-stream",
    "x-dt-auth-token": ""  # <-- Swap this out immediately!
}

# 5. Send challenge
res = requests.post(lic_url, data=challenge, headers=headers)

if res.status_code == 200:
    try:
        # Safely unpack the server-side JSON container object
        response_json = res.json()
        print("Successfully unpacked DRMtoday JSON wrapper. Decoding...")
        license_data = base64.b64decode(response_json["license"])
    except (ValueError, KeyError):
        # Fallback wrapper if the backend structure dynamically shifted
        license_data = res.content

    try:
        cdm.parse_license(session_id, license_data)
        for key in cdm.get_keys(session_id):
            if key.type == "CONTENT":
                print(f"\nFOUND KEY -> {key.kid}:{key.key.hex()}\n")
    except Exception as e:
        print(f"Error parsing license protocol payload: {e}")
else:
    print(f"Error {res.status_code}: {res.text}")

cdm.close(session_id)
