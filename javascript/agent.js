/**
 * A simple scheduling agent that handles incoming patient calls.
 *
 * Uses OpenAI's API with tool calling to decide what to do.
 * The agent can look up patients and their appointments through our EHR integrations.
 *
 * Requires: npm install (installs the `openai` package)
 * Requires: OPENAI_API_KEY env var
 */

import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Add new tool definitions here as you add more agent capabilities
// Example:
//   {
//       type: "function",
//       function: {
//           name: "cancel_appointment",
//           description: "Cancel an existing appointment for a patient in the EHR system",
//           parameters: {
//               type: "object",
//               properties: {
//                   clinic_name: {
//                       type: "string",
//                       description: "The name of the clinic to search in",
//                   },
//                   appointment_id: {
//                       type: "string",
//                       description: "The unique identifier of the appointment to cancel",
//                   },
//               },
//               required: ["clinic_name", "appointment_id"],
//           },
//       },
//   },
const TOOL_DEFINITIONS = [];

// Implement tool functions that interact with the EHR services
// Example:
// function _searchPatient({ clinic_name, date_of_birth }) {
//     ...
//     return { found: true, patients: [...], message: "Found patient: ..." };
// }

// Register tool functions here (name → function mapping)
const TOOL_FUNCTIONS = {
  // search_patient: _searchPatient,
};

const SYSTEM_PROMPT = `You are a friendly scheduling assistant for a medical clinic.
You help patients look up their information and appointments over the phone.

Guidelines:
- Always verify the patient's identity by asking for their date of birth
- Collect patient's DOB
- Use the search_patient tool when the patient provides their DOB
- If multiple patients match
    - Collect patient's First and Last Name
    - Match with the results using the provided name

- Be concise and professional, like a real front desk staff member
- Do NOT provide medical advice — only help with scheduling`;

/** Run an interactive agent session. */
export async function runAgent() {
  const messages = [{ role: "system", content: SYSTEM_PROMPT }];

  console.log(`\n${"=".repeat(50)}`);
  console.log("  Scheduling Agent");
  console.log("  Type 'quit' to exit");
  console.log(`${"=".repeat(50)}\n`);

  // Get initial greeting
  let response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages,
    tools: TOOL_DEFINITIONS,
  });
  const greeting =
    response.choices[0].message.content || "Hi! How can I help you today?";
  messages.push({ role: "assistant", content: greeting });
  console.log(`Agent: ${greeting}\n`);

  const rl = readline.createInterface({ input, output });

  try {
    while (true) {
      const userInput = (await rl.question("Patient: ")).trim();
      if (!userInput) {
        continue;
      }
      if (userInput.toLowerCase() === "quit") {
        break;
      }

      messages.push({ role: "user", content: userInput });

      // Loop: LLM may call tools multiple times before responding
      while (true) {
        response = await client.chat.completions.create({
          model: "gpt-4o-mini",
          messages,
          tools: TOOL_DEFINITIONS,
        });
        const choice = response.choices[0].message;

        // If no tool calls, the agent is responding with text
        if (!choice.tool_calls || choice.tool_calls.length === 0) {
          const text = choice.content || "";
          messages.push({ role: "assistant", content: text });
          console.log(`\nAgent: ${text}\n`);
          break;
        }

        // Append the assistant message with tool calls
        messages.push(choice);

        // Execute each tool call
        for (const toolCall of choice.tool_calls) {
          const fnName = toolCall.function.name;
          const fnArgs = JSON.parse(toolCall.function.arguments);

          console.log(`  [Tool: ${fnName}(${JSON.stringify(fnArgs)})]`);
          const result = TOOL_FUNCTIONS[fnName](fnArgs);
          console.log(`  [Result: ${result.message}]`);

          messages.push({
            role: "tool",
            tool_call_id: toolCall.id,
            content: JSON.stringify(result),
          });
        }
      }
    }
  } finally {
    rl.close();
  }
}
