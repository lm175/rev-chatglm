# rev-chatglm
智谱清言(chatglm)逆向免费api


## 使用示例

    from revGLM import glm

    chatbot = glm.ChatBot(
        Cookie = "你的Cookie" # Cookie可以从浏览器的请求头中获取
    )

    res = chatbot.ask("画一幅风景画")
    print(res.content)
    print(res.image_url)


## 识图对话
可以将图片的bytes数据作为列表传入

    import requests

    image_1 = requests.get("https://avatars.githubusercontent.com/u/170833701").content
    with open('example.png', 'rb') as f: # 把example.png替换为实际的本地文件路径
        image_2 = f.read()
    
    chatbot.ask("这两个图片分别是什么？", images=[image_1, image_2])


## 连续对话
调用ask方法时可以传入`conversation_id`来继续之前的对话，若不传入该参数或传入空字符串则会创建新的对话

ask方法(非流式)会返回一个对象，该对象中包含本次对话的`conversation_id`属性

    res = chatbot.ask("你好") # 创建一个新的对话
    print(res.content)
    conversation_id = res.conversation_id # 获取这次对话的id

    res_2 = chatbot.ask("我刚刚跟你说什么了？", conversation_id=conversation_id) # 继续先前的对话
    print(res_2.content)
    # res_2中的conversation_id与res中的相同


## 对话记录管理

    chatbot.get_conversations() # 获取所有对话记录
    chatbot.del_conversation(conversation_id) # 删除指定对话
