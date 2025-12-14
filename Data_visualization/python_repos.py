import requests

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
print(f"Repositories returned:{len(repo_dicts)}")

#研究第一个仓库
repo_dict=repo_dicts[0]
#print(f"\nKeys:{len(repo_dict)}")
#for key in sorted(repo_dict.keys()):
#    print(key)
print("\nSelected information about each repository:")
for repo_dict in repo_dicts:
    print(f"Name:{repo_dict['name']}")
    print(f"Owner:{repo_dict['owner']['login']}")
    print(f"Stars:{repo_dict['stargazers_count']}")
    print(f"Repository:{repo_dict['html_url']}")
    print(f"Created:{repo_dict['created_at']}")
    print(f"Updated:{repo_dict['updated_at']}")
    print(f"Description:{repo_dict['description']}")
    print("\n")