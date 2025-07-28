import streamlit as st
import time
import random
from openai import OpenAI

def generate_reasoning_steps_for_credibility_task():
    """Generate realistic reasoning steps for the social media credibility evaluation task."""
    return [
        "I need to evaluate this social media post about green tea and cancer prevention for credibility. Let me break down the claims systematically.",
        "First, I'll examine the specific claims: 1) A peer-reviewed Stanford study exists, 2) 50,000 participants over 10 years, 3) 87% cancer risk reduction from 3 cups daily, 4) 'Big Pharma doesn't want you to know.'",
        "Checking the methodology claims: A 10-year study with 50,000 participants sounds plausible for epidemiological research, but I need to verify if such a study actually exists from Stanford.",
        "The 87% risk reduction is an extremely high effect size that would be groundbreaking if true. Such dramatic results would typically be widely reported in major medical journals and news outlets.",
        "Red flags I'm noticing: 1) The 'Big Pharma conspiracy' language, 2) Urgency to 'share before they take it down,' 3) Hashtags like #GreenTeaCure suggest oversimplification, 4) No citation of the actual study.",
        "I should also consider what legitimate research says about green tea and cancer. While some studies suggest modest benefits, the scientific consensus doesn't support such dramatic claims.",
        "The post uses persuasive but unscientific language patterns common in health misinformation: definitive claims ('proves'), conspiracy theories, and emotional appeals.",
        "Based on my analysis, this appears to be misleading health information that could potentially harm people by promoting false hope or delaying proper medical care."
    ]

# --- Inject custom CSS including blinking/details styles ---
st.markdown("""
<style>
  /* your existing styling… */

  /* Hide default marker */
  details summary {
    list-style: none;
    cursor: pointer;
  }
  details summary::-webkit-details-marker {
    display: none;
  }

  /* Blink effect on the <summary> text */
  @keyframes fadeOut {
    from { opacity: 1; }
    to   { opacity: 0.2; }
  }
  .blinking {
    animation: fadeOut 0.8s ease-in-out infinite alternate;
  }
  /* stop blinking once expanded */
  details[open] summary.blinking {
    animation: none;
  }

  /* hide the full list by default */
  .reasoning-list {
    display: none;
  }
  /* show it when <details> is open */
  details[open] .reasoning-list {
    display: block;
    max-height: 300px;
    overflow-y: auto;
    padding: 8px;
    background: #fafafa;
    border-radius: 6px;
    border-left: 3px solid #e1e5e9;
  }
</style>
""", unsafe_allow_html=True)

# Show title
st.markdown('<h1 class="main-title">What\'s on the agenda today?</h1>', unsafe_allow_html=True)

# Initialize OpenAI
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_reasoning_history" not in st.session_state:
    st.session_state.current_reasoning_history = []
if "reasoning_step_counter" not in st.session_state:
    st.session_state.reasoning_step_counter = 0

# Display past messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        # show the expander for the final reasoning/time
        if "reasoning" in message:
            with st.expander(f"Thought for {message['thinking_duration']} seconds"):
                for i, step in enumerate(message["reasoning"], 1):
                    st.markdown(f"**Step {i}:** {step}")
                st.markdown('<div class="done-indicator">✓ Done</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# If new user message, generate reasoning + response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1

    steps = generate_reasoning_steps_for_credibility_task()
    start_time = time.time()
    details_container = st.empty()

    # Loop through steps with blinking/details
    for step in steps:
        st.session_state.current_reasoning_history.append(step)
        # build combined <details> HTML
        html = f"""
        <details>
          <summary class="reasoning-block blinking">
            {step}
          </summary>
          <div class="reasoning-list">
            {"".join(
              f'<div style="margin-bottom:12px;"><strong>Step {i}:</strong> {s}</div>'
              for i, s in enumerate(st.session_state.current_reasoning_history, 1)
            )}
          </div>
        </details>
        """
        details_container.markdown(html, unsafe_allow_html=True)
        time.sleep(2.5)

    details_container.empty()
    thinking_duration = int(time.time() - start_time)

    # show the final expander
    with st.expander(f"Thought for {thinking_duration} seconds"):
        for i, s in enumerate(steps, 1):
            st.markdown(f"**Step {i}:** {s}")
        st.markdown('<div class="done-indicator">✓ Done</div>', unsafe_allow_html=True)

    # get and stream the actual LLM response
    response_placeholder = st.empty()
    full_response = ""
    try:
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)

        # action buttons
        st.markdown("""
        <div class="action-buttons">
          <button class="action-button" onclick="navigator.clipboard.writeText(document.querySelector('.assistant-message').innerText)" title="Copy">📋</button>
          <button class="action-button" title="Upvote">👍</button>
          <button class="action-button" title="Downvote">👎</button>
        </div>
        """, unsafe_allow_html=True)

        # save to session
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "reasoning": steps,
            "thinking_duration": thinking_duration
        })

    except Exception as e:
        st.error(f"Error generating response: {e}")

# Auto-resize JS
st.components.v1.html("""
<script>
  // ...your existing auto-resize code...
</script>
""", height=0)
