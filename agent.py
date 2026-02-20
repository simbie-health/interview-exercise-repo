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
from tools.patient_lookup import search_patient

client = OpenAI(api_key="OPENAI_API_KEY")

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

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_patient",
            "description": "Search for a patient by date of birth. Use when the patient provides their DOB to verify identity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_of_birth": {
                        "type": "string",
                        "description": "Patient date of birth in YYYY-MM-DD format",
                    },
                },
                "required": ["date_of_birth"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "search_patient": search_patient,
}


def run_agent(clinic: str):
    """Run an interactive agent session for a given clinic."""

    messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"\n{'=' * 50}")
    print(f"  Scheduling Agent — {clinic}")
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

                # Inject clinic — the LLM doesn't need to know about it
                fn_args["clinic"] = clinic

                print(f"  [Tool: {fn_name}({fn_args})]")
                result = TOOL_FUNCTIONS[fn_name](**fn_args)
                print(f"  [Result: {result['message']}]")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })
