echo "Updating system..."
pacman -Syu --noconfirm
echo "Done[+]"
echo "Installig Python..."
pacman -S --noconfirm
echo "Done[+]"

VENV_DIR=".venv"

echo "Cheking virtualenv..."

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv..."
  python3 -m venv "$VENV_DIR"
fi

if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  "$VENV_DIR/bin/pip" install -r requirements.txt
fi
echo ""
echo "Let,go!"
"$VENV_DIR/bin/python" script.py
