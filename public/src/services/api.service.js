import {API_CONFIG} from "../config/api.config.js";
import {MapService} from "./map.service.js";

export class ApiService {
    static async loadPlaces(map) {
        try {
            console.log("Fetching places from:", `${API_CONFIG.MAIN.LIST}`);
            const response = await fetch(`${API_CONFIG.MAIN.LIST}`);
            if (!response.ok)
                throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            console.log("API response data:", data);

            if (!Array.isArray(data) || data.length === 0) {
                console.log("No places data found or empty array");
                return;
            }

            const markers = [];
            data.forEach((place) => {
                console.log("Processing place:", place);

                try {
                    place.date = new Date(place.date).toLocaleDateString();
                } catch (e) {
                    console.error("Date conversion error:", e);
                    place.date = "Unknown date";
                }

                if (place.latitude && place.longitude) {
                    console.log(`Adding marker at [${place.latitude}, ${place.longitude}]`);
                    const marker = MapService.addMarker(place, map);
                    if (marker) {
                        markers.push([place.latitude, place.longitude]);
                    } else {
                        console.warn("Marker creation failed for:", place);
                    }
                } else {
                    console.warn("Missing coordinates for place:", place);
                }
            });

            console.log(`Created ${markers.length} markers`);

            if (markers.length > 0) {
                map.fitBounds(markers, {
                    padding: [50, 50],
                    maxZoom: 15,
                });
            }
        } catch (error) {
            console.error("Error loading places:", error);
        }
    }

    static async submitPlace(formData) {
        try {

            const response = await fetch(`${API_CONFIG.MAIN.CREATE}`, {
                method: "POST",
                body: formData,
            });

            console.log("Response status:", response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error("Server error response:", errorText);
                throw new Error(errorText);
            }

            const result = await response.json();
            console.log("Success response:", result);
            return result;

        } catch (error) {
            console.error("Full error in submitPlace:", error);
            throw error;
        }
    }

    static async deletePlace(id) {
        try {
            console.log("Deleting place with ID:", id);

            const response = await fetch(`${API_CONFIG.MAIN.DELETE}?id=${id}`, {
                method: "DELETE",
            });

            if (!response.ok) {
                throw new Error("Error during deletion");
            }

        } catch (error) {
            console.error("Error deleting place:", error);
            throw error;
        }
    }

    static async getStats() {
        try {
            const response = await fetch(`${API_CONFIG.MAIN.STATS}`);
            if (!response.ok)
                throw new Error("Error retrieving statistics");

            const data = await response.json();
            console.log("Stats data:", data);
            return data;
        } catch (error) {
            console.error("Error getting stats:", error);
            return {totalEntries: 0, uniqueCountries: 0};
        }
    }
}

async function updateStats() {
    const result = await ApiService.getStats();

    document.getElementById(
        "compteur"
    ).innerText = `Nb de pays visités : ${result.uniqueCountries} \nNb de lieux visités : ${result.totalEntries}`;
}

document.addEventListener("DOMContentLoaded", async () => {
    await updateStats();
});

window.updateStats = updateStats;