"""Create a package-local token and temporary secret input, without printing it."""
from pathlib import Path
import secrets
ROOT = Path(__file__).resolve().parents[1]
env_path = ROOT / '.env'
if env_path.exists():
    raise SystemExit('Existing .env preserved; do not rotate a token implicitly')
token = secrets.token_urlsafe(48)
temporary = ROOT / '.build/deployment/token.txt'
temporary.parent.mkdir(parents=True, exist_ok=True)
with temporary.open('x', encoding='utf-8') as stream:
    stream.write(token)
with env_path.open('x', encoding='utf-8') as stream:
    stream.write('WORKBOOK_MCP_URL=\nWORKBOOK_MCP_API_TOKEN=' + token + '\n')
print('Package .env and temporary Secret Manager input created; token omitted.')
