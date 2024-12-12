!ffmpeg -i $NEWS_URL -loglevel debug -vn -acodec copy -f wav pipe:1 2>ffmpeg.log | \
ffmpeg -y -i pipe:0 -ac 1 -ar 16000 -f s16le -acodec pcm_s16le pipe:1 2>>ffmpeg.log | \
pv -qL 32000 | websocat -v --no-close --binary $WEBSOCKET_URL >websocat.log 2>&1