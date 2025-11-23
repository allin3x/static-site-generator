import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        #print(f"Node: {node} - {node.text} - {node.text_type} - {node.url}")
        if node.text_type != TextType.TEXT:
            #new_nodes.extend(node)
            new_nodes.append(node)
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
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            before, after = text.split(image_markdown, 1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for text_val, url in links:
            link_markdown = f"[{text_val}]({url})"
            before, after = text.split(link_markdown, 1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(text_val, TextType.LINK, url))
            text = after
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
