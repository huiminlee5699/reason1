import streamlit as st
import time
import random
from openai import OpenAI

def generate_reasoning_steps_for_credibility_task():
    """Generate realistic reasoning steps for the social media credibility evaluation task."""
    
    reasoning_steps = [
        "I need to evaluate this social media post about green tea and cancer prevention for credibility. Let me break down the claims systematically.",
        
        "First, I'll examine the specific claims: 1) A peer-reviewed Stanford study exists, 2) 50,000 participants over 10 years, 3) 87% cancer risk reduction from 3 cups daily, 4) 'Big Pharma doesn't want you to know.'",
        
        "Checking the methodology claims: A 10-year study with 50,000 participants sounds plausible for epidemiological research, but I need to verify if such a study actually exists from Stanford.",
        
        "The 87% risk reduction is an extremely high effect size that would be groundbreaking if true. Such dramatic results would typically be widely reported in major medical journals and news outlets.",
        
        "Red flags I'm noticing: 1) The 'Big Pharma conspiracy' language, 2) Urgency to 'share before they take it down,' 3) Hashtags like #GreenTeaCure suggest oversimplification, 4) No citation of the actual study.",
        
        "I should also consider what legitimate research says about green tea and cancer. While some studies suggest modest benefits, the scientific consensus doesn't support such dramatic claims.",
        
        "The post uses persuasive but unscientific language patterns common in health misinformation: definitive claims ('proves'), conspiracy theories, and emotional appeals.",
        
        "Based on my analysis, this appears to be misleading health information that could potentially harm people by promoting false hope or delaying proper medical care."
    ]
    
    return reasoning_steps

# Custom CSS for clean, minimal ChatGPT-like interface
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    
    .main-title {
        text-align: center;
        font-size: 28px;
        font-weight: 400;
        color: #2d2d2d;
        margin-bottom: 30px;
        margin-top: 20px;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .reasoning-block {
        background-color: #f8f9fa;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        color: #2d2d2d;
        animation: fadeIn 0.3s ease-in;
        max-width: 80%;
        text-align: left;
    }
    
    .user-message {
        background-color: #f0f0f0;
        border: 1px solid #d1d5db;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0 8px auto;
        max-width: 70%;
        text-align: left;
        font-size: 14px;
        color: #2d2d2d;
    }
    
    .assistant-message {
        background-color: white;
        padding: 12px 0;
        margin: 8px 0;
        max-width: 100%;
        text-align: left;
        font-size: 14px;
        color: #2d2d2d;
    }
    
    .action-buttons {
        display: flex;
        gap: 8px;
        margin-top: 12px;
        padding-top: 8px;
        justify-content: flex-start;
    }
    
    .action-button {
        background: none;
        border: none;
        cursor: pointer;
        padding: 6px;
        border-radius: 4px;
        color: #9ca3af;
        font-size: 16px;
        transition: background-color 0.2s;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .action-button:hover {
        background-color: #f3f4f6;
        color: #6b7280;
    }
    
    .done-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #10b981;
        font-size: 14px;
        margin-top: 12px;
        font-weight: 500;
    }
    
    .fade-transition {
        animation: fadeOut 0.2s ease-out, fadeIn 0.2s ease-in 0.2s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0.3; }
    }
    
    /* Hide default Streamlit chat styling */
    .stChatMessage {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stChatMessage > div {
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Center the chat input initially */
    .initial-input-container {
        display: flex;
        justify-content: center;
        margin: 40px 0;
    }
    
    .stChatInput {
        max-width: 600px;
    }
</style>
""", unsafe_allow_html=True)

# Show title
st.markdown('<h1 class="main-title">What\'s on the agenda today?</h1>', unsafe_allow_html=True)

# Use the API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []



# Display existing messages with custom styling
for message in st.session_state.messages:
    if message["role"] == "user":
        # User message - right aligned, light grey
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message - left aligned
        st.markdown(f"""
        <div class="assistant-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        # If it's an assistant message with reasoning, show the dropdown
        if "reasoning" in message:
            thinking_duration = message.get("thinking_duration", 0)
            with st.expander(f"Thought for {thinking_duration} seconds"):
                for i, step in enumerate(message["reasoning"], 1):
                    st.markdown(f"**Step {i}:** {step}")
                
                # Add "Done" indicator at the end
                st.markdown("""
                <div class="done-indicator">
                    ✓ Done
                </div>
                """, unsafe_allow_html=True)
            
            # Add action buttons (copy, upvote, downvote)
            st.markdown("""
            <div class="action-buttons">
                <button class="action-button" onclick="navigator.clipboard.writeText(document.querySelector('.assistant-message').innerText)" title="Copy">
                    📋
                </button>
                <button class="action-button" title="Upvote">
                    👍
                </button>
                <button class="action-button" title="Downvote">
                    👎
                </button>
            </div>
            """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything..."):
    # Add user message - will be displayed with custom styling above
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Force a rerun to show the user message first
    st.rerun()
    
# Generate AI response if there's a new user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Generate reasoning steps for the credibility task
    reasoning_steps = generate_reasoning_steps_for_credibility_task()
    
    # Track timing for the "Thought for X seconds" feature
    start_time = time.time()
    
    # Display reasoning steps with blinking animation (each one replaces the previous)
    reasoning_container = st.empty()
    for i, step in enumerate(reasoning_steps):
        # Show reasoning step
        reasoning_container.markdown(f"""
        <div class="reasoning-block">
            {step}
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(2.0)  # Time to read the reasoning step
        
        # Brief fade effect before next step
        if i < len(reasoning_steps) - 1:  # Don't fade the last step
            reasoning_container.markdown(f"""
            <div class="reasoning-block fade-transition">
                {step}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.4)  # Brief fade duration
    
    # Clear the reasoning container
    reasoning_container.empty()
    
    # Calculate total thinking time
    end_time = time.time()
    thinking_duration = int(end_time - start_time)
    
    # Get actual response from OpenAI
    try:
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Capture the response
        response_placeholder = st.empty()
        full_response = ""
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(f"""
                <div class="assistant-message">
                    {full_response}
                </div>
                """, unsafe_allow_html=True)
        
        # Add the "Thought for X seconds" dropdown after the response
        with st.expander(f"Thought for {thinking_duration} seconds"):
            for i, step in enumerate(reasoning_steps, 1):
                st.markdown(f"**Step {i}:** {step}")
            
            # Add "Done" indicator at the end
            st.markdown("""
            <div class="done-indicator">
                ✓ Done
            </div>
            """, unsafe_allow_html=True)
        
        # Add action buttons (copy, upvote, downvote)
        st.markdown("""
        <div class="action-buttons">
            <button class="action-button" onclick="navigator.clipboard.writeText(document.querySelector('.assistant-message').innerText)" title="Copy">
                📋
            </button>
            <button class="action-button" title="Upvote">
                👍
            </button>
            <button class="action-button" title="Downvote">
                👎
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        # Store message with reasoning and timing
        message_data = {
            "role": "assistant", 
            "content": full_response, 
            "reasoning": reasoning_steps,
            "thinking_duration": thinking_duration
        }
        st.session_state.messages.append(message_data)
        
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
