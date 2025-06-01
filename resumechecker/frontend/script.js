document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const fileName = document.getElementById("fileName");
  const form = document.getElementById("uploadForm");
  const resultBox = document.getElementById("result");
  const scoreEl = document.getElementById("score");
  const foundEl = document.getElementById("found");
  const missingEl = document.getElementById("missing");
  const feedbackEl = document.getElementById("feedback");
  const confidenceEl = document.getElementById("confidence");
  const uploadBtn = document.getElementById("uploadBtn");

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) { // 2MB limit
        alert("File size exceeds 2MB. Please upload a smaller file.");
        fileInput.value = "";
        fileName.textContent = "No file uploaded";
      } else {
        fileName.textContent = file.name;
      }
    } else {
      fileName.textContent = "No file uploaded";
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (fileInput.files.length === 0) {
      alert("Please upload a PDF resume.");
      return;
    }

    const file = fileInput.files[0];
    if (file.size > 2 * 1024 * 1024) {
      alert("File size exceeds 2MB.");
      return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Analyzing...";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to upload resume.");
      }

      scoreEl.textContent = data.score;
      foundEl.textContent = data.found.length ? data.found.join(", ") : "None";
      missingEl.textContent = data.missing.length ? data.missing.join(", ") : "None";
      feedbackEl.textContent = data.prediction ? "Good Resume ✅" : "Needs Improvement ⚠️";
      confidenceEl.textContent = data.confidence + "%";

      resultBox.style.display = "block";
    } catch (error) {
      alert(error.message);
    } finally {
      uploadBtn.disabled = false;
      uploadBtn.textContent = "Upload & Analyze";
    }
  });
});
