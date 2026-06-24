# Gemini Omni Flash (gemini-omni-flash-preview) Documentation

***Confidential: The following is under embargo until further notice. Please do not publicly share or post this information.***

Gemini Omni Flash (codenamed **gemini-omni-flash-preview**) is a high-performance multimodal model designed for high-speed video generation, editing, and cinematic control. Unlike traditional video generation models that produce a single output, Omni lets you iteratively refine and edit your videos through natural language conversation — just describe what you want to change, and the model applies the edit while preserving the parts you want to keep.

***Key differentiator:*** *Unlike Veo (which uses the `generate_videos` endpoint), Gemini Omni Flash is available exclusively through the [Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview). Every call — whether generating a first video or editing an existing one — uses `create_interaction`. This means you can generate a video, then edit it through follow-up prompts — all within a single conversation and without having to download or upload anything.*

**Check out [the colab](https://colab.sandbox.google.com/drive/1XTxbQoVmJr9UYA-LUXDPmSr2woPE-vZZ?resourcekey=0-YXhl5MhhIrarxU2Xu3yhAQ) if you prefer an interactive get started guide.**

## Key features

- **Text-to-Video:** Generate 10s videos from text prompts.  
- **Image-to-Video:** Animate static images with motion prompts.  
- **Interpolation:** Create smooth transitions between two keyframes.  
- **Subject Reference:** Generate videos using specific subject images.  
- **Multi-turn Editing:** Iteratively refine videos using interaction history.

## Text-to-Video

Generate a video from a text prompt using create\_interaction. Set the response\_modalities to \["VIDEO"\] to receive video output. The model generates a video with audio based on your text description. Write detailed prompts for best results — describe the scene, camera movement, lighting, and mood.

* **Python**

```py
from google import genai
client = genai.Client()

interaction = client.interactions.create(
    model="gemini-omni-flash-preview",
    input="A hyper-realistic close-up of a cat drinking a large cup of tea.",
    response_format={"type": "video"},
    background=False,
    store=False,
    stream=False
)
with open("cat.mp4", "wb") as f:
    f.write(interaction.output_video.data)
```

* **JavaScript**

```javascript
import { GoogleGenAI } from '@google/genai';
const ai = new GoogleGenAI();

const interaction = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: 'A hyper-realistic cat drinking tea.',
  response_format: { type: 'video' },
  background: false,
  store: false,
  stream: false,
});
```

* **REST**

```shell
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-H "Api-Revision: 2026-05-20" \
-d '{
 "model": "gemini-omni-flash-preview",
 "input": "A hyper-realistic close-up of a cat drinking a large cup of tea.",
 "response_format": {"type": "video"},
 "background": false,
 "store": false,
 "stream": false
}'
```

### 

### REST response schema

When using the REST API directly, note that the convenience field `interaction.output_video` is **SDK-only**. The raw JSON response contains the video output nested within the `steps` array.

**Raw REST JSON structure:**

```json
{
  "steps": [
    { "type": "user_input", "content": [{"type": "text", "text": "..."}] },
    { "type": "thought", "content": [{"text": "...", "type": "thought"}] },
    {
      "type": "model_output",
      "content": [
        {
          "type": "video",
          "mime_type": "video/mp4",
          "data": "AAAAIGZ0eXBpc29t..." // Base64 encoded video data
        }
      ]
    }
  ],
  "id": "v1_...",
  "status": "completed",
  "model": "gemini-omni-flash-preview",
  "object": "interaction"
}
```

## 

## Control aspect ratio (portrait/landscape)

Set the `aspect_ratio` to `"9:16"` to create portrait videos. Default is landscape ones (16:9).

* **Python**

```py
interaction = client.interactions.create(
    model="gemini-omni-flash-preview",
    input="A futuristic city with neon lights and flying cars, cyberpunk style",
    response_format={
        "type": "video",
        "aspect_ratio": "9:16"  # Supported values: "9:16", "16:9"
    }
)
```

* **JavaScript**

```javascript
const interaction = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: 'A futuristic city with neon lights and flying cars, cyberpunk style',
  response_format: {
    type: 'video',
    aspect_ratio: '9:16' // Supported values: '9:16', '16:9'
  },
});
```

* **REST**

```shell
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-d '{
 "model": "gemini-omni-flash-preview",
 "input": "A futuristic city with neon lights and flying cars, cyberpunk style",
 "response_format": {
   "type": "video",
   "aspect_ratio": "9:16"
 }
}'
```

## Image-to-Video

Animate a still image by passing it as input alongside a text prompt that describes the desired motion. Depending on your prompt, the model will decide how to use the images. This is useful for bringing product shots, illustrations, or photographs to life.

* **Python**

```py
interaction = client.interactions.create(
    model="gemini-omni-flash-preview",
    input=[
        {"type": "image", "data": base64_image, "mime_type": "image/jpeg"},
        {"type": "text", "text": "Animate this scene."}
    ],
    response_format={"type": "video"}
)
```

* **JavaScript**

```javascript
const interaction = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: [
    { type: 'image', data: base64Image, mime_type: 'image/jpeg' },
    { type: 'text', text: 'Animate this scene.' },
  ],
  response_format: { type: 'video' },
});
```

* **REST**

```shell
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-H "Api-Revision: 2026-05-20" \
-d '{
 "model": "gemini-omni-flash-preview",
 "input": [
   {"type": "image", "data": "'"$BASE64_IMAGE"'", "mime_type": "image/jpeg"},
   {"type": "text", "text": "Animate this scene."}
 ],
 "response_format": {"type": "video"},
 "background": false,
 "store": false,
 "stream": false
}'
```

***Tip:** For best results with image-to-video, use high-resolution images and provide specific motion descriptions. Vague prompts like "make it move" produce less compelling results than detailed descriptions of the camera movement, subject motion, and environmental effects.*

### 

### Video Interpolation

If you provide 2 images or state that the video should start from a certain image, the model should understand that you want to create an interpolation video between your two references. Note that the end frame is not fully supported yet.

* **Python**

```py
interaction = client.interactions.create(
    model="gemini-omni-flash-preview",
    input=[
        {"type": "image", "data": start_b64, "mime_type": "image/png"},
        {"type": "image", "data": end_b64, "mime_type": "image/png"},
        {"type": "text", "text": "A smooth timelapse from sunrise to sunset."}
    ],
    response_format={"type": "video"}
)
```

* **JavaScript**

```javascript
const interaction = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: [
    { type: 'image', data: startData, mime_type: 'image/png' },
    { type: 'image', data: endData, mime_type: 'image/png' },
    { type: 'text', text: 'A smooth timelapse from sunrise to sunset.' },
  ],
  response_format: { type: 'video' },
});
```

* **REST**

```shell
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-H "Api-Revision: 2026-05-20" \
-d '{
 "model": "gemini-omni-flash-preview",
 "input": [
   {"type": "image", "data": "'"$START_B64"'", "mime_type": "image/png"},
   {"type": "image", "data": "'"$END_B64"'", "mime_type": "image/png"},
   {"type": "text", "text": "A smooth timelapse from sunrise to sunset."}
 ],
 "response_format": {"type": "video"},
 "background": false,
 "store": false,
 "stream": false
}'
```

### Subject Reference

Generate a video incorporating specific subjects provided as reference images.

* **Python**

```py
interaction = client.interactions.create(
    model="gemini-omni-flash-preview",
    input=[
        {"type": "image", "data": cat_b64, "mime_type": "image/png"},
        {"type": "image", "data": yarn_b64, "mime_type": "image/png"},
        {"type": "text", "text": "A cat playfully batting at a ball of yarn."}
    ],
    response_format={"type": "video"}
)
```

* **JavaScript**

```javascript
const interaction = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: [
    { type: 'image', data: catData, mime_type: 'image/png' },
    { type: 'image', data: yarnData, mime_type: 'image/png' },
    { type: 'text', text: 'A cat playfully batting at a ball of yarn.' },
  ],
  response_format: { type: 'video' },
});
```

* **REST**

```shell
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-H "Api-Revision: 2026-05-20" \
-d '{
 "model": "gemini-omni-flash-preview",
 "input": [
   {"type": "image", "data": "'"$CAT_B64"'", "mime_type": "image/png"},
   {"type": "image", "data": "'"$YARN_B64"'", "mime_type": "image/png"},
   {"type": "text", "text": "A cat playfully batting at a ball of yarn."}
 ],
 "response_format": {"type": "video"},
 "background": false,
 "store": false,
 "stream": false
}'
```

## 

## Stateful Video Editing

This is the defining capability of Gemini Omni Flash. The Interactions API lets you generate a video and then iteratively edit it through follow-up prompts, just like having a conversation. Each turn builds on the previous result — the model remembers the video context and applies your requested changes while preserving elements you haven't mentioned. Chain turns together using previous\_interaction\_id to maintain context between edits.

***How it works:** Each call to `create_interaction` returns an `interaction_id`. Pass this ID as `previous_interaction_id` in the next turn to maintain context. The model automatically tracks the conversation history and the generated video state.*

**Note about EEA regulations**: If you are in the EEU (Europe, UK, CH…), you will only be able to edit Omni generated videos (via interactions chaining), without celebrities nor children.

The following example demonstrates how to generate a first video then edit it:

* **Python**

```py
# Turn 1: Generate initial video
res1 = client.interactions.create(model="gemini-omni-flash-preview", input="A dog running.")

# Turn 2: Edit the previous video
res2 = client.interactions.create(
    model="gemini-omni-flash-preview",
    previous_interaction_id=res1.id,
    input="Change the setting to a snowy winter wonderland."
)
```

* **JavaScript**

```javascript
// Turn 1: Generate initial video
const res1 = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: 'A dog running.',
});

// Turn 2: Edit the previous video
const res2 = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  previous_interaction_id: res1.id,
  input: 'Change the setting to a snowy winter wonderland.',
});
```

* **REST**

```shell
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-H "Api-Revision: 2026-05-20" \
-d '{
 "model": "gemini-omni-flash-preview",
 "previous_interaction_id": "'"$PREVIOUS_ID"'",
 "input": "Change the setting to a snowy winter wonderland.",
 "background": false,
 "store": true,
 "stream": false
}'
```

Each turn in the conversation produces a complete new video. The model understands context from prior turns, so you can make incremental changes — adjust lighting, swap backgrounds, modify camera angles, add or remove elements — without re-describing the entire scene. You can chain as many turns as needed to achieve your desired result.

## Edit your own videos (Not available in the EEU)

Here’s how to upload your videos using the file API then edit them with Omni.

* **Python**

```py
# Upload video using the file API
import time

video_file = client.files.upload(file="Video.mp4")

while video_file.state == "PROCESSING":
    print('Waiting for video to be processed.')
    time.sleep(10)
    video_file = client.files.get(name=video_file.name)

if video_file.state == "FAILED":
  raise ValueError(video_file.state)
print(f'Video processing complete: ' + video_file.uri)

# Edit your video
interaction = client.interactions.create(
    model=OMNI_MODEL,
    input=[
        {"type": "document", "uri": video_file.uri},
        {"type": "text", "text": "Add magical arifacts in each bowl"}
    ],
)
```

Note: you can also pass the data directly in byte64, but since videos can be quite big we recommend using the File API.

```shell
#!/bin/bash
VIDEO_B64=$(encode_file "$VIDEO_FILE")

curl -sS -w "\n[HTTP %{http_code}]\n" "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d @- <<EOF > video_editing_response.json
{
  "model": "gemini-omni-flash-preview",
  "input": [
    {
      "type": "user_input",
      "content": [
        {
          "type": "video",
          "mime_type": "video/mp4",
          "data": "$VIDEO_B64"
        },
        {
          "type": "text",
          "text": "Make the video a pixar animation style."
        }
      ]
    }
  ],
  "background": false,
  "store": false,
  "stream": false,
  "response_format": { "type": "video" }
}
EOF
```

## URI delivery (Waiting & Polling)

For videos larger than 4MB, it is recommended to use `delivery="uri"` in `response_format`. This returns a Google-hosted URI that you must poll until the video is `ACTIVE` before downloading.

* **Python**

```py
import time

# 1. Request video via URI delivery
interaction = client.interactions.create(
    model="gemini-omni-flash-preview",
    input="A beautiful sunset.",
    response_format={"type": "video", "delivery": "uri"}
)

# 2. Extract file name and poll for ACTIVE state
video_output = interaction.output_video
file_name = video_output.uri.split("/")[-1] # Extract ID

print("Waiting for video processing...")
while True:
    f_info = client.files.get(name=f"files/{file_name}")
    if f_info.state.name == "ACTIVE":
        break
    elif f_info.state.name == "FAILED":
        raise RuntimeError("Generation failed.")
    time.sleep(5)

# 3. Download the final video
video_bytes = client.files.download(file=video_output.uri)
with open("output.mp4", "wb") as f:
    f.write(video_bytes)
```

* **JavaScript**

```javascript
// 1. Request video via URI delivery
const interaction = await ai.interactions.create({
  model: 'gemini-omni-flash-preview',
  input: 'A beautiful sunset.',
  response_format: { type: 'video', delivery: 'uri' },
});

// 2. Extract file name and poll for ACTIVE state
const videoOutput = interaction.output_video;
const fileId = videoOutput.uri.match(/files\/([a-zA-Z0-9]+)/)[1];
const name = `files/${fileId}`;

console.log("Waiting for video processing...");
while (true) {
  const fInfo = await ai.files.get({ name });
  if (fInfo.state.name === 'ACTIVE') break;
  if (fInfo.state.name === 'FAILED') throw new Error("Generation failed.");
  await new Promise(r => setTimeout(r, 5000));
}

// 3. Download the final video
await ai.files.download({
  file: videoOutput,
  downloadPath: 'output.mp4',
});
console.log("💾 Saved video to output.mp4");
```

* **REST**

```shell
#!/bin/bash

_1. Initial request to generate the video_
RESPONSE=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/interactions?key=$API_KEY" \
-H "Content-Type: application/json" \
-H "Api-Revision: 2026-05-20" \
-d '{
 "model": "gemini-omni-flash-preview",
 "input": "A beautiful sunset over a calm ocean.",
 "response_format": {"type": "video", "delivery": "uri"},
 "background": false,
 "store": false,
 "stream": false
}')

_Extract FILE_ID from the URI (e.g., "files/abc-123" -> "abc-123")_
FILE_URI=$(echo $RESPONSE | jq -r '.output_video.uri')
FILE_ID=$(echo $FILE_URI | cut -d'/' -f2)

echo "Video requested (ID: $FILE_ID). Waiting for processing..."

_2. Polling loop_
while true; do
 # Get current file status
 STATUS_JSON=$(curl -s -X GET "https://generativelanguage.googleapis.com/v1beta/files/$FILE_ID?key=$API_KEY")
 STATE=$(echo $STATUS_JSON | jq -r '.state')

 if [ "$STATE" == "ACTIVE" ]; then
   echo "Processing complete! Downloading..."
   break
 elif [ "$STATE" == "FAILED" ]; then
   echo "Error: Generation failed."
   exit 1
 else
   echo "Current state: $STATE... (waiting 5s)"
   sleep 5
 fi
done

_3. Final download_
curl -L -X GET "https://generativelanguage.googleapis.com/v1beta/files/$FILE_ID:download?alt=media&key=$API_KEY" \
--output "output.mp4"

echo "Done! Video saved to output.mp4"
```

**Raw REST JSON structure (URI):**

```json
{
  "steps": [
    { "type": "user_input", "content": [{"type": "text", "text": "..."}] },
    { "type": "thought", "content": [{"text": "...", "type": "thought"}] },
    {
      "type": "model_output",
      "content": [
        {
          "type": "video",
          "mime_type": "video/mp4",
          "uri": "https://generativelanguage.googleapis.com/v1beta/files/...:download?alt=media"
        }
      ]
    }
  ],
  "id": "v1_...",
  "status": "completed",
  "model": "gemini-omni-flash-preview",
  "object": "interaction"
}
```

***Note on GET interaction:*** *Currently (but this is being fixed), calling* `GET /v1beta/interactions/{id}` *returns the video as inline base64 data in the* `data` *field, even if the interaction was originally created with* `delivery: "uri"`*. The* `uri` *field is only guaranteed to be present in the initial creation response or SSE stream.*

### Background Mode & Two-tier Polling (Experimental)

For workflows where you cannot maintain a long-lived connection, you can use `background: true`. However, this changes the polling flow:

1. **POST** `/v1beta/interactions` with `"background": true` → Returns an `interaction_id` immediately with `status: "in_progress"`.  
2. **Poll GET** `/v1beta/interactions/{interaction_id}` until `status` becomes `"completed"`.  
3. **Extract the file URI** from `steps[].content[]`.  
4. **Poll GET** `/v1beta/files/{file_id}` until `state` is `"ACTIVE"` or `“PROCESSING”` (as you don’t need to wait for the video to be tokenized)  
5. **Download** using `GET /v1beta/files/{file_id}:download?alt=media` with the `-L` flag.

> [!CAUTION]
> **Preview Limitation:** Background mode currently has known issues with stateful interactions (chained edits). For the most reliable experience, use synchronous calls (`background: false`) with streaming (`stream: true`). We recommend using only `stream: false` for the preview.

## 

## Best Practices

- **Use URI Delivery:** For videos larger than 4MB (\>720p when available), use `delivery="uri"` in `response_format` to avoid payload size limits.  
- **Poll for Processing:** Always wait for the `ACTIVE` state before attempting to download or reference the video in subsequent turns.  
- **Optimized Performance:** We recommend explicitly setting `background=false`, `store=false`, and `stream=false` for faster, synchronous unary generation.  
- **Prompt Precision:** Be specific about style, lighting, and camera angles.

## Limitations

Keep the following limitations in mind when working with Gemini Omni Flash during the Early Access Program:

* *System instructions, temperature, top\_p, stop sequences, and negative prompts are not supported but you can put your negatives in the regular prompt: eg Do not do X). Please tell us if that’s a problem for you.*  
* *All generated videos include SynthID watermarking, which is invisible to viewers but can be detected programmatically for provenance verification.*  
* *Video generation times vary based on duration, resolution, and current API load. Longer and higher-resolution videos take more time to generate.*  
* *Content safety filters are applied to both input prompts and generated video (and depend on your region). Prompts that violate usage policies will be blocked.*  
  


## We Want Your Feedback

Please start by answering [the survey](https://forms.gle/FQ6sm6daje2F7t8t9), then if you have other things you want to share with us, please reply directly to this email with your findings. We are specifically looking to understand your experience across both model performance and API integration:

Industry-Specific Feedback:

* Industry Use Cases: We are looking for explicit feedback from industries like film studios, advertising, marketing, education, and gaming. How is Omni working for your specific industry use cases?  
* Veo Workflows: Is Omni able to support your existing Veo video model workflows? If not, what are the gaps?

API & Integration Experience:

* Awareness & Adoption: Were you aware of the Interactions API prior to this program?  
* Integration Challenges: Do you foresee any trouble integrating the Interactions API into your existing systems or architecture? If so, why?  
* Ease of Use: How would you rate the overall developer experience and ease of use of the Interactions API when building multi-turn video workflows?  
* Resolution: Would you prefer to generate all resolutions with Omni to only 720p one and upscale them later with a cheaper model?

Model Quality & Prompting:

* Unstructured Prompting: How well is the conversational, unstructured prompting working for your specific use cases compared to other methods? Please share specific prompts you've tested.  
* Use Cases & Comparisons: What are your primary use cases for Omni? If you are currently using other video generation models (like Veo), how does Omni compare in quality and prompt adherence?  
* Text-Free Output: How important is it for your application to generate video-only outputs (guaranteeing no text generation in the visual output), and why?

