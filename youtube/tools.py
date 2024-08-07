import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Annotated

def retreive_youtube_transcription(youtube_url: Annotated[str, "The youtube url to retreive transcriptions from"]) -> Annotated[str, "The combined transcript"]:
    """
    Useful to search for video transcriptions from the given url
    The input should be a youtube url string
    :param youtube_url: str, youtube url to retreive transcriptions
    """

    print("📝 transcribing ...")

    pattern = r"(?:v=|be/|/watch\?v=|\?feature=youtu.be/)([\w-]+)"

    match = re.search(pattern, youtube_url)

    if not match:
        return "Error: Invalid YouTube URL"

    video_id = match.group(1)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    combined_transcript = " ".join([item.get("text", "") for item in transcript])

    return combined_transcript

