/**
 * Simbie AI — Interview Exercise: Backend/Integrations
 *
 * We build AI agents that handle phone calls for medical clinics.
 * Each clinic uses a different EHR (Electronic Health Records) system.
 *
 * Currently no tools are integrated. Your task: build the integrations.
 *
 * Run the agent:
 *     node main.js
 */

import { runAgent } from "./agent.js";

async function main() {
  await runAgent();
}

main();
