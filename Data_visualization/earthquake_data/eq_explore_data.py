from pathlib import Path #Python内置的文件路径操作模块
# Path是核心类-让路径操作更简洁直观；Path("")表示文件路径，定位文件（夹）；read/write_text()读写文件
import json #Python内置的数据处理模块，专门用来处理JSON格式的数据，轻量级数据交换格式
#loads()解析，将JSON字符串转为Python列表/字典；dumps()生成，转回JSON字符串；load/dump()读写文件
import plotly.express as px #第三方库的可视化简单接口，主打交互式可视化，比Matplotlib更适合展示数据
#快速绘制折线、散点、柱状图、地图；直接传入pd的DataFrame数据；生成图表可导出为html格式
import pandas as pd #Python数据分析的核心第三方库
#可以很方便地对结构化数据进行处理（JSON,csv,excel..数据）

#将数据作为字符串读取并转换为Python对象
path=Path("C:/Users/g3472/Desktop/py_projects_demo/Data_visualization/data/eq_data_30_day_m1.geojson")
try:
    contents=path.read_text()
except:
    contents=path.read_text(encoding='UTF-8')

all_eq_data=json.loads(contents) #loads方法可以把传入的文件字符串转化成Python里字典/列表...

#查看数据集中的所有地震，拆解JSON，提取数据到独立列表，按数据类型分组
all_eq_dicts=all_eq_data['features'] #其实是features键对应的值，该值是列表
"""mags,titles,lons,lats=[],[],[],[]
for eq_dict in all_eq_dicts:
    mag=eq_dict['properties']['mag']
    title=eq_dict['properties']['title']
    lon=eq_dict['geometry']['coordinates'][0]
    lat=eq_dict['geometry']['coordinates'][1]
    mags.append(mag)
    titles.append(title)
    lons.append(lon)
    lats.append(lat)""" #手动添加，麻烦！
mags=[eq_dict['properties']['mag']for eq_dict in all_eq_dicts]
titles=[eq_dict['properties']['title']for eq_dict in all_eq_dicts]
#'properties'这个键对应的值是字典，于是只能用“键”（'mag'和'title'）来访问对应的“值”
lons=[eq_dict['geometry']['coordinates'][0]for eq_dict in all_eq_dicts]
lats=[eq_dict['geometry']['coordinates'][1]for eq_dict in all_eq_dicts]
#'coordinates'键对应的值是列表，用[]访问

#平行列表→表格结构（DataFrame），按“每个地震”分组
data=pd.DataFrame(
    data=zip(lons,lats,titles,mags),columns=['经度','纬度','位置','震级']
) #zip返回的每个元组的数据分别为第1、2、3、4个列表的第n个元素
  #columns指定列名
#print(data.head()) #head方法能返回列表的前五行

#绘制散点图
fig=px.scatter(
    #x=lons,
    #y=lats,
    data,x='经度',y='纬度',
    labels={'x':'经度','y':'纬度'},
    range_x=[-200,200],range_y=[-90,90],
    height=800,title='全球地震散点图',
    size='震级',size_max=10,
    color='震级',
    hover_name='位置'
)

#将绘制图像存为html格式，使程序不运行也能查看该图像
fig.write_html('global_earthquakes.html')
fig.show()