#!/bin/bash
# save_github_token.sh - store the read-only GitHub token for the dashboard's GitHub card.
# Rob runs it himself, so the token never appears in chat:
#     ssh -t idsa-dify-syd 'bash ~/save_github_token.sh'
# What it does: asks for the token without showing it on screen, saves it to
# .github_traffic.key (only the ubuntu user can read it), then makes one test call to
# GitHub's traffic statistics and prints only the result code (200 = works).
set -euo pipefail
KEY=/home/ubuntu/idsa-dify-project/.github_traffic.key
read -r -s -p "Paste the GitHub token (nothing will show), then press Enter: " T; echo
[ -n "$T" ] || { echo "Nothing pasted; nothing saved."; exit 1; }
umask 077; printf '%s\n' "$T" > "$KEY"; chmod 600 "$KEY"; unset T
code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $(cat "$KEY")" \
  -H "Accept: application/vnd.github+json" -H "User-Agent: ardc-educator-dashboard" \
  https://api.github.com/repos/au-research/AI-educators/traffic/views)
case "$code" in
  200) echo "Saved and working (GitHub answered 200). You can close this window." ;;
  401) echo "Saved, but GitHub says the token is not valid (401). Check it was copied in full." ;;
  403) echo "Saved, but GitHub says the token lacks permission (403). It needs read access to the repository's administration/traffic." ;;
  *)   echo "Saved; GitHub answered $code. Tell Claude this number." ;;
esac
