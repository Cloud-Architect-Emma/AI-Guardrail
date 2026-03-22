import os, pathlib, sys
from openai import OpenAI

api_key = os.environ["MODEL_API_KEY"]

client = OpenAI(api_key=api_key)

extensions = {".kt", ".java", ".xml", ".json", ".md", ".txt", ".yaml", ".yml"}
files = [p for p in pathlib.Path(".").rglob("*") if p.suffix in extensions and ".git" not in p.parts]

if not files:
    print("No files to scan.")
    pathlib.Path(".scan-result").write_text("PASS")
    sys.exit(0)

combined = ""
for f in files[:20]:
    try:
        combined += f"\n\n--- {f} ---\n" + f.read_text(errors="ignore")
    except Exception:
        pass

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[
        {"role": "system",
         "content": "You are a mobile-app code reviewer. Scan for secrets, PII, or policy violations. Reply with PASS or FAIL."},
        {"role": "user", "content": combined}
    ]
)

result = response.choices[0].message.content
print(result)
pathlib.Path(".scan-result").write_text(result)
if result.strip().upper().startswith("FAIL"):
    sys.exit(1)
