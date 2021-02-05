import os
import shutil
from bota import constant

gist_path = os.path.join(constant.REPO_PATH, constant.YT_GIST_ID)


def pull_latest_yt_links_from_github_gist():
    try:
        shutil.rmtree(gist_path)
        print("Remove gist folder")
    except:
        print("FOlder doesnt exists: ", gist_path)
    os.system(f"cd {constant.REPO_PATH} && git clone https://gist.github.com/{constant.YT_GIST_ID}.git")
    all_yt_pth = os.path.join(gist_path, os.path.basename(constant.ALL_YT_LINK_PATH))
    yt_pth = os.path.join(gist_path, os.path.basename(constant.YT_LINK_PATH))
    shutil.copy(yt_pth, constant.YT_LINK_PATH)
    shutil.copy(all_yt_pth, constant.ALL_YT_LINK_PATH)
