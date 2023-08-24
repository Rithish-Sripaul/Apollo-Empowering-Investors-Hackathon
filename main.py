import time 
import tkinter as tk
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from selenium import webdriver
driver = webdriver.Chrome(executable_path='./chromedriver')

driver.get('http://www.google.com/');
curr_url = ""
summarizer = pipeline('summarization' ,model="sshleifer/distilbart-cnn-12-6")
sentiment_pipe = pipeline("text-classification", model="incredible45/News-Sentimental-model-Buy-Neutral-Sell")
root = tk.Tk()
root.overrideredirect(True)
def close_window():
  root.destroy()
while True:
  if curr_url != driver.current_url:
    curr_url = driver.current_url
    if "youtube.com/watch" in driver.current_url:
      youtube_video = driver.current_url
      video_id = youtube_video.split("=")[1]
      YouTubeTranscriptApi.get_transcript(video_id)
      transcript = YouTubeTranscriptApi.get_transcript(video_id)
      transcript_arr = []
      result = ""
      for i in transcript:
        result += ' ' + i['text']

      # SUMMARIZING TEXT
      num_iters = int(len(result)/1000)
      summarized_text = []
      for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
      summarized_text = " ".join(summarized_text)
      print(summarized_text)
      left = 0
      count = 0
      arr = []
      for i in range(len(summarized_text)):
        if summarized_text[i] == " ":
          count += 1
          if count == 300:
            arr.append(summarized_text[left:i])
            left = i
            count = 0
      # arr.append(summarized_text[left:])
      print(arr)
      output = sentiment_pipe(arr)
      max_sentiment = output[0]
      print(output)
      for i in range(len(output)):
        if output[i]["score"] > max_sentiment["score"]:
          max_sentiment = output[i]
      print(max_sentiment)
      if max_sentiment["label"] == "negative":
        perc = round(100 * max_sentiment["score"], 2)
        result_text = f"The chances of this Youtube video being fake: \n SCAM: {perc}% \n NOT SCAM: {100 - perc}%"
      else:
        perc = round(100 * max_sentiment["score"], 2)
        result_text = f"The chances of this Youtube video being fake: \n SCAM: {100 - perc}% \n NOT SCAM: {perc}%"
      label = tk.Label(root, text=result_text)
      label.pack()
      # root.after(15000, close_window)
      root.mainloop()


      #  NEUTRAL or POSITIVE
      # "THE CHANCES OF THIS BEING A FAKE ARE:"
      # "SCAM: " : % negative
      # "NOT SCAM: " : 100 - % negative
      # print(transcript_arr)
      # break

# driver.quit()