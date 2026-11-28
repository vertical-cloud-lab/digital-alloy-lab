#!/usr/bin/env bash
# Install viewer.py as a systemd user service for the Pi's desktop user, so the unit's display shows its camera(s)
# from every boot on. Needs no root, installs no package and touches no system file: only files in ~/.config and
# ~/.local/share. Run it on the Pi, as the user the desktop logs in as, with viewer.py next to it:
#
#   bash install.sh                               # every camera found, side by side
#   bash install.sh --cameras imx477 imx708       # front unit: HQ on the left, Module 3 Wide on the right
#   bash install.sh --rotate 90                   # a panel mounted in portrait
#   bash install.sh --no-blanking ...             # also stop the desktop blanking the screen after 10 min idle
#   bash install.sh --uninstall
#
# Any other arguments go to viewer.py (python3 viewer.py --help). Running it again replaces the old settings.
# Afterwards:  systemctl --user status viewport-viewer    journalctl --user -u viewport-viewer -f
#              systemctl --user stop viewport-viewer       (frees the cameras until the next boot or start)
set -euo pipefail
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}   # an SSH session may not set it
NAME=viewport-viewer
DIR=$HOME/.local/share/$NAME
UNIT=$HOME/.config/systemd/user/$NAME.service
AUTOSTART=$HOME/.config/labwc/autostart   # raspi-config's screen-blanking switch is a swayidle line in here

if [ "${1:-}" = --uninstall ]; then
  systemctl --user disable --now $NAME.service 2>/dev/null || true
  rm -f "$UNIT"
  rm -rf "$DIR"
  systemctl --user daemon-reload
  echo "removed $NAME (screen blanking left as it is)"
  exit 0
fi

NO_BLANKING=0
ARGS=()
for a in "$@"; do
  if [ "$a" = --no-blanking ]; then NO_BLANKING=1; else ARGS+=("$a"); fi
done

SRC=${VIEWER_PY:-$(dirname "$0")/viewer.py}
[ -f "$SRC" ] || { echo "viewer.py isn't next to install.sh; set VIEWER_PY=/path/to/viewer.py" >&2; exit 1; }
for mod in picamera2 numpy; do
  python3 -c "import $mod" 2>/dev/null || { echo "python3 can't import $mod (python3-$mod on Raspberry Pi OS)" >&2; exit 1; }
done
python3 -c "import PyQt5.QtWidgets" 2>/dev/null || python3 -c "import PyQt6.QtWidgets" 2>/dev/null ||
  { echo "needs PyQt5 or PyQt6 (sudo apt install python3-pyqt5)" >&2; exit 1; }
# Check the arguments now rather than in a restart loop at boot.
python3 - "$SRC" "${ARGS[@]}" <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("viewer", sys.argv[1])
viewer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(viewer)
viewer.parse_args(sys.argv[2:])
EOF

mkdir -p "$DIR" "$(dirname "$UNIT")"
install -m 644 "$SRC" "$DIR/viewer.py"
EXEC=""
for a in "${ARGS[@]}"; do   # quote each argument for systemd: \ and " escaped, % and $ doubled
  a=${a//\\/\\\\}; a=${a//\"/\\\"}; a=${a//%/%%}; a=${a//\$/\$\$}
  EXEC+=" \"$a\""
done
cat > "$UNIT" <<EOF
[Unit]
Description=rePowder viewport cameras: full-screen live view on the unit's display
# Starts with the desktop user's session, which the Pi logs in to automatically at boot. viewer.py waits for the
# desktop to come up, and systemd starts it again if it exits (a camera unplugged, for example).

[Service]
ExecStart=/usr/bin/python3 -u %h/.local/share/$NAME/viewer.py$EXEC
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable $NAME.service
systemctl --user restart $NAME.service
echo "installed: $UNIT"
grep '^ExecStart' "$UNIT"

if [ -e "$AUTOSTART" ] && grep -q swayidle "$AUTOSTART"; then
  if [ $NO_BLANKING = 1 ]; then
    cp "$AUTOSTART" "$AUTOSTART.bak-$(date +%F)"
    sed -i '/swayidle/d' "$AUTOSTART"   # what raspi-config's "Screen Blanking: No" does to this file
    pkill -u "$(id -u)" -x swayidle || true   # and stop it for the current session
    echo "screen blanking: turned off (old file kept as $AUTOSTART.bak-$(date +%F))"
  else
    echo "screen blanking: ON, so the panel goes dark after 10 min without a key or touch;" \
         "rerun with --no-blanking to turn it off"
  fi
else
  echo "screen blanking: off"
fi
sleep 8
systemctl --user --no-pager --lines=0 status $NAME.service | head -5 || true
journalctl --user -u $NAME.service -n 12 --no-pager -o cat 2>/dev/null || echo "(no user journal; run viewer.py by hand to see its output)"
