import os
import sqlite3
from datetime import datetime
import traceback

# Configurable paths via environment variables with fallback defaults
DB_PATH = os.getenv('NAVIDROME_DB_PATH', './navidrome.db')
OUTPUT_HTML = os.getenv('OUTPUT_HTML_PATH', './public/index.html')

def get_all_users():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def get_aggregated_scrobbles(user_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                m.title, 
                m.artist, 
                COUNT(*) AS play_count, 
                MAX(s.submission_time) AS last_played 
            FROM scrobbles s 
            JOIN media_file m ON s.media_file_id = m.id 
            JOIN user u ON s.user_id = u.id 
            WHERE u.name = ?
            GROUP BY m.title, m.artist
            ORDER BY play_count DESC, last_played DESC, m.artist ASC
        """, (user_name,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching scrobbles for {user_name}: {e}")
        return []

def generate_html():
    print("Fetching users from Navidrome DB...")
    users = get_all_users()
    print(f"Found users: {users}")
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Listening Dashboard - All-Time Top Tracks</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #121212; color: #e0e0e0; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #fff; margin-bottom: 30px; }
        .container { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; max-width: 1800px; margin: 0 auto; }
        .card { background: #1e1e1e; border-radius: 10px; padding: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); }
        h2 { border-bottom: 2px solid #333; padding-bottom: 10px; color: #bb86fc; margin-top: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #2c2c2c; font-size: 14px; }
        th { color: #888; font-weight: 600; }
        .time { color: #888; font-size: 12px; white-space: nowrap; }
        .plays { text-align: center; font-weight: bold; color: #03dac6; }
        .count { font-size: 13px; color: #aaa; margin-bottom: 15px; }
        @media (max-width: 600px) {
            body { padding: 10px; }
            .container { grid-template-columns: 1fr; }
            .card { padding: 15px; }
        }
    </style>
</head>
<body>
    <h1>All-Time Top Tracks & History</h1>
    <div class="container">
"""

    for user in users:
        print(f"Processing scrobbles for {user}...")
        rows = get_aggregated_scrobbles(user)
        html_content += f"""
        <div class="card">
            <h2>{user}</h2>
            <div class="count">Unique tracks played: {len(rows)}</div>
            <table>
                <tr><th>Track</th><th>Artist</th><th class="plays">Plays</th><th class="time">Last Played</th></tr>
"""
        for title, artist, play_count, last_played in rows:
            try:
                dt = datetime.fromtimestamp(int(last_played)).strftime('%Y-%m-%d %H:%M')
            except:
                dt = str(last_played)
            html_content += f"<tr><td>{title}</td><td>{artist}</td><td class=\"plays\">{play_count}</td><td class=\"time\">{dt}</td></tr>\n"
        
        html_content += """
            </table>
        </div>
"""

    html_content += """
    </div>
</body>
</html>
"""

    print(f"Writing HTML to {OUTPUT_HTML}...")
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html_content)
    print("Dashboard HTML generated successfully for all users.")

if __name__ == '__main__':
    try:
        print("Starting script execution...")
        generate_html()
    except Exception as e:
        print("An error occurred during execution:")
        traceback.print_exc()