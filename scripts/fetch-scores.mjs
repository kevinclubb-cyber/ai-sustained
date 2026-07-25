// scripts/fetch-scores.mjs
// Pulls all AI Survival Scores from HubSpot contacts and writes scores.json
// No dependencies - uses built-in fetch (Node 18+).
//
// PLACEHOLDER TO CONFIRM: the internal name of the score property.
// Check in HubSpot: Settings > Properties > search "AI Survival Score" > internal name.
const SCORE_PROPERTY = "ai_survival_score";

const TOKEN = process.env.HUBSPOT_TOKEN;
if (!TOKEN) {
  console.error("HUBSPOT_TOKEN env var is missing");
  process.exit(1);
}

const SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/search";

async function fetchAllScores() {
  const scores = [];
  let after = undefined;

  while (true) {
    const body = {
      filterGroups: [
        {
          filters: [
            { propertyName: SCORE_PROPERTY, operator: "HAS_PROPERTY" },
          ],
        },
      ],
      properties: [SCORE_PROPERTY],
      limit: 200,
      ...(after ? { after } : {}),
    };

    const res = await fetch(SEARCH_URL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      console.error(`HubSpot API error ${res.status}: ${await res.text()}`);
      process.exit(1);
    }

    const data = await res.json();

    for (const contact of data.results ?? []) {
      const raw = contact.properties?.[SCORE_PROPERTY];
      const num = Number(raw);
      if (raw !== null && raw !== "" && Number.isFinite(num)) {
        scores.push(num);
      }
    }

    after = data.paging?.next?.after;
    if (!after) break;

    // stay well inside HubSpot search rate limits (4 req/sec)
    await new Promise((r) => setTimeout(r, 300));
  }

  return scores;
}

const scores = await fetchAllScores();
scores.sort((a, b) => a - b);

const output = {
  updated: new Date().toISOString(),
  count: scores.length,
  scores, // sorted ascending, numbers only - no PII published
};

const { writeFileSync } = await import("node:fs");
writeFileSync("scores.json", JSON.stringify(output));
console.log(`Wrote scores.json with ${scores.length} scores`);
