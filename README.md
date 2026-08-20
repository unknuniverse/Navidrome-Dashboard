# Navidrome Dashboard
A lightweight, self-hosted multi-user dashboard for Navidrome.  
**Aggregates play counts, filters duplicates, sorts your top tracks, and serves a clean, mobile-responsive HTML page via Nginx.**

## Features
- 🕒 **All-Time Stats**: Aggregates total play counts and tracks the most recent timestamp for every song played.
- 👥 **Multi-User Support**: Automatically detects all registered Navidrome users and creates individual cards for each.
- 🧠 **Smart Sorting**: Ordered by total plays (descending), then last played date, then alphabetically by artist name.
- 📱 **Fully Responsive**: Adapts cleanly to wide desktop screens and stacks vertically on mobile devices.
- ⚡ **Zero Heavy Dependencies**: Runs entirely via standard Python libraries and a lightweight Nginx container.

## Setup & Instructions

### 1. Repository Structure
Ensure you have your project directory set up with your two files:<br>

your-dashboard-folder/<br>
├── dashboard.py<br>
└── docker-compose.yml

And make sure you have an empty public directory for the generated HTML output:
`mkdir -p public`

### 2. Generate the Dashboard HTML
You can run the Python script on-demand using a temporary Python container. 

Mount your project folder to /app and your Navidrome data directory to /nddata:<br>

`docker run --rm -v $(pwd):/app -v /path/to/your/navidrome/data:/nddata -e NAVIDROME_DB_PATH="/nddata/navidrome.db" -e OUTPUT_HTML_PATH="/app/public/index.html" python:3.11-slim python /app/dashboard.py`

### 3. Start the Web Server
Spin up the Nginx container using Docker Compose:
`docker compose up -d`

You can now view your dashboard in your browser at `http://<your-server-ip>:8081`.

### Automation (Crontab)
To keep the dashboard updated automatically, you can add a cron job on your host machine to regenerate the HTML page once a day at midnight.

Open your crontab editor:
`crontab -e`

Add the following line (making sure to replace `/home/username/dashboard` with your absolute project path and `/path/to/your/navidrome/data` with your actual Navidrome data path):

`0 0 * * * docker run --rm -v /home/username/dashboard:/app -v /path/to/your/navidrome/data:/nddata -e NAVIDROME_DB_PATH="/nddata/navidrome.db" -e OUTPUT_HTML_PATH="/app/public/index.html" python:3.11-slim python /app/dashboard.py`

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/theunknownuniverse)

https://unknownuniverse.uk/