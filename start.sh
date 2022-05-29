PORT=${1:-8080}
WORKERS=${2:-2}
gunicorn -w $WORKERS -b 0.0.0.0:$PORT src.server:app