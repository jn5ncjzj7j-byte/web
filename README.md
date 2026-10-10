
# Minecraft Bedrock Server Auto Update Checker

A simple Bash script that checks the Minecraft Bedrock Dedicated Server (BDS) download page every hour.

Designed for Android users running Ubuntu through Termux and PRoot-Distro.

## Features

- Automatically checks every hour.
- Displays detected Minecraft Bedrock version numbers.
- Runs inside Ubuntu on Termux.
- No PC required.
- Uses Bash and curl.
- Stop anytime with Ctrl+C.

## Requirements

- Termux
- Ubuntu installed through PRoot-Distro
- Internet connection
- curl, grep, and sort

## 1. Open Ubuntu

In Termux, run:

    proot-distro login ubuntu

## 2. Install dependencies

Inside Ubuntu, run:

    apt update
    apt install -y curl

## 3. Create the checker

Run:

    nano mc-update-check.sh

Paste this code:
    
#!/usr/bin/env bash

URL="https://www.minecraft.net/en-us/download/server/bedrock"
STATE="$HOME/.mc_bedrock_last_version"

while true; do
    echo
    echo "========================================"
    echo " Minecraft Bedrock Update Checker"
    echo "========================================"

    PAGE=$(curl -fsSL --max-time 30 \
        -A "Mozilla/5.0" "$URL" 2>/dev/null)

    if [ -z "$PAGE" ]; then
        echo "ERROR: Could not download the official page."
        echo "Check your internet connection and try again."
    else
        VERSION=$(printf '%s' "$PAGE" |
            grep -oE '26\.[0-9]+(\.[0-9]+)?' |
            sort -Vu |
            tail -n 1)

        if [ -z "$VERSION" ]; then
            echo "Could not detect a version."
            echo "The website format may have changed."
        else
            OLD=$(cat "$STATE" 2>/dev/null)

            echo "Detected version: $VERSION"

            if [ -z "$OLD" ]; then
                echo "$VERSION" > "$STATE"
                echo "Saved the first detected version."
            elif [ "$VERSION" != "$OLD" ]; then
                echo "Version changed: $OLD -> $VERSION"
                echo "$VERSION" > "$STATE"
            else
                echo "No detected version change."
            fi
        fi
    fi

    echo "Next check in 1 hour."
    sleep 3600
done


Save with Ctrl+O, press Enter, then Ctrl+X.

## 4. Run the checker

Make it executable:

    chmod +x mc-update-check.sh

Start it:

    ./mc-update-check.sh

The script checks the page and waits one hour before checking again.

Press Ctrl+C to stop it.

## Official Download Page

https://www.minecraft.net/en-us/download/server/bedrock

## Running Bedrock Dedicated Server

After extracting the official Linux server package, enter your server directory:

    cd serverfolder

Replace serverfolder with your actual directory name.

Launch it on a compatible ARM64 environment with Box64 and the required libraries:

    box64 ./bedrock_server

## Limitations

- This script searches the download page for version numbers beginning with 26.
- The detected version is not guaranteed to be the latest downloadable Linux BDS release.
- Mojang may change the website format.
- This is a checker, not a full automatic updater.
- It does not download updates, back up worlds, replace server files, or restart the server.

Always back up your worlds before updating.

## Disclaimer

Minecraft Bedrock Dedicated Server belongs to Mojang/Microsoft. This is an independent community project and is not affiliated with or endorsed by them.
