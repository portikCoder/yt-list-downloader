import sys
from typing import List

import youtube_dl
from youtube_dl import DownloadError

NO_TRIALS = 2

# DEFAULT_FORMAT = "243+250/242+139/278+140"
# DEFAULT_FORMAT = "134+250/243+250/242+139/278+140"
DEFAULT_FORMAT = "134+250/243+250/242+139/278+140"

ACCEPTABLE_VIDEO_FORMAT_IDS = ['242', '278']

ACCEPTABLE_AUDIO_FORMAT_IDS = ['139', '140']


def download_videos_by_id(video_watch_ids: List[str]):
    # video_watch_ids = not_found_res = ["jRhyUuZa3U8"]  # dev-purpose
    for watch_ids in video_watch_ids:
        # for watch_id in watch_ids:
        #     download(watch_id)
        download(watch_ids)
        print("*" * 50)


def download(watch_or_playlist_id_or_url: str) -> None:
    """

    :param watch_or_playlist_id_or_url: could be even the watch- or playlist id, even a full URL, doesn't matter
    :return: -
    """
    if watch_or_playlist_id_or_url is None:
        print(f"EMPTY input given: {watch_or_playlist_id_or_url}", file=sys.stderr)
        return

    print(watch_or_playlist_id_or_url)

    # with youtube_dl.YoutubeDL(craft_ydl_config(listformats=True)) as ydl:
    with youtube_dl.YoutubeDL(craft_ydl_config()) as ydl:
        for _ in range(NO_TRIALS):
            try:
                result = ydl.extract_info(
                    f"{watch_or_playlist_id_or_url}",
                    # download=False  # We just want to extract the info
                    download=True
                )
                break
            except DownloadError as de:
                # try:
                #     format_config = find_closest_format(watch_or_playlist_id_or_url)
                #     print("next format to be tried: ", format_config)
                #     ydl.params['format'] = format_config
                # except:
                #     print(f"NO format has been selected!", file=sys.stderr)
                    print(f"Playlist download error: {de}", file=sys.stderr)

        else:
            print(f"NO success after a while in case of '{watch_or_playlist_id_or_url}' for some reason!",
                  file=sys.stderr)
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
        print(ke, file=sys.stderr)


def find_closest_format(watch_id: str) -> str:
    # config = {"listformats": True, }
    config = {}

    with youtube_dl.YoutubeDL(config) as ydl:
        # meta = ydl.extract_info(f"http://www.youtube.com/watch?v={watch_id}", download=False)
        meta = ydl.extract_info(f"{watch_id}", download=False)
        formats = meta.get('formats', [meta])
        print("avail formats: ", formats)

        available_formats = youtube_dl.YoutubeDL({}).extract_info(f"http://www.youtube.com/watch?v={watch_id}",
                                                                  download=False).get('formats')

        video_formats = [x for x in available_formats if x['width'] is not None]
        audio_formats = [x for x in available_formats if x['width'] is None]

        result_video_format_id = find_required_format_for(ACCEPTABLE_VIDEO_FORMAT_IDS, video_formats)
        result_audio_format_id = find_required_format_for(ACCEPTABLE_AUDIO_FORMAT_IDS, audio_formats)

        print(formats)
        ACCEPTABLE_VIDEO_FORMAT_IDS.remove(result_video_format_id)
        ACCEPTABLE_AUDIO_FORMAT_IDS.remove(result_audio_format_id)
        return f"{result_video_format_id}+{result_audio_format_id}"


def find_required_format_for(acceptable_audio_format_ids, audio_formats) -> str:
    result_audio_format_id = None
    for acceptable_audio_format_id in acceptable_audio_format_ids:
        required_audio_format: dict = list(
            filter(lambda x: x['format_id'] == acceptable_audio_format_id, audio_formats))[0]
        if required_audio_format:
            result_audio_format_id = required_audio_format['format_id']
            break
    return result_audio_format_id


def craft_ydl_config(format: str = DEFAULT_FORMAT, listformats: bool = False):
    return {
        "ignore_errors": True,
        "no_overwrites": True,
        "continue": True,
        # "outtmpl": "%(id)s.%(ext)s",
        "outtmpl": "./video-output/%(playlist_title)s/%(id)s-___-%(title)s.%(ext)s",

        "format": format,

        'listformats': listformats,

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
    }
