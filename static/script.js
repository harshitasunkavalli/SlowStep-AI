
const goalForm = document.getElementById("goalForm");
const generateBtn = document.getElementById("generateBtn");
const statusBox = document.getElementById("status");
const planSection = document.getElementById("planSection");
const planResult = document.getElementById("planResult");

goalForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const goal = document.getElementById("goal").value.trim();
    const days = Number(document.getElementById("days").value);
    const minutes = Number(document.getElementById("minutes").value);
    const mood = document.getElementById("mood").value;

    if (!goal) {
        statusBox.textContent = "Please enter your goal first.";
        return;
    }

    generateBtn.disabled = true;
    generateBtn.textContent = "Creating your plan...";
    statusBox.textContent = "🌱 Your AI companion is preparing small steps...";
    planSection.classList.add("hidden");
    planResult.replaceChildren();

    try {
        const response = await fetch("/generate-plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                goal,
                days,
                minutes,
                mood
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not generate your plan.");
        }

        const tasks = data.tasks;

        if (!Array.isArray(tasks) || tasks.length === 0) {
            throw new Error("The AI did not return a valid plan. Please try again.");
        }

        tasks.forEach((task, index) => {
            const card = document.createElement("article");
            card.className = "plan-day";

            const heading = document.createElement("h3");
            heading.textContent = `🌿 Day ${task.day ?? index + 1}`;

            const description = document.createElement("p");
            description.textContent = task.task;

            card.append(heading, description);
            planResult.appendChild(card);
        });

        statusBox.textContent = "✨ Your plan is ready. Start with just one small step!";
        planSection.classList.remove("hidden");
        planSection.scrollIntoView({ behavior: "smooth", block: "start" });

    } catch (error) {
        statusBox.textContent = `⚠️ ${error.message}`;
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "Create My Small Steps ✨";
    }
});
