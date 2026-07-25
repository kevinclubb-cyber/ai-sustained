// Client-side percentile snippet for ai-sustained.com/learn
// Call showRank(userScore) after the quiz calculates the score out of 100.
// Renders into an element with id="rank-result" - add that div to your results section:
//   <div id="rank-result"></div>

async function showRank(userScore) {
  const el = document.getElementById("rank-result");
  if (!el) return;

  try {
    // cache-bust so users get the latest published file
    const res = await fetch("/scores.json?t=" + Date.now());
    if (!res.ok) throw new Error("scores.json not found");
    const data = await res.json();

    const scores = data.scores; // sorted ascending
    const total = scores.length;
    if (total < 10) {
      // too few results for a meaningful rank - fail quietly
      el.textContent = "";
      return;
    }

    // number of scores strictly below the user's
    const below = scores.filter((s) => s < userScore).length;
    const percentile = Math.round((below / total) * 100);

    // rank: 1 = top scorer (ties share the better rank)
    const above = scores.filter((s) => s > userScore).length;
    const rank = above + 1;

    el.innerHTML = `You scored higher than <strong>${percentile}%</strong> of participants
      &mdash; rank <strong>${rank}</strong> of <strong>${total + 1}</strong>.`;
  } catch (err) {
    // never break the results page over a rank widget
    console.warn("Rank unavailable:", err);
    el.textContent = "";
  }
}
