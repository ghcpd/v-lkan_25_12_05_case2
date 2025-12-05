import json
import os
from pathlib import Path
from gtts import gTTS

# Define output folder
OUTPUT_FOLDER = "audio_files"
JSONL_FILE = "text_convert_mp3.jsonl"

# Create output folder if it doesn't exist
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

print(f"Output folder: {OUTPUT_FOLDER}")

# Read and process the JSONL file
with open(JSONL_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # Skip empty lines
            data = json.loads(line)
            item_id = data.get('id')
            annotation_type = data.get('annotation_type')
            conversations = data.get('conversations', [])
            
            print(f"\nProcessing ID: {item_id}")
            
            # Process each conversation
            for conv in conversations:
                from_speaker = conv.get('from')
                text_value = conv.get('value', '').strip()
                
                if not text_value:
                    print(f"  Skipping empty text for {from_speaker}")
                    continue
                
                # Determine filename based on speaker
                if from_speaker == 'human':
                    filename = f"human_{item_id}.mp3"
                elif from_speaker == 'gpt':
                    filename = f"gpt_{item_id}.mp3"
                else:
                    print(f"  Skipping unknown speaker: {from_speaker}")
                    continue
                
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                
                # Check if file already exists
                if os.path.exists(filepath):
                    print(f"  File already exists: {filename}")
                    continue
                
                try:
                    # Create TTS object and save MP3
                    print(f"  Converting: {filename}")
                    print(f"    Text: {text_value[:50]}...")
                    tts = gTTS(text=text_value, lang='en', slow=False)
                    tts.save(filepath)
                    print(f"    ✓ Saved: {filename}")
                except Exception as e:
                    print(f"    ✗ Error converting {filename}: {str(e)}")

print("\n" + "="*50)
print("Conversion complete!")
print(f"All MP3 files saved to: {OUTPUT_FOLDER}/")
