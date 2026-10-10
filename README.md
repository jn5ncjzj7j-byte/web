
# Minecraft Bedrock Server Auto Update Checker

A simple Bash script for checking the latest Minecraft Bedrock Dedicated Server (BDS) release from Termux Ubuntu.

Designed for Android users running Ubuntu through PRoot-Distro and Box64.

## Features

- Checks for new stable Linux BDS releases.
- Checks automatically every hour.
- Remembers the last detected version.
- Shows when a new version is available.
- Does not require a PC.
- Does not modify your existing server files.

## Requirements

- Termux
- Ubuntu through PRoot-Distro
- Internet connection
- curl and jq

## 1. Open Ubuntu

In Termux, run:

    proot-distro login ubuntu

## 2. Install dependencies

Inside Ubuntu:

    apt update
    apt install -y curl jq

## 3. Create the checker

Run:

    nano mc-update-check.sh

Paste the following code:

    #!/usr/bin/env bash

    set -u

    API="https://raw.githubusercontent.com/Bedrock-OSS/BDS-Versions/main/versions.json"
    STATE="$HOME/.mc_bedrock_last_version"

    while true; do
        echo
        echo "========================================"
        echo " Minecraft Bedrock Update Checker"
        echo "========================================"

        DATA=$(curl -fsSL --max-time 30 "$API" 2>/dev/null || true)

        if [ -z "$DATA" ]; then
            echo "ERROR: Could not fetch version information."
            echo "Check your internet connection and try again."
        else
            VERSION=$(printf '%s' "$DATA" | jq -er '.linux.stable' 2>/dev/null || true)

            if [ -z "$VERSION" ] || [ "$VERSION" = "null" ]; then
                echo "ERROR: Could not read the latest stable version."
            else
                OLD=$(cat "$STATE" 2>/dev/null || true)

                echo "Latest stable Linux BDS: $VERSION"

                if [ -z "$OLD" ]; then
                    printf '%s\n' "$VERSION" > "$STATE"
                    echo "Saved the initial version."
                elif [ "$VERSION" != "$OLD" ]; then
                    echo "NEW VERSION DETECTED!"
                    echo "Previous: $OLD"
                    echo "Latest:   $VERSION"
                    printf '%s\n' "$VERSION" > "$STATE"
                else
                    echo "Your saved version matches the latest check."
                fi
            fi
        fi

        echo "Next check in 1 hour."
        sleep 3600
    done

Save with Ctrl+O, press Enter, then Ctrl+X.

## 4. Run the checker

    chmod +x mc-update-check.sh
    ./mc-update-check.sh

The script checks every hour. Press Ctrl+C to stop it.

## Official BDS Downloads

https://www.minecraft.net/en-us/download/server/bedrock

## Version Information Source

https://github.com/Bedrock-OSS/BDS-Versions

## Important

This script checks the latest stable Linux BDS version recorded by the community version archive. The archive may occasionally lag behind Mojang's release.

This is an update checker only. It does not download or install updates, back up worlds, or restart the server.

Always back up your worlds before updating server files.

## Disclaimer

Minecraft Bedrock Dedicated Server belongs to Mojang/Microsoft. This is an independent community project and is not affiliated with or endorsed by them.
