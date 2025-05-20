import streamlit as st

# Force Python to use pysqlite3 instead of system SQLite
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# # Now apply no_chroma_patch and continue
# import no_chroma_patch
import os

os.environ["CHROMA_DB_IMPL"] = "duckdb"

from crewai import Crew, Process
from agents import news_researcher, news_writer
from tasks import research_task, write_task
import os
import re

# Page config
st.set_page_config(page_title="AI Content Generator", page_icon="🤖")

# Reduce spacing with custom CSS
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    div[data-testid="stMarkdownContainer"] > p { margin-bottom: 0.3rem; }
    h1, h2, h3 { margin-top: 0.8rem; margin-bottom: 0.5rem; }
    .simple-text {
        font-family: sans-serif;
        line-height: 1.5;
        color: black;
        background: none;
        padding: 0;
        border: none;
        font-size: 1rem;
    }
    /* Equal spacing between all paragraphs */
    .simple-text p {
        margin-top: 0;
        margin-bottom: 0.7rem; /* Consistent small space between paragraphs */
    }
</style>
""", unsafe_allow_html=True)

# Helper function to clean the output text
def clean_output(text):
    # Remove markdown code blocks (```markdown, ```, etc.)
    text = re.sub(r'```[\w]*\n', '', text)
    text = re.sub(r'```', '', text)
    
    # Remove excessive newlines (more than 2 in a row)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove any special markdown headings
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Format for HTML rendering with paragraphs
    # Convert paragraph breaks to HTML paragraph tags
    formatted_html = text.replace('\n\n', '</p><p>')
    formatted_html = '<p>' + formatted_html + '</p>'
    
    return formatted_html

# Sidebar for API keys
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    
    # Toggle for showing/hiding API key inputs
    show_keys = st.checkbox("Show API Key Fields", value=False)
    
    if show_keys:
        google_key = st.text_input("Google API Key", type="password", 
                                  value=os.environ.get("GOOGLE_API_KEY", ""))
        serper_key = st.text_input("Serper API Key", type="password",
                                  value=os.environ.get("SERPER_API_KEY", ""))
        
        if google_key:
            os.environ["GOOGLE_API_KEY"] = google_key
        if serper_key:
            os.environ["SERPER_API_KEY"] = serper_key
            
        st.info("API keys are stored only for this session")
    else:
        st.text("Check the box above to configure API keys")
    
    # Add instructions
    st.markdown("---")
    st.markdown("### 💡 How it works")
    st.markdown("""
    1. Enter a research topic
    2. Click Generate
    3. AI agents will research and write
    4. Download your article
    """)

# Main content
st.title("🤖 AI Content Generator")
st.markdown("Create research articles with AI agents 🔍✏️")

# Topic input with emoji
topic = st.text_input("🔎 Research Topic:", placeholder="AI in healthcare")

# Generate button with emoji
if st.button("🚀 Generate", disabled=not topic, type="primary"):
    if not os.environ.get("GOOGLE_API_KEY") or not os.environ.get("SERPER_API_KEY"):
        st.error("⚠️ Please configure API keys in the sidebar")
    else:
        try:
            # Show simple progress message
            with st.spinner("🤖 AI agents are working on your content..."):
                # Create and execute crew
                crew = Crew(
                    agents=[news_researcher, news_writer],
                    tasks=[research_task, write_task],
                    process=Process.sequential,
                    verbose=True
                )
                
                result = crew.kickoff(inputs={'topic': topic})
                
                # Extract content
                try:
                    if hasattr(result, 'raw'):
                        content = result.raw
                    elif hasattr(result, 'output'):
                        content = result.output
                    else:
                        content = str(result)
                except:
                    content = str(result)
                
                # Clean and format the content
                formatted_content = clean_output(content)
                
                # Create plain text version for download
                plain_content = formatted_content.replace('<p>', '').replace('</p>', '\n\n').strip()
            
            # Success message
            st.success("✅ Content generated!")
            
            # Display article header
            st.markdown(f"### 📄 Article: {topic}")
            
            # Display as custom HTML with cleaned content
            st.markdown(f'<div class="simple-text">{formatted_content}</div>', unsafe_allow_html=True)
            
            # Download button (use plain content for download)
            st.download_button(
                "📥 Download Article",
                plain_content,
                file_name=f"{topic.replace(' ', '-')}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Simple footer
st.caption("Built with CrewAI and Streamlit")
