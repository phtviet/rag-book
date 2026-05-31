import re
from pypdf import PdfReader

def clean_text(text: str) -> str:
    """Apply minimal cleanup to extracted PDF text."""
    # Rejoin words split across lines by hyphenation
    # Pattern: word ending in hyphen, followed by whitespace, followed by word
    # We handle both regular hyphen and the unicode soft hyphen
    text = re.sub(r'(\w+)[‐-]\s+(\w+)', r'\1\2', text)
    
    # Collapse multiple consecutive whitespace into single space
    # but preserve paragraph breaks (double newlines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def extract_book(pdf_path: str, skip_front_pages: int = 0, skip_back_pages: int = 0):
    """Extract text from a PDF, returning a list of (page_number, text) tuples."""
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    pages = []
    start = skip_front_pages
    end = total_pages - skip_back_pages
    
    for page_num in range(start, end):
        raw_text = reader.pages[page_num].extract_text()
        cleaned = clean_text(raw_text)
        # Skip pages that came out mostly empty (covers, blank pages)
        if len(cleaned) < 50:
            continue
        # page_num is zero-indexed internally; store as 1-indexed for humans
        pages.append((page_num + 1, cleaned))
    
    return pages


if __name__ == "__main__":
    pdf_path = "ai_engineering.pdf"
    
    # Skip the cover, copyright, dedication, TOC (roughly first 20 pages)
    # and skip the back-cover marketing page (last 1 page)
    # These numbers are eyeballed; we can refine if needed.
    pages = extract_book(pdf_path, skip_front_pages=20, skip_back_pages=1)
    
    print(f"Extracted {len(pages)} content pages.")
    print(f"Total characters: {sum(len(text) for _, text in pages):,}")
    print()
    
    # Sanity check: print a sample of pages
    sample_indices = [0, len(pages) // 2, len(pages) - 1]
    for idx in sample_indices:
        page_num, text = pages[idx]
        print(f"=" * 70)
        print(f"Book page {page_num} ({len(text)} chars)")
        print(f"=" * 70)
        print(text[:400])
        print()