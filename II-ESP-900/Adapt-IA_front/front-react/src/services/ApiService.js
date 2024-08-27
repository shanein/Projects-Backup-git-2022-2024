import CampaignModel from '../Model/CampaignModel';
import { api } from '../services/config';

class ApiService {

    constructor() {
        this.campagn_id = 0;
        this.campaign = new CampaignModel();
    }

    async  PostDraftCampaign(name, description, start_date, end_date, budget, is_smart, address, postal_code, targets, video_file) {
    
  

        const formDataDraft = new FormData();
        if(name != undefined){
          formDataDraft.set("name", name);
        }
        if(name != undefined){
          formDataDraft.set("name", name);
        }
    
        if(name != undefined){
          formDataDraft.set("name", name);
        }
    
        if(description != undefined){
          formDataDraft.set("description", description);
        }
    
        if(start_date != undefined){
          formDataDraft.set("start_date", start_date);
        }
    
        if(end_date != undefined){
          formDataDraft.set("end_date", end_date);
        }
    
        if(budget != undefined){
          formDataDraft.set("budget", budget);
        }
        if(is_smart != undefined){
          formDataDraft.set("is_smart", is_smart);
        }

        if(address != undefined){
          formDataDraft.set("address", address);
        }

        if(postal_code != undefined){
          formDataDraft.set("postal_code", postal_code);
        }

        if(postal_code != undefined){
          formDataDraft.set("cibles_json", targets);
        }

        const isURL = /^(http|https):\/\/[^ "]+$/.test(video_file);

        if (isURL) {
    // file est une URL, faire quelque chose ici
        } else {
         // file n'est pas une URL, c'est probablement un fichier local, donc vous pouvez ajouter le fichier au FormData
         if(video_file != undefined){
          formDataDraft.set("video_file", video_file);
        }

        }
       

        try {
          const resp = await api.post("/campaignsdraft", formDataDraft, { timeout: 5000 },{
            headers: {
              'Content-Type': 'multipart/form-data' // Indique que les données sont envoyées sous forme de formData
            }, 
          });

     
          return resp.data;

        } catch (error) {
          console.error(error);
        }
      }

      async getCampaignsByCampaignId(campaignId) {
        try {
          const resp = await api.get(`/campaigns/${campaignId}`);
            this.campaign = new CampaignModel(
                resp.data.id,
                resp.data.name,
                resp.data.description,
                resp.data.start_date,
                resp.data.end_date,
                resp.data.budget,
                resp.data.is_smart,
                resp.data.address,
                resp.data.postal_code,
                resp.data.cibles_json,
                resp.data.video_file,
                resp.data.is_smart,
                resp.data.is_active
            );

    
          return  this.campaign;
        } catch (error) {
          console.error(error);
        }
      }


      async updateDraftCampaign(campaign_id, name, details, start_date, end_date, budget, is_smart, address, postal_code, targets, file) {

    
        const formData = new FormData();
        formData.append("name", name);
        formData.append("description", details);
        formData.append("start_date", start_date); // Ensure date is in ISO format
        formData.append("end_date", end_date); // Ensure date is in ISO format
        formData.append("budget", budget);
        formData.append("is_smart", is_smart);
        formData.append("address", address); // Convert address object to string
        formData.append("postal_code", postal_code);
        formData.append("cibles_json", targets); // Convert targets object to string

  
    
        if(name != undefined){
          formData.set("name", name);
        }
    
        if(details != undefined){
          formData.set("description", details);
        }
    
        if(start_date != undefined){
          formData.set("start_date", start_date);
        }
    
        if(end_date != undefined){
          formData.set("end_date", end_date);
        }
    
        if(budget != undefined){
          formData.set("budget", budget);
        }
        if(is_smart != undefined){
          formData.set("is_smart", is_smart);
        }

        if(address != undefined){
          formData.set("address", address);
        }

        if(postal_code != undefined){
          formData.set("postal_code", postal_code);
        }

        if(postal_code != undefined){
          formData.set("cibles_json", targets);
        }
    
        const isURL = /^(http|https):\/\/[^ "]+$/.test(file);

        if (isURL) {
    // file est une URL, faire quelque chose ici
        } else {
         // file n'est pas une URL, c'est probablement un fichier local, donc vous pouvez ajouter le fichier au FormData
        formData.append("video_file", file);
        }
    
        try {
            const resp = await api.patch(`/campaigndraft/${campaign_id}`, formData, { timeout: 5000 });

 
            return resp.data;
        } catch (error) {
            console.error("Error updating campaign draft:", error);
            throw error;
        }
    }
    
      async updateDraftCampaignStatus(campagn_id, is_active) {
        try {
          const resp = await api.patch(`/updateisactive/${campagn_id}?is_active=${is_active}`);
          this.campagn = new CampaignModel(
            resp.data.id,
            resp.data.name,
            resp.data.description,
            resp.data.start_date,
            resp.data.end_date,
            resp.data.budget,
            resp.data.is_smart,
            resp.data.address,
            resp.data.postal_code,
            resp.data.cibles_json,
            resp.data.video_file,
            resp.data.is_active
          );
          return this.campagn;
     
        } catch (error) {
          console.error(error);
          
        }
      }

      async deleteVideoByVideoUrl(videoUrl) {
        try {
          const resp = await api.delete(`/videourl?video_url=${videoUrl}`);
          return resp.data;
        } catch (error) {
          console.error(error);
        }
      }


      async  updateCampaign(campaignId, name, description, budget, is_smart) {
        try {
          const data = {
            name,
            description,
            budget
          };
          const resp = await api.patch(`/updateCampaignIsValid/${campaignId}`, JSON.stringify(data), {
            headers: {
              'Content-Type': 'application/json'
            }
          });
        
          // Supposons que resp.data est l'objet de campagne mis à jour renvoyé par le serveur
          return resp.data;
        } catch (error) {
          console.error(error);
          throw error; // rejet de l'erreur pour la gestion dans les couches supérieures
        }
      }


}

const apiService = new ApiService(); // Créez une instance de la classe ApiService

export { apiService };