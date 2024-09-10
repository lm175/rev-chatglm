data = {
    "id": "66d725412bc0ea4a64d89ee2",
    "conversation_id": "66d724d41a9683c6ef516afc",
    "assistant_id": "65940acff94777010aa6b796",
    "parts": 
    [{
        "id": "66d725412bc0ea4a64d89ee2",
        "conversation_id": "66d724d41a9683c6ef516afc",
        "assistant_id": "65940acff94777010aa6b796", 
        "role": "assistant",
        "content": 
        [{
            "type": "text",
            "text": "\u91cc\u6602\u5728\u6807\u51c6\u5bf9\u6218\u4e2d\u9002\u5408\u7684\u5730\u56fe\u6709\uff1a  \n1. \u51b0\u51bb\u4e4b\u6811\uff08Frozen Forest\uff09\uff1a\u8fd9\u5f20\u5730\u56fe\u7684\u7279\u70b9\u662f\u6709\u8bb8\u591a\u6811\u6728\u548c\u704c\u6728\u4e1b\uff0c\u53ef\u4ee5\u63d0\u4f9b\u826f\u597d\u7684\u63a9\u62a4\u3002\u91cc\u6602\u53ef\u4ee5\u5229\u7528\u8fd9\u4e9b\u5730\u5f62\u5143\u7d20\u8fdb\u884c\u4f0f\u51fb\uff0c\u540c\u65f6\u4e5f\u53ef\u4ee5\u5229\u7528\u706b\u7bad\u53d1\u5c04\u5668\u7684"
        }],
        "model": "cogvlm",
        "created_at": "2024-09-03 23:03:29",
        "meta_data": {},
        "status": "init",
        "logic_id": "ae08eb5c-6a05-11ef-baaa-3ec4855f02a3"
    }],
    "created_at": "2024-09-03 23:03:29",
    "meta_data": 
    {
        "mention_conversation_id": "",
        "is_test": False,
        "input_question_type": "xxxx",
        "channel": "",
        "draft_id": "",
        "quote_log_id": "",
        "platform": "pc",
        "ip": "121.22.29.122",
        "exp_groups": 
        [
            "mainchat_funcall:control:control",
            "chat_aisearch:control:control",
            "mainchat_rag:control:control",
            "mainchat_searchrateboost:control:control",
            "mainchat_searchengine:exp:serpapi_bing"
        ],
        "referer": "",
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "display_rag_slice": False
    },
    "status": "init",
    "last_error": {}
}


class ChatContent:
    """对话内容"""
    content_type: str = ""
    content: str | list = ""
    image_url: str = ""

    def __init__(self, content: list[dict | None]) -> None:
        if content:
            self.content_type = content[0].get('type')
            self.content = content[0].get(self.content_type)

    @property
    def _image(self) -> str:
        if self.content:
            return self.content[0].get('image_url')
        return ""



class ChatResponse(ChatContent):
    """响应内容"""
    conversation_id: str

    def __init__(self, data: dict) -> None:
        self.conversation_id = data.get('conversation_id')
        self.__dict__ = data

        parts: list[dict] = data.get('parts')
        if parts:
            super().__init__(parts[0].get('content'))
