async function askLLM() {
    const question = document.getElementById("question").value.trim();  // <-- .trim() is important
    if (!question) {
        alert("Please enter a question!");
        return;
    }

    const responseDiv = document.getElementById("response");
    const historyUl = document.getElementById("history");

    const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })  // sending key: 'question'
    });

    const data = await res.json();
    responseDiv.innerText = "Answer: " + data.answer;

    const hist = await fetch("/history").then(r => r.json());
    historyUl.innerHTML = "";
    for (let pair of hist.history.reverse()) {
        let li = document.createElement("li");
        li.textContent = `Q: ${pair.question} → A: ${pair.answer}`;
        historyUl.appendChild(li);
    }
}
