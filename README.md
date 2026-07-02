# FaceOnLive — Face Liveness Detection SDK for Linux

Server-side **passive face liveness detection (anti-spoofing)** for Linux, exposed through a Python interface over the native engine. Detects presentation attacks — printed photos, screen replays, and masks.

> Part of the [FaceOnLive](https://faceonlive.com) on-premises biometric SDK suite.

## Features
- Passive liveness — no user action required; a single frame is enough.
- Detects print, replay (screen), and mask spoofing.
- On-premises and offline; ideal for backend verification pipelines.

## Requirements
| | |
|---|---|
| OS | Linux x86-64 |
| Runtime | Python 3.8+ |
| Engine | native liveness engine (included under `engine/`) |

## Setup
1. Get a license key — free trial at **https://faceonlive.com**.
2. Provide the key via the `LICENSE_KEY` environment variable, or `license.txt` (replace the `<YOUR_LICENSE_KEY>` placeholder).
3. Install Python dependencies and run the provided demo.

## Quick start (Python)
```python
from engine.header import *

init_sdk()                      # ttv_init
result = detect_face_rgb(image) # ttv_detect_face → face box + liveness score
```

## API reference (Python bindings → native)
| Binding | Native | Description |
|---|---|---|
| `get_version()` | `ttv_version` | SDK version. |
| `get_deviceid()` | `ttv_get_hwid` | Machine hardware ID (for offline licensing). |
| `init_sdk()` / `init_sdk_offline()` | `ttv_init` / `ttv_init_offline` | Initialize online or offline. |
| `detect_face_rgb(image)` | `ttv_detect_face` | Detect a face and return its liveness score. |

## License & support
Requires a valid license key — get one at **[faceonlive.com](https://faceonlive.com)**. Keep `license.txt` out of version control. Questions: contact@faceonlive.com

## 📦 Full SDK download
This repository contains the source/demo code only. Download the complete SDK — engine libraries and models, with full project structure — from the [Releases](../../releases) page and extract it over this project.
