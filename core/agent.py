import re
from typing import List, Dict

from core.brain import Brain
from core.memory import Memory
from tools.search import SearchTool
from tools.todo import TodoManager
from tools.reader import DocumentReader

class Agent:
    """Orchestrates the LLM, memory, and tools using a ReAct loop."""
    def __init__(self, model_name: str = "llama3"):
        self.brain = Brain(model_name=model_name)
        self.memory = Memory()
        self.search_tool = SearchTool()
        self.todo_manager = TodoManager()
        self.document_reader = DocumentReader()

    def _build_system_prompt(self, user_name: str, user_info: str, agent_name: str, agent_role: str,
                                 agent_instructions: str) -> str:
        """Dynamically builds the system prompt based on UI configuration."""
        return f"""You are {agent_name}, acting as a {agent_role}.

User Profile:
- Name: {user_name}
- Info: {user_info}

Your Instructions:
{agent_instructions}

You must think step-by-step and use the exact format below.

Tools:
1. "search": Search the internet. Input: query.
2. "add_todo": Add a task. Input: description.
3. "mark_todo": Mark task done. Input: task ID (int).
4. "read_file": Read a document. Input: file path.
5. "save_memory": Remember a fact. Input: fact.
6. "search_memory": Recall a fact. Input: query.

FORMAT INSTRUCTIONS:
Option 1 - Use a tool:
Thought: I need to use a tool.
Action: [tool_name]
Action Input: [input string]

Option 2 - Final Answer:
Thought: I have the answer.
Final Answer: [your response]
"""

    def run(self, user_query: str, chat_history: List[Dict[str, str]] = None, max_iterations: int = 5,
            user_name: str = "User", user_info: str = "", agent_name: str = "Agent", agent_role: str = "Assistant",
            agent_instructions: str = "") -> str:
        """Executes the Thought -> Action -> Observation loop."""
        self.latest_monologue = []

        system_prompt = self._build_system_prompt(user_name, user_info, agent_name, agent_role, agent_instructions)

        chat_history = chat_history or []
        messages = [{"role": "system", "content": system_prompt}] + chat_history

        # Automatically inject relevant memories
        relevant_memories = self.memory.search_memory(user_query)
        if relevant_memories:
            messages.append({
                "role": "system",
                "content": f"Relevant context from your memory: {relevant_memories}"
            })

        messages.append({"role": "user", "content": user_query})

        for _ in range(max_iterations):
            llm_response = self.brain.chat(messages)
            self.latest_monologue.append(f"🤖 Agent Thought:\n{llm_response}")
            messages.append({"role": "assistant", "content": llm_response})

            # Check for final answer
            if "Final Answer:" in llm_response:
                return llm_response.split("Final Answer:")[-1].strip()

            # Parse tool execution request
            action_match = re.search(r"Action:\s*(.+)", llm_response)
            input_match = re.search(r"Action Input:\s*(.+)", llm_response)

            if action_match and input_match:
                # Extract and clean up the action and input
                action = action_match.group(1).strip().strip("[]")
                action_input = input_match.group(1).strip().strip("[]")

                observation = self._execute_tool(action, action_input)
                self.latest_monologue.append(f"🛠️ Tool Observation ({action}):\n{observation}")
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                # Force correct formatting if the LLM hallucinates
                messages.append({
                    "role": "user",
                    "content": "Observation: Invalid format. Use 'Action:' and 'Action Input:' or 'Final Answer:'."
                })

        return "Error: Reached maximum iterations without a Final Answer."

    def _execute_tool(self, action: str, action_input: str) -> str:
        """Routes the requested action to the corresponding tool."""
        try:
            if action == "search":
                return self.search_tool.search(action_input)
            elif action == "add_todo":
                return self.todo_manager.add_task(action_input)
            elif action == "mark_todo":
                task_id = int("".join(filter(str.isdigit, action_input)))
                return self.todo_manager.mark_done(task_id)
            elif action == "read_file":
                return self.document_reader.read_file(action_input)
            elif action == "save_memory":
                self.memory.add_memory(text=action_input)
                return "Fact saved to long-term memory."
            elif action == "search_memory":
                memories = self.memory.search_memory(action_input)
                return f"Found in memory: {memories}" if memories else "Nothing found in memory."
            else:
                return f"Error: Tool '{action}' not recognized."

        except Exception as e:
            return f"Error executing '{action}': {str(e)}"