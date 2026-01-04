"use client";

import { useEffect } from "react";
import axios from "axios";

export default function ThemeManager() {
    const applyTheme = async () => {
        try {
            console.log("ThemeManager: Fetching settings...");
            // Add timestamp to prevent caching
            const res = await axios.get(`http://localhost:8000/settings?t=${Date.now()}`);
            const theme = res.data.theme;
            console.log("ThemeManager: Applied theme:", theme);

            // Remove existing classes
            document.documentElement.classList.remove("dark", "light");

            // Apply new theme
            if (theme === "light") {
                document.documentElement.classList.add("light");
                // Also set data-theme attribute for some libraries
                document.documentElement.setAttribute("data-theme", "light");
            } else {
                document.documentElement.classList.add("dark");
                document.documentElement.setAttribute("data-theme", "dark");
            }
        } catch (e) {
            console.error("Failed to apply theme:", e);
        }
    };

    useEffect(() => {
        applyTheme();

        const handleSettingsChanged = () => {
            console.log("ThemeManager: settingsChanged event received");
            applyTheme();
        };

        // Listen for custom event from SettingsModal
        window.addEventListener("settingsChanged", handleSettingsChanged);

        return () => {
            window.removeEventListener("settingsChanged", handleSettingsChanged);
        };
    }, []);

    return null;
}
