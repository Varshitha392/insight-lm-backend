from youtubesearchpython import VideosSearch


def get_related_videos(query):

    videos_search = VideosSearch(query, limit=5)

    results = videos_search.result()

    videos = []

    for video in results["result"]:

        videos.append({
            "title": video["title"],
            "link": video["link"]
        })

    return videos