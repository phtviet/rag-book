from extract import extract_book

def digit_ratio(text: str) -> float:
    """Fraction of characters that are digits. Index pages score very high."""
    if not text:
        return 0.0
    digits = sum(1 for c in text if c.isdigit())
    return digits / len(text)


if __name__ == "__main__":
    # Use the SAME extraction as the current index, so we're inspecting the real corpus.
    pages = extract_book("ai_engineering.pdf", skip_front_pages=20, skip_back_pages=1)

    # Score every page by digit density.
    scored = [(page_num, digit_ratio(text), text) for page_num, text in pages]

    # Sort by ratio, highest first — the most index-like pages float to the top.
    scored.sort(key=lambda x: x[1], reverse=True)

    print("Top 15 pages by digit ratio (likely index/junk):\n")
    for page_num, ratio, text in scored[:15]:
        preview = text[:90].replace("\n", " ")
        print(f"  page {page_num}: digit_ratio={ratio:.3f}  | {preview}...")

    print("\nFor contrast — 5 pages with LOW digit ratio (normal content):\n")
    for page_num, ratio, text in scored[-5:]:
        preview = text[:90].replace("\n", " ")
        print(f"  page {page_num}: digit_ratio={ratio:.3f}  | {preview}...")