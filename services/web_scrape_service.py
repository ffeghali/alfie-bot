from youtube_transcript_api import YouTubeTranscriptApi

# This may become a webscrapping methods service using different APIs 

def get_yt_transcript(url):
    """Scrapes the full transcript from the given youtube video url """
    video_id = url.split("v=")[1]
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_transcript = " ".join([item['text'] for item in transcript_list])
    return full_transcript