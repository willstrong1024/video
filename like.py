#!/usr/bin/python3

import httplib2
import os
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "config/client_secrets.json"

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
    %s
with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
    CLIENT_SECRETS_FILE))

RATINGS = ('like', 'dislike', 'none')

def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        scope=YOUTUBE_READ_WRITE_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("config/%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))

def like_video(youtube, args):
  youtube.videos().rate(
    id=args.video_id,
    rating=args.rating
  ).execute()

if __name__ == "__main__":
    argparser.add_argument("--video-id", required=True,
        help="ID of video whose thumbnail you're updating.")
    argparser.add_argument("--rating", default="like", choices=RATINGS,
        help='Indicates whether the rating is "like", "dislike", or "none".')
    args = argparser.parse_args()

    youtube = get_authenticated_service(args)

    try:
        like_video(youtube, args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    else:
        print(('The %s rating has been added for video ID %s.' %
            (args.rating, args.video_id)))
