#!/usr/bin/env bash
set -e

spinner() {
  local pid=$1
  local msg="$2"
  local spin='|/-\'
  local i=0

  while kill -0 "$pid" 2>/dev/null; do
    i=$(( (i + 1) % 4 ))
    printf "\r%s %c" "$msg" "${spin:$i:1}"
    sleep 0.1
  done
}

clear

# ============================
# Display banner
# ============================
if [ -f "banner.txt" ]; then
  cat banner.txt
else
  echo "⚠️  banner.txt not found"
fi

# ============================
# Display info line
# ============================
DATE_NOW=$(date +"%Y-%m-%d %H:%M:%S")
USER_NOW=$(whoami)
HOST_NOW=$(hostname)

echo
echo "ℹ️  User: $USER_NOW | Host: $HOST_NOW | Date: $DATE_NOW"
echo "------------------------------------------------------------"
echo

# ============================
# Python checks
# ============================
PYTHON_BIN=$(command -v python3)

if [ -z "$PYTHON_BIN" ]; then
  echo "❌ python3 not found"
  exit 1
fi

PY_VERSION=$($PYTHON_BIN - << 'EOF'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
EOF
)

REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PY_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
  echo "❌ Python >= 3.9 required (found $PY_VERSION)"
  exit 1
fi

echo "✅ Python $PY_VERSION detected"

# ============================
# Install deps & run script
# ============================
echo
MSG="📦 Installing required Python packages :"
$PYTHON_BIN -m pip install --upgrade pip > /dev/null 2>&1
$PYTHON_BIN -m pip install numpy pandas > /dev/null 2>&1
SCRIPT_PID=$!

spinner $SCRIPT_PID "$MSG"

wait $SCRIPT_PID
printf "\r%s Done.\n" "$MSG"

MSG="🚀 Running database generation script :"

PYTHONUNBUFFERED=1 $PYTHON_BIN generate_db.py > /dev/null 2>&1 &
SCRIPT_PID=$!

spinner $SCRIPT_PID "$MSG"

wait $SCRIPT_PID
printf "\r%s Done.\n" "$MSG"

echo "🎉 Done."
