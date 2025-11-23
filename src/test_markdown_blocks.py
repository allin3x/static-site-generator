import unittest
from markdown_blocks import (markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md2 = """
        Block 1



        Block 2
        """
        blocks = markdown_to_blocks(md2)
        self.assertEqual(blocks,
        ["Block 1", "Block 2"],)
    
    def test_block_to_block_type_heading_1(self):
        block_type = block_to_block_type("# Heading 1")
        self.assertEqual(block_type.HEADING, BlockType.HEADING)

    def test_block_to_block_type_heading_2(self):
        block_type = block_to_block_type("## Heading 2")
        self.assertEqual(block_type.HEADING, BlockType.HEADING)
    
    def test_block_to_block_type_heading_3(self):
        block_type = block_to_block_type("### Heading 3")
        self.assertEqual(block_type.HEADING, BlockType.HEADING)
    
    def test_block_to_block_type_heading_4(self):
        block_type = block_to_block_type("#### Heading 4")
        self.assertEqual(block_type.HEADING, BlockType.HEADING)
    
    def test_block_to_block_type_heading_5(self):
        block_type = block_to_block_type("##### Heading 5")
        self.assertEqual(block_type.HEADING, BlockType.HEADING)

    def test_block_to_block_type_heading_6(self):
        block_type = block_to_block_type("###### Heading 6")
        self.assertEqual(block_type.HEADING, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block_type = block_to_block_type("``` Code Block ```")
        self.assertEqual(block_type.CODE, BlockType.CODE)

    def test_block_to_block_type_uolist(self):
        block_text = """- 1\n- 2\n- 3"""
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type.ULIST, BlockType.ULIST)

    def test_block_to_block_type_olist(self):
        block_text = """1. a\n2. b\n3. c"""
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type.OLIST, BlockType.OLIST)

    def test_block_to_block_type_paragraph(self):
        block_type = block_to_block_type("Just some text")
        self.assertEqual(block_type.PARAGRAPH, BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

