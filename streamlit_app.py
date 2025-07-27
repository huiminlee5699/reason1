import streamlit as st
import time
import random
from openai import OpenAI

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

# Get API key from secrets or user input
openai_api_key = st.secrets.get("OPENAI_API_KEY", None)

if not openai_api_key:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_reasoning" not in st.session_state:
        st.session_state.show_reasoning = True
    
    # Sidebar controls for research conditions
    with st.sidebar:
        st.header("Research Controls")
        st.session_state.show_reasoning = st.checkbox("Show Reasoning Process", value=True)
        reasoning_length = st.selectbox("Reasoning Detail Level", ["Short", "Medium", "Long"])
        reasoning_speed = st.slider("Reasoning Speed (seconds between steps)", 0.5, 3.0, 1.5)
    
    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "reasoning" in message:
                # Display reasoning blocks if they exist
                for reasoning_step in message["reasoning"]:
                    st.markdown(f"""
                    <div class="reasoning-block">
                        <div class="reasoning-header">🧠 Reasoning Step</div>
                        {reasoning_step}
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response with reasoning
        with st.chat_message("assistant"):
            reasoning_steps = []
            
            if st.session_state.show_reasoning:
                # Generate reasoning steps based on the prompt
                reasoning_steps = generate_reasoning_steps(prompt, reasoning_length)
                
                # Display reasoning steps with animation
                reasoning_containers = []
                for i, step in enumerate(reasoning_steps):
                    container = st.empty()
                    reasoning_containers.append(container)
                    
                    # Show thinking indicator
                    container.markdown(f"""
                    <div class="thinking-indicator">
                        🧠 Thinking<span class="dot-animation">...</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(reasoning_speed)
                    
                    # Show reasoning step
                    container.markdown(f"""
                    <div class="reasoning-block">
                        <div class="reasoning-header">🧠 Reasoning Step {i+1}</div>
                        {step}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Generate final response
            if st.session_state.show_reasoning:
                thinking_container = st.empty()
                thinking_container.markdown("""
                <div class="thinking-indicator">
                    🤖 Generating final response<span class="dot-animation">...</span>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
                thinking_container.empty()
            
            # Get actual response from OpenAI
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            response = st.write_stream(stream)
            
            # Store message with reasoning
            message_data = {"role": "assistant", "content": response}
            if st.session_state.show_reasoning:
                message_data["reasoning"] = reasoning_steps
            
            st.session_state.messages.append(message_data)


def generate_reasoning_steps(prompt, length="Medium"):
    """Generate simulated reasoning steps based on the prompt and desired length."""
    
    # Base reasoning templates
    analysis_steps = [
        f"I need to analyze the question: '{prompt}'",
        "Let me break this down into key components",
        "I should consider multiple perspectives on this topic",
        "I need to draw from relevant knowledge and examples"
    ]
    
    domain_specific = []
    prompt_lower = prompt.lower()
    
    # Add domain-specific reasoning based on prompt content
    if any(word in prompt_lower for word in ["calculate", "math", "number", "compute"]):
        domain_specific.extend([
            "This appears to be a mathematical or computational problem",
            "I should identify the relevant formulas or methods",
            "Let me work through this step by step"
        ])
    elif any(word in prompt_lower for word in ["explain", "what is", "how does"]):
        domain_specific.extend([
            "This is a request for explanation or definition",
            "I should provide clear, accurate information",
            "I'll structure this in a logical, easy-to-follow way"
        ])
    elif any(word in prompt_lower for word in ["compare", "difference", "versus"]):
        domain_specific.extend([
            "This requires a comparative analysis",
            "I should identify key similarities and differences",
            "I'll organize this comparison systematically"
        ])
    elif any(word in prompt_lower for word in ["recommend", "suggest", "should I"]):
        domain_specific.extend([
            "This is asking for recommendations or advice",
            "I should consider multiple factors and options",
            "I need to provide balanced, helpful guidance"
        ])
    else:
        domain_specific.extend([
            "Let me consider the context and implications",
            "I should provide a comprehensive response",
            "I'll ensure my answer is helpful and accurate"
        ])
    
    synthesis_steps = [
        "Now I'll synthesize this information into a coherent response",
        "I should ensure my answer directly addresses the question",
        "Let me verify this reasoning makes sense"
    ]
    
    all_steps = analysis_steps + domain_specific + synthesis_steps
    
    # Adjust based on length preference
    if length == "Short":
        return random.sample(all_steps, min(3, len(all_steps)))
    elif length == "Medium":
        return random.sample(all_steps, min(5, len(all_steps)))
    else:  # Long
        return all_steps[:7]  # Take first 7 to maintain logical flow
