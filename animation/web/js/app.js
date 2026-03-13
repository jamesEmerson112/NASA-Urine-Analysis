document.addEventListener("DOMContentLoaded", () => {
    const panels = document.querySelectorAll(".panel");
    const videoPanels = document.getElementById("video-panels");
    const tabBar = document.getElementById("tab-bar");
    const viewButtons = document.querySelectorAll(".view-controls button");
    const tabButtons = document.querySelectorAll(".tab-bar button");
    const syncCheckbox = document.getElementById("sync-playback");

    let currentView = "tabbed";
    let currentTab = "mlp";

    // --- View mode switching ---
    viewButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const view = btn.dataset.view;
            if (view === currentView) return;

            viewButtons.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            currentView = view;

            videoPanels.className = "video-panels " + view;

            if (view === "tabbed") {
                tabBar.classList.remove("hidden");
                panels.forEach((p) => p.classList.remove("active"));
                document
                    .getElementById("panel-" + currentTab)
                    .classList.add("active");
            } else {
                tabBar.classList.add("hidden");
                panels.forEach((p) => p.classList.add("active"));
            }

            // Pause hidden videos
            pauseHiddenVideos();
        });
    });

    // --- Tab switching ---
    tabButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const tab = btn.dataset.tab;
            if (tab === currentTab && currentView === "tabbed") return;

            tabButtons.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            currentTab = tab;

            panels.forEach((p) => p.classList.remove("active"));
            document.getElementById("panel-" + tab).classList.add("active");

            pauseHiddenVideos();
        });
    });

    // --- Video controls ---
    // Play/Pause
    document.querySelectorAll(".play-pause").forEach((btn) => {
        btn.addEventListener("click", () => {
            const video = document.getElementById(btn.dataset.video);
            if (video.paused) {
                if (syncCheckbox.checked && currentView !== "tabbed") {
                    playAllVisible();
                } else {
                    video.play();
                }
            } else {
                if (syncCheckbox.checked && currentView !== "tabbed") {
                    pauseAllVisible();
                } else {
                    video.pause();
                }
            }
        });
    });

    // Step buttons
    document.querySelectorAll(".step-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const video = document.getElementById(btn.dataset.video);
            const step = parseFloat(btn.dataset.step);
            video.pause();
            video.currentTime = Math.max(
                0,
                Math.min(video.duration || 0, video.currentTime + step)
            );

            if (syncCheckbox.checked && currentView !== "tabbed") {
                syncAllTo(video.currentTime);
            }
        });
    });

    // Seek bars
    document.querySelectorAll(".seek-bar").forEach((bar) => {
        bar.addEventListener("input", () => {
            const video = document.getElementById(bar.dataset.video);
            if (video.duration) {
                const time = (bar.value / 1000) * video.duration;
                video.currentTime = time;

                if (syncCheckbox.checked && currentView !== "tabbed") {
                    syncAllTo(time);
                }
            }
        });
    });

    // Time update handler
    document.querySelectorAll("video").forEach((video) => {
        video.addEventListener("timeupdate", () => {
            updateControls(video);
        });

        video.addEventListener("play", () => {
            const btn = document.querySelector(
                `.play-pause[data-video="${video.id}"]`
            );
            if (btn) btn.innerHTML = "&#9646;&#9646;";
        });

        video.addEventListener("pause", () => {
            const btn = document.querySelector(
                `.play-pause[data-video="${video.id}"]`
            );
            if (btn) btn.innerHTML = "&#9654;";
        });

        video.addEventListener("ended", () => {
            const btn = document.querySelector(
                `.play-pause[data-video="${video.id}"]`
            );
            if (btn) btn.innerHTML = "&#9654;";
        });
    });

    // --- Helper functions ---
    function updateControls(video) {
        const bar = document.querySelector(
            `.seek-bar[data-video="${video.id}"]`
        );
        const timeDisplay = document.querySelector(
            `.time-display[data-video="${video.id}"]`
        );

        if (bar && video.duration) {
            bar.value = (video.currentTime / video.duration) * 1000;
        }

        if (timeDisplay) {
            timeDisplay.textContent =
                formatTime(video.currentTime) +
                " / " +
                formatTime(video.duration || 0);
        }
    }

    function formatTime(seconds) {
        if (isNaN(seconds)) return "0:00";
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return m + ":" + (s < 10 ? "0" : "") + s;
    }

    function pauseHiddenVideos() {
        panels.forEach((panel) => {
            if (
                !panel.classList.contains("active") &&
                currentView === "tabbed"
            ) {
                const video = panel.querySelector("video");
                if (video) video.pause();
            }
        });
    }

    function getVisibleVideos() {
        const videos = [];
        panels.forEach((panel) => {
            if (
                currentView !== "tabbed" ||
                panel.classList.contains("active")
            ) {
                const video = panel.querySelector("video");
                if (video) videos.push(video);
            }
        });
        return videos;
    }

    function playAllVisible() {
        getVisibleVideos().forEach((v) => v.play());
    }

    function pauseAllVisible() {
        getVisibleVideos().forEach((v) => v.pause());
    }

    function syncAllTo(time) {
        getVisibleVideos().forEach((v) => {
            if (v.duration) {
                v.currentTime = Math.min(time, v.duration);
            }
        });
    }
});
