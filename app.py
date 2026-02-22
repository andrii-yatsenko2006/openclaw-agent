import streamlit as st
from core.agent import Agent

# 1. Page Configuration
st.set_page_config(
    page_title="OpenClaw AI Agent",
    page_icon="🤖",
    layout="wide"
)

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    # Allow the user to change the model on the fly
    model_name = st.text_input("Ollama Model", value="llama3")

    st.header("👤 User Profile")
    user_name = st.text_input("Name", value="User")
    user_info = st.text_area("Basic Info", value="I am testing the OpenClaw agent.")

    st.header("🤖 Agent Persona")
    agent_name = st.text_input("Agent Name", value="OpenClaw")
    agent_role = st.text_input("Role", value="Grumpy Coder")
    agent_instructions = st.text_area("System Instructions",
                                      value="You are a grumpy but brilliant coder. Be sarcastic but helpful in your Final Answers.")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.agent_history = []
        st.rerun()

# 3. Session State Initialization
# Streamlit reruns the script on every user interaction.
# We use session_state to keep the agent and history alive between reruns.
if "agent" not in st.session_state or st.session_state.get("current_model") != model_name:
    st.session_state.agent = Agent(model_name=model_name)
    st.session_state.current_model = model_name

if "messages" not in st.session_state:
    # Messages for the UI display
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI agent. How can I help you today?"}]

if "agent_history" not in st.session_state:
    # Strict history format for the LLM context
    st.session_state.agent_history = []

# Check if this is the start of a new conversation (only greeting exists)
if len(st.session_state.messages) == 1:
    tasks = st.session_state.agent.todo_manager.get_tasks()
    # Filter only pending tasks
    pending_tasks = [t for t in tasks if t['status'] == 'pending']

    # If there are pending tasks, the agent proactively offers to help
    if pending_tasks:
        proactive_msg = f"I see we still have {len(pending_tasks)} unfinished task(s), like '{pending_tasks[0]['task']}'. Shall we work on that?"
        st.session_state.messages.append({"role": "assistant", "content": proactive_msg})
        st.session_state.agent_history.append({"role": "assistant", "content": proactive_msg})

# 4. Main UI Layout
st.title("🤖 OpenClaw AI Agent")
st.write("A local ReAct agent with tools: Search, Memory, To-Do, and Document Reader.")

chat_col, todo_col = st.columns([7, 3])

with todo_col:
    st.header("📋 Live To-Do Board")

    # Fetch tasks directly from the agent's manager
    current_tasks = st.session_state.agent.todo_manager.get_tasks()

    if current_tasks:
        for t in current_tasks:
            # Choose icon based on status
            icon = "✅" if t["status"] == "done" else "⏳"
            # Draw a nice UI card for each task
            with st.container(border=True):
                st.markdown(f"**{icon} Task ID: {t['id']}**")
                st.write(t['task'])
    else:
        st.info("No tasks pending. Add one via chat!")

with chat_col:
    # Display all previous messages in the chat interface
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input and Processing
    if prompt := st.chat_input("Ask me anything or give me a task..."):
        # Show user message in UI immediately
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Trigger the Agent
        with st.chat_message("assistant"):
            with st.spinner("Thinking and using tools..."):
                response = st.session_state.agent.run(
                    user_query=prompt,
                    chat_history=st.session_state.agent_history,
                    user_name=user_name,
                    user_info=user_info,
                    agent_name=agent_name,
                    agent_role=agent_role,
                    agent_instructions=agent_instructions
                )
                st.markdown(response)

        # Save assistant response to UI messages
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Update the internal history for the LLM context
        st.session_state.agent_history.append({"role": "user", "content": prompt})
        st.session_state.agent_history.append({"role": "assistant", "content": response})

        # Rerun the app to instantly update the Live To-Do board on the right
        st.rerun()