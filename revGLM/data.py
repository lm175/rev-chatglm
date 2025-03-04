from dataclasses import dataclass, field
from typing import List, Dict


class Content:
    def __init__(
            self,
            type: str = 'text',
            text: str = '',
            image: List[Dict] = [{}],
            tool_calls: List[Dict] = [{}],
            content: str = '',
            code: str = '',
            third_distribute: str = '',
            **kwargs
    ):
        self.type = type
        self.text = text
        self.image = image if image is not None else [{}]
        self.image_url = self.image[0].get('image_url', '') if self.image else ''
        self.tool_calls = tool_calls if tool_calls is not None else [{}]
        self.content = content
        self.code = code
        self.third_distribute = third_distribute

        for key, value in kwargs.items():
            setattr(self, key, value)


class PartMetaData:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclass
class Parts:
    id: str = ''
    conversation_id: str = ''
    assistant_id: str = '65940acff94777010aa6b796'
    role: str = 'assistant'
    content: List[Content] = field(default_factory=lambda: [Content()])
    model: str = 'chatglm-all-tools'
    recipient: str = 'all'
    created_at: str = ''
    meta_data: PartMetaData = field(default_factory=PartMetaData)
    status: str = 'init'
    logic_id: str = ''

    def __post_init__(self):
        if isinstance(self.content, list) and all(isinstance(c, dict) for c in self.content):
            self.content = [Content(**c) for c in self.content] # type: ignore


@dataclass
class MetaData:
    if_plus_model: bool = False
    plus_model_available: bool = False
    img_list: List = field(default_factory=list)
    file_list: List = field(default_factory=list)
    new_conversation: bool = True


@dataclass
class ChatResponse:
    """响应内容"""
    id: str = ''
    conversation_id: str = ''
    assistant_id: str = '65940acff94777010aa6b796'
    parts: List[Parts] = field(default_factory=lambda: [Parts()])
    created_at: str = ''
    meta_data: MetaData = field(default_factory=MetaData)
    status: str = 'init'
    last_error: Dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.parts, list) and all(isinstance(p, dict) for p in self.parts):
            self.parts = [Parts(**p) for p in self.parts] # type: ignore
        
        if self.parts and self.parts[0].content:
            self.content = self.parts[0].content[0].text
            self.image_url = self.parts[0].content[0].image_url
        else:
            self.content = ''
            self.image_url = ''