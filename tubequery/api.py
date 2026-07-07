from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from summarize import generate_summary

from util import get_youtube_id
from chunker import fetch_transcript, build_chunks
from retrieval import embed_chunks, retrieve
from generate import generate_answer
from cache import load_from_cache, save_to_cache, show_all_cached_videos

from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
  video_url:str
  question: str

class SummarizeRequest(BaseModel):
    video_url: str



@app.get("/health")
def health_check():
  return {"status":"ok"}

@app.get("/cached_videos")
def cached_videos():
  videos=show_all_cached_videos()
  return {
    "cached_videos": videos,
    "count":len(videos)

  }





@app.post("/ask")
def ask(request: AskRequest):

  video_id=get_youtube_id(request.video_url)

  if video_id is None:
    raise HTTPException(status_code=400, detail="Invalid YouTube URL")


  chunks_with_embeddings=load_from_cache(video_id)

  if chunks_with_embeddings is None:
    try:
      transcript=fetch_transcript(video_id)
    except Exception as e:
      raise HTTPException(status_code=400,detail=f"could not fetch transcript: {str(e)}")
    
    chunks= build_chunks(transcript)
    chunks_with_embeddings=embed_chunks(chunks)
    save_to_cache(video_id,chunks_with_embeddings)
  

  retrieved= retrieve(request.question, chunks_with_embeddings, top_k=3)
  
  answer= generate_answer(request.question,retrieved)

  return{
    "video_id": video_id,
    "question": request.question,
    "answer": answer
  }

@app.post("/summarize")
def summarize(request: SummarizeRequest):
    video_id = get_youtube_id(request.video_url)
    
    if video_id is None:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Reuse cache — same chunks whether we're doing Q&A or summarizing
    chunks_with_embeddings = load_from_cache(video_id)
    
    if chunks_with_embeddings is None:
        try:
            transcript = fetch_transcript(video_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not fetch transcript: {str(e)}")
        
        chunks = build_chunks(transcript)
        chunks_with_embeddings = embed_chunks(chunks)
        save_to_cache(video_id, chunks_with_embeddings)
    
    # For summarization we don't need embeddings — just the chunks
    try:
        summary = generate_summary(chunks_with_embeddings)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "video_id": video_id,
        "summary": summary
    }