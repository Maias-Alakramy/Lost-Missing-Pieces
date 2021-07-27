'''
The generale form of the sub:
number/n
start time --> end time/n
One line subtitle/n
/n
OR
Multi line/n
Subtitle/n
/n

and so on

Time format:
00:00:00,000
HH:MM:SS,mmm

Time indeces:
0|0|:|0|0|:|0|0|,|0|0 |0 |  |- |- |> |  |0 |0 |: |0 |0 |: |0 |0 |, |0 |0 |0 |
0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|
'''
lines = []
for i in range(1,14):
	path = "subtitles/zzgtv-lost-mp-e" + str(i) + ".srt"
	if i < 10:
		path = "subtitles/zzgtv-lost-mp-e0" + str(i) + ".srt"
	file = open(path, "r")
	file_lines = file.readlines()
	for line in file_lines:
		lines.append(line)

msec_delay = int(input("Enter subtitles' delay millisecond: "))
sec_delay = int(input("Enter subtitles' delay second: "))
min_delay = int(input("Enter subtitles' delay minute: "))
hour_delay = int(input("Enter subtitles' delay hour: "))

num_indeces = []
diff_indeces = []
start_times = []
end_times = []

def printAll1D(arr):
	for a in arr:
		print(a,end=" ")
	print()

class Time():
	"""
	This calss is created to store subtitles' time and the
	base time to shift the subtitles in an elegant way
	"""

	def __init__(self, Hour, Minute, Second, milisecond):
		self.HH = Hour
		self.MM = Minute
		self.SS = Second
		self.mmm = milisecond
		

	def to_time_formate(self):
		if self.HH<10:
			text = "0" + str(self.HH)
		else:
			text = str(self.HH)

		text += ":"

		if self.MM<10:
			text += "0" + str(self.MM)
		else:
			text += str(self.MM)

		text+=":"

		if self.SS<10:
			text+="0"+str(self.SS)
		else:
			text+=str(self.SS)

		text+=","

		if self.mmm<100:
			if self.mmm<10:
				text+="00"+str(self.mmm)
			else:
				text+="0"+str(self.mmm)
		else:
			text+=str(self.mmm)
		return text

def Delay(base_time,j):
	start_times[j-1].mmm += base_time.mmm
	start_times[j-1].SS += base_time.SS + start_times[j-1].mmm//1000
	start_times[j-1].mmm %= 1000
	start_times[j-1].MM += base_time.MM + start_times[j-1].SS // 60
	start_times[j-1].SS %= 60
	start_times[j-1].HH += base_time.HH + start_times[j-1].MM // 60
	start_times[j-1].MM %= 60
		
	end_times[j-1].mmm += base_time.mmm
	end_times[j-1].SS += base_time.SS + end_times[j-1].mmm//1000
	end_times[j-1].mmm %= 1000
	end_times[j-1].MM += base_time.MM + end_times[j-1].SS // 60
	end_times[j-1].SS %= 60
	end_times[j-1].HH += base_time.HH + end_times[j-1].MM // 60
	end_times[j-1].MM %= 60

	text = start_times[j-1].to_time_formate() + " --> " + end_times[j-1].to_time_formate() + "\n"
	lines[num_indeces[j-1][0]+1] = text
	return 


for i,a in enumerate(lines):
	try:
		int(a)
		num_indeces.append([i,len(num_indeces)+1])
		if(int(lines[num_indeces[-1][0]]) <= int(lines[num_indeces[-2][0]])):
			diff_indeces.append([i,num_indeces[-1][1]])
	except:
		pass
diff_indeces.append([num_indeces[-1][0],num_indeces[-1][1]+1])

for a,_ in num_indeces[:]:
	s_msec = int(lines[a+1][9:12])
	s_sec = int(lines[a+1][6:8])
	s_min = int(lines[a+1][3:5])
	s_hour = int(lines[a+1][0:2])
	start_times.append(Time(s_hour,s_min,s_sec,s_msec))

	e_msec = int(lines[a+1][26:29])
	e_sec = int(lines[a+1][23:25])
	e_min = int(lines[a+1][20:22])
	e_hour = int(lines[a+1][17:19])
	end_times.append(Time(e_hour,e_min,e_sec,e_msec))

for i,[init,index] in enumerate(diff_indeces[:]):
	if i == len(diff_indeces)-1:
		continue

	base_time_msec = end_times[diff_indeces[i][1]-2].mmm + msec_delay
	base_time_sec = end_times[diff_indeces[i][1]-2].SS + sec_delay + base_time_msec // 1000
	base_time_msec %= 1000
	base_time_min = end_times[diff_indeces[i][1]-2].MM + min_delay + base_time_sec // 60
	base_time_sec %= 60
	base_time_hour = end_times[diff_indeces[i][1]-2].HH + hour_delay + base_time_min // 60
	base_time_min %= 60
	base_time = Time(base_time_hour,base_time_min,base_time_sec,base_time_msec)

	for j in range(index,diff_indeces[i+1][1]):
		Delay(base_time,j)

for [_,index] in num_indeces:
	lines[_]=str(index)+"\n"

file.close()

f = open("AllInSub.srt", "w")
for a in lines:
	f.write(a)
f.close()
print("A new file called \"AllInSub\" has been created "\
	"containing the new fixed subtitle")

input()