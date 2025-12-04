from pathlib import Path #读写文件使用的Path模块
import csv #该模块帮助处理csv格式的文件
import matplotlib.pyplot as plt
from datetime import datetime

from matplotlib.pyplot import fill_between

path=Path("C:/Users/g3472/Desktop/py_projects_demo/Data_visualization/weather_data/sitka_weather_2021_full.csv")
#给Path传入文件路径，得到一个实例
lines=path.read_text().splitlines()
#对path调用read_text方法，splitlines对字符串以换行符进行拆分
#因此lines是一个列表，每个元素就是csv文件的每一行

reader=csv.reader(lines)
header_row=next(reader) #使用next，只返回reader中的一行
#for index,column_header in enumerate(header_row):
    #print(index,column_header)
#给enumerate函数传入header_row列表，会返回列表的索引和本身的组合

#提取日期和最高温度
dates,highs,lows=[],[],[]
for row in reader: #datetime中 %H,%M 表示小时,分钟
    if row[7].strip()!='':
        current_date=datetime.strptime(row[2],"%Y-%m-%d")
        high=int(row[7])
        low=int(row[8])
        dates.append(current_date)
        highs.append(high)
        lows.append(low)
    #print(highs) #上一次调用next函数已经读完第一行了，这次从第二行开始读

#根据最高温度绘制图形
plt.style.use('seaborn-v0_8-white')
fig,ax=plt.subplots() #调用库里的subplots得到图像对象和轴对象
ax.plot(dates,highs,color='red',alpha=0.6) #plot方法用来绘制折线图
ax.plot(dates,lows,color='blue',alpha=0.6) #alpha为颜色透明度
ax.fill_between(dates,highs,lows,facecolor='blue',alpha=0.1)
#fill_between方法能给两条折线之间的空隙填充颜色，传入1个x值2个y值，facecolor为中间的填充色

#设置图形的格式
ax.set_title("Daily High And Low Temperature,2021",fontsize=24)
ax.set_xlabel('',fontsize=16)
fig.autofmt_xdate() #用于绘制倾斜的日期标签，避免太长导致彼此重叠
ax.set_ylabel("Temperature (F)",fontsize=16)
ax.tick_params(labelsize=16)

plt.show()