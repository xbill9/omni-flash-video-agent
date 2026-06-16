# Gemini Omni Flash Video Agent

This repository contains tools, scripts, and an MCP (Model Context Protocol) server for interacting with **Gemini Omni Flash** (codenamed **bouncybohr**), a high-performance multimodal model designed for high-speed video generation, stateful editing, and cinematic control.

Unlike traditional video generation models, Gemini Omni Flash utilizes the stateful **Interactions API** which allows you to iteratively edit and refine videos using natural language conversation within a single session.

**GitHub Repository:** [xbill9/omni-flash-video-agent](https://github.com/xbill9/omni-flash-video-agent)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed. Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

Set your Gemini API Key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 🛠 Project Structure

- **[server.py](file:///home/xbill/omni-flash-video-agent/server.py)**: A FastMCP server that exposes tools to generate, edit, and animate videos.
- **[generate_gemma_video.py](file:///home/xbill/omni-flash-video-agent/generate_gemma_video.py)**: Script demonstrating one-shot text-to-video generation.
- **[update_gemma_video.py](file:///home/xbill/omni-flash-video-agent/update_gemma_video.py)**: Script demonstrating stateful, multi-turn video editing using `previous_interaction_id`.
- **[requirements.txt](file:///home/xbill/omni-flash-video-agent/requirements.txt)**: Python dependencies.
- **[eap.md](file:///home/xbill/omni-flash-video-agent/eap.md)**: Official Early Access Program (EAP) documentation for Gemini Omni Flash (`bouncybohr`).
- **[GEMINI.md](file:///home/xbill/omni-flash-video-agent/GEMINI.md)**: Essential references for the Google GenAI Interactions API and prompting guide.

---

## ⚙️ Running the Scripts

### 1. One-Shot Video Generation
To generate a video from a text prompt:
```bash
python generate_gemma_video.py
```
This saves the output video to `gemma_devops.mp4`.

### 2. Multi-turn Video Editing (Stateful)
To generate an initial video and then statefully edit it (e.g., adding text overlays, modifying the background):
```bash
python update_gemma_video.py
```
This saves:
- The initial output as `gemma_devops_initial.mp4`
- The statefully edited output as `gemma_devops_updated.mp4`

---

## 🤖 Model Context Protocol (MCP) Server

The project includes a FastMCP server that exposes Gemini Omni Flash's capabilities as tools for AI agents.

### Start the MCP Server
You can run the server locally using the MCP CLI:
```bash
mcp dev server.py
```

### Exposed MCP Tools

1. **`generate_video(prompt: str, aspect_ratio: str = '16:9', delivery: str = 'inline')`**
   - Generates a 10s video from a text prompt.
   - Supported aspect ratios: `16:9` and `9:16`.
   - Delivery modes: `inline` (base64) or `uri` (recommended for larger files).
   - Returns the path to the saved video and the stateful `interaction_id`.

2. **`edit_video(previous_interaction_id: str, edit_prompt: str, delivery: str = 'inline')`**
   - Edits an existing video using the `previous_interaction_id` to maintain contextual history.
   - Refines elements (e.g. changing scenery, adding subjects) while keeping the overall video context stable.

3. **`animate_image(image_path: str, motion_prompt: str, delivery: str = 'inline')`**
   - Animates a static local image using a motion description.

4. **`interpolate_images(start_image_path: str, end_image_path: str, prompt: str, delivery: str = 'inline')`**
   - Creates a smooth video transition (e.g., a timelapse) between two keyframes.

5. **`generate_with_subjects(subject_image_paths: list[str], prompt: str, delivery: str = 'inline')`**
   - Generates a video incorporating specific subjects/characters from local reference images.

6. **`edit_user_video(video_path: str, edit_prompt: str, delivery: str = 'inline')`**
   - Uploads a local user video via the File API and edits it with Omni Flash.

---

## 📚 Documentation
For complete API specifications, payload samples, and capabilities, refer to:
- [eap.md](file:///home/xbill/omni-flash-video-agent/eap.md) - Early Access Program API Documentation
- [GEMINI.md](file:///home/xbill/omni-flash-video-agent/GEMINI.md) - Key links to Google Dev APIs
