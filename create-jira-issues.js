require("dotenv").config();
const fs = require("fs");
const axios = require("axios");

const {
  JIRA_BASE_URL,
  JIRA_EMAIL,
  JIRA_API_TOKEN,
  JIRA_PROJECT_KEY,
  DRY_RUN,
} = process.env;

const dryRun = DRY_RUN !== "false";

function formatDescription(item) {
  const lines = [];

  lines.push(`h2. QA Story`);
  lines.push(item.qa_story.title);
  lines.push("");

  lines.push(`h2. Acceptance Criteria`);
  for (const ac of item.qa_story.acceptance_criteria) {
    lines.push(`* ${ac}`);
  }
  lines.push("");

  lines.push(`h2. Test Scenarios`);
  for (const ts of item.test_scenarios) {
    lines.push(`h3. ${ts.id}: ${ts.title}`);
    lines.push("*Steps:*");
    for (let i = 0; i < ts.steps.length; i++) {
      lines.push(`# ${ts.steps[i]}`);
    }
    lines.push(`*Expected Result:* ${ts.expected_result}`);
    lines.push("");
  }

  if (item.edge_cases.length > 0) {
    lines.push(`h2. Edge Cases`);
    for (const ec of item.edge_cases) {
      lines.push(`* *${ec.description}* — ${ec.expected_behavior}`);
    }
  }

  return lines.join("\n");
}

function buildPayload(item) {
  return {
    fields: {
      project: { key: JIRA_PROJECT_KEY },
      summary: item.feature,
      description: formatDescription(item),
      issuetype: { name: "Story" },
      labels: ["AI_GENERATED"],
    },
  };
}

async function createIssue(payload) {
  const response = await axios.post(
    `${JIRA_BASE_URL}/rest/api/3/issue`,
    payload,
    {
      auth: { username: JIRA_EMAIL, password: JIRA_API_TOKEN },
      headers: { "Content-Type": "application/json" },
    }
  );
  return response.data;
}

async function main() {
  if (!JIRA_BASE_URL || !JIRA_EMAIL || !JIRA_API_TOKEN || !JIRA_PROJECT_KEY) {
    console.error("Missing required .env variables. Check your .env file.");
    process.exit(1);
  }

  const raw = fs.readFileSync("outputs/qa_output.json", "utf-8");
  const items = JSON.parse(raw);

  console.log(`Found ${items.length} features. DRY_RUN=${dryRun}\n`);

  for (const item of items) {
    const payload = buildPayload(item);

    if (dryRun) {
      console.log(`[DRY RUN] ${item.feature}`);
      console.log(JSON.stringify(payload, null, 2));
      console.log("---\n");
      continue;
    }

    try {
      const result = await createIssue(payload);
      console.log(`Created: ${result.key} — ${item.feature}`);
    } catch (err) {
      const msg = err.response?.data?.errors || err.message;
      console.error(`Failed: ${item.feature}`);
      console.error(msg);
      console.log("");
    }
  }

  console.log("Done.");
}

main();
