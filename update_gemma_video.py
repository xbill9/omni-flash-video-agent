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
    
    # Step 1: Generate the initial video (MUST set store=True to get an interaction_id)
    initial_prompt = (
        "A hyper-realistic 3D rendering of an NVIDIA L4 GPU inside a sleek, futuristic "
        "datacenter server rack. Holographic charts showing rising throughput graphs and "
        "latency curves float in the air in front of the server. Glowing data packets "
        "stream through the fiber optic cables in a cyberpunk style, representing "
        "high-performance AI inference."
    )
    
    print(f"1. Generating initial video (store=True)...")
    try:
        interaction_1 = client.interactions.create(
            model="gemini-omni-flash-preview",
            input=initial_prompt,
            response_modalities=["video"],
            background=False,
            store=True,
            stream=False
        )
        
        initial_id = interaction_1.id
        print(f"🟢 Initial video generated. Interaction ID: {initial_id}")
        
        # Save initial video just in case
        with open("gemma_devops_initial.mp4", "wb") as f:
            f.write(base64.b64decode(interaction_1.output_video.data))
            
    except Exception as e:
        print(f"🔴 Initial generation failed: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Step 2: Edit the video using stateful previous_interaction_id
    edit_prompt = "Add a holographic text label 'Gemma4 12B' floating above the GPU."
    print(f"\n2. Editing video using previous_interaction_id={initial_id}...")
    print(f"Prompt: '{edit_prompt}'")
    
    try:
        interaction_2 = client.interactions.create(
            model="gemini-omni-flash-preview",
            previous_interaction_id=initial_id,
            input=edit_prompt,
            response_modalities=["video"],
            background=False,
            store=True,
            stream=False
        )
        
        output_filename = "gemma_devops_updated.mp4"
        print(f"Writing updated video data to {output_filename}...")
        with open(output_filename, "wb") as f:
            f.write(base64.b64decode(interaction_2.output_video.data))
            
        print(f"🟢 Success! Edited video saved to {os.path.abspath(output_filename)}")
        print(f"New Interaction ID: {interaction_2.id}")
        
    except Exception as e:
        print(f"🔴 Stateful editing failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
