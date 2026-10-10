Minecraft Bedrock Server Auto Update Checker

A simple Bash script that checks the Minecraft Bedrock Dedicated Server (BDS) download page every hour and reports detected version numbers.

Designed for Android users running Ubuntu through Termux and PRoot-Distro.

Features

* Checks every hour automatically.
* Reports detected Minecraft Bedrock version numbers.
* Runs inside Ubuntu on Termux.
* No PC required.
* Uses Bash and curl.
* Stops when you press Ctrl+C.

Requirements

* Termux
* Ubuntu installed through PRoot-Distro
* An internet connection
* curl, grep, and sort

1. Open Ubuntu

In Termux, run:

proot-distro login ubuntu

2. Install dependencies

Inside Ubuntu, run:

bash```
apt update
apt install -y curl
```

3. Create the checker script

Run:

bash```
nano mc-update-check.sh
```

Paste the following code:

bash```
#!/usr/bin/env bash
URL="https://www.minecraft.net/en-us/download/server/bedrock"
while true; do
    echo "========================================"
    echo "Checking Minecraft Bedrock updates..."
    echo "========================================"
    PAGE=$(curl -fsSL "$URL" 2>/dev/null)
    if [ -z "$PAGE" ]; then
        echo "Failed to access the official download page."
    else
        VERSION=$(printf '%s' "$PAGE" |
            grep -oE '26\.[0-9]+(\.[0-9]+)?' |
            sort -Vu |
            tail -n 1)
        if [ -n "$VERSION" ]; then
            echo "Latest version mentioned: $VERSION"
        else
            echo "Could not detect a version number."
        fi
    fi
    echo "Next check in 1 hour."
    sleep 3600
done
```

Save the file using Ctrl+O, press Enter, and exit with Ctrl+X.

4. Run the checker

Make the script executable:

bash```
chmod +x mc-update-check.sh
```

Start checking:

bash```
./mc-update-check.sh
```

Example output:

========================================
Checking Minecraft Bedrock updates...
========================================
Latest version mentioned: 26.x
Next check in 1 hour.

The example output is illustrative; the script prints whatever matching version number it detects.

Press Ctrl+C to stop the checker.

Important limitations

This is a basic page-based checker, not a verified latest-version detector. It only searches for version numbers beginning with 26. and selects the highest one found. It may report an outdated or unrelated version, miss future version formats, or fail when Mojang changes its website.

It does not automatically download or install updates, back up worlds, or restart the server.

Official download page:

https://www.minecraft.net/en-us/download/server/bedrock

Running the Bedrock server

After extracting the official Linux server package, enter your server directory:

cd serverfolder

Replace serverfolder with your actual directory name.

On a compatible ARM64 Ubuntu environment with Box64 and the required libraries installed, launch the server with:

bash```
box64 ./bedrock_server
```


Warning: Back up your worlds before updating server files. This checker does not modify your server installation.

Disclaimer

This is an independent community project and is not affiliated with Mojang or Microsoft. Minecraft Bedrock Dedicated Server is their software.
