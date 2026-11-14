#!/usr/bin/env bash
# Display and encode load test for a viewport-camera Pi, with synthetic video (no camera needed).
# Run on the Pi, inside the desktop session's environment:
#   WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/$(id -u) bash bench.sh [seconds]
set -u
# Every background process gets its own stdout (/dev/null). One that inherits the $(...) pipe
# keeps the command substitution open until it exits, and ffplay never exits on its own.
T=${1:-30}
W=/tmp/vpd/bench; mkdir -p $W; cd $W
HZ=$(getconf CLK_TCK)
cpu_total() { awk '/^cpu /{print $2+$3+$4+$5+$6+$7+$8+$9, $5+$6}' /proc/stat; }   # total, idle+iowait
proc_ticks() { local s=0; for p in "$@"; do [ -r /proc/$p/stat ] && s=$((s + $(awk '{print $14+$15+$16+$17}' /proc/$p/stat))); done; echo $s; }

# Two synthetic "camera" feeds side by side, 400 x 300 each, 30 fps, shown full screen.
DISPLAY_GRAPH="testsrc2=s=400x300:r=30[a];testsrc2=s=400x300:r=30,hue=h=90[b];[a][b]hstack,pad=800:480:0:90[out0]"
ENC() {  # $1 = preset, $2 = tag ; 1080p30 synthetic source paced in real time, x264 to null
  ffmpeg -hide_banner -nostdin -loglevel error -stats -re -f lavfi -i "testsrc2=s=1920x1080:r=30" -t $T \
    -c:v libx264 -preset $1 -tune zerolatency -b:v 4M -maxrate 4M -bufsize 8M -g 60 -pix_fmt yuv420p -f null - > /dev/null 2> enc_$2.log &
  echo $!
}
SRC() {  # the 1080p30 synthetic source alone, no encode: its cost is part of every ENC figure
  ffmpeg -hide_banner -nostdin -loglevel error -stats -re -f lavfi -i "testsrc2=s=1920x1080:r=30" -t $T -f rawvideo -y /dev/null > /dev/null 2> enc_$1.log &
  echo $!
}
SHOW() {
  ffplay -hide_banner -fs -noborder -an -f lavfi -i "$DISPLAY_GRAPH" > /dev/null 2> show_$1.log &
  echo $!
}
run() {  # name, then commands that print PIDs
  local name=$1; shift
  local pids=""
  for c in "$@"; do pids="$pids $($c)"; done
  sleep 3
  read t0 i0 < <(cpu_total); p0=$(proc_ticks $pids); s0=$(date +%s.%N)
  sleep $((T - 6))
  read t1 i1 < <(cpu_total); p1=$(proc_ticks $pids); s1=$(date +%s.%N)
  temp=$(vcgencmd measure_temp | cut -d= -f2); thr=$(vcgencmd get_throttled | cut -d= -f2)
  if [ -n "${GRAB:-}" ]; then grim -o HDMI-A-2 grab_$name.png 2>/dev/null; fi
  sleep 4
  for p in $pids; do kill $p 2>/dev/null; done; wait 2>/dev/null
  awk -v n=$name -v t0=$t0 -v t1=$t1 -v i0=$i0 -v i1=$i1 -v p0=$p0 -v p1=$p1 -v s0=$s0 -v s1=$s1 -v hz=$HZ -v temp=$temp -v thr=$thr \
    'BEGIN{busy=100*(1-(i1-i0)/(t1-t0)); pc=100*(p1-p0)/hz/(s1-s0); printf "%-22s system CPU %5.1f%% of 4 cores | test processes %6.1f%% of one core | %s | throttled=%s\n", n, busy, pc, temp, thr}'
  for f in enc_*.log show_*.log; do [ -s $f ] || continue
    printf "    %-18s %s\n" $f "$(tr '\r' '\n' < $f | grep -E 'fps=|fd=' | tail -1 | sed -E 's/ +/ /g')"; done
  rm -f enc_*.log show_*.log
}
echo "idle: $(cat /proc/loadavg) $(vcgencmd measure_temp) $(vcgencmd get_throttled)"
run show_only        "SHOW a"
run src_1080p_only   "SRC s"
run enc1_ultrafast   "ENC ultrafast u1"
run enc2_ultrafast   "ENC ultrafast u1" "ENC ultrafast u2"
run enc2_veryfast    "ENC veryfast v1"  "ENC veryfast v2"
GRAB=1 run enc2_ultrafast_show "ENC ultrafast u1" "ENC ultrafast u2" "SHOW a"
free -m | head -2
