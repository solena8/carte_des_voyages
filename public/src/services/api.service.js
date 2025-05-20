import { API_CONFIG } from "../config/api.config.js";
import { MapService } from "./map.service.js";

export class ApiService {
  static async loadPlaces(map) {
    try {
      console.log("Fetching places from:", `${API_CONFIG.MAIN.URL}/list`);
      const response = await fetch(`${API_CONFIG.MAIN.URL}/list`);
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      console.log("API response data:", data); // Debug the response
      
      if (!Array.isArray(data) || data.length === 0){
        console.log("No places data found or empty array");
        return;
      }

      const markers = [];
      data.forEach((place) => {
        console.log("Processing place:", place); // Debug each place object
        
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

  static async submitPlace(data) {
    try {
      console.log("Submitting place data:", data);
      const response = await fetch(`${API_CONFIG.MAIN.URL}/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP Error: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Error submitting place:", error);
      throw error;
    }
  }

  static async deletePlace(id) {
    try {
      console.log("Deleting place with ID:", id);
      
      const response = await fetch(`${API_CONFIG.MAIN.URL}/delete?id=${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
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
      const response = await fetch(`${API_CONFIG.MAIN.URL}/stats`);
      if (!response.ok)
        throw new Error("Error retrieving statistics");

      const data = await response.json();
      console.log("Stats data:", data);
      return data;
    } catch (error) {
      console.error("Error getting stats:", error);
      return { totalEntries: 0, uniqueCountries: 0 };
    }
  }
}

// Update stats in the DOM
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