import youtube_dl, pickle
from bota import constant
from datetime import datetime


             # UCVTyTA7-g9nopHeHbeuvpRA is the channel id (1517+ videos)
# PLAYLIST_ID = 'UUVTyTA7-g9nopHeHbeuvpRA'  # Late Night with Seth Meyers
# PLAYLIST_ID = "PLYoT1sEFy-cUVg1CmNxbrE1fmgAptwe-6"
#
# with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
#
#     playd = ydl.extract_info(PLAYLIST_ID, download=False)
#
#     with open('playlist.pickle', 'wb') as f:
#         pickle.dump(playd, f, pickle.HIGHEST_PROTOCOL)
#
#     vids = [vid for vid in playd['entries'] if 'A Closer Look' in vid['title']]
#     print(sum('Trump' in vid['title'] for vid in vids), '/', len(vids))
#

# pth = "playlist.pickle"
# with open('playlist.pickle', 'rb') as f:
#     a = pickle.load(f)
# print(1)

PLAYLIST_ID = "PLYoT1sEFy-cUVg1CmNxbrE1fmgAptwe-6"


class YoutubeVideo:
    def __init__(self):
        self.base_video_url = 'https://www.youtube.com/watch?v='

    def fetch_links_from_yt_dl(self, playlist_id):
        with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
            playd = ydl.extract_info(playlist_id, download=False)
            return playd

    def post_process_results(self, results):
        final_results = []
        entries = results['entries']

        for entry in entries:
            video_link = entry['webpage_url']
            description = entry['description']
            title = entry['title']
            published = entry['upload_date']
            published = published[:4] + '-' + published[4:6] + '-' + published[6:]
            published = datetime.strptime(published, '%Y-%m-%d')
            info = {'link': video_link,
                    'title': title,
                    'published': published,
                    'description': description}
            final_results.append(info)
        return final_results

    def get_video_links(self, playerlist_id=PLAYLIST_ID):
        r = self.fetch_links_from_yt_dl(playerlist_id)
        r = self.post_process_results(r)
        return r


if __name__ == '__main__':
    yt = YoutubeVideo()
    r = yt.get_video_links()
    for x in r:
        print(x)
