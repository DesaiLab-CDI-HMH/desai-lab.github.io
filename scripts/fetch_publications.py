import yaml
import os
from scholarly import scholarly

# Replace with your actual Google Scholar ID
scholar_id = "hhKlTYYAAAAJ"

# Fetch author data
author = scholarly.search_author_id(scholar_id)
filled_author = scholarly.fill(author, sections=["publications"])

publications = []
for pub in filled_author['publications']:
    try:
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get('bib', {})
        title = bib.get('title', '')
        authors = bib.get('author', '')
        venue = bib.get('venue', '')
        year = bib.get('pub_year', '')
        link = pub_filled.get('eprint_url', '')

        publications.append({
            'title': title,
            'authors': authors,
            'venue': venue,
            'year': year,
            'link': link
        })
    except Exception as e:
        print(f"Error processing publication: {e}")
        continue

# Path to write the YAML file (corrected path!)
output_path = "/Users/Jigar/lab-website/desailab-site/_data/publications.yml"

# Ensure the _data directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write to YAML
with open(output_path, 'w') as f:
    yaml.dump(publications, f, allow_unicode=True, sort_keys=False)

print(f"✅ Saved {len(publications)} publications to {output_path}")
