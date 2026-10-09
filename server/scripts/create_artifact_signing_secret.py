"""Create only a server-side download-signing secret, never a client API key."""

from pathlib import Path
import secrets

# Repository root .build/ is git-ignored private staging.
ROOT = Path(__file__).resolve().parents[2]
target = ROOT / ".build/deployment/artifact-signing-secret.txt"
target.parent.mkdir(parents=True, exist_ok=True)
with target.open("x", encoding="utf-8") as stream:
    stream.write(secrets.token_urlsafe(48))
print("Server signing-secret input created; its value was omitted. Store it as WORKBOOK_ARTIFACT_SIGNING_SECRET in Secret Manager.")
