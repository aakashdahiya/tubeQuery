import os
import json
import numpy as np

CACHE_DIR="cache"

def save_to_cache(video_id,chunks_with_embeddings):
  #makeing sure that cache folder exists
  os.makedirs(CACHE_DIR,exist_ok=True)

  #convert each chunk's embedding from numpy to plain list
  serialization_chunks=[]

  for chunk in chunks_with_embeddings:

    serialization_chunks.append({
      "text":chunk["text"],
      "start_time":chunk['start_time'],
      "end_time":chunk["end_time"],
      "embedding":chunk["embedding"].tolist()
    })

  filepath=os.path.join(CACHE_DIR,f"{video_id}.json")

  #write to disk
  with open(filepath,'w') as f:
    json.dump(serialization_chunks,f)
  
  print(f"Cached {len(serialization_chunks)} chunks to {filepath}")


def load_from_cache(video_id):
  filepath= os.path.join(CACHE_DIR,f"{video_id}.json")

  #if no file exists return none
  if not os.path.exists(filepath):
    return None
  
  #read with File
  with open(filepath,"r") as f:
    cached_chunks=json.load(f)

  #convert embeddings back from list to numpy arrays

  for chunks in cached_chunks:
    chunks["embedding"]=np.array(chunks["embedding"],dtype=np.float32)
  
  print(f"Loaded {len(cached_chunks)} chunks from cache: {filepath}")

  return cached_chunks



    
#get a list of all the cached video
def show_all_cached_videos():
  
  if not os.path.exists(CACHE_DIR):
    return []


  files=os.listdir(CACHE_DIR)
  video_ids=[f.replace(".json","") for f in files]
  return video_ids


if __name__=="__main__":
  video=show_all_cached_videos()
  print(f"Found {len(video)} in cached video")
  for f in video:
    print(f" - {f}")
