import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def process_posts(raw_file_path, processed_file_path=None):
    """
    Reads a JSON file, cleans the content, enriches it with metadata, and saves.
    """
    # --- STAGE 1 CLEANING: Read file and replace byte-level errors ---
    # This is the most robust way to read a potentially corrupted file.
    # It reads the raw bytes and replaces any invalid sequences.
    with open(raw_file_path, 'rb') as file:
        raw_data = file.read()
    file_content = raw_data.decode('utf-8', errors='replace')
    posts = json.loads(file_content)
    # --- END STAGE 1 ---

    enriched_posts = []
    print(f"Found {len(posts)} posts to process...")
    for i, post in enumerate(posts):
        print(f"Processing post {i+1}/{len(posts)}...")
        # Pass the text to the next function for the final cleaning stage
        metadata = extract_metadata(post['text'])
        post_with_metadata = post | metadata
        enriched_posts.append(post_with_metadata)

    print("Unifying tags...")
    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post.get('tags', [])
        if unified_tags and isinstance(current_tags, list):
            new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
            post['tags'] = list(new_tags)

    with open(processed_file_path, mode="w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4, ensure_ascii=False)

    print(f"Successfully processed and saved data to {processed_file_path}")


def extract_metadata(post_text):
    """Extracts metadata after performing the final cleaning for the API call."""

    # --- STAGE 2 CLEANING: Heal character-level errors before the API call ---
    # This 'surrogatepass' handler is specifically designed to fix the
    # 'surrogates not allowed' error from your traceback. It finds and
    # repairs any characters that Stage 1 could not fix.
    cleaned_post = post_text.encode('utf-8', 'surrogatepass').decode('utf-8')
    # --- END STAGE 2 ---

    template = '''
    You are given a LinkedIn post. You need to extract metadata.
    CRITICAL: Your response MUST be ONLY a raw JSON object with keys "line_count", "language", and "tags".
    Here is the post:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    # Use the fully cleaned variable for the API call
    response = chain.invoke(input={"post": cleaned_post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as e:
        print(f"Warning: Could not parse LLM output. Error: {e}. Skipping.")
        return {"line_count": 0, "language": "Unknown", "tags": []}
    return res


def get_unified_tags(posts_with_metadata):
    """Unifies tags using an LLM."""
    unique_tags = set()
    for post in posts_with_metadata:
        if 'tags' in post and isinstance(post['tags'], list):
            unique_tags.update(post['tags'])
    if not unique_tags:
        return {}

    unique_tags_list = ','.join(unique_tags)
    template = '''Unify these tags. Your output MUST be ONLY a raw JSON object
    mapping original tags to unified tags. Example: {{"Job Hunting": "Job Search"}}
    Tags: {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as e:
        print(f"Warning: Could not unify tags. Error: {e}. Skipping.")
        return {}
    return res


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")