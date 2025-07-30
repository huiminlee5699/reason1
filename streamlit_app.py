import streamlit as st
import time
import asyncio

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

def get_fixed_response():
    """Return the fixed response for the credibility evaluation."""
    return """Based on my search of recent Stanford research and the broader scientific literature on green tea and cancer, **this post should be flagged as misleading**. Here's why:

**Red Flags in the Post:**
1. **No verifiable study found**: Despite searching Stanford's recent cancer research, I found no study matching these claims. Stanford researchers are currently working on AI cancer prediction tools, new surgical techniques, and immunotherapies - but nothing about green tea.
2. **Exaggerated language**: The use of "PROVES" is a major red flag. Scientific studies show "mixed" evidence for green tea's cancer-fighting properties, with some studies showing "promising correlations" while others "have found little to no significant impact on cancer incidence" Green tea and cancer | EBSCO Research Starters.
3. **Unrealistic claim**: An 87% reduction in cancer risk would be extraordinary and would be front-page news worldwide. Current research shows "mixed findings" for most cancer types and "mostly null association" for several others Green tea and cancer and cardiometabolic diseases: a review of the current epidemiological evidence | European Journal of Clinical Nutrition.
4. **Conspiracy theory elements**: "Big Pharma doesn't want you to know" and "Share before they take it down" are classic misinformation tactics designed to bypass critical thinking.

**What the Science Actually Shows:**
Research indicates green tea "may be linked to a reduced risk of certain cancers, particularly stomach cancer in populations with high green tea consumption" but "clinical evidence regarding green tea's cancer-fighting properties is mixed" Green tea and cancer | EBSCO Research Starters. For most cancer types, studies show "mixed findings" or "mostly null association" Green tea and cancer and cardiometabolic diseases: a review of the current epidemiological evidence | European Journal of Clinical Nutrition.

**Recommendations for Users:**
1. **Don't share** - This appears to be health misinformation
2. **Check sources** - Look for peer-reviewed studies with proper citations
3. **Be skeptical** of dramatic health claims with conspiracy elements
4. **Consult healthcare providers** for evidence-based health information

**Verdict**: This post is misleading and potentially harmful as it may encourage people to rely on unsubstantiated claims rather than proven cancer prevention methods."""

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
    
    .user-message {
        background-color: #f0f0f0;
        border: 1px solid #d1d5db;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0 8px auto;
        max-width: 70%;
        text-align: left;
        font-size: 16px;
        color: #2d2d2d;
        line-height: 1.5;
    }
    
    .assistant-message {
        background-color: white;
        padding: 12px 0;
        margin: 8px 0;
        max-width: 100%;
        text-align: left;
        font-size: 16px;
        color: #2d2d2d;
        line-height: 1.6;
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
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Auto-expanding chat input */
    .stChatInput {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Make container wider */
    .main .block-container {
        max-width: 1000px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Reasoning dropdown styling */
    .reasoning-dropdown {
        background-color: #f8f9fa !important;
        border: 1px solid #e1e5e9 !important;
        border-radius: 8px !important;
        margin: 16px 0 !important;
        animation: fadeIn 0.3s ease-in;
    }
    
    .reasoning-step {
        margin-bottom: 16px;
        padding: 12px;
        background-color: #ffffff;
        border-radius: 6px;
        border-left: 3px solid #e1e5e9;
        line-height: 1.5;
        font-size: 16px;
        color: #2d2d2d;
        animation: fadeIn 0.4s ease-out;
    }
    
    .thinking-header {
        color: #6b7280;
        font-size: 14px;
        font-weight: 500;
        padding: 16px;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        border-bottom: 1px solid #e1e5e9;
        margin: 0;
    }
    
    .reasoning-content {
        padding: 0 16px 16px 16px;
        background-color: #f8f9fa;
        border-radius: 0 0 8px 8px;
    }
    
    /* Style streamlit expander to match our design */
    details[data-testid="stExpander"] {
        background-color: #f8f9fa !important;
        border: 1px solid #e1e5e9 !important;
        border-radius: 8px !important;
        margin: 16px 0 !important;
        box-shadow: none !important;
    }
    
    details[data-testid="stExpander"] summary {
        padding: 16px !important;
        cursor: pointer !important;
        font-size: 14px !important;
        color: #6b7280 !important;
        border-radius: 8px !important;
        background-color: #f8f9fa !important;
        border: none !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }
    
    details[data-testid="stExpander"] summary:hover {
        background-color: #f1f3f4 !important;
        color: #4b5563 !important;
    }
    
    details[data-testid="stExpander"][open] summary {
        border-bottom: 1px solid #e1e5e9 !important;
        border-radius: 8px 8px 0 0 !important;
        margin-bottom: 0 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #f8f9fa !important;
        border: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 0 !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Show title
st.markdown('<h1 class="main-title">What\'s on the agenda today?</h1>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_reasoning_history" not in st.session_state:
    st.session_state.current_reasoning_history = []
if "reasoning_step_counter" not in st.session_state:
    st.session_state.reasoning_step_counter = 0
if "show_reasoning_live" not in st.session_state:
    st.session_state.show_reasoning_live = False
if "current_step_index" not in st.session_state:
    st.session_state.current_step_index = 0
if "reasoning_complete" not in st.session_state:
    st.session_state.reasoning_complete = False

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show reasoning dropdown if present
        if "reasoning" in message:
            thinking_duration = message.get("thinking_duration", 0)
            with st.expander(f"Thought for {thinking_duration} seconds", expanded=False):
                for i, step in enumerate(message["reasoning"], 1):
                    st.markdown(f"""
                    <div class="reasoning-step">
                        <strong>Step {i}:</strong> {step}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="done-indicator">
                    ✓ Done
                </div>
                """, unsafe_allow_html=True)
        
        # Assistant message
        st.markdown(f"""
        <div class="assistant-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        # Add action buttons
        st.markdown("""
        <div class="action-buttons">
            <button class="action-button" title="Copy">📋</button>
            <button class="action-button" title="Upvote">👍</button>
            <button class="action-button" title="Downvote">👎</button>
        </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show user message immediately
    st.markdown(f"""
    <div class="user-message">
        {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Reset reasoning state
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1
    st.session_state.show_reasoning_live = False
    st.session_state.current_step_index = 0
    st.session_state.reasoning_complete = False
    
    # Generate reasoning steps
    reasoning_steps = generate_reasoning_steps_for_credibility_task()
    
    # Track timing
    start_time = time.time()
    
    # Create the "Thinking..." dropdown
    thinking_expander = st.expander("Thinking...", expanded=False)
    
    # Check if user clicked the dropdown
    if thinking_expander:
        st.session_state.show_reasoning_live = True
    
    # If user opened the dropdown, show reasoning steps progressively
    if st.session_state.show_reasoning_live:
        with thinking_expander:
            reasoning_container = st.container()
            
            # Show reasoning steps progressively
            for i, step in enumerate(reasoning_steps):
                with reasoning_container:
                    # Show all previous steps plus current one
                    for j in range(i + 1):
                        st.markdown(f"""
                        <div class="reasoning-step">
                            <strong>Step {j + 1}:</strong> {reasoning_steps[j]}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Wait before showing next step
                time.sleep(2.5)
            
            # Show "Done" indicator
            st.markdown("""
            <div class="done-indicator">
                ✓ Done
            </div>
            """, unsafe_allow_html=True)
    
    # If user didn't open dropdown, just wait for the total duration
    else:
        total_wait_time = len(reasoning_steps) * 2.5
        time.sleep(total_wait_time)
    
    # Calculate thinking duration
    end_time = time.time()
    thinking_duration = int(end_time - start_time)
    
    # Clear the "Thinking..." and show final dropdown
    thinking_expander.empty()
    
    # Show final reasoning dropdown
    with st.expander(f"Thought for {thinking_duration} seconds", expanded=False):
        for i, step in enumerate(reasoning_steps, 1):
            st.markdown(f"""
            <div class="reasoning-step">
                <strong>Step {i}:</strong> {step}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="done-indicator">
            ✓ Done
        </div>
        """, unsafe_allow_html=True)
    
    # Get and display the response with typing effect
    fixed_response = get_fixed_response()
    response_placeholder = st.empty()
    displayed_response = ""
    
    # Split response into words for typing effect
    words = fixed_response.split(' ')
    
    for i, word in enumerate(words):
        displayed_response += word + ' '
        response_placeholder.markdown(f"""
        <div class="assistant-message">
            {displayed_response}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)  # Fast typing speed
    
    # Add action buttons
    st.markdown("""
    <div class="action-buttons">
        <button class="action-button" title="Copy">📋</button>
        <button class="action-button" title="Upvote">👍</button>
        <button class="action-button" title="Downvote">👎</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Store message with reasoning
    message_data = {
        "role": "assistant", 
        "content": fixed_response, 
        "reasoning": reasoning_steps,
        "thinking_duration": thinking_duration
    }
    st.session_state.messages.append(message_data)
    
    # Rerun to show the conversation properly
    st.rerun()
