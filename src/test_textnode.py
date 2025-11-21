import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        italic_node = TextNode("Test Node", TextType.ITALIC)
        bold_node = TextNode("Test Node", TextType.BOLD)
        bold2 = TextNode("Bold Node", TextType.BOLD)
        plain_node = TextNode("Text Node", TextType.TEXT)
        code_node = TextNode("Test Node", TextType.CODE)
        link_node = TextNode("Test Node", TextType.LINK)
        img_node = TextNode("Test Node", TextType.IMG)

        url_node = TextNode("Bold Node", TextType.BOLD, "www.google.at")

        self.assertNotEqual(italic_node, bold_node)
        self.assertNotEqual(italic_node, plain_node)
        self.assertNotEqual(italic_node, code_node)
        self.assertNotEqual(italic_node, link_node)
        self.assertNotEqual(italic_node, img_node)

        self.assertNotEqual(bold_node, bold2)
        self.assertNotEqual(bold2, url_node)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_text_node_to_html_node(self):
        # TEXT NODE
        text_node = TextNode("This is some Text Text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is some Text Text")

        # BOLD NODE
        text_node = TextNode("This is some Text Text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is some Text Text")

        # LINK NODE
        text_node = TextNode("This is some Text Text", TextType.LINK)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is some Text Text")

if __name__ == "__main__":
    unittest.main()
