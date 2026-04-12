echo "Updating system..."
pacman -Syu --noconfirm
echo "Done[+]"
echo "Installing Python..."
pacman -S python --noconfirm
echo "Done[+]"

VENV_DIR=".venv"

echo "Cheking virtualenv..."

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv..."
  python -m venv "$VENV_DIR"
fi

if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  "$VENV_DIR/bin/pip" install -r requirements.txt
fi
echo ""
echo "Let's go!"
"$VENV_DIR/bin/python" script.vpy
