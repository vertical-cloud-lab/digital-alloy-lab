#!/usr/bin/env bash
# Read-only report of a viewport-camera Pi's display, cameras and inputs. Changes nothing.
# Prints no hostname, user name or address, so the output can be committed.
# Run on the Pi:  bash probe.sh
export WAYLAND_DISPLAY=${WAYLAND_DISPLAY:-wayland-0} XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}
echo "== board";   tr -d '\0' < /proc/device-tree/model; echo; free -m | awk '/^Mem/{print "RAM " $2 " MB"}'
echo "== os";      . /etc/os-release; echo "$PRETTY_NAME, kernel $(uname -r)"
echo "== desktop"; systemctl get-default; pgrep -x labwc >/dev/null && echo "labwc running" || echo "no labwc"
echo "== hdmi connectors"
for c in /sys/class/drm/card*-HDMI-A-*; do
  echo "$(basename $c): $(cat $c/status), EDID $(wc -c < $c/edid) bytes, modes: $(sort -u $c/modes | tr '\n' ' ')"
done
echo "== active mode (KMS)"; kmsprint 2>/dev/null | grep -E "^Connector|Crtc" | sed 's/^ *//'
echo "== active mode (Wayland)"; wlr-randr 2>/dev/null | grep -E "^[A-Z]|current"
echo "== cameras"; rpicam-hello --list-cameras 2>&1 | grep -vE "^\[" | head -8
echo "== usb";     lsusb | grep -v "root hub" || echo "no USB devices (so no USB touch controller)"
echo "== input";   grep -E "^N:" /proc/bus/input/devices | cut -d'"' -f2
echo "== boot config (display lines)"; grep -nE "^\s*(dtoverlay|display_|hdmi|max_framebuffers|disable_fw_kms)" /boot/firmware/config.txt
tr ' ' '\n' < /proc/cmdline | grep -E "^video=" || echo "no video= on the kernel command line"
echo "== temperature"; vcgencmd measure_temp; vcgencmd get_throttled
