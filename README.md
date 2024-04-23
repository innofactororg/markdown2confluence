# markdown2confluence

Convert your Markdown files into Confluence pages with ease using the `markdown2confluence` script. It uploads all files from a specified Markdown directory to a Confluence space, maintaining the folder hierarchy as page structure.

## Prerequisites

Before you get started, locate the space ID and page ID in your Confluence URL by navigating to the desired space and page in your web browser.

## Configuration

Set the following environment variables in your environment before running the script:

- `CONFLUENCE_URL`: The URL to your Confluence instance's API endpoint, e.g., `https://your-instance.atlassian.net/wiki/rest/api/`
- `CONFLUENCE_USERNAME`: Your Confluence username
- `CONFLUENCE_PASSWORD`: Your Confluence password or API token
- `CONFLUENCE_SPACE`: The ID of the space in Confluence where the pages will be created
- `CONFLUENCE_PARENT_PAGE_ID`: The ID of the parent page under which the new pages will be created
- `MARKDOWN_FOLDER`: The path to your folder containing markdown files INSIDE the container, e.g. /data

## Example usage

To upload sample markdown files to Confluence, ensure you have a `.env` file containing necessary key=value pairs for configuration. Then, run the following Docker command:

```bash
# Run from the root of this repo
docker run --rm --env-file=.env -v $(pwd)/markdownsample:/data ghcr.io/innofactororg/markdown2confluence:0.1.0-alpha
```

This command will start a Docker container, which reads your `.env` file (containing the required environment variable settings), and synchronizes the contents of your local Markdown folder with your Confluence space.

