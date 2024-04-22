import logging
import os
import markdown
import re
from config.get_config import get_config
from pages_controller import create_page, attach_file


CONFIG = get_config()


def folderContainsMarkdown(folder_path):
    for entry in os.scandir(folder_path):
        if entry.is_dir() and folderContainsMarkdown(entry.path):
            return True
        elif entry.is_file() and entry.name.endswith('.md'):
            return True
    return False


def publish_folder(folder, login, password, parent_page_id=None):
    logging.info(f"Publishing folder: {folder}")
    for entry in os.scandir(folder):
        if entry.is_dir():
            # Recursively publish directories that contain markdown files
            if folderContainsMarkdown(entry.path):
                publish_directory(entry, login, password, parent_page_id)

        elif entry.is_file() and entry.name.endswith('.md'):
            # Publish only markdown files
            publish_file(entry, login, password, parent_page_id)

        elif entry.is_symlink():
            logging.info(f"Found symlink: {entry.path}")


def publish_directory(entry, login, password, parent_page_id):
    logging.info(f"Found directory: {entry.path}")
    current_page_id = create_page(
        title=entry.name,
        content="<ac:structured-macro ac:name=\"children\" ac:schema-version=\"2\" "
                "ac:macro-id=\"80b8c33e-cc87-4987-8f88-dd36ee991b15\"/>",
        parent_page_id=parent_page_id,
        login=login,
        password=password
    )
    publish_folder(entry.path, login, password, current_page_id)


def publish_file(entry, login, password, parent_page_id):
    logging.info(f"Found file: {entry.path}")

    if entry.name.lower().endswith('.md'):
        process_markdown_file(entry, login, password, parent_page_id)
    else:
        logging.info(
            f"File: {entry.path} is not a MD file. Publishing has been rejected.")


def process_markdown_file(entry, login, password, parent_page_id):
    new_file_content, files_to_upload = process_markdown_content(entry.path)

    page_id_for_file_attaching = create_page(
        title=entry.name,
        content=markdown.markdown(new_file_content, extensions=[
                                  'markdown.extensions.tables', 'fenced_code']),
        parent_page_id=parent_page_id,
        login=login,
        password=password
    )

    upload_attachments(files_to_upload, login, password,
                       page_id_for_file_attaching)


def process_markdown_content(file_path):
    new_file_content = ""
    files_to_upload = []

    with open(file_path, 'r', encoding="utf-8") as md_file:
        for line in md_file:
            result = re.findall(r"\A!\[.*]\((?!http)(.*)\)", line)
            if result:
                result = result[0]
                logging.debug(f"Found file for attaching: {result}")
                print(f"Found file for attaching: {result}")
                files_to_upload.append(result)
                new_file_content += f"<ac:image> <ri:attachment ri:filename=\"{result.split('/')[-1]}\" /></ac:image>"
            else:
                new_file_content += line

    return new_file_content, files_to_upload


def upload_attachments(files_to_upload, login, password, page_id_for_file_attaching):
    if files_to_upload:
        for file in files_to_upload:
            print("file: ", file)

            # NOTE: Find the problem that this solves and fix it in a better way
            if file.startswith('/'):
                file = '.' + file

            image_path = os.path.join(
                CONFIG["markdown_folder"], file)
            if os.path.isfile(image_path):
                logging.info(
                    f"Attaching file: {image_path} to the page: {page_id_for_file_attaching}")
                with open(image_path, 'rb') as attached_file:
                    attach_file(
                        page_id=page_id_for_file_attaching,
                        attached_file=attached_file,
                        login=login,
                        password=password
                    )
            else:
                logging.error(
                    f"File: {image_path} not found. Nothing to attach")
