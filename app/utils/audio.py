import ffmpeg

async def get_audio_duration(file_url: str) -> str:
    """Extracts duration from an audio file hosted on Azure Blob Storage."""
    try:
        probe = ffmpeg.probe(file_url, v="error", select_streams="a:0", show_entries="format=duration")
        duration = float(probe["format"]["duration"])

        minutes = int(duration // 60)
        seconds = int(duration % 60)

        return f"{minutes:02}:{seconds:02}"  # MM:SS format

    except Exception as e:
        print(f"Error extracting duration: {str(e)}")
        return "00:00"  # Default value in case of an error