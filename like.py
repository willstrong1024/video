#!/usr/bin/python3

import argparse
import os
import re

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRETS_FILE = 'config/client_secrets.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

RATINGS = ('like', 'dislike', 'none')

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def like_video(youtube, args):
  youtube.videos().rate(
    id=args.video_id,
    rating=args.rating
  ).execute()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--video-id', required=True, help='ID of video to like.')
  parser.add_argument('--rating', default='like',
    choices=RATINGS,
    help='Indicates whether the rating is "like", "dislike", or "none".')
  args = parser.parse_args()

  youtube = get_authenticated_service()
  try:
    like_video(youtube, args)
  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
  else:
    print(('The %s rating has been added for video ID %s.' %
           (args.rating, args.video_id)))
