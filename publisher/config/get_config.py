import os
import argparse


def get_config():
    # Parse arguments with LOGIN and PASSWORD for Confluence
    parser = argparse.ArgumentParser(
        description='Publish markdown files to Confluence.')
    parser.add_argument('--confluence-username', required=False,
                        help='Confluence login username.',
                        default=os.environ.get('CONFLUENCE_USERNAME'))
    parser.add_argument('--confluence-password', required=False,
                        help='Confluence login password.',
                        default=os.environ.get('CONFLUENCE_PASSWORD'))
    parser.add_argument('--url', required=False,
                        help='Confluence URL',
                        default=os.environ.get('CONFLUENCE_URL', "https://yourdomain.atlassian.net/wiki/rest/api/"))
    parser.add_argument('--space', required=False,
                        help='Confluence space key',
                        default=os.environ.get('CONFLUENCE_SPACE', "yourspace"))
    parser.add_argument('--parent_page_id', required=False,
                        help='Confluence parent page ID',
                        default=os.environ.get('CONFLUENCE_PARENT_PAGE_ID', "65777"))
    parser.add_argument('--search_pattern', required=False,
                        help='Confluence search pattern to find pages.',
                        default=os.environ.get('CONFLUENCE_SEARCH_PATTERN', "(this page is autogenerated)"))
    parser.add_argument('--github_md', required=False,
                        help='GitHub folder with markdown files.',
                        default=os.environ.get('GITHUB_FOLDER_WITH_MD_FILES', "./data"))
    parser.add_argument('--github_images', required=False,
                        help='GitHub folder with image files.',
                        default=os.environ.get('GITHUB_FOLDER_WITH_IMAGE_FILES', "./data_images"))

    args = parser.parse_args()

    return {
        'confluence_url': args.url,
        'confluence_space': args.space,
        'confluence_parent_page_id': args.parent_page_id,
        'confluence_search_pattern': args.search_pattern,
        'github_folder_with_md_files': args.github_md,
        'github_folder_with_image_files': args.github_images,
        'confluence_username': args.confluence_username,
        'confluence_password': args.confluence_password,
        # Add other settings as needed
    }
