# Learning Analytics Hackathon
## 2017.01.28

* filter out elements that have few interactions (e.g. 20 or less) - these may be testing elements created by instructor
* moving pages -- hard to determine order of course elements



* median time spent per page
* toggle time or hits


* filter tree by population (e.g. some students only view videos, some students only do problems)

* a session is, e.g. half an hour
* we can track events per session
* look at all events (ignore page close): and calculate time between events

* excluded "problem_check" where event field is "NA"

list of event types:
hide_transcript
load_video
page_close
pause_video
play_video
problem_check
problem_graded
problem_reset
problem_save
problem_show
seek_video
seq_goto
seq_next
seq_prev
show_transcript
speed_change_video
stop_video


* some rows with problems:

{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'load_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:09:38Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1""}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'play_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:12:43Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 0.0149375}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'pause_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:13:26Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.4737205}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'play_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:13:26Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.5938663}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'stop_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:13:26Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.4737205}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'pause_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:14:09Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.490783}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'stop_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:14:09Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.490783}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '275', 'user_id': '5937', 'event_type': 'load_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T10:28:46Z', 'event': '"{""code"": ""q50pVM5ThQ0"", ""id"": ""05590450559045b545844eaaa561fe09391213f""}"', 'name': '3.4. The Greenhouse Effect'}
{'category': 'sequential', 'element_order': '275', 'user_id': '5937', 'event_type': 'play_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T11:02:04Z', 'event': '"{""code"": ""q50pVM5ThQ0"", ""id"": ""05590450559045b545844eaaa561fe09391213f"", ""currentTime"": 0.0330625}"', 'name': '3.4. The Greenhouse Effect'}
{'category': 'sequential', 'element_order': '275', 'user_id': '5937', 'event_type': 'pause_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T11:04:11Z', 'event': '"{""code"": ""q50pVM5ThQ0"", ""id"": ""05590450559045b545844eaaa561fe09391213f"", ""currentTime"": 125.7329323}"', 'name': '3.4. The Greenhouse Effect'}
{'category': 'sequential', 'element_order': '275', 'user_id': '5937', 'event_type': 'stop_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T11:04:11Z', 'event': '"{""code"": ""q50pVM5ThQ0"", ""id"": ""05590450559045b545844eaaa561fe09391213f"", ""currentTime"": 125.7329323}"', 'name': '3.4. The Greenhouse Effect'}


the ID should be:
0559045b545844eaaa561fe09391213f
not
05590450559045b545844eaaa561fe09391213f


and these rows:
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'load_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:09:38Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1""}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'play_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:12:43Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 0.0149375}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'pause_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:13:26Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.4737205}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'play_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:13:26Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.5938663}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'stop_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:13:26Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.4737205}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'pause_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:14:09Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.490783}"', 'name': '3.1. Energy from the Sun'}
{'category': 'sequential', 'element_order': '219', 'user_id': '5937', 'event_type': 'stop_video', 'module': "3. Earth's Energy Budget", 'time': '2015-11-26T08:14:09Z', 'event': '"{""code"": ""t6jBrV3T4jg"", ""id"": ""97055169705516d01b5406c82d0ef9ec6eacce1"", ""currentTime"": 42.490783}"', 'name': '3.1. Energy from the Sun'}


I couldn't find a corresponding ID in course_axis.tsv

## Improvements for data collection

* track page loads -- we only have (partial) navigation events within sequential elements


