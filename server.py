import os
import base64
import time
from google import genai
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Gemini Omni Flash Video Agent")

# Initialize the Gemini client
client = genai.Client()
MODEL_NAME = "bouncybohr"

def _get_image_data(image_path: str) -> dict:
    """Helper to convert local image file to base64 input dict."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    mime_type = "image/png"
    if image_path.lower().endswith((".jpg", ".jpeg")):
        mime_type = "image/jpeg"
    elif image_path.lower().endswith(".webp"):
        mime_type = "image/webp"
        
    with open(image_path, "rb") as f:
        data_b64 = base64.b64encode(f.read()).decode("utf-8")
        
    return {"type": "image", "data": data_b64, "mime_type": mime_type}

def _handle_response(interaction, delivery: str, output_prefix: str) -> str:
    """Helper to handle inline vs URI delivery and save the resulting video."""
    video_output = getattr(interaction, "output_video", None)
    if not video_output:
        return (
            f"🟢 Interaction completed successfully.\n"
            f"• Interaction ID: {interaction.id}\n"
            f"• Note: No direct video output was found in the response."
        )
        
    output_filename = f"{output_prefix}_{int(time.time())}.mp4"
    
    if delivery == "uri" and getattr(video_output, "uri", None):
        file_name = video_output.uri.split("/")[-1]
        print(f"Waiting for video processing on Google File API (ID: {file_name})...")
        while True:
            f_info = client.files.get(name=f"files/{file_name}")
            if f_info.state.name == "ACTIVE":
                break
            elif f_info.state.name == "FAILED":
                raise RuntimeError("Google File API video processing failed.")
            time.sleep(5)
            
        print("Downloading video via File API...")
        video_bytes = client.files.download(file=video_output.uri)
    else:
        # Default/inline base64 delivery
        data = getattr(video_output, "data", None)
        if not data:
            raise ValueError("No video data found in output_video.")
        video_bytes = base64.b64decode(data)
        
    with open(output_filename, "wb") as f:
        f.write(video_bytes)
        
    return (
        f"🟢 Video successfully saved!\n"
        f"• Saved to: {os.path.abspath(output_filename)}\n"
        f"• Delivery mode: {delivery}\n"
        f"• Interaction ID: {interaction.id}"
    )

@mcp.tool()
def generate_video(prompt: str, aspect_ratio: str = "16:9", delivery: str = "inline") -> str:
    """
    Generates an initial video from a text prompt.
    - prompt: The text description of the video.
    - aspect_ratio: '16:9' (landscape) or '9:16' (portrait).
    - delivery: 'inline' (default, base64) or 'uri' (recommended for files > 4MB).
    """
    try:
        response_format = {"type": "video"}
        if aspect_ratio in ["9:16", "16:9"]:
            response_format["aspect_ratio"] = aspect_ratio
        if delivery == "uri":
            response_format["delivery"] = "uri"
            
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            response_format=response_format,
            background=False,
            store=True,
            stream=False
        )
        
        return _handle_response(interaction, delivery, "gen")
    except Exception as e:
        return f"🔴 Generation failed: {str(e)}"

@mcp.tool()
def edit_video(previous_interaction_id: str, edit_prompt: str, delivery: str = "inline") -> str:
    """
    Edits a previously generated video using its interaction ID.
    The model maintains contextual elements while applying your edit.
    - previous_interaction_id: The ID from the previous turn.
    - edit_prompt: Natural language description of what to change.
    - delivery: 'inline' or 'uri'.
    """
    try:
        response_format = {"type": "video"}
        if delivery == "uri":
            response_format["delivery"] = "uri"
            
        interaction = client.interactions.create(
            model=MODEL_NAME,
            previous_interaction_id=previous_interaction_id,
            input=edit_prompt,
            response_format=response_format,
            background=False,
            store=True,
            stream=False
        )
        
        return _handle_response(interaction, delivery, "edit")
    except Exception as e:
        return f"🔴 Editing failed: {str(e)}"

@mcp.tool()
def animate_image(image_path: str, motion_prompt: str, delivery: str = "inline") -> str:
    """
    Animates a static local image using a motion description.
    - image_path: Path to the local image file.
    - motion_prompt: Instructions on how the image should animate.
    - delivery: 'inline' or 'uri'.
    """
    try:
        img_data = _get_image_data(image_path)
        
        response_format = {"type": "video"}
        if delivery == "uri":
            response_format["delivery"] = "uri"
            
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=[img_data, {"type": "text", "text": motion_prompt}],
            response_format=response_format,
            background=False,
            store=True,
            stream=False
        )
        
        return _handle_response(interaction, delivery, "animated")
    except Exception as e:
        return f"🔴 Animation failed: {str(e)}"

@mcp.tool()
def interpolate_images(start_image_path: str, end_image_path: str, prompt: str, delivery: str = "inline") -> str:
    """
    Creates an interpolation transition video between two local keyframe images.
    - start_image_path: Path to the first image.
    - end_image_path: Path to the final image.
    - prompt: Instruction detailing the transition (e.g. 'A smooth timelapse from sunrise to sunset').
    - delivery: 'inline' or 'uri'.
    """
    try:
        start_img = _get_image_data(start_image_path)
        end_img = _get_image_data(end_image_path)
        
        response_format = {"type": "video"}
        if delivery == "uri":
            response_format["delivery"] = "uri"
            
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=[start_img, end_img, {"type": "text", "text": prompt}],
            response_format=response_format,
            background=False,
            store=True,
            stream=False
        )
        
        return _handle_response(interaction, delivery, "interpolation")
    except Exception as e:
        return f"🔴 Interpolation failed: {str(e)}"

@mcp.tool()
def generate_with_subjects(subject_image_paths: list[str], prompt: str, delivery: str = "inline") -> str:
    """
    Generates a video incorporating specific subjects provided as reference image paths.
    - subject_image_paths: List of local paths to subject images.
    - prompt: Description of the scene and subject actions.
    - delivery: 'inline' or 'uri'.
    """
    try:
        inputs = []
        for path in subject_image_paths:
            inputs.append(_get_image_data(path))
        inputs.append({"type": "text", "text": prompt})
        
        response_format = {"type": "video"}
        if delivery == "uri":
            response_format["delivery"] = "uri"
            
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=inputs,
            response_format=response_format,
            background=False,
            store=True,
            stream=False
        )
        
        return _handle_response(interaction, delivery, "subject")
    except Exception as e:
        return f"🔴 Subject reference generation failed: {str(e)}"

@mcp.tool()
def edit_user_video(video_path: str, edit_prompt: str, delivery: str = "inline") -> str:
    """
    Uploads a local video using the Gemini File API and edits it with Gemini Omni Flash.
    - video_path: Path to the local video file to upload and edit.
    - edit_prompt: Instruction of what to change in the video (e.g. 'Make it a Pixar animation style').
    - delivery: 'inline' or 'uri'.
    """
    try:
        if not os.path.exists(video_path):
            return f"🔴 Video file not found: {video_path}"
            
        print(f"Uploading video {video_path} via Gemini File API...")
        video_file = client.files.upload(file=video_path)
        
        print("Waiting for uploaded video to be processed...")
        while video_file.state == "PROCESSING":
            time.sleep(5)
            video_file = client.files.get(name=video_file.name)
            
        if video_file.state == "FAILED":
            raise ValueError("Gemini File API video upload processing failed.")
            
        print(f"Video uploaded successfully. URI: {video_file.uri}")
        
        response_format = {"type": "video"}
        if delivery == "uri":
            response_format["delivery"] = "uri"
            
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=[
                {"type": "document", "uri": video_file.uri},
                {"type": "text", "text": edit_prompt}
            ],
            response_format=response_format,
            background=False,
            store=True,
            stream=False
        )
        
        return _handle_response(interaction, delivery, "user_edit")
    except Exception as e:
        return f"🔴 Editing user video failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
