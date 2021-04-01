import re

class PostProcessingText():
  def __init__(self):
    self.wake_keyword = ["เตือน", "เรียก", "ปลุก", ]
    self.middle_keywords = ["ไป", "เป็น", "แล้ว"]

  def handle_simple_time(self, time_text):
    if((time_text[1] == None) or (time_text[1] == "0")):
      return time_text[0]
    else:
      return time_text[0]+"."+time_text[1]

  def handle_complex_time(self, text, user_times):
    wake_position = None
    time = None
    for keyword in self.wake_keyword:
      if(keyword in text):
        wake_position = re.search(keyword, text).start()
        break
    if(wake_position != None):
      for user_time in user_times:
        if(user_time[2] > wake_position):
          time = self.handle_simple_time(user_time)
    return time

  def handle_multiple_time(self, text, user_times):
    oldTime = None
    newTime = None
    middle_position = None

    ### Check whether oldTime and newTime
    for keyword in self.middle_keywords:
      if(keyword in text):
        middle_position = re.search(keyword, text).start()
        break
    if(middle_position != None):
      for user_time in user_times:
        if(user_time[2] < middle_position):
          oldTime = self.handle_simple_time(user_time)
        else:
          newTime = self.handle_simple_time(user_time)
    return oldTime, newTime

  def post_processing_user_intent(self, tokenized_text=None, user_intent=None, request_func=None):
    text = "".join(tokenized_text)
    ans = {"requestFunc": request_func}
    user_label, user_device, user_times = user_intent
    if(request_func == "createAlarm"):
      if(user_times != None):
        if(len(user_times) == 1):
          ans["time"] = self.handle_simple_time(user_times[0])
        else:
          ans["time"] = self.handle_complex_time(text, user_times)

    elif(request_func == "deleteAlarm"):
      if(user_label != None):
        ans["label"] = user_label
      if(("ทั้งหมด" in text) or ("หมด" in text)):
        ans["time"] = "all"
      elif(user_times != None):
        if(len(user_times) == 1):
          ans["time"] = self.handle_simple_time(user_times[0])
        else:
          ans["time"] = self.handle_complex_time(text,user_times)

    elif(request_func == "addLabel"):
      if(user_label != None):
        ans["label"] = user_label
      if(user_times != None):
        if(len(user_times) == 1):
          ans["time"] = self.handle_simple_time(user_times[0])
        else:
          ans["time"] = self.handle_complex_time(text, user_times)

    elif(request_func == "updateAlarm"):
      if(user_label != None):
        ans["label"] = user_label
      if(user_device != None):
        ans["device"] = user_device
      
      if(user_times != None):
        if(len(user_times) == 2):
          ans["oldTime"], ans["newTime"] = self.handle_multiple_time(text, user_times)
        else:
          ans["newTime"] = self.handle_complex_time(text, user_times)

    return ans
