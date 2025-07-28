import streamlit as st
import time
from openai import OpenAI

# Generate realistic reasoning steps for the credibility task
def generate_reasoning_steps_for_credibility_task():
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

# Custom CSS (including blinking/details behavior)
st.markdown("""
<style>
    /* existing styles omitted for brevity... */

    /* hide default details marker */
    details summary {
      list-style: none;
      cursor: pointer;
    }
    details summary::-webkit-details-marker {
      display: none;
    }

    /* blink effect on summary text */
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0.2; }
    }
    .blinking {
      animation: fadeOut 0.8s ease-in-out infinite alternate;
    }
    /* stop blinking when expanded */
    details[open] summary.blinking {
      animation: none;
    }

    /* hide full list by default */
    .reasoning-list {
      display: none;
    }
    /* show list when <details> is open */
    details[open] .reasoning-list {
      display: block;
      max-height: 300px;
      overflow-y: auto;
      padding: 8px;
      background-color: #fafafa;
      border-radius: 6px;
      border-left: 3px solid #e1e5e9;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 style="text-align:center; font-size:28px; color:#2d2d2d;">What\'s on the agenda today?</h1>', unsafe_allow_html=True)

# Initialize OpenAI client
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Initialize session state
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_reasoning_history" not in st.session_state:
        st.session_state.current_reasoning_history = []
    if "reasoning_step_counter" not in st.session_state:
        st.session_state.reasoning_step_counter = 0
init_state()

# Display past messages
def render_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div style='background:#f0f0f0; border-radius:18px; padding:12px 16px; margin:8px auto 8px auto; max-width:70%;'>" +
                        f"{message['content']}" +
                        "</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:white; padding:12px; margin:8px 0; max-width:100%;'>" +
                        f"{message['content']}" +
                        "</div>", unsafe_allow_html=True)
render_messages()

# Chat input
tif prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.experimental_rerun()

# When there's a new user message, generate reasoning + response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Reset for new reasoning
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1

    # Get reasoning steps
    reasoning_steps = generate_reasoning_steps_for_credibility_task()

    # Display dynamic blinking box + expandable list
    details_container = st.empty()
    for step in reasoning_steps:
        st.session_state.current_reasoning_history.append(step)
        html = f"""
        <details>
          <summary class="reasoning-block blinking">{step}</summary>
          <div class="reasoning-list">
            {''.join(
              f'<div style="margin-bottom:12px;"><strong>Step {i}:</strong> {s}</div>'
              for i, s in enumerate(st.session_state.current_reasoning_history, 1)
            )}
          </div>
        </details>
        """
        details_container.markdown(html, unsafe_allow_html=True)
        time.sleep(2.5)

    # Generate and stream actual assistant response
    try:
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[m for m in st.session_state.messages],
            stream=True,
        )
        response_placeholder = st.empty()
        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                response_placeholder.markdown(
                    f"<div style='background:white; padding:12px; margin:8px 0;'>{full_response}</div>",
                    unsafe_allow_html=True
                )
        # store message
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
    except Exception as e:
        st.error(f"Error generating response: {e}")

# Auto-resize JS for Streamlit input
st.components.v1.html("""
<script>
function setupAutoResize() {
    const textareas = document.querySelectorAll('.stChatInput textarea');
    textareas.forEach(textarea => {
        if (!textarea.hasAttribute('data-auto-resize-setup')) {
            textarea.setAttribute('data-auto-resize-setup', 'true');
            textarea.style.height = '48px';
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 200) + 'px';
            });
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    setTimeout(() => { this.style.height = '48px'; }, 100);
                }
            });
            textarea.addEventListener('blur', function() {
                if (this.value.trim() === '') {
                    this.style.height = '48px';
                }
            });
        }
    });
}
setInterval(setupAutoResize, 500);
setupAutoResize();
</script>
""", height=0)
