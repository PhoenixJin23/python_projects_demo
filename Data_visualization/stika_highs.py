from pathlib import Path #读写文件使用的Path模块
import csv #该模块帮助处理csv格式的文件

path=Path('weather_data\\sitka_weather_07-2014.csv')
#给Path传入文件路径，得到一个实例
lines=path.read_text().splitlines()
#对path调用read_text方法，splitlines对字符串以换行符进行拆分
#因此lines是一个列表，每个元素就是csv文件的每一行

reader=csv.reader(lines)
header_row=next(reader) #使用next，只返回reader中的一行
print(header_row)