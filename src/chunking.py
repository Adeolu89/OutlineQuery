from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
import re

# Alternative: Simple but effective approach for your specific case
def parse_course_outline_simple(html_content: str):
    """Simple approach that preserves structure for course schedules"""
    

    soup = BeautifulSoup(html_content, "html.parser")
    
    # Get TOC structure
    toc_links = soup.select("aside.outline-toc a[href^='#']")
    toc_ids = [link["href"].lstrip("#") for link in toc_links]
    
    sections = {}
    
    for link in toc_links:
        section_id = link["href"].lstrip("#")
        section_name = link.get_text(strip=True)
        
        header = soup.find(id=section_id)
        if not header:
            continue
        
        # Find the next header to know where to stop
        next_header = None
        for next_link in toc_links[toc_links.index(link) + 1:]:
            next_header = soup.find(id=next_link["href"].lstrip("#"))
            if next_header:
                break
        
        # Get all text between this header and the next
        content_parts = []
        current = header
        
        while current and current != next_header:
            if hasattr(current, 'get_text'):
                text = current.get_text(separator=' ', strip=True)
                if text and len(text) > 10:
                    # Skip if it's just the header text repeated
                    if text != section_name:
                        content_parts.append(text)
            current = current.next_sibling
            if current is None:
                # If we've reached the end, get remaining elements
                for remaining in header.find_all_next():
                    if next_header and remaining == next_header:
                        break
                    if hasattr(remaining, 'get_text'):
                        text = remaining.get_text(separator=' ', strip=True)
                        if text and len(text) > 10 and text != section_name:
                            content_parts.append(text)
                break
        
        # Simple deduplication: remove exact duplicates while preserving order
        seen = set()
        unique_parts = []
        for part in content_parts:
            # Normalize whitespace for comparison
            normalized = ' '.join(part.split())
            if normalized not in seen and len(normalized) > 15:
                seen.add(normalized)
                unique_parts.append(part)
        
        if unique_parts:
            sections[section_name] = '\n'.join(unique_parts)
    
    return sections

def advanced_deduplicate_text(text):
    """More sophisticated text deduplication"""
    lines = text.split('\n')
    unique_lines = []
    seen_normalized = set()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Normalize for comparison (remove punctuation, lowercase)
        normalized = re.sub(r'[^\w\s]', '', line.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        # Skip very short lines
        if len(normalized) < 5:
            continue
        
        # Check for substantial overlap with existing lines
        is_duplicate = False
        for seen in seen_normalized:
            # Check if lines are very similar (>80% overlap)
            words1 = set(normalized.split())
            words2 = set(seen.split())
            if len(words1) > 0 and len(words2) > 0:
                overlap = len(words1.intersection(words2))
                similarity = overlap / max(len(words1), len(words2))
                if similarity > 0.8:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            seen_normalized.add(normalized)
            unique_lines.append(line)
    
    return '\n'.join(unique_lines)

def create_chunks_improved(sections):
    """Create chunks with better preprocessing"""
    processed_sections = {}
    
    for name, content in sections.items():
        # Apply advanced deduplication
        cleaned_content = advanced_deduplicate_text(content)
        processed_sections[name] = cleaned_content
    
    docs = [
        Document(page_content=content, metadata={"section": name})
        for name, content in processed_sections.items()
        if content.strip()  # Only include non-empty sections
    ]
    
    splitter = CharacterTextSplitter(
        chunk_size=1100,
        chunk_overlap=50,  # Reduced overlap since content is cleaner
        separator='.'
    )
    
    chunked_docs = splitter.split_documents(docs)
    return chunked_docs
