import streamlit as st
import openai

# Set OpenAI API Key (Replace with your own key)
openai.api_key = "your-api-key-here"

# Function to generate AI-powered blog content
def generate_blog_post(topic, tone):
    prompt = f"""
    Write a blog post about {topic} in a {tone} tone. Include:
    - A strong introduction
    - Key points with explanations
    - A compelling conclusion
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional blog writer."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("📝 AI-Powered Blog & Article Generator")

topic = st.text_input("Enter a Topic:")
tone = st.selectbox("Select a Writing Tone:", ["Casual", "Professional", "Humorous"])

if st.button("Generate Blog Post"):
    if topic:
        blog_post = generate_blog_post(topic, tone)
        st.subheader("Generated Blog Post:")
        st.write(blog_post)
        
        # Allow download of the generated content
        st.download_button(
            label="Download Blog Post",
            data=blog_post,
            file_name="blog_post.txt",
            mime="text/plain"
        )
    else:
        st.error("Please enter a topic to generate a blog post.")
