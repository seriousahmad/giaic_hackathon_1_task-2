"""
Text chunking utilities for RAG system.
"""
import re
from typing import List, Dict, Any
import logging


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks of specified size.

    Args:
        text: Text to chunk
        chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of overlapping characters between chunks

    Returns:
        List of text chunks
    """
    if not text or len(text.strip()) == 0:
        return []

    # Clean up the text by normalizing whitespace
    text = re.sub(r'\s+', ' ', text)

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're near the end, just take the rest
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Find a good breaking point (try to break at sentence or word boundaries)
        chunk = text[start:end]

        # Look for a good break point within the last 100 characters
        break_points = [chunk.rfind(' ', chunk_size - 200, chunk_size - 100),
                       chunk.rfind('.', chunk_size - 200, chunk_size - 100),
                       chunk.rfind('!', chunk_size - 200, chunk_size - 100),
                       chunk.rfind('?', chunk_size - 200, chunk_size - 100)]

        break_point = max([bp for bp in break_points if bp != -1], default=-1)

        if break_point != -1 and break_point > chunk_size // 2:
            # Break at the good point
            actual_end = start + break_point + 1
            chunks.append(text[start:actual_end])
            start = actual_end - overlap
        else:
            # No good break point found, just take the chunk
            chunks.append(text[start:end])
            start = end - overlap

    # Filter out empty chunks and very small chunks
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]

    return chunks


def chunk_markdown_content(content: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split markdown content into chunks while preserving structural context.

    Args:
        content: Markdown content to chunk
        chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of overlapping characters between chunks

    Returns:
        List of chunk dictionaries with content and metadata
    """
    # Split content by headers to preserve document structure
    lines = content.split('\n')
    sections = []
    current_section = []
    current_header = "Introduction"

    for line in lines:
        if line.strip().startswith('#'):
            # Save the previous section
            if current_section:
                sections.append({
                    'header': current_header,
                    'content': '\n'.join(current_section)
                })
            # Start a new section
            current_header = line.strip('# ').strip()
            current_section = [line]
        else:
            current_section.append(line)

    # Add the last section
    if current_section:
        sections.append({
            'header': current_header,
            'content': '\n'.join(current_section)
        })

    # Now chunk each section
    chunks = []
    for section in sections:
        section_chunks = chunk_text(section['content'], chunk_size, overlap)
        for i, chunk in enumerate(section_chunks):
            chunks.append({
                'content': chunk,
                'metadata': {
                    'section': section['header'],
                    'chunk_index': i,
                    'total_chunks': len(section_chunks)
                }
            })

    return chunks


def chunk_mdx_content(content: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split MDX content into chunks while preserving document structure.
    This function handles MDX files which contain frontmatter.

    Args:
        content: MDX content to chunk
        chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of overlapping characters between chunks

    Returns:
        List of chunk dictionaries with content and metadata
    """
    # Extract frontmatter if it exists
    frontmatter = None
    main_content = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            main_content = parts[2]

    # Parse frontmatter to get title and other metadata
    title = "Unknown Chapter"
    if frontmatter:
        title_match = re.search(r'title:\s*["\']?(.*?)["\']?', frontmatter)
        if title_match:
            title = title_match.group(1)

    # Now chunk the main content
    lines = main_content.split('\n')
    sections = []
    current_section = []
    current_header = "Introduction"

    for line in lines:
        if line.strip().startswith('#'):
            # Save the previous section
            if current_section:
                sections.append({
                    'header': current_header,
                    'content': '\n'.join(current_section)
                })
            # Start a new section
            current_header = line.strip('# ').strip()
            current_section = [line]
        else:
            current_section.append(line)

    # Add the last section
    if current_section:
        sections.append({
            'header': current_header,
            'content': '\n'.join(current_section)
        })

    # Now chunk each section
    chunks = []
    for section in sections:
        section_chunks = chunk_text(section['content'], chunk_size, overlap)
        for i, chunk in enumerate(section_chunks):
            chunk_metadata = {
                'title': title,
                'section': section['header'],
                'chunk_index': i,
                'total_chunks': len(section_chunks)
            }

            # Add any additional frontmatter metadata
            if frontmatter:
                sidebar_match = re.search(r'sidebar_position:\s*(\d+)', frontmatter)
                if sidebar_match:
                    chunk_metadata['chapter_number'] = int(sidebar_match.group(1))

            chunks.append({
                'content': chunk,
                'metadata': chunk_metadata
            })

    return chunks


def create_chunks_from_file(file_path: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Create chunks from a file, automatically detecting content type.

    Args:
        file_path: Path to the file to chunk
        chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of overlapping characters between chunks

    Returns:
        List of chunk dictionaries with content and metadata
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if file_path.lower().endswith('.mdx'):
        return chunk_mdx_content(content, chunk_size, overlap)
    elif file_path.lower().endswith(('.md', '.markdown')):
        return chunk_markdown_content(content, chunk_size, overlap)
    else:
        # Default to plain text chunking
        chunks = chunk_text(content, chunk_size, overlap)
        return [{'content': chunk, 'metadata': {'source': file_path}} for chunk in chunks]


logger = logging.getLogger(__name__)