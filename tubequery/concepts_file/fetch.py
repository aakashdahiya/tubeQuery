#not in use - just to see how we create chunks 

from youtube_transcript_api import YouTubeTranscriptApi

video_id='B92hd3ZTfZE'

ytt_instance=YouTubeTranscriptApi()
transcript=ytt_instance.fetch(video_id)
print("type", type(transcript))

chunks =[]
current_text=""
start_time=None
max_chunk=500


for snippet in transcript:
 
  if current_text=="":
    start_time=snippet.start
  
  current_text=current_text+" "+snippet.text
  
  if len(current_text)>=max_chunk:
    chunks.append({"start_time":start_time,"text":current_text,"end_time": snippet.start+snippet.duration})
    current_text=""
    start_time=None
  
if current_text!="":
  chunks.append({"start_time":start_time,"text":current_text,"end_time": transcript[-1].start+transcript[-1].duration})
  
print("Length of Chunks is ", len(chunks))

for i in chunks:
  print("\n\n",i)


