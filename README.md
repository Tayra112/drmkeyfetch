# DRM Key Fetcher

A collection of simple Python scripts to fetch Widevine decryption keys (`KID:KEY`) for use with downstream tools like `N_m3u8DL-RE`.

## Prerequisites

Before running the scripts, make sure you have the following:

1. **Python 3.x** installed on your system.
2. A valid **CDM device file** in `.wvd` format.
3. [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE) (used for downloading and processing streams).

## How to Get Your Stream Data

* **PSSH:** `N_m3u8DL-RE` can automatically assist you in extracting and getting the required PSSH from the stream.
* **License URL:** Open your browser's **Developer Tools** (F12) and go to the **Network** tab. Filter by `method:POST` or search for terms like `license`, `widevine`, or `wv` to locate the digital rights management license endpoint.

## Usage

Navigate to the directory and run the specific script for the platform you want to target:

```bash
python XXXfetch.py
