#!/usr/bin/env bash
# Put a deck on a live URL that works on any device.
#
# Usage:
#   bash scripts/deploy.sh my-deck.html          # a single file
#   bash scripts/deploy.sh ./my-deck/            # a folder, if it has images
#
# Uses Vercel's free tier. The link stays up until the user deletes it from
# their dashboard.

set -euo pipefail

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
    echo "Usage: bash scripts/deploy.sh <deck.html | folder/>"
    exit 1
fi

if [[ ! -e "$TARGET" ]]; then
    echo "No such file or folder: $TARGET"
    exit 1
fi

# --- Prerequisites --------------------------------------------------------
if ! command -v npx >/dev/null 2>&1; then
    cat <<'MSG'
Node is not installed, and Vercel's CLI needs it.

  macOS:    brew install node
  Windows:  winget install OpenJS.NodeJS
  Other:    https://nodejs.org

Then run this again.
MSG
    exit 1
fi

if ! npx --yes vercel whoami >/dev/null 2>&1; then
    cat <<'MSG'
Not signed in to Vercel yet. It is free and takes a minute:

  1. Go to https://vercel.com/signup and sign up with GitHub, Google or email
  2. Run:  npx vercel login
  3. Follow the prompt, which opens a browser to authorise
  4. Then run this script again

MSG
    exit 1
fi

# --- Assemble a deploy folder --------------------------------------------
# A folder is deployed as-is, which is the reliable path when a deck has
# images. A single file gets a temporary folder with any assets it references.
TMP=""
cleanup() { [[ -n "$TMP" && -d "$TMP" ]] && rm -rf "$TMP"; }
trap cleanup EXIT

if [[ -d "$TARGET" ]]; then
    DEPLOY_DIR="$TARGET"
    if [[ ! -f "$DEPLOY_DIR/index.html" ]]; then
        HTML_COUNT=$(find "$DEPLOY_DIR" -maxdepth 1 -name '*.html' | wc -l | tr -d ' ')
        if [[ "$HTML_COUNT" == "1" ]]; then
            echo "No index.html. Copying the single HTML file to index.html."
            TMP=$(mktemp -d)
            cp -R "$DEPLOY_DIR"/. "$TMP"/
            mv "$TMP"/*.html "$TMP/index.html"
            DEPLOY_DIR="$TMP"
        else
            echo "Folder needs an index.html. Rename the main deck file."
            exit 1
        fi
    fi
else
    TMP=$(mktemp -d)
    cp "$TARGET" "$TMP/index.html"

    SRC_DIR=$(dirname "$TARGET")

    # Pull in anything referenced by src=, href= or url() with a relative path.
    # Missing an asset here is the usual cause of a deployed deck with broken
    # images, so this looks at CSS url() too, not just src attributes.
    grep -oE '(src|href)="[^"]+"|url\((["'"'"']?)[^)"'"'"']+\1\)' "$TARGET" 2>/dev/null \
        | sed -E 's/^(src|href)="//; s/^url\(["'"'"']?//; s/["'"'"']?\)$//; s/"$//' \
        | grep -vE '^(https?:|data:|#|/)' \
        | sort -u \
        | while read -r ASSET; do
            [[ -z "$ASSET" ]] && continue
            if [[ -f "$SRC_DIR/$ASSET" ]]; then
                mkdir -p "$TMP/$(dirname "$ASSET")"
                cp "$SRC_DIR/$ASSET" "$TMP/$ASSET"
                echo "  bundled $ASSET"
            fi
        done

    DEPLOY_DIR="$TMP"
fi

# --- Deploy ---------------------------------------------------------------
echo ""
echo "Deploying..."
npx --yes vercel deploy --prod --yes "$DEPLOY_DIR"

cat <<'MSG'

Done. Things to pass on to the user:

  - The link works on any device. Text it, Slack it, email it.
  - Running this again on the same deck updates the same URL. No new link.
  - To take it down: https://vercel.com/dashboard, then delete the project.
  - The free tier is generous. They will not be charged.

Open the link and check the images actually load before telling them it is
ready. If any are broken, put the deck and its assets in one folder and deploy
the folder instead.
MSG
