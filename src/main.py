import argparse
import os
import sys
import time
from dotenv import load_dotenv

# Ensure we can import from src if running from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import generate_blog

def ensure_output_dir():
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def save_to_file(topic, data):
    output_dir = ensure_output_dir()
    # Sanitize topic for filename
    safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"Blog_{safe_topic}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {data['title']}\n\n")
        f.write(data['content'])
        
    return filepath

def main():
    # 1. Load Enviroment Variables
    load_dotenv()
    
    # 2. Parse Arguments
    parser = argparse.ArgumentParser(description="AI Blog Agent: Generate blogs locally.")
    parser.add_argument("topic", help="The topic of the blog post to generate.")
    parser.add_argument("--dry-run", action="store_true", help="Generate and print to console only, do not save.")
    
    args = parser.parse_args()
    
    # 3. Generate Content
    print(f"Generating blog post on topic: '{args.topic}'...")
    try:
        blog_data = generate_blog(args.topic)
        print("\n--- Generated Content ---")
        print(f"Title: {blog_data['title']}")
        print(f"Content Length: {len(blog_data['content'])} chars")
        print("-------------------------\n")
    except Exception as e:
        print(f"Error generating blog: {e}")
        return

    if args.dry_run:
        print("Dry run completed. Output not saved.")
        return

    # 4. Save to File
    print(f"Saving to file...")
    try:
        filepath = save_to_file(args.topic, blog_data)
        print(f"Successfully saved blog post to:\n{filepath}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
