import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def download_videos(singer_name, n):
    print(f"Searching and downloading {n} videos for '{singer_name}'...")
    
    ydl_opts = {
        # THE FIX: Request a combined video file to bypass the audio SABR blocks
        'format': 'best', 
        'extractor_args': {
            'youtube': {
                'player_client': ['default,-tv,web_safari,web_embedded']
            }
        }, 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_audio_%(autonumber)s.%(ext)s',
        'default_search': 'ytsearch',
        'quiet': True,
        'extract_audio': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{n}:{singer_name} audio"])
        print("Download complete.")
    except Exception as e:
        print(f"Error during download: {e}")
        sys.exit(1)

def process_and_merge_audio(duration, output_filename):
    print(f"Trimming first {duration} seconds and merging...")
    combined_audio = AudioSegment.empty()
    
    files = [f for f in os.listdir('.') if f.startswith('temp_audio_') and f.endswith('.mp3')]
    
    if not files:
        print("No audio files found. Download may have failed.")
        sys.exit(1)
        
    for file in files:
        try:
            audio = AudioSegment.from_file(file, format="mp3")
            combined_audio += audio[:duration * 1000] 
        except Exception as e:
            print(f"Error processing {file}: {e}")
        finally:
            if os.path.exists(file):
                os.remove(file)
            
    try:
        combined_audio.export(output_filename, format="mp3")
        print(f"Successfully created mashup: {output_filename}")
    except Exception as e:
        print(f"Error saving final output: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer_name = sys.argv[1]
    
    try:
        n = int(sys.argv[2])
        y = int(sys.argv[3])
        output_filename = sys.argv[4]
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be valid integers.")
        sys.exit(1)

    download_videos(singer_name, n)
    process_and_merge_audio(y, output_filename)

if __name__ == "__main__":
    main()
