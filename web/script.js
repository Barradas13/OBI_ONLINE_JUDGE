const JUDGE0_URL = "https://judge.darlon.com.br";

function toBase64(str) {
  return btoa(unescape(encodeURIComponent(str)));
}
function fromBase64(str) {
  return decodeURIComponent(escape(atob(str)));
}

async function loadLanguages() {
  try {
    const res = await fetch(`${JUDGE0_URL}/languages`);
    const langs = await res.json();
    const select = document.getElementById("language");
    langs.forEach(lang => {
      const opt = document.createElement("option");
      opt.value = lang.id;
      opt.textContent = lang.name;
      select.appendChild(opt);
    });
  } catch (err) {
    console.error("Erro ao carregar linguagens:", err);
  }
}
loadLanguages();

document.getElementById("runButton").addEventListener("click", async () => {
  const sourceCode = document.getElementById("code").value.trim();
  const languageId = document.getElementById("language").value;
  //const exercise = document.getElementById("exercise").value;
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "<h3>Baixando e testando...<h3>";

  if (!sourceCode || !languageId) {
    alert("Selecione uma linguagem e insira o código.");
    return;
  }

  try {
    const zipUrl = `../obiteste/2024f1pj_ogro.zip`; // ex: /tests/exercise1.zip
    const resp = await fetch(zipUrl);
    const blob = await resp.blob();

    const zip = await JSZip.loadAsync(blob);
    const files = Object.keys(zip.files);
    const inFiles = files.filter(f => f.endsWith(".in")).sort();
    const outFiles = files.filter(f => f.endsWith(".sol")).sort();

    let passed = 0;
    let total = inFiles.length;

    resultsDiv.innerHTML = `<h3>Executando ${total} casos de teste...</h3>`;

    for (let i = 0; i < total; i++) {
      const input = await zip.file(inFiles[i]).async("string");
      const expected = (await zip.file(outFiles[i]).async("string")).trim();

      const payload = {
        source_code: toBase64(sourceCode),
        stdin: toBase64(input),
        language_id: parseInt(languageId),
        base64_encoded: true,
        wait: true
      };

      const res = await fetch(`${JUDGE0_URL}/submissions?base64_encoded=true&wait=true`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await res.json();
      const output = fromBase64(result.stdout || "").trim();
      const status = result.status?.description || "Erro";

      //const ok = output === expected ? "✅ OK" : "❌ Falhou";
      if (output === expected) passed++;

      const caseDiv = document.createElement("div");
      caseDiv.innerHTML = `
        <b>Teste ${i+1}:</b> ${passed} <br>
        <i>Status:</i> ${status} <br>
        <i>Esperado:</i> <pre>${expected}</pre>
        <i>Obtido:</i> <pre>${output}</pre>
        <hr>
      `;
      resultsDiv.appendChild(caseDiv);
    }

    resultsDiv.querySelector("h3").remove();
    resultsDiv.innerHTML = `<h2>Resultado final: ${passed}/${total} casos corretos</h2>` + resultsDiv.innerHTML;
  } catch (error) {
    console.error(error);
    resultsDiv.textContent = "Erro ao executar testes.";
  }
});