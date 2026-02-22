import streamlit as st
from core.memory import Memory
from tools.todo import TodoManager

# 1. Page Configuration
st.set_page_config(
    page_title="Under the Hood",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Under the Hood")
st.write("Inspect the agent's internal state, including its long-term vector memory and persistent task list.")

# Initialize the components to read the data
# We don't need the LLM here, just the storage managers
memory = Memory()
todo_manager = TodoManager()

st.header("⚙️ Working Memory (Context Window)")
st.write("Raw messages currently stored in the agent's short-term memory (Session State).")

# Display the raw chat history if it exists
if "agent_history" in st.session_state and st.session_state.agent_history:
    # st.json automatically formats dictionaries into a nice, readable block
    st.json(st.session_state.agent_history)
else:
    st.info("The short-term memory is empty. Start a conversation in the chat!")

# 2. Long-Term Memory Section
st.divider()
st.header("🧠 Long-Term Memory (ChromaDB)")
st.write("Facts and details the agent has learned about you across sessions.")

# Fetch all data from ChromaDB
memories_data = memory.get_all_memories()

# Check if the database has any documents stored
if memories_data and memories_data.get('documents') and len(memories_data['documents']) > 0:
    formatted_memory = []
    for i in range(len(memories_data['ids'])):
        formatted_memory.append({
            "ID": memories_data['ids'][i],
            "Memory Content": memories_data['documents'][i],
            "Metadata": memories_data['metadatas'][i]
        })

    # Display as an interactive dataframe
    st.dataframe(formatted_memory, use_container_width=True)
else:
    st.info("The agent's memory is currently empty. Ask it to 'remember' something in the chat!")

# 3. To-Do List Section
st.divider()
st.header("✅ Persistent To-Do List (JSON)")
st.write("Tasks managed by the agent, saved in a local JSON file.")

# Fetch tasks from the JSON file
tasks = todo_manager.get_tasks()

if tasks:
    st.dataframe(tasks, use_container_width=True)
else:
    st.info("The to-do list is empty. Ask the agent to 'add a task' in the chat!")

# 4. Internal Monologue
st.divider()
st.header("💭 Internal Monologue")
st.write("A log showing the agent's step-by-step 'Thought process' for the LAST query.")

if "agent" in st.session_state and hasattr(st.session_state.agent, 'latest_monologue') and st.session_state.agent.latest_monologue:
    # Print each step of the monologue
    for step in st.session_state.agent.latest_monologue:
        with st.container(border=True):
            st.markdown(step)
else:
    st.info("No internal monologue recorded yet. Ask the agent a complex question that requires tools!")