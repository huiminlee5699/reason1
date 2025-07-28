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

# Custom CSS to make it look more like ChatGPT
st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f8;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .reasoning-block {
        background-color: #f1f1f1;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        font-family: 'SF Mono', Monaco, Inconsolata, 'Roboto Mono', Consolas, 'Courier New', monospace;
        font-size: 14px;
        color: #374151;
        animation: fadeIn 0.5s ease-in;
    }
    
    .reasoning-header {
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 8px;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .thinking-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #6b7280;
        font-style: italic;
        margin: 8px 0;
    }
    
    .dot-animation {
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 20% { opacity: 0; }
        50% { opacity: 1; }
        100% { opacity: 0; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Show title and description
st.title("🤖 AI Reasoning Chat")
st.write("Chat interface with visible AI reasoning process for research purposes.")

# Use the API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []



# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Display the final answer
        st.markdown(message["content"])
        
        # If it's an assistant message with reasoning, show the dropdown
        if message["role"] == "assistant" and "reasoning" in message:
            thinking_duration = message.get("thinking_duration", 0)
            with st.expander(f"💭 Thought for {thinking_duration} seconds"):
                for i, step in enumerate(message["reasoning"], 1):
                    st.markdown(f"**Step {i}:** {step}")

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate assistant response with reasoning
    with st.chat_message("assistant"):
        # Generate reasoning steps for the credibility task
        reasoning_steps = generate_reasoning_steps_for_credibility_task()
        
        # Track timing for the "Thought for X seconds" feature
        start_time = time.time()
        
        # Display reasoning steps with animation (each one replaces the previous)
        reasoning_container = st.empty()
        for i, step in enumerate(reasoning_steps):
            # Show thinking indicator
            reasoning_container.markdown(f"""
            <div class="thinking-indicator">
                🧠 Thinking<span class="dot-animation">...</span>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1.0)  # Brief thinking pause
            
            # Show reasoning step (replaces previous)
            reasoning_container.markdown(f"""
            <div class="reasoning-block">
                <div class="reasoning-header">🧠 Reasoning</div>
                {step}
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(2.0)  # Time to read the reasoning step
        
        # Clear the reasoning container
        reasoning_container.empty()
        
        # Calculate total thinking time
        end_time = time.time()
        thinking_duration = int(end_time - start_time)
        
        # Generate final response
        final_thinking_container = st.empty()
        final_thinking_container.markdown("""
        <div class="thinking-indicator">
            🤖 Generating final response<span class="dot-animation">...</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
        final_thinking_container.empty()
        
        # Get actual response from OpenAI
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        response = st.write_stream(stream)
        
        # Add the "Thought for X seconds" dropdown after the response
        with st.expander(f"💭 Thought for {thinking_duration} seconds"):
            for i, step in enumerate(reasoning_steps, 1):
                st.markdown(f"**Step {i}:** {step}")
        
        # Store message with reasoning and timing
        message_data = {
            "role": "assistant", 
            "content": response, 
            "reasoning": reasoning_steps,
            "thinking_duration": thinking_duration
        }
        st.session_state.messages.append(message_data)
