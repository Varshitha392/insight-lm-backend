from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):

    if "v=" in url:
        return url.split("v=")[1]

    return url


def get_youtube_transcript(url):

    video_id = extract_video_id(url)

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = " ".join([t["text"] for t in transcript])

    return text