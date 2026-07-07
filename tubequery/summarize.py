import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def format_chunks_for_summary(chunks):
    parts = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        start = format_time(chunk["start_time"])
        end = format_time(chunk["end_time"])
        parts.append(f"[{start}-{end}] {chunk['text'].strip()}")
    return "\n\n".join(parts)


def generate_summary(chunks):
    excerpts_text = format_chunks_for_summary(chunks)
    
    system_prompt = """You are creating a structured educational summary of a YouTube video from its transcript.

Return valid JSON with this exact structure:
{
  "overview": "2-3 sentence high-level summary of what the video covers",
  "key_concepts": [
    {
      "concept": "Short name of the concept",
      "explanation": "1-2 sentence explanation",
      "timestamp": "MM:SS"
    }
  ],
  "main_takeaways": [
    "Actionable takeaway 1",
    "Actionable takeaway 2",
    "Actionable takeaway 3"
  ],
  "notable_quotes": [
    {
      "quote": "The direct quote from the video",
      "timestamp": "MM:SS"
    }
  ]
}

Rules:
- Include 3-6 key concepts. Pick the most important ones.
- Include 3-5 main takeaways.
- Include 2-4 notable quotes. Only include quotes that are genuinely striking or memorable.
- Every timestamp must match the format MM:SS (e.g., "5:32", "12:45").
- Use timestamps from the excerpt markers you see in the transcript.
- Return only the JSON. No preamble, no markdown, no explanation."""

    user_message = f"""Here is the full transcript of the video with timestamps:

{excerpts_text}

Generate the structured summary now."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "{"}
        ]
    )
    
    # Prefill was "{" so we prepend it to the response
    raw_json = "{" + response.content[0].text
    
    try:
        summary = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON: {str(e)}")
    
    return summary