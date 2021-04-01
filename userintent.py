import re
from num_thai.thainumbers import NumThai

class UserIntent:
  def __init__(self, label_regex_list, device_list, time_regex_list):
    self.label_regex_list = label_regex_list
    self.device_list = device_list
    self.time_regex_list = time_regex_list
    self.bai_mapping = {
        "บ่ายสอง": "14",
        "บ่ายสาม": "15",
        "บ่ายสี่": "16",
        "บ่ายห้า": "17",
        "บ่ายหก": "18",
        "บ่าย": "13",
    }
    self.tee_mapping = {
        "ตีหนึ่ง": "1",
        "ตีสอง": "2",
        "ตีสาม": "3",
        "ตีสี่" : "4",
        "ตีห้า": "5",
        "ตีหก": "6",
    }
    self.yam = {
        "สองยาม": "24",
        "ยามหนึ่ง": "21",
        "ยามสอง": "24",
        "ยามสาม": "3",
        "ยามสี่": "6",
    }

  def find_label(self, text):
    for rule in self.label_regex_list:
      label = re.findall(rule, text, re.U)
      if(len(label)>0):
        return label[0]
    return None

  def find_device(self, text):
    for kw in self.device_list:
      if(kw in text):
        return kw
    return None

  def find_time(self, text):
    ans = []
    for rule in self.time_regex_list:
      for i in re.finditer(rule, text, re.U):
        ans.append((i[0], i.start()))
    if(len(ans) == 0):
      return None
    return ans 

  def find_user_intent(self, text):
    text = "".join(text)
    user_label = self.find_label(text)
    user_device = self.find_device(text)
    user_times = self.find_time(text)
    if(user_times != None):
      user_times = self.user_time_text_to_number(user_times)
    return user_label, user_device, user_times

  def user_time_text_to_number(self, user_times):
    num = NumThai()
    ans = []
    # print(user_times)
    for user_time, user_position in user_times:
      hour = None
      minute = None
      
      if(user_time in ["เที่ยงตรง", "เที่ยงวัน", "เที่ยง"]):
        ans.append(("12", minute, user_position))
      
      elif(user_time in ["เที่ยงคืน"]):
        ans.append(("24", minute, user_position))
      
      elif(user_time in ["ทุ่มตรง"]):
        ans.append(("19", minute, user_position))

      elif("นาฬิกาเย็น" in user_time):
        tmp_split = user_time.split("นาฬิกาเย็น")
        hour = str(int(num.TextThaiToNumber(tmp_split[0]))+12)
        if("นาที" in tmp_split[1]):
          minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
        ans.append((hour, minute, user_position))

      elif("นาฬิกา" in user_time):
        tmp_split = user_time.split("นาฬิกา")
        hour = num.TextThaiToNumber(tmp_split[0])
        if("นาที" in tmp_split[1]):
          minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
        ans.append((hour, minute, user_position))

      elif("ทุ่มครึ่ง" in user_time):
        tmp_split = user_time.split("ทุ่มครึ่ง")
        if(len(tmp_split[0]) != 0):
          hour = str(int(num.TextThaiToNumber(tmp_split[0]))+18)
        else:
          ans.append(("19", "30", user_position))
      
      elif("ทุ่ม" in user_time):
        tmp_split = user_time.split("ทุ่ม")
        if(len(tmp_split[0]) != 0):
          hour = str(int(num.TextThaiToNumber(tmp_split[0]))+18)
          if ("นาที" in tmp_split[1]):
            minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
          ans.append((hour, minute, user_position))
        else:
          hour = str(int(num.TextThaiToNumber(tmp_split[1]))+18)
          ans.append((hour, minute, user_position))
      
      elif("โมงเย็น" in user_time):
        tmp_split = user_time.split("โมงเย็น")

        if(tmp_split[0] in self.bai_mapping.keys()):
          hour = self.bai_mapping[tmp_split[0]]
        else:
          hour = str(int(num.TextThaiToNumber(tmp_split[0]))+12)

        if("นาที" in tmp_split[1]):
          minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
        ans.append((hour, minute, user_position))
      
      elif("โมงเช้า" in user_time):
        tmp_split = user_time.split("โมงเช้า")
        if(tmp_split[0] in self.bai_mapping.keys()):
          hour = self.bai_mapping[tmp_split[0]]
        else:
          hour = num.TextThaiToNumber(tmp_split[0])
        if("นาที" in tmp_split[1]):
          minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
        ans.append((hour, minute, user_position))
      
      elif("โมงตรง" in user_time): ### check บ่าย
        tmp_split = user_time.split("โมงตรง")
        if(tmp_split[0] in self.bai_mapping.keys()):
          hour = self.bai_mapping[tmp_split[0]]
        else:
          hour = num.TextThaiToNumber(tmp_split[0])
        ans.append((hour, "0", user_position))
      
      elif("โมงครึ่ง" in user_time): ### check บ่าย 
        tmp_split = user_time.split("โมงครึ่ง")
        if(tmp_split[0] in self.bai_mapping.keys()):
          hour = self.bai_mapping[tmp_split[0]]
        else:
          hour = num.TextThaiToNumber(tmp_split[0])
        ans.append((hour, "30", user_position))

      elif("โมง" in user_time): ### check บ่าย 
        tmp_split = user_time.split("โมง")
        if(tmp_split[0] in self.bai_mapping.keys()):
          hour = self.bai_mapping[tmp_split[0]]
        else:
          hour = num.TextThaiToNumber(tmp_split[0])
        if("นาที" in tmp_split[1]):
          minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
        ans.append((hour, minute, user_position))
      
      elif("บ่าย" in user_time):
        for t, v in self.bai_mapping.items():
          if(t in user_time):
            tmp_split = user_time.split(t)
            hour = v
            if("นาที" in tmp_split[1]):
              minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
            elif("ครึ่ง" in tmp_split[1]):
              minute = "30"
            ans.append((hour, minute, user_position))
            break

      elif("ยาม" in user_time):
        for t,v in self.yam.items():
          if(t in user_time):
            tmp_split = user_time.split(t)
            hour = v
            if("นาที" in tmp_split[1]):
              minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
            elif("ครึ่ง" in tmp_split[1]):
              minute = "30"
            ans.append((hour, minute, user_position))
            break

      elif("ตี" in user_time):
        for t,v in self.tee_mapping.items():
          if(t in user_time):
            tmp_split = user_time.split(t)
            hour = v
            if("นาที" in tmp_split[1]):
              minute = num.TextThaiToNumber(tmp_split[1].split("นาที")[0])
            elif("ครึ่ง" in tmp_split[1]):
              minute = "30"
            ans.append((hour, minute, user_position))
            break
    return ans
