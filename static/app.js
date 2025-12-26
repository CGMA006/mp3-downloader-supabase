const downloadBtn = document.getElementById("downloadBtn");
const urlInput = document.getElementById("urlInput");
const status = document.getElementById("status");


downloadBtn.addEventListener("click", () => {

    // const url le value store garcha
    // .value le input field ko value lina milcha ra .trim le extra spaces hatauna milcha
    const url = urlInput.value.trim();
    if (!url) {
        status.textContent = "Status: Please enter a URL";
        return;
    }
    status.textContent = "Status: Downloading...";
    downloadBtn.disabled = true;

    fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === "Download complete") {
                status.textContent = "Status: Download complete!";
            } else {
                status.textContent = "Status: Error";
            }
        })
        .catch(() => {
            status.textContent = "Status: Server error";
        })
        .finally(() => {
            downloadBtn.disabled = false;
        });
});