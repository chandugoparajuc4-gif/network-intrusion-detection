
const form = document.getElementById("predictionForm");
const featuresDiv = document.getElementById("features");
const resultDiv = document.getElementById("result");
const historyList = document.getElementById("historyList");

const API_URL = "http://127.0.0.1:5000";

let featureNames = [];


// ========================================
// LOAD FEATURES
// ========================================

async function loadFeatures() {
    try {
        const response = await fetch(`${API_URL}/features`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not load features");
        }

        featureNames = data.features;
        featuresDiv.innerHTML = "";

        featureNames.forEach((name) => {
            const field = document.createElement("div");
            field.className = "field";

            const label = document.createElement("label");
            label.textContent = name;

            const input = document.createElement("input");
            input.type = "number";
            input.step = "any";
            input.required = true;
            input.dataset.feature = name;

            field.appendChild(label);
            field.appendChild(input);
            featuresDiv.appendChild(field);
        });

    } catch (error) {
        showResult(
            "Could not load features: " + error.message,
            "error"
        );
    }
}


// ========================================
// DISPLAY RESULT
// ========================================

function showResult(message, type) {
    resultDiv.textContent = message;
    resultDiv.className = "result " + type;
}


// ========================================
// PREDICT NETWORK TRAFFIC
// ========================================

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {};

    // Keep the entered values
    for (const input of featuresDiv.querySelectorAll("input")) {
        if (input.value.trim() === "") {
            showResult(
                "Please fill in all 78 features.",
                "error"
            );
            input.focus();
            return;
        }

        payload[input.dataset.feature] = Number(input.value);
    }

    showResult("Analyzing traffic...", "normal");

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction failed");
        }

        const isNormal = data.prediction === "BENIGN";

        showResult(
            "Prediction: " + data.prediction + " — " + data.status,
            isNormal ? "normal" : "attack"
        );

        // Refresh prediction history and statistics
        await Promise.all([
            loadHistory(),
            loadStats()
        ]);

    } catch (error) {
        showResult(
            "Error: " + error.message,
            "error"
        );
    }
});


// ========================================
// LOAD SAMPLE DATA
// ========================================

document.getElementById("loadSample").addEventListener(
    "click",
    async () => {
        try {
            const response = await fetch(`${API_URL}/sample`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Could not load sample"
                );
            }

            document.querySelectorAll("#features input").forEach(
                (input) => {
                    input.value = data[input.dataset.feature] ?? "";
                }
            );

            showResult(
                "Sample data loaded successfully!",
                "normal"
            );

        } catch (error) {
            showResult(
                "Error: " + error.message,
                "error"
            );
        }
    }
);


// ========================================
// PREDICTION HISTORY
// ========================================

function displayHistory(records) {
    historyList.innerHTML = "";

    if (!records || records.length === 0) {
        historyList.textContent = "No predictions yet.";
        return;
    }

    records.forEach((record) => {
        const item = document.createElement("div");
        const isNormal = record.prediction === "BENIGN";

        item.className =
            "history-item " + (isNormal ? "normal" : "attack");

        const title = document.createElement("strong");
        title.textContent = "Prediction: " + record.prediction;

        const statusText = document.createElement("p");
        statusText.textContent = "Status: " + record.status;

        const timeText = document.createElement("p");
        const date = new Date(record.created_at);

        timeText.textContent =
            "Time: " + (
                isNaN(date.getTime())
                    ? record.created_at
                    : date.toLocaleString()
            );

        item.appendChild(title);
        item.appendChild(statusText);
        item.appendChild(timeText);

        historyList.appendChild(item);
    });
}


// Load history from SQLite through Flask
async function loadHistory() {
    try {
        const response = await fetch(`${API_URL}/history`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Could not load prediction history"
            );
        }

        displayHistory(data);

    } catch (error) {
        historyList.textContent =
            "Could not load history: " + error.message;
    }
}


// ========================================
// DASHBOARD STATISTICS
// ========================================

async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Could not load statistics"
            );
        }

        document.getElementById("totalPredictions").textContent =
            data.total_predictions;

        document.getElementById("normalTraffic").textContent =
            data.normal_traffic;

        document.getElementById("attacksDetected").textContent =
            data.attacks_detected;

    } catch (error) {
        console.error("Statistics error:", error);
    }
}


// ========================================
// START APPLICATION
// ========================================

async function startApplication() {
    await loadFeatures();

    await Promise.all([
        loadHistory(),
        loadStats()
    ]);
}

startApplication();