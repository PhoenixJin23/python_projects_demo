from die import Die
import plotly.express as px

#创建一个D6
die_1=Die()
die_2=Die()

#骰几次骰子并将结果存储在一个列表中
results=[]
for roll_num in range(1000):
    result=die_1.roll()+die_2.roll()
    results.append(result)

#分析结果，数不同的点数被投出来的次数
frequencies=[] #记录各个点数被投出来的次数
max_result=die_1.num_sides+die_2.num_sides
poss_results=range(2,max_result+1) #包含所有投掷的可能性（1-6），但左闭右开
for value in poss_results: #for循环依次从1到6，统计每个点数被投出来的次数
    frequency=results.count(value)
    frequencies.append(frequency)
#print(frequencies)

#对结果进行可视化
title="Devils Roll Their Dices,Angels Roll Their Eyes"
labels={'x':'Result','y':'Frequency of Result'}
fig=px.bar(x=poss_results,y=frequencies,title=title,labels=labels) #bar是用来绘制直方图的函数,x为所有可能的点数，y为分别出现的次数
#进一步定制图形
fig.update_layout(xaxis_dtick=1)
fig.show()