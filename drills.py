#drill1
def word_count(word):
  split= word.split()
  no_of_words=len(split)
  return(no_of_words)

#drill2
def count_vowels(word):
  count=0
  for i in word:
    if i in 'aeiou':
      count+=1
  
  return count


#drill 3
def is_Plaindrom(word):
  return word==word[::-1]


#drill 4
def count_word_frequency(sentence):
  split_sentence=sentence.split()
  word_count={}
  for i in split_sentence:
    if i in word_count:
      word_count[i]+=1
    else:
      word_count[i]=1
  
  return word_count


#drill 5
def top_word(text):
  find_top_word=count_word_frequency(text)
  best_word=''
  best_count=0
  for key, value in find_top_word.items():
    print(key, value)
    if value>best_count:
      best_count=value
      best_word=key
  return best_word


#drill6
# working with classes

# below is an empty class and an object cerated on it named emp1
class Empolye:
  def __init__(self):
    pass
    
    
emp1=Empolye()
#print(emp1)  

class Person():
  def __init__(self,name,lastname):
    self.name=name
    self.lastname=lastname
  
  def greet(self):
    return f"Hello {self.name} {self.lastname}" 
  
# person1=Person("aakash","dahiya")
# person2=Person("Sagar","dabas")
# person3=Person("Preet","singh")
# print(person1.greet())
# print(person2.greet())
# print(person3.greet())
    

#drill 7

numbers = [1,2,3,4,5,6,7,8,9,10]

dublue_even_numbers=[i*2 for i in numbers if i%2==0]
#print(dublue_even_numbers)


#drill 8
# Use a list comprehension to make a list of just the words longer than 3 characters, in uppercase.
# Expected output: ["HELLO", "WONDERFUL", "AMAZING"]

given_words=['hi','by','a','cat','monday','hy']
uppercasing_letters=[i.upper() for i in given_words if len(i)>=3]

#print(uppercasing_letters)

#drill 9 fake testing

chunks = [
    {"text": "first chunk", "start_time": 0.0, "end_time": 12.5},
    {"text": "second chunk", "start_time": 12.5, "end_time": 24.8},
    {"text": "third chunk", "start_time": 24.8, "end_time": 38.1},
]

start_times=[i['start_time'] for i in chunks]
#print(start_times)


#drill 10

chunks = [
    {"text": "intro to chunking", "start_time": 0.0, "end_time": 12.5},
    {"text": "why size matters", "start_time": 12.5, "end_time": 24.8},
    {"text": "boundary problems", "start_time": 24.8, "end_time": 38.1},
    {"text": "the solution", "start_time": 38.1, "end_time": 55.0},
    {"text": "closing thoughts", "start_time": 55.0, "end_time": 70.0},
]

#a. A list of just the texts of chunks longer than 15 seconds (end_time - start_time > 15)

l1=[i for i in chunks if (i["end_time"]-i["start_time"])>15]
print(l1)

#b. A list of dicts with only text and duration (where duration = end_time - start_time). Hint: the expression in a comprehension can be a dict. [{"text": c["text"], "duration": c["end_time"] - c["start_time"]} for c in chunks]

l2=[[{i,d}] for i in chunks if d==i['end_time']-i['start_time']]
print(l2)

#c. The total duration of all chunks combined. Hint: comprehension gives you a list of durations, then sum() adds them up.

