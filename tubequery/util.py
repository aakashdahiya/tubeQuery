from urllib.parse import urlparse, parse_qs
import re

def get_youtube_id(url):
    # Standardize format by stripping whitespaces and trailing slashes
    url = url.strip().rstrip('/')
    
    # Method 1: Use urllib for standard and short URLs
    parsed = urlparse(url)
    
    # Handle short links (youtu.be/VIDEO_ID)
    if parsed.netloc == 'youtu.be':
        return parsed.path.lstrip('/')
        
    # Handle standard desktop/mobile links (://youtube.com)
    if 'youtube.com' in parsed.netloc and parsed.path == '/watch':
        query = parse_qs(parsed.query)
        if 'v' in query:
            return query['v'][0]
            
    # Method 2: Use RegEx for Shorts, Embeds, Live, and edge cases
    # Matches /v/, /embed/, /shorts/, /live/ followed by 11 valid characters
    regex_pattern = r'(?:v|embed|shorts|live)\/([a-zA-Z0-9_-]{11})'
    match = re.search(regex_pattern, url)
    if match:
        return match.group(1)
        
    return None













# --- Test cases demonstrating accuracy ---


if __name__=="__main__":
    video_id=get_youtube_id('https://www.youtube.com/watch?v=OLUWpt64GMc&list=RDOLUWpt64GMc&start_radio=1')

    print(video_id)