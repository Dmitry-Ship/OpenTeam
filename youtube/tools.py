import re
from youtube_transcript_api import YouTubeTranscriptApi

def retreive_youtube_transcription(youtube_url):
    print("📝 transcribing ...", youtube_url)

    pattern = r"(?:v=|be/|/watch\?v=|\?feature=youtu.be/)([\w-]+)"

    match = re.search(pattern, youtube_url)

    if not match:
        return "Error: Invalid YouTube URL"

    video_id = match.group(1)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    combined_transcript = " ".join([item.get("text", "") for item in transcript])

    return combined_transcript

