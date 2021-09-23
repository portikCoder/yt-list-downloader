import datetime
import os
import re
from datetime import timedelta
from typing import List

import tqdm as tqdm
from googleapiclient.discovery import build

from youtube_downloader import download_videos_by_id

VIDEO_WATCH_IDS = """6cFU7KVgb0w
BDEqF1Xd7-s
UeNIg-9GsXY
IOcDvbYmnqA
VXqLWQGUC54
a0FhnqvY_qk
iCp8g_DzHMs
B2nJVg4ujeQ
ZvTm3Lc3-lw
bGbXARRBFhg
pcNriLHA9Zw
B2nJVg4ujeQ
pcNriLHA9Zw
C06bH2fQxpo
ZvTm3Lc3-lw
bGbXARRBFhg
34QaOE5KGN8
TNPhuTaJNZY
3x-YZHeXHyA
ca4iytumul8
ca4iytumul8
vKEInwNIeho
AnTzdW9oOY4
wCNHXBdhmVQ
uQHFKVEHLyo
IVhIYs7nsr0
EIiYqzzVsLU
pU8252z0zxY
ryr6Frm7pok
ryr6Frm7pok
Tq8_GfpBZFo
3x-YZHeXHyA
Wu7T-ws0qNQ
rfodroO2LLc
NTuOX2j5QSI
Q0w4Ldh3DHA
QQR8C_ckzMk
t-QRKVKfHIM
N4aJOjK-N0w
GKzlswrfaP4
mr7GmhwNFGU
lblL-v7hjY0
OlQz0g3HomQ
5hog8YPMG58
HytFiVKrKS0
MXDbO7Bi714
KobIGa932FM
zxrq_ov79lI
K4F89smbWfQ
ZWUVdzmiU80
BysQmSPwisA
VaqE3fvFwUE
fTKHvfPr38U
qPY6AtIS7_Y
3OCIh21sOOY
27p0GP3E3KA
kxobrEC3MWs
tWE0Zr_Bxjo
glKYGBTGb0k
zU5XiktiNUM
L6e1qmQzoY0
IFolUobmRZs
pfWaRnp9gks
QVifDCGH2_8
gW0X6ew4rxw
UD0r88mvhpA
l6tRQDYoyh8
VZmmCHqDm14
hXbCPFrM0xI
m7B8GzNhUSA
vxG20biT3mw
3qOJMvFKv3k
9JdtGf1IpVo
yceDqLB9AGY
GN6jXtI0YeQ
WVpD0LARpHM
XOUbGg6KL5U
ZknCAPfIUy4
DyzwsParW4Q
jV-vfDBolGQ
RNvog7uxl84
GPDQj7BQsqc
3xcU8iyPWTU
2hzLyeqswkc
LR_fG8Za9FQ
jXR7rm4aULQ
d3ij5H1gHh8
QrJXbIFT4Z0
1jqHDCdxMBU
CsTzKofwjyM
59Lmvs6vAu0
6_Q5EEUawS4
3V91V7kBNXU
psoYZJrF4Fs
cCHMFrwUqhY
yXrhqWvK9DQ
mzfCB71HVRk
cKmSK37Ussg
a0MLB-jfUjo
NCiyolveWAg
1k8zFXyEUhE
KKhOH4Rxttk
LcNscq1hFjs
M26xnH1hQf4
xBsS_G5KkmU
m16VNg_T7ek
-YbPae-CotE
PsfKkn8VjUI
u20QBSp5qTg
ZzduPPKzR6I
udj7oC9tlh8
p-wHPCY6R3o
Y698-QMl4R4
t62Z5FPlWBA
e28GwjHOjpI
ax-5YETj5tQ
KHsni6xOk8o
KlD_0xFk5aQ
Ik-CStWEN80
9XwrBr7LwQI
v4lP1FB3TXo
jRhyUuZa3U8
dNSRzm2kgms
lEu8SQafevQ
N8wCAgXwvQk
2fUEnMqbuo0
ImU4vBXtYnI
CELT-eF8ZkA
s6NEeARKXDs
rmyIJhVGRTY
Neesv5sVcdQ
-A18BRruWFI
LXxJ8--D57g
vqeBZpnaj08
54dmoNnscJA
xt0jAywEdoE
Kp1l-BJPzsc
iaKCf_FWVM4
IuacJRuLpGE
dlAxjWH7-XE
JxcyUL16_B8
6TgZu5AEK0A
OOqFd6wps0w
eujH8cBh4TU
PwsLmcB0D6A
m7B8GzNhUSA
YMPwj55TFME
mTGHIa-GxNA
xYWeNwGmJXU
QrqtUIRjenA
4sisuN9gz0E
fUbiW74SyLQ
qxzbQZfzDiY
N8wCAgXwvQk
9fWbC2MUXzM
8FzwZSZx0Sw
Cq4ASp-7WOk
NDfy-BdM_Ck
_F4vyE3srMs
iafsOfqSFwg
8lL53eUaY3A
hLGmH4wcBjM
YMES-CT68I4
6xhFYqBBhIc
Km_zEvQRyv8
vPIrIsnQri0
4ay-Y9htSUY
7gD6yInQDr4
M-yJl6TXocI
JxbA-iJpjoI
S-kSWKcOXrE
3sIW72Ilq7o
3sIW72Ilq7o
NaXAHCIVYns
NaXAHCIVYns
80Vb0Wr4H44
80Vb0Wr4H44
FelO1-JTB_Q
9Wu7U9xRb2c
9Wu7U9xRb2c
-mscUPgspIs
61b1iZJ4gxg
wzye4-JdXR8
rZ84f2FhNEg
CC5ca6Hsb2Q
""".split("\n")


def get_total_hours_for(playlist):
    api_key = os.environ.get('YT_API_KEY')

    youtube = build('youtube', 'v3', developerKey=api_key)

    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    total_seconds = 0

    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()

        vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]
        VIDEO_WATCH_IDS.append(vid_ids)

        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = item['contentDetails']['duration']

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_seconds += video_seconds

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break

    total_seconds = int(total_seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return hours, minutes, seconds


def get_playlist_ids_from(playlists: List[str]):
    BEHIND_ID_TAG = "/playlist?list="
    return [playlist[playlist.find(BEHIND_ID_TAG) + len(BEHIND_ID_TAG):] for playlist in playlists]


def main():
    # total_hours, total_minutes, total_seconds = find_watch_ids_and_content_lengths()

    # print_content_length(total_hours, total_minutes, total_seconds)

    download_videos_by_id(VIDEO_WATCH_IDS)


def print_content_length(total_hours, total_minutes, total_seconds):
    sum_total_seconds = total_hours * 3600 + total_minutes * 60 + total_seconds
    timedelta_of_fulltime = datetime.timedelta(seconds=sum_total_seconds)
    print(f"Raw total time in h:m:s => {total_hours}:{total_minutes}:{total_seconds}")
    str(datetime.timedelta(seconds=666))
    days, hours, minutes = timedelta_of_fulltime.days, timedelta_of_fulltime.seconds // 3600, timedelta_of_fulltime.seconds % 3600 // 60
    seconds = timedelta_of_fulltime.seconds - hours * 3600 - minutes * 60
    hours += days * 24
    print(f"Raw total time in h:m:s => {hours}:{minutes}:{seconds}")
    print(f"{timedelta_of_fulltime}")


def find_watch_ids_and_content_lengths():
    total_hours = total_minutes = total_seconds = 0
    from input import playlists
    playlist_ids = get_playlist_ids_from(playlists)
    for playlist in tqdm.tqdm(playlist_ids):
        hours, minutes, seconds = get_total_hours_for(playlist=playlist)
        # print(f'{hours}:{minutes}:{seconds}')

        total_hours += hours
        total_minutes += minutes
        total_seconds += seconds
    return total_hours, total_minutes, total_seconds


if __name__ == "__main__":
    # playlist = "PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU"
    # playlist = "PLZ7Ye5d76T7j-QdeSLenweE_E_w2gWGDd"

    main()
