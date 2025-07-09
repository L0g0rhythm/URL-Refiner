const processBtn = document.getElementById("processBtn");
const urlsInputEl = document.getElementById("urlsInput");
const fuzzValueEl = document.getElementById("fuzzValue");
const excludeParamsEl = document.getElementById("excludeParams");
const ignorePathEl = document.getElementById("ignorePath");
const urlsOutputEl = document.getElementById("urlsOutput");
const urlsProcessedEl = document.getElementById("urlsProcessed");
const duplicatesRemovedEl = document.getElementById("duplicatesRemoved");
const urlsOutputCountEl = document.getElementById("urlsOutputCount");
const errorBannerEl = document.getElementById("errorBanner");
const errorMessageEl = document.getElementById("errorMessage");

/**
 * Shows an error message in the UI.
 * @param {string} message - The error message to display.
 */
function displayError(message) {
  errorMessageEl.textContent = message;
  errorBannerEl.style.display = "block";
}

/**
 * Hides the error message banner.
 */
function hideError() {
  errorBannerEl.style.display = "none";
}

/**
 * Updates the statistics display in the UI.
 * @param {object} stats - The statistics object from the backend.
 */
function updateStats(
  stats = { total_input: 0, duplicates_removed: 0, total_output: 0 }
) {
  urlsProcessedEl.textContent = stats.total_input;
  duplicatesRemovedEl.textContent = stats.duplicates_removed;
  urlsOutputCountEl.textContent = stats.total_output;
}

// Attach event listener when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  processBtn.addEventListener("click", async () => {
    // 1. Clear previous errors and disable button
    hideError();
    urlsOutputEl.value = "Processing...";
    processBtn.disabled = true;
    processBtn.textContent = "Please wait...";

    // 2. Gather all data from the UI
    const urls = urlsInputEl.value.split("\n").filter(Boolean); // Filter out empty lines

    const config = {
      mode: document.querySelector('input[name="mode"]:checked').value,
      value: fuzzValueEl.value,
      exclude_params: excludeParamsEl.value
        .split(",")
        .map((p) => p.trim())
        .filter(Boolean),
      ignore_path: ignorePathEl.checked,
    };

    if (urls.length === 0) {
      displayError("Please enter at least one URL.");
      urlsOutputEl.value = "";
      processBtn.disabled = false;
      processBtn.textContent = "Process";
      return;
    }

    try {
      // 3. Call the exposed Python function and await the structured result
      const result = await eel.process_urls_py(urls, config)();

      // 4. Display results or errors based on the structured response
      if (result && result.status === "success") {
        urlsOutputEl.value = result.data.join("\n");
        updateStats(result.stats);
      } else {
        // Handle errors returned from Python
        const message = result ? result.message : "An unknown error occurred.";
        displayError(message);
        urlsOutputEl.value = "Processing failed. See error message above.";
        updateStats(); // Reset stats
      }
    } catch (error) {
      // Handle unexpected JS errors or communication failures with Eel
      console.error("Eel communication error:", error);
      displayError("A communication error occurred with the backend.");
      urlsOutputEl.value =
        "Processing failed. Could not connect to the backend.";
      updateStats(); // Reset stats
    } finally {
      // 5. Re-enable the button
      processBtn.disabled = false;
      processBtn.textContent = "Process";
    }
  });
});
