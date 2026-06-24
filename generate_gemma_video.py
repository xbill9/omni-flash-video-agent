import os
import sys
import time
import base64
from google import genai

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("🔴 Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
        
    print("Initializing Gemini Client...")
    client = genai.Client()
    
    # Prompt curated from the gemma.md content (GPU serving, DevOps agent, performance visualization)
    prompt = (
        "A hyper-realistic 3D rendering of an NVIDIA L4 GPU inside a sleek, futuristic "
        "datacenter server rack. Holographic charts showing rising throughput graphs and "
        "latency curves float in the air in front of the server. Glowing data packets "
        "stream through the fiber optic cables in a cyberpunk style, representing "
        "high-performance AI inference."
    )
    
    print(f"Submitting video generation request for prompt:\n'{prompt}'\n")
    
    try:
        interaction = client.interactions.create(
            model="gemini-omni-flash-preview",
            input=prompt,
            response_modalities=["video"],
            background=False,
            store=False,
            stream=False
        )
        
        output_filename = "gemma_devops.mp4"
        print(f"Writing video data to {output_filename}...")
        video_bytes = base64.b64decode(interaction.output_video.data)
        with open(output_filename, "wb") as f:
            f.write(video_bytes)
            
        print(f"🟢 Success! Video saved to {os.path.abspath(output_filename)}")
        
    except Exception as e:
        print(f"🔴 Error generating video: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
