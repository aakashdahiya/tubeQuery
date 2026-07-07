#step 2- import the chunks and embed them


from sentence_transformers import SentenceTransformer
from sentence_transformers import util
from chunker import build_chunks, fetch_transcript
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-V2")


#adding embeding in the chunks list 
def embed_chunks(chunks):

  #all texts in the chunks
  texts=[e['text']for e in chunks]

  #embedding all the texts from the chunks
  embeds=model.encode(texts)

  for i in range(len(chunks)):
    chunks[i]["embedding"]=embeds[i]

  return chunks


def retrieve(question, chunks_with_embeddings, top_k=3):

  #embedding question
  question_embedding=model.encode(question)

  #creating an array of embedded chunks from the chunks with embeddeing list
  chunks_embedding=np.array([i["embedding"] for i in (chunks_with_embeddings) ])

  #computing similarities bw question and chunks embeddings
  calculate_similarities=util.cos_sim(question_embedding,chunks_embedding)

  score=calculate_similarities[0]

  #pair of chunks with its scores
  scored_chunks=[]

  for i in range(len(chunks_with_embeddings)):
    scored_chunks.append({
      "chunk":chunks_with_embeddings[i],
      "score":float(score[i])
    })
  
  scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    
  return scored_chunks[:top_k]



if __name__=="__main__":
  video_id = "kwEtOyaFhCA"
  transcript = fetch_transcript(video_id)
  chunks = build_chunks(transcript)
  chunks_with_embeddings = embed_chunks(chunks)


  question='what is the net worth of trump'
  results=retrieve(question,chunks_with_embeddings,top_k=3)


  for i in range(len(results)):
      r = results[i]
      print(f"\n--- Result {i+1} (score: {r['score']:.4f}) ---")
      print(f"Time: {r['chunk']['start_time']:.1f}s - {r['chunk']['end_time']:.1f}s")
      print(f"Text: {r['chunk']['text'][::]}...")


