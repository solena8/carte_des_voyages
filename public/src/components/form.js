import {SELECTED_LOCATION} from "../config/config.js";
import {ApiService} from "../services/api.service.js";
import {ImageService} from "../services/image.service.js";
import {MapService} from "../services/map.service.js";

export class FormHandler {
    static initializeFormSubmission(map) {
        const form = document.getElementById("placeForm");
        form.addEventListener("submit", (event) =>
            this.handleFormSubmit(event, map)
        );
    }

    static async handleFormSubmit(event, map) {
        event.preventDefault(); // Toujours bloquer le rechargement en premier

        if (!SELECTED_LOCATION.latitude || !SELECTED_LOCATION.longitude) {
            alert("Veuillez sélectionner une adresse valide");
            return;
        }

        const imageFile = document.getElementById("imageUpload").files[0];
        console.log("Image file selected:", imageFile);

        if (!imageFile) {
            alert("Veuillez sélectionner une image");
            return;
        }

        if (!imageFile) {
            alert("Veuillez sélectionner une image");
            return;
        }

        const data = this.collectFormData();

        const formData = new FormData();
        formData.append("name", data.name);
        formData.append("date", data.date);
        formData.append("city", data.city);
        formData.append("country", data.country);
        formData.append("latitude", data.latitude.toString());
        formData.append("longitude", data.longitude.toString());
        formData.append("imageUpload", imageFile);

        try {
            console.log("Image file:", imageFile);
            const result = await ApiService.submitPlace(formData);
            console.log(formData)
            this.showSuccessMessage(result);
            await window.updateStats();
            const newMap = MapService.resetMap();
            await ApiService.loadPlaces(newMap);

            this.resetForm();
        } catch (error) {
            console.error("Erreur lors de la soumission:", error);
            alert("Une erreur est survenue lors de l'enregistrement");
        }
    }

    static collectFormData() {
        return {
            name: document.getElementById("name").value,
            date: document.getElementById("date").value,
            city: SELECTED_LOCATION.city,
            country: SELECTED_LOCATION.country,
            latitude: SELECTED_LOCATION.latitude,
            longitude: SELECTED_LOCATION.longitude,
        };
    }

    static showSuccessMessage(result) {
        document.getElementById(
            "responseMessage"
        ).innerText = `Lieu ajouté : ${result.name} à ${result.city}, ${result.country}`;
    }

    static resetForm() {
        document.getElementById("placeForm").reset();
        const preview = document.getElementById("preview");
        const uploadLabel = document.querySelector('label[for="imageUpload"]');

        if (preview) {
            preview.style.display = 'none';
            preview.src = '';
        }

        if (uploadLabel) {
            uploadLabel.textContent = "Choisir une image";
        }

        document.getElementById("responseMessage").innerText = '';
    }
}