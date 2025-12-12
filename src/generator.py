import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate

def generate_blog(topic: str) -> dict:
    """
    Generates a blog post title and content based on the given topic
    using a HuggingFace Chat model.
    """
    
    if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables.")

    # 1. Configure the Endpoint
    repo_id = "HuggingFaceH4/zephyr-7b-beta" 
    
    endpoint = HuggingFaceEndpoint(
        repo_id=repo_id,
        task="text-generation", # The endpoint class requires this, but we wrap it
        max_new_tokens=1024,
        temperature=0.7,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )

    # 2. Wrap in ChatHuggingFace
    # This handles the "conversational" formatting
    chat_llm = ChatHuggingFace(llm=endpoint)

    # 3. Define Chat Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert blog writer. Write a comprehensive and engaging blog post."),
        ("human", "Topic: {topic}\n\nPlease format the output as:\nTitle: [Title]\n\n[Body]")
    ])
    
    # 4. Create Chain
    chain = prompt | chat_llm
    
    # 5. Run Chain
    result = chain.invoke({"topic": topic})
    
    # Result is an AIMessage
    content_text = result.content

    # 6. Parse Output
    lines = content_text.strip().split('\n')
    title = "Untitled"
    content = content_text
    
    for i, line in enumerate(lines):
        if line.lower().startswith("title:"):
            title = line[6:].strip()
            content = "\n".join(lines[i+1:]).strip()
            break
            
    return {
        "title": title,
        "content": content
    }

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print(generate_blog("The Future of AI Agents"))

