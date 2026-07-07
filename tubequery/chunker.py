#step1 imports video script and the build chunks function returns chunks of the video

from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_id):
    ytt_api=YouTubeTranscriptApi()
    fetched_transcript=ytt_api.fetch(video_id)
    return fetched_transcript


def build_chunks(fetched_transcript, max_length=500):

    current_state=''
    chunks= []

    for snippet in fetched_transcript:
        if current_state != '' and len(current_state) + len(snippet.text) + 1 > max_length:
            chunks.append({"text":current_state,"start_time":start_time, "end_time":end_time})      
            current_state=''
            start_time=None

        if current_state=='':
            start_time=snippet.start

        current_state=current_state+" "+snippet.text
        end_time = snippet.start + snippet.duration  
        
    if current_state != '':
        chunks.append({
            "text": current_state,
            "start_time": start_time,
            "end_time": end_time
        })

    return chunks



if __name__=="__main__":

    video_id="StjGg6CecSc"


    fetched_transcript = fetch_transcript(video_id)
    chunks = build_chunks(fetched_transcript)

    print(f"Created {len(chunks)} chunks")
    print(f"Last chunk: {chunks[-1]}")




                                                                                                                         












