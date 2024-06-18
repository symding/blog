import os
folder_path = "../blog"
files = [os.path.join(dirpath, file) for dirpath, dirnames, files in os.walk(folder_path) for file in files]
import re
import json
tags_map = dict()
blogs = []
for file in files:
    if file.endswith(".md"):
        name = file.replace(folder_path,"").split(".m")[0].split("-")
        with open(file,"r") as f:
            file_str = f.read()
            title = re.findall("title: (.+)",file_str)
            tags = re.findall("tags: \[(.+)\]",file_str)[0].split(",")
            for t in tags:
                tags_map[t.lower()] = tags_map.setdefault(t.lower(), 0) + 1
            desc = re.findall("> (.+)",file_str)
        url = f'/blog{"/".join(name[:3])}/{"-".join(name[3:])}'
        blogs.append({
            "url":url,
            "title":title,
            "desc":desc
        })
blogs.sort(key=lambda x:x["url"],reverse=True)
tags = [(k,v) for k,v in tags_map.items()]
tags.sort(key=lambda k:k[1],reverse=True)
import json
js_str = f'''const recentPost={json.dumps({"blogs":blogs[:10],"tags":tags})};
export default recentPost; '''
with open("../src/components/HomepageFeatures/recentPost.js","w") as f:
    f.write(js_str)

