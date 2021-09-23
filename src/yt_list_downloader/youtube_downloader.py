from typing import List

import youtube_dl
from youtube_dl import YoutubeDL, DownloadError


def download(watch_id: str):
    print(watch_id)
    ydl = youtube_dl.YoutubeDL(
        {"outtmpl": "%(id)s.%(ext)s",
         # "format": "18",
         # "format": "243+250",
         "format": "250",
         # "format": "250",
         #    'listformats': True,
         'nocheckcertificate': True,
         # 'postprocessors': [{
             # 'key': 'FFmpegExtractAudio',
             # 'key': 'FFmpegVideoConvertor',

             # 'key': 'ExecAfterDownload',

         #     'preferredcodec': 'mp3',
         #     'preferredquality': '192',
         #     "ffmpeg-location" : "C:\\ffmpeg\\bin",
         #     "exec_cmd": 'ffmpeg -y -i 6cFU7KVgb0w.webm -vf "setpts=1.25*PTS" -r 24 6cFU7KVgb0w_FFMPEG.webm'
             # "exec_cmd": 'ffmpeg -n -i 6cFU7KVgb0w.webm -vf "setpts=1.25*PTS" -r 24 6cFU7KVgb0w_FFMPEG.webm'

         # }],

         # "ffmpeg-location" : "C:/ffmpeg/bin/ffmpeg.exe"
         # "ffmpeg-location" : "C:\\ffmpeg\\bin\\ffmpeg.exe",
         # "external-downloader": "ffmpeg"
         # "postprocessor_args": [
         # "exec": 'ffmpeg -y -i 6cFU7KVgb0w.webm -vf "setpts=1.25*PTS" -r 24 6cFU7KVgb0w_FFMPEG.webm'
             # [
             # *('ffmpeg -y -i 6cFU7KVgb0w.webm -vf "setpts=1.25*PTS" -r 24 6cFU7KVgb0w_FFMPEG.webm'.split())
             # *('ffmpeg -y -i 6cFU7KVgb0w.f243.webm -vf "setpts=1.25*PTS" -r 24 6cFU7KVgb0w_FFMPEG.webm'.split())
         # ]
         })

    with ydl:
        try:
            result = ydl.extract_info(
                f"http://www.youtube.com/watch?v={watch_id}",
                # download=False  # We just want to extract the info
                download=True  # We just want to extract the info
            )
        except DownloadError as de:
            print(de)
            return

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    # print(video)
    try:
        video_url = video['url']
        # print(video_url)
    except KeyError as ke:
        print(ke)


def download_videos_by_id(video_watch_ids: List[List[str]]):
    already_downloaded_videos = []

    for watch_ids in video_watch_ids[:1]:
        # for watch_id in watch_ids:
        #     download(watch_id)
        download(watch_ids)
