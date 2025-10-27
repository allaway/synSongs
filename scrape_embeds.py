import csv
import requests
import re
import time
from urllib.parse import urlparse

def extract_embed_id(song_url):
    """Extract embed ID from Suno song page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(song_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Look for the embed ID in the page
        # The page typically has: data-track-id="embed-uuid" or similar patterns
        patterns = [
            r'"id":"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
            r'embed/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})',
            r'"trackId":"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
            r'data-track-id="([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                embed_id = match.group(1)
                print(f"✓ Found embed ID: {embed_id}")
                return embed_id
        
        print(f"✗ Could not find embed ID in page")
        return None
    except Exception as e:
        print(f"✗ Error fetching {song_url}: {e}")
        return None

def generate_embed_html(embed_id):
    """Generate the embed HTML code"""
    return f'<iframe src="https://suno.com/embed/{embed_id}" width="760" height="240"><a href="https://suno.com/song/{embed_id}">Listen on Suno</a></iframe>'

def update_csv():
    """Update CSV with embed codes"""
    rows = []
    updated_count = 0
    
    # Read existing CSV
    with open('songz.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        
        for i, row in enumerate(reader, 2):
            doc_url = row[0] if len(row) > 0 else ''
            song_url = row[1] if len(row) > 1 else ''
            embed = row[2] if len(row) > 2 else ''
            
            # If we have a song_url but no embed, try to scrape it
            if song_url and not embed:
                print(f"\n[Line {i}] Processing: {doc_url}")
                embed_id = extract_embed_id(song_url)
                
                if embed_id:
                    embed = generate_embed_html(embed_id)
                    updated_count += 1
                    time.sleep(1)  # Rate limiting
            
            rows.append([doc_url, song_url, embed])
    
    # Write updated CSV
    with open('songz.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"\n\n✓ Updated CSV with {updated_count} new embed codes")

if __name__ == '__main__':
    print("Starting Suno embed scraper...")
    update_csv()
