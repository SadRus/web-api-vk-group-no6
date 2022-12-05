# Public comics to the VK Public.
### Description

Script will public random comics on a VK Public`s wall with a comic alt comment.
Comics downloaded from https://xkcd.com/json.html

### Objective of project

Script written for educational purposes within online courses for web developers [dvmn.org](https://dvmn.org/).

### Installing

Python3 must be installed. 
Use `pip` (or `pip3`) for install requirements:
```
pip install -r requirements.txt
```

### Enviroment

Firstly you need to create VK public.
Secondary you must register your app at https://vk.com/apps?act=manage for client_id.
Then you need to get access_token within implicit flow method and save it in enviroment variables.

You needs to create .env file in main folder for enviroment variables.
VK_ACCESS_TOKEN - it`s yours access_token, which we get above.
VK_GROUP_ID - you can get group ID at https://regvk.com/id/
VK_VERSION_API - choose API version that you needed.

### Usage

From scripts folder:
```
python(or python3) main.py
```
### Example
After initilaze script you post a random comic on a your public wall.
![image](https://user-images.githubusercontent.com/79669407/205518895-b6d8d326-9aff-4fc2-879f-532cb30cd88e.png)

