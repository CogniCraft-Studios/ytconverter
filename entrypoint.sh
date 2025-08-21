#!/bin/sh
set -e

if [ -n "$YT2MP3COOKIES_TXT_B64" ]; then
  echo "$YT2MP3COOKIES_TXT_B64" | base64 -d > /cookies/cookies.txt
  chmod 600 /cookies/cookies.txt
fi

exec "$@"
