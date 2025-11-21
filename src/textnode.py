from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    '''
        TextType Class to handle Types of Text.
    '''
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "img"

class TextNode():
    '''
        Textnode Class
    '''
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False 

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    # your implementation here
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        props = {
            'href' : text_node.url
        }
        return LeafNode("a", text_node.text, props)
    elif text_node.text_type == TextType.IMG:
        props = {
            "alt" : text_node.text,
            "src" : text_node.url
        }
        return LeafNode("img", "", props)
    else:
        raise ValueError("Text_node to HTML input Wrong")
