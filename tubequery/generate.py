from anthropic import Anthropic
from dotenv import load_dotenv
from cache import load_from_cache, save_to_cache
from util import get_youtube_id

load_dotenv()
client=Anthropic()

def format_time(seconds):
  minutes=int(seconds//60)
  secs=int(seconds%60)
  return f"{minutes}:{secs:02d}"

def format_chunks_for_prompts(retrieved):
  parts=[]
  for i in range(len(retrieved)):
    chunks=retrieved[i]["chunk"]
    start=format_time(chunks['start_time'])
    end=format_time(chunks['end_time'])
    parts.append(f"[Excerpt {i+1},{start}-{end}]\n{chunks['text'].strip()}")
  return "\n\n".join(parts)

def generate_answer(question, retrieved_chunks):
  excerpts_text=format_chunks_for_prompts(retrieved_chunks)

  system_prompt=""" you are answering question about a youtube video using the provided youtube transcript excerpts 
  
  rules:
  - Use only information from the excerpts. Do not use general knowledge. 
  - If the answer is not in the excerpts, say "I could't find the in the video" - do not guess. 
  - When you answer, cite which excerpts by its timestemps, eg "(at 21:54)".
  - Be concise. Answer in 1-3 sentences unless more details needed
  
  """

  user_message= f"""Here are the relevant excerpts from the video {excerpts_text} 

  Question: {question}"""
  

  response=client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        system=system_prompt,
        messages=[
          {"role":"user","content":user_message}
        ]
      )

  return response.content[0].text



from retrieval import retrieve, embed_chunks 
from chunker import fetch_transcript, build_chunks

if __name__=="__main__":

  videourl=input("Enter video url")

  video_id=get_youtube_id(videourl)

  #tring to load from cache first
  chunks_with_embeddings=load_from_cache(video_id)

  if chunks_with_embeddings is None:
    #cache miss run the fill pipeline

    print("Fetching Transcript")
    transcript=fetch_transcript(video_id)

    print("Building Chunks...")
    chunks=build_chunks(transcript)

    print("Embedding Chunks..")
    chunks_with_embeddings=embed_chunks(chunks)

    save_to_cache(video_id,chunks_with_embeddings)

  continue_question="y"
  while continue_question=='y':
  
    question=input("What is your questions ")

    print("Retrieving relevant chunks...")
    retrieved=retrieve(question,chunks_with_embeddings,top_k=3)

    print("Generating answer...\n")

    answer=generate_answer(question,retrieved)

    print("="*60)
    print("Answer:")
    print("="*60)
    print(answer)
    print()

    continue_question=input("Enter 'y' to continue questioning: ")
