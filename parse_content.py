import json
import os

def parse_content_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by end-block delimiter
    blocks = content.split('===')
    
    poems = []
    prose = []
    quotes = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Split header and body
        parts = block.split('---')
        if len(parts) < 2:
            print(f"Skipping malformed block (missing '---'): {block[:50]}...")
            continue
            
        header_text = parts[0].strip()
        body_text = "---".join(parts[1:]).strip() # Rejoin rest in case body has ---
        
        # Parse headers
        headers = {}
        for line in header_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                headers[key.strip().lower()] = val.strip()
        
        entry_type = headers.get('type', '').lower()
        title = headers.get('title', 'Untitled')
        year = headers.get('year', '2024')
        
        entry = {
            'title': title,
            'year': year,
            'type': entry_type.capitalize()
        }

        if entry_type == 'poem':
            entry['body'] = f"<p>{body_text.replace(chr(10), '<br>')}</p>"
            poems.append(entry)
            
        elif entry_type == 'prose':
            # Prose formatting: 
            # 1. Split by double newlines to find paragraphs
            paragraphs = body_text.split('\n\n')
            
            # 2. For each paragraph, replace single newlines with spaces (unwrapping) and wrap in <p>
            formatted_paragraphs = []
            for p in paragraphs:
                if p.strip():
                    # Replace single newlines within a paragraph with a space
                    clean_p = p.replace('\n', ' ').strip()
                    formatted_paragraphs.append(f"<p>{clean_p}</p>")
            
            entry['body'] = "".join(formatted_paragraphs)
            prose.append(entry)
            
        elif entry_type == 'quote':
            entry['body'] = f"<p>{body_text}</p>"
            quotes.append(entry)

    return poems, prose, quotes

def parse_all_content(source_dir='content_source'):
    all_poems = []
    all_prose = []
    all_quotes = []

    if not os.path.exists(source_dir):
        print(f"Directory {source_dir} not found. Creating it...")
        os.makedirs(source_dir)
        return [], [], []

    # Walk through all files in the directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Parsing: {file_path}")
                try:
                    p, pr, q = parse_content_file(file_path)
                    all_poems.extend(p)
                    all_prose.extend(pr)
                    all_quotes.extend(q)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    return all_poems, all_prose, all_quotes

if __name__ == "__main__":
    poems, prose, quotes = parse_all_content('content_source')
    
    # Create content directory if not exists
    if not os.path.exists('content'):
        os.makedirs('content')
        
    # Standard fallback quotes if none found anywhere
    if not quotes:
         quotes = [
            {
                "title": "On Resilience",
                "body": "<p>\"We are not defined by how we fall, but how we choose to rise.\"</p>",
                "type": "Quote",
                "year": "2024"
            },
            {
                "title": "The Blank Page",
                "body": "<p>\"The blank page is not a void, but a vast expanse of possibility waiting for the first step.\"</p>",
                "type": "Quote",
                "year": "2024"
            }
        ]

    data = {
        "poems": poems,
        "prose": prose,
        "quotes": quotes
    }
    
    with open('content/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated content/data.json from {len(poems)} poems, {len(prose)} prose, {len(quotes)} quotes.")

