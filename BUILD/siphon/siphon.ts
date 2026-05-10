import { readFileSync, appendFileSync } from 'fs';
import { join } from 'path';

// SIPHON v0: Four-field extraction
// Run: bun run BUILD/siphon/siphon.ts <transcript_path>

const SYSTEM_PROMPT = `You are SIPHON. Extract the provided session transcript into exactly this YAML format.
Do not output markdown blocks, just the raw YAML.

session:
  id: "session-NNN"
  date: YYYY-MM-DD
  decisions: []      # what changed
  corrections: []    # what was wrong
  next_action: ""    # what to do
  current_truth: ""  # one sentence the next session inherits
`;

async function extract(transcriptPath: string) {
  const transcript = readFileSync(transcriptPath, 'utf-8');
  
  console.log("SIPHON v0: Extracting session...");
  
  // In v0, we use the GLM-5 API via fetch to avoid heavy SDK dependencies
  const response = await fetch('https://api.z.ai/api/coding/paas/v4/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.ZAI_API_KEY || process.env.GLM_API_KEY || ''}`
    },
    body: JSON.stringify({
      model: 'glm-5.1', // Using the latest Z.AI coding model
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: transcript }
      ],
      temperature: 0.1
    })
  });

  if (!response.ok) {
    console.error("Extraction failed:", await response.text());
    process.exit(1);
  }

  const data = await response.json();
  let yamlOutput = data.choices[0].message.content;
  
  // Clean up potential markdown code blocks if the model ignores the prompt instruction
  yamlOutput = yamlOutput.replace(/^```yaml\n/, '').replace(/^```\n/, '').replace(/\n```$/, '');
  
  const memoryPath = join(process.cwd(), 'MEMORY', 'MEMORY.md');
  appendFileSync(memoryPath, `\n---\n${yamlOutput}\n`);
  
  console.log(`Extraction appended to ${memoryPath}`);
}

const target = process.argv[2];
if (!target) {
  console.error("Usage: bun run BUILD/siphon/siphon.ts <transcript_path>");
  process.exit(1);
}

extract(target);
