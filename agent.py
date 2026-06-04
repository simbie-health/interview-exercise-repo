"""
A simple scheduling agent that handles incoming patient calls.

Uses OpenAI's API with tool calling to decide what to do.
The agent can look up patients and their appointments through our EHR integrations.

Requires: pip install openai
Requires: OPENAI_API_KEY env var
"""

import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Add new tool definitions here as you add more agent capabilities
# Example:
#   {
#       "type": "function",
#       "function": {
#           "name": "cancel_appointment",
#           "description": "Cancel an existing appointment for a patient in the EHR system",
#           "parameters": {
#               "type": "object",
#               "properties": {
#                   "clinic_name": {
#                       "type": "string",
#                       "description": "The name of the clinic to search in"
#                   },
#                   "appointment_id": {
#                       "type": "string",
#                       "description": "The unique identifier of the appointment to cancel"
#                   }
#               },
#               "required": ["clinic_name", "appointment_id"],
#           },
#       },
#   },
TOOL_DEFINITIONS = []

# Implement tool functions that interact with the EHR services
# Example:
# def _search_patient(clinic_name: str, date_of_birth: str) -> dict:
#     ...
#     return {"found": True, "patients": [...], "message": "Found patient: ..."}

# Register tool functions here (name → function mapping)
TOOL_FUNCTIONS = {
    # "search_patient": _search_patient,
}

SYSTEM_PROMPT = """You are a friendly scheduling assistant for a medical clinic.
You help patients look up their information and appointments over the phone.

Guidelines:
- Always verify the patient's identity by asking for their date of birth
- Collect patient's DOB
- Use the search_patient tool when the patient provides their DOB
- If multiple patients match
    - Collect patient's First and Last Name
    - Match with the results using the provided name

- Be concise and professional, like a real front desk staff member
- Do NOT provide medical advice — only help with scheduling"""

def run_agent():
    """Run an interactive agent session."""

    messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"\n{'=' * 50}")
    print(f"  Scheduling Agent")
    print(f"  Type 'quit' to exit")
    print(f"{'=' * 50}\n")

    # Get initial greeting
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,  # type: ignore
        tools=TOOL_DEFINITIONS,  # type: ignore
    )
    greeting = response.choices[0].message.content or "Hi! How can I help you today?"
    messages.append({"role": "assistant", "content": greeting})
    print(f"Agent: {greeting}\n")

    while True:
        user_input = input("Patient: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})

        # Loop: LLM may call tools multiple times before responding
        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,  # type: ignore
                tools=TOOL_DEFINITIONS,  # type: ignore
            )
            choice = response.choices[0].message

            # If no tool calls, the agent is responding with text
            if not choice.tool_calls:
                text = choice.content or ""
                messages.append({"role": "assistant", "content": text})
                print(f"\nAgent: {text}\n")
                break

            # Append the assistant message with tool calls
            messages.append(choice.model_dump())

            # Execute each tool call
            for tool_call in choice.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                print(f"  [Tool: {fn_name}({fn_args})]")
                result = TOOL_FUNCTIONS[fn_name](**fn_args)
                print(f"  [Result: {result['message']}]")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })
