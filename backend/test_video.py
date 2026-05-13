from app.services.video_recommendation import get_related_videos

videos = get_related_videos("Election Commission of India")

print(videos)