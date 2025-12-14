import requests
import plotly.express as px

#执行API调用并查看响应
url="https://api.github.com/search/repositories"
url+="?q=language:python+sort:stars+stars:>10000" #添加更加详细的查询条件

headers={"Accept":"application/vnd.github.v3+json"} #请求头？Accept告诉客户端我们想要接收什么样的数据类型
r=requests.get(url,headers=headers)
print(f"Status code:{r.status_code}") #记录请求的状态码，如果是2开头就请求成功，4：客户端错误（我们），5：服务器错误（对方）

#将响应转换为字典
response_dict=r.json()

#处理结果
#print(response_dict.keys())

print(f"Total repositories:{response_dict['total_count']}") #打印GitHub里符合条件的代码仓库
print(f"Complete results:{not response_dict['incomplete_results']}") #告知用户端服务器是否在有限的时间里完成的查询（没有：False）

repo_dicts=response_dict['items']
repo_links,stars,hover_texts=[],[],[]
for repo_dict in repo_dicts:
    #将仓库名转换为链接
    repo_name=repo_dict['name']
    repo_url=repo_dict['html_url']
    repo_link=f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)
    #创建悬停文本
    owner=repo_dict['owner']['login']
    description=repo_dict['description']
    hover_text=f"{owner}<br />{description}" #<br/>标签产生一个空行，分开owner和description
    hover_texts.append(hover_text)
    stars.append(repo_dict['stargazers_count'])


title="Most-Starred Python Projects on GitHub"
labels={'x':'Repository','y':'Stars'}
fig=px.bar(x=repo_links,y=stars,title=title,labels=labels,hover_name=hover_texts)
fig.update_layout(title_font_size=28,xaxis_title_font_size=20,yaxis_title_font_size=20)
fig.update_traces(marker_color='SteelBlue',marker_opacity=0.65)
fig.show()
