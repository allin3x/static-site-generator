import os
import sys
import shutil
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    list_dir = os.listdir(dir_path_content)

    for item in list_dir:
        # if item is a file -> Copy
        fullpath_item = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        # Path is File
        if os.path.isfile(fullpath_item):
            # print(f"File {fullpath_item}")
            if fullpath_item.endswith(".md"):
                html_dest_path = dest_path.replace(".md", ".html")
                generate_page(fullpath_item, template_path, html_dest_path, basepath)
        # Path is Dir
        elif os.path.isdir(fullpath_item):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(fullpath_item, template_path, dest_path, basepath)
            # print(f"Dir: {fullpath_item}")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating Page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    # read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)

    basepath_href = f'href="{basepath}"'
    template = template.replace('href="/"', basepath_href)

    basepath_src = f'src="{basepath}"'
    template = template.replace('src="/"', basepath_src)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)


def extract_title(markdown: str):
    markdown_list = markdown.split("\n")
    for item in markdown_list:
        # print(f"Item: {item[2:]}")
        # print(f"Item (repr): {repr(item[2:])}")
        if item.startswith("# "):
            return item[2:].strip()
    raise ValueError("No H1 Header in Markdown")


def clean_folder(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)


def copy_content(src, dest):
    list_dir = os.listdir(src)
    # print(os.listdir(src))
    for item in list_dir:
        # if item is a file -> Copy
        fullpath_item = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        print(fullpath_item)
        if os.path.isfile(fullpath_item):
            shutil.copy(fullpath_item, dest_path)
            print(f"Copied {fullpath_item} to {dest_path}")
        # if item is dir -> go listdir again -> than do same thing again.
        elif os.path.isdir(fullpath_item):
            os.mkdir(dest_path)
            copy_content(fullpath_item, dest_path)
            print(f"Recursion func: {fullpath_item} {dest_path}")


def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    clean_folder("docs")
    copy_content("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
