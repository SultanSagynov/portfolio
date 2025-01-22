import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def extract_video_id(url):
    # Regex to extract video ID from a YouTube URL
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def fetch_transcripts_from_urls(video_urls):
    data = []
    for url in video_urls:
        video_id = extract_video_id(url)
        if not video_id:
            print(f"Invalid URL: {url}")
            continue

        try:
            # Fetch the transcript in Russian
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ru'])
            formatter = TextFormatter()
            formatted_text = formatter.format_transcript(transcript)
            
            data.append({
                'video_url': url,
                'video_id': video_id,
                'transcript': formatted_text
            })
            print(f"Fetched transcript for video: {url}")
        except Exception as e:
            print(f"Failed to fetch transcript for video: {url}, Error: {e}")
    return data

def save_to_csv(data, file_name="russian_youtube_transcripts.csv"):
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Transcripts saved to {file_name}")

# List of YouTube video URLs
video_urls = [
    'https://www.youtube.com/watch?v=BjP1F7A5LBw&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=1',
    'https://www.youtube.com/watch?v=BjP1F7A5LBw&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=1',
    'https://www.youtube.com/watch?v=2xitKOwLT8w&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=2',
    'https://www.youtube.com/watch?v=F263-BPtVyE&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=3',
    'https://www.youtube.com/watch?v=Xj9wXnvd90w&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=4',
    'https://www.youtube.com/watch?v=Qz7hhTi-3cY&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=5',
    'https://www.youtube.com/watch?v=FqpVw2HP_GU&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=6',
    'https://www.youtube.com/watch?v=FG519L7Gn0Q&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=7',
    'https://www.youtube.com/watch?v=3f33oyUhwko&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=8',
    'https://www.youtube.com/watch?v=HjNvpfrxHNg&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=9',
    'https://www.youtube.com/watch?v=SwM4aCYWMH8&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=10',
    'https://www.youtube.com/watch?v=dhAZTrxiNVc&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=11',
    'https://www.youtube.com/watch?v=1qOGEE6ieBI&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=12',
    'https://www.youtube.com/watch?v=KFpErnoLnvM&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=13',
    'https://www.youtube.com/watch?v=UPnadsWP10A&list=PL1mxkDJa7Zy479R1dZkYhKKtDijx20mPU&index=14',
    'https://www.youtube.com/watch?v=BlFU_tP8C_w,'
    # Add more URLs here
]

# Fetch and save transcripts
transcripts_data = fetch_transcripts_from_urls(video_urls)
save_to_csv(transcripts_data)
