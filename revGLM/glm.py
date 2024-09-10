import requests, json, time
from typing import Union, Generator
from fake_useragent import UserAgent

from .entity import ChatResponse

class ChatBot:

    base_api = "https://chatglm.cn/chatglm"
    refresh_token: str

    def __init__(self, Cookie: str) -> None:
        spt = Cookie.split(";")
        cookies = {}
        for it in spt:
            it = it.strip()
            if it:
                equ_loc = it.find("=")
                key = it[:equ_loc]
                value = it[equ_loc + 1:]
                cookies[key] = value
        self.refresh_token = cookies.get('chatglm_refresh_token')

        self._access_token = None
        self._token_expiry = 0


    @property
    def access_token(self) -> str:
        """每隔1小时刷新验证令牌"""
        current_time = time.time()
        if not self._access_token or current_time > self._token_expiry:
            refresh_url = f"{self.base_api}/user-api/user/refresh"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.refresh_token}',
            }
            response = requests.post(refresh_url, headers=headers)
            if response.status_code == 200:  
                self._access_token = f"Bearer {response.json().get('result').get('access_token')}"
                self._token_expiry = current_time + 3600  
            else:  
                raise Exception("Failed to refresh access token")  

        return self._access_token

    @property
    def headers(self) -> dict:
        return {
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "App-Name": "chatglm",
            "Authorization": self.access_token,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://chatglm.cn",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": UserAgent().chrome,
            "X-App-Platform": "pc",
            "X-App-Version": "0.0.1",
            "X-Lang": "zh",
            "accept": "text/event-stream",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    

    def _stream_ask(
            self,
            prompt: str,
            conversation_id: str = "",
            timeout: int = 60,
            image: bytes = None
    ) -> Generator[ChatResponse, None, None]:
        """流式回复

        Args:
            prompt (str): 提问内容
            conversation_id (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """
        data = {
            "assistant_id": "65940acff94777010aa6b796", # chatglm
            "conversation_id": conversation_id,
            "meta_data": {
                "mention_conversation_id": "",
                "is_test": False,
                "input_question_type": "xxxx",
                "channel": "",
                "draft_id": "",
                "quote_log_id": "",
                "platform": "pc"
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        resp = requests.post(
            url=f"{self.base_api}/backend-api/assistant/stream",
            headers=self.headers,
            json=data,
            timeout=timeout,
            stream=True
        )

        if resp.status_code == 200:
            for chunk in resp.iter_lines(decode_unicode=True):
                if chunk:
                    chunk = str(chunk).strip()
                    if chunk == "event:message":
                        continue
                    chunk = chunk[6:]
                    data = json.loads(chunk)
                    
                    result = ChatResponse(data)
                    yield result
        else:
            raise Exception(resp.text)

    def _non_stream_ask(
            self,
            prompt: str,
            conversation_id: str = "",
            timeout: int = 60,
            image: bytes = None
    ) -> ChatResponse:
        """非流式回复

        Args:
            prompt (str): 提问内容
            conversation_id (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """

        result = None
        image_url = None
        for resp in self._stream_ask(
                prompt,
                conversation_id,
                timeout,
                image
        ):
            result = resp
            if result.content_type == "image" :
                image_url = result._image

        result.image_url = image_url
        return result


    def ask(
            self,
            prompt: str,
            conversation_id: str = "",
            timeout: int = 60,
            stream: bool = False,
            image: bytes = None
    ) -> Union[Generator[ChatResponse, None, None], ChatResponse]:
        """提问

        Args:
            prompt (str): 提问内容
            conversation_id (str, optional): 对话id. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            stream (bool, optional): 是否流式. Defaults to False.
            image (bytes, optional): 图片二进制数据. Defaults to None.
        """

        if stream:
            return self._stream_ask(
                prompt,
                conversation_id,
                timeout,
                image
            )
        else:
            return self._non_stream_ask(
                prompt,
                conversation_id,
                timeout,
                image
            )
    