This is the Interactions API:

https://ai.google.dev/api/interactions-api

promoting guide:

https://deepmind.google/models/gemini-omni/prompt-guide/

details:
https://ai.google.dev/api/interactions.md.txt

**Project Repository:** [xbill9/omni-flash-video-agent](https://github.com/xbill9/omni-flash-video-agent)

---

## ⚡ Gemini Omni Flash (`bouncybohr`) Cheat Sheet

Gemini Omni Flash (`bouncybohr`) is exclusively accessed via the **Interactions API** (`client.interactions.create`).

### 🔑 Essential Parameters

- **`model`**: Set to `"bouncybohr"`.
- **`input`**: A text prompt (string) or a list containing base64 images and text prompts (e.g. `[{"type": "image", "data": "...", "mime_type": "image/png"}, {"type": "text", "text": "Animate this"}]`).
- **`response_format`**:
  - `{"type": "video"}` for default video output.
  - `{"type": "video", "aspect_ratio": "9:16"}` for portrait videos.
  - `{"type": "video", "delivery": "uri"}` for large files delivered via Google File API URI.
- **`previous_interaction_id`**: Set to a prior interaction's ID to perform stateful editing on that video context.
- **`store`**: Set to `True` if you plan to edit the output in subsequent turns (returns an `interaction_id`).

### 🛠 Project Implementation Mapping

These Interactions API parameters are mapped to Python implementations in this codebase:
- **Text-to-Video**: [generate_gemma_video.py](file:///home/xbill/omni-flash-video-agent/generate_gemma_video.py) and `generate_video` tool in [server.py](file:///home/xbill/omni-flash-video-agent/server.py).
- **Stateful Video Editing**: [update_gemma_video.py](file:///home/xbill/omni-flash-video-agent/update_gemma_video.py) and `edit_video` tool in [server.py](file:///home/xbill/omni-flash-video-agent/server.py).
- **Image-to-Video Animation**: `animate_image` tool in [server.py](file:///home/xbill/omni-flash-video-agent/server.py).
- **Interpolation between Keyframes**: `interpolate_images` tool in [server.py](file:///home/xbill/omni-flash-video-agent/server.py).
- **Subject-based Video Generation**: `generate_with_subjects` tool in [server.py](file:///home/xbill/omni-flash-video-agent/server.py).
- **User Video Upload & Edit**: `edit_user_video` tool in [server.py](file:///home/xbill/omni-flash-video-agent/server.py).

