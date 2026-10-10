Bro, on Termux or Linux, you can automatically check the latest Minecraft version using Mojang’s official version manifest. No PC or Box64 needed just to check the version.

There are two ways:

* One-time check: print the latest release version.
* Auto-check: check periodically and notify you when a new release comes out.

1. Check the latest Minecraft Java version

Run this directly in Termux:

pkg install curl jq -y
curl -s https://piston-meta.mojang.com/mc/game/version_manifest_v2.json | jq -r '.latest.release'

Example output:

26.2

That is an example only; your command will show the version currently listed by Mojang.

2. Automatically check for new releases

This script checks every hour and prints a message only when the latest release changes.

Create the script:

nano mc-version-check.sh

Paste this code:

#!/data/data/com.termux/files/usr/bin/bash
URL="https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
FILE="$HOME/.mc_latest_version"
while true; do
    LATEST=$(curl -fsSL "$URL" | jq -r '.latest.release')
    if [ -n "$LATEST" ] && [ "$LATEST" != "null" ]; then
        OLD=$(cat "$FILE" 2>/dev/null)
        if [ "$LATEST" != "$OLD" ]; then
            echo "Minecraft release: $LATEST"
            if [ -n "$OLD" ]; then
                echo "New version detected: $OLD -> $LATEST"
            fi
            echo "$LATEST" > "$FILE"
        else
            echo "No update. Latest: $LATEST"
        fi
    else
        echo "Failed to check Minecraft version."
    fi
    sleep 3600
done

Save in nano with Ctrl+O, Enter, then Ctrl+X.

Run it:

bash```
chmod +x mc-version-check.sh
./mc-version-check.sh
```
* Checks once per hour.
* Remembers the last version in ~/.mc_latest_version.
* Detects when Mojang publishes a newer release.
* Keeps running until you press Ctrl+C.

The script checks Minecraft Java Edition’s latest stable release, not snapshots.

Note: Termux must remain running for this loop to continue reliably. If you meant Minecraft Bedrock Dedicated Server (BDS) instead of Java Edition, tell me—that uses a different version-checking method.
