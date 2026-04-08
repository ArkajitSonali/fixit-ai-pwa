const API_URL = "https://fixit-ai-pwa.onrender.com/explain";

// DOM Elements
const errorMsgInput = document.getElementById("error-message");
const codeSnippetInput = document.getElementById("code-snippet");
const explainBtn = document.getElementById("explain-btn");
const clearBtn = document.getElementById("clear-btn");
const copyBtn = document.getElementById("copy-btn");

// States
const emptyState = document.getElementById("empty-state");
const loadingState = document.getElementById("loading-state");
const errorState = document.getElementById("error-state");
const resultContainer = document.getElementById("result-container");
const errorAlert = document.getElementById("error-alert");

// Output Elements
const badgeLanguage = document.getElementById("badge-language");
const badgeType = document.getElementById("badge-type");
const badgeSeverity = document.getElementById("badge-severity");

const outExplanation = document.getElementById("out-explanation");
const cardDym = document.getElementById("card-dym");
const outDym = document.getElementById("out-dym");
const outCause = document.getElementById("out-cause");
const outAnalogy = document.getElementById("out-analogy");
const outFixes = document.getElementById("out-fixes");
const outCode = document.getElementById("out-code");
const outTips = document.getElementById("out-tips");

const historyList = document.getElementById("history-list");

let historyData = [];

document.addEventListener("DOMContentLoaded", () => {
    loadHistory();
});

function showState(state) {
    emptyState.classList.add("hidden");
    loadingState.classList.add("hidden");
    errorState.classList.add("hidden");
    resultContainer.classList.add("hidden");

    if (state === "empty") emptyState.classList.remove("hidden");
    else if (state === "loading") loadingState.classList.remove("hidden");
    else if (state === "error") errorState.classList.remove("hidden");
    else if (state === "result") resultContainer.classList.remove("hidden");
}

explainBtn.addEventListener("click", async () => {
    const errorMsg = errorMsgInput.value.trim();
    const codeSnippet = codeSnippetInput.value.trim();

    if (!errorMsg && !codeSnippet) {
        showError("Please enter an error message or code snippet.");
        return;
    }

    showState("loading");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                error_message: errorMsg,
                code_snippet: codeSnippet
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        renderResult(data);
        saveHistory({ errorMsg, codeSnippet, result: data });

    } catch (err) {
        console.error(err);
        showError(err.message);
    }
});

clearBtn.addEventListener("click", () => {
    errorMsgInput.value = "";
    codeSnippetInput.value = "";
    showState("empty");
});

copyBtn.addEventListener("click", () => {
    const code = outCode.innerText;
    navigator.clipboard.writeText(code).then(() => {
        const originalText = copyBtn.innerText;
        copyBtn.innerText = "Copied!";
        setTimeout(() => copyBtn.innerText = originalText, 2000);
    }).catch(err => {
        console.error("Failed to copy", err);
    });
});

function renderResult(data) {
    showState("result");

    // Badges
    badgeLanguage.innerText = data.language || "Unknown";
    badgeType.innerText = data.error_type || "Error";

    badgeSeverity.innerText = data.severity || "Unknown";
    badgeSeverity.className = "badge"; // reset class
    const sev = (data.severity || "").toLowerCase();
    if (sev === "high") badgeSeverity.classList.add("badge-danger");
    else if (sev === "medium") badgeSeverity.classList.add("badge-warning");
    else if (sev === "low") badgeSeverity.classList.add("badge-low");

    // Text fields
    outExplanation.innerText = data.explanation || "N/A";
    outCause.innerText = data.root_cause || "N/A";
    outAnalogy.innerText = data.analogy || "N/A";
    outCode.innerText = data.corrected_code || "N/A";

    // Did you mean
    if (data.did_you_mean && data.did_you_mean.trim() !== "") {
        cardDym.classList.remove("hidden");
        outDym.innerText = data.did_you_mean;
    } else {
        cardDym.classList.add("hidden");
    }

    // Fixes List
    outFixes.innerHTML = "";
    if (Array.isArray(data.fixes)) {
        data.fixes.forEach(fix => {
            const li = document.createElement("li");
            li.innerText = fix;
            outFixes.appendChild(li);
        });
    }

    // Tips List
    outTips.innerHTML = "";
    if (Array.isArray(data.prevention_tips)) {
        data.prevention_tips.forEach(tip => {
            const li = document.createElement("li");
            li.innerText = tip;
            outTips.appendChild(li);
        });
    }
}

function showError(msg) {
    errorAlert.innerText = msg;
    showState("error");
}

function saveHistory(item) {
    // Keep last 5 history items
    historyData.unshift(item);
    if (historyData.length > 5) historyData.pop();
    localStorage.setItem("debugAI_history", JSON.stringify(historyData));
    updateHistoryUI();
}

function loadHistory() {
    const saved = localStorage.getItem("debugAI_history");
    if (saved) {
        historyData = JSON.parse(saved);
        updateHistoryUI();
    }
}

function updateHistoryUI() {
    historyList.innerHTML = "";
    historyData.forEach((item, index) => {
        const li = document.createElement("li");
        li.className = "history-item";
        // Title logic: Use error msg if exists, otherwise a snippet of code
        const title = item.errorMsg ? item.errorMsg : (item.codeSnippet.substring(0, 30) + "...");
        li.innerText = title || "Unknown Error";

        li.addEventListener("click", () => {
            errorMsgInput.value = item.errorMsg;
            codeSnippetInput.value = item.codeSnippet;
            renderResult(item.result);
        });
        historyList.appendChild(li);
    });
}
