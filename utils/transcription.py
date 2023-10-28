import openai
import os 
import asyncio

openai.api_key = "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"

chunks_dir = "./experimental/current_chunks"
transcripts = []
for chunk in os.listdir(chunks_dir):
    loop = asyncio.get_event_loop()
    chunk_path = os.path.join(chunks_dir, chunk), 'rb'
    result = loop.run_in_executor(None, model.transcribe, file_path)
    transcript = openai.Audio.transcribe('whisper-1', chunk_file, format='srt')
    transcripts.append(transcript.text)

print(transcripts)
        
