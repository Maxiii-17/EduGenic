"""Vercel serverless entrypoint: exposes the FastAPI app via Mangum."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app  # noqa: E402
from mangum import Mangum  # noqa: E402

handler = Mangum(app)
