import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

app.post("/build", async (req, res) => {
  const repoUrl = req.body.repo;
  const [owner, repo] = repoUrl.replace("https://github.com/", "").split("/");

  await fetch(
    `https://api.github.com/repos/${owner}/${repo}/actions/workflows/build.yml/dispatches`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${GITHUB_TOKEN}`,
        "Accept": "application/vnd.github+json"
      },
      body: JSON.stringify({ ref: "main" })
    }
  );

  res.json({
    actions: `https://github.com/${owner}/${repo}/actions`
  });
});

app.listen(3000, () => console.log("Server running"));
