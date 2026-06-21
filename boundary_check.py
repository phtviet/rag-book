# boundary_check.py to check where the index begins and ends
from extract import extract_book

pages = extract_book("ai_engineering.pdf", skip_front_pages=20, skip_back_pages=1)
page_dict = {pn: text for pn, text in pages}

for pn in [519, 520, 521, 522, 533, 534, 535]:
    if pn in page_dict:
        preview = page_dict[pn][:100].replace("\n", " ")
        print(f"page {pn}: {preview}...")
    else:
        print(f"page {pn}: (not in corpus)")

# Check on Page 519 and 534 specifically
from pypdf import PdfReader

reader = PdfReader("ai_engineering.pdf")
for pdf_idx in [519, 534]:   # 0-indexed: corresponds to "page 520" and "page 535"
    raw = reader.pages[pdf_idx].extract_text()
    print(f"PDF index {pdf_idx} (book page {pdf_idx+1}): {len(raw)} chars")
    print(repr(raw[:120]))
    print()