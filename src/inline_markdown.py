import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        #print(f"Node: {node} - {node.text} - {node.text_type} - {node.url}")
        if node.text_type != TextType.TEXT:
            new_nodes.extend(node)
            continue
        # 2. If the delimiter isn’t in the text, keep the node as-is
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        # 3. Split by delimiter
        parts = node.text.split(delimiter)

        # 4. If we got an even number of parts, delimiters are unbalanced
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown, unmatched delimiter")

        # 5. Build new nodes from parts
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                # Outside delimiters: normal TEXT node
                # TEXT Node
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text: str):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(regex, text)
    #print(f"Matches: {matches}")
    return matches

def extract_markdown_links(text: str):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    #print(f"Matches: {matches}")
    return matches

def split_nodes_image(old_nodes):
    pass

def split_nodes_link(old_nodes):
    pass