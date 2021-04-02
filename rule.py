label_regex_list = ["ตั้ง.*(?<!ก)ว่า(.*)นะ", "ชื่อว่า(.*)ไปเป็น", "ชื่อว่า(.*)นะ", "ชื่อว่า(.*)ไปเป็น", "ชื่อว่า(.*)ออกไป", "ชื่อว่า(.*)ทิ้งไป", "ชื่อว่า(.*)นะ",
                    "เลเบลว่า(.*)ไปเป็น", "เลเบลเป็น(.*)ออกไป", "เลเบลเป็น(.*)ทิ้งไป", 
                    "เรียกว่า(.*)ไปเป็น", "ชื่อ(.*)ไปเป็น", "ชื่อ(.*)ช่วยเปลี่ยนเวลาเป็น", "ชื่อ(.*)ออกไป", "ชื่อ(.*)ทิ้งไป", "(?<!ไม่ต้องตั้ง)ชื่อ(.*)นะ",  
                    "(?<!ก)ว่า(.*)ทิ้งไป", "(?<!ก)ว่า(.*)ออกไป", "(?<!ก)ว่า(.*)", ]
device_list = ["iphone", "ไอโฟน", "ipad", "ไอแพด", "แมคบุ๊ค", "applewatch", "แอปเปิ้ลวอช", "macbook", "โน๊ตบุ๊ค", "มือถือ", "คอม", "นาฬิกาข้อมือ"]
number_single_digit = "หนึ่ง|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า"
number_two_digit = "ยี่|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า"
number_one_digit = "เอ็ด|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า"

case_tee = f"(ตี(({number_single_digit})|(({number_two_digit})?สิบ({number_one_digit})?)))"
case_mong = f"((({number_single_digit})|(({number_two_digit})?สิบ({number_one_digit})?))โมง(เช้า|เย็น)?)"
case_tum = f"((({number_single_digit})|(({number_two_digit})?สิบ({number_one_digit})?))ทุ่ม)"
case_tum2 = f"(ทุ่ม(({number_single_digit})|(({number_two_digit})?สิบ({number_one_digit})?)))"
case_bai = f"(บ่าย(({number_single_digit})|(({number_two_digit})?สิบ({number_one_digit})?))(โมง(เช้า|เย็น)?)?)|(บ่ายโมง)"
case_nariga = f"((({number_single_digit})|(({number_two_digit})?สิบ({number_one_digit})?))นาฬิกา(เช้า|เย็น)?))(ครึ่ง|ตรง"
case_yam = f"(ยามหนึ่ง|ยามสอง|ยามสาม|ยามสี่|สองยาม)"
case_minute = f"(((({number_two_digit})?สิบ({number_one_digit})?)|({number_single_digit}))(นาที)?)"
time_regex_list = ["((ทุ่มตรง|ทุ่มหนึ่ง)|(เที่ยง(คืน|วัน)?)|"+case_yam+"|"+case_tee+"|"+case_mong+"|"+case_tum+"|"+case_tum2+"|"+case_bai+"|"+case_nariga+"|"+case_minute+")?"]
