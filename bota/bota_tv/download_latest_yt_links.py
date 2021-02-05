import os
import shutil
from bota import constant

gist_path = os.path.join(constant.REPO_PATH, 'youtube_link_gist/')


def pull_latest_yt_links_from_github_gist():
    os.system(f"cd {gist_path} && git pull")
    all_yt_pth = os.path.join(gist_path, os.path.basename(constant.ALL_YT_LINK_PATH))
    yt_pth = os.path.join(gist_path, os.path.basename(constant.YT_LINK_PATH))
    shutil.copy(yt_pth, constant.YT_LINK_PATH)
    shutil.copy(all_yt_pth, constant.ALL_YT_LINK_PATH)
