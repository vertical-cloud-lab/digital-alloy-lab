#!/bin/sh
# Navigate the headed Chrome on :99 by typing a URL into the address bar (real X keyboard input).
# usage: xnav.sh URL WAIT_SECONDS
export DISPLAY=:99
WID=$(xdotool search --onlyvisible --class "google-chrome" | head -1)
xdotool windowactivate --sync "$WID" 2>/dev/null
xdotool mousemove --sync $((600 + $(od -An -N1 -tu1 /dev/urandom))) $((400 + $(od -An -N1 -tu1 /dev/urandom)))
xdotool key --clearmodifiers ctrl+l
python3 -c "import time; time.sleep(0.4)"
printf '%s' "$1" | xdotool type --delay 25 --file -
xdotool key Return
python3 -c "import time,sys; time.sleep(float(sys.argv[1]))" "${2:-7}"
# a few wheel scrolls, as a reader would
for i in 1 2 3 4; do xdotool click 5; python3 -c "import time,random; time.sleep(random.uniform(0.2,0.6))"; done
