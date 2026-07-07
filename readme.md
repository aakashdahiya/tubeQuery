TubeQuery is a RAG web application. It take a youtbe video link and a question related to the video as an iput from the user, and responds back with a answer to that question as is presented in the video. The answer is presented in a casual manner and comes with the video time stemp. If the answer is not present in the video the app simply tells that it can't find an answer to the question in that video.

To Run the app:

- simply open the tubequery in an IDE, and create/open a virtual environment
- In the root folder, run the command: npm install, it will install all the dependencies
- Run the uvicorn app using this command: python -m uvicorn api:app --reload
- Open the index.html file in a browser
- The app is now runing in your browser

About the funcationality:

- We first fetch the video transcript using the YouTubeTranscriptApi
- Once we have the transcript we build chunks from that transcript
- We then embed the transcript chunks along with the inputed question
- After that we compute the similarities between the question and transcript chunks, and sort them.
- We are also caching the videos so that we are not repetedly embedding the same videos
- There is a generate.py file which generates the answers usign the claud api. We have a system prompt and a user message defined here.
