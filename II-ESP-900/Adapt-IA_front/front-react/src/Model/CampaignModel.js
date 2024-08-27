class CampaignModel {
    constructor({
        id = '',
        name = '',
        description = '',
        start_date = '',
        end_date = '',
        budget = 0,
        is_smart = false,
        address = '',
        postal_code = '',
        cibles_json = '{}', // Assumant que cela devrait être une chaîne JSON
        video_file = '',
        is_active = false
    } = {}) { // Notez le {} par défaut ici
        this.id = id;
        this.name = name;
        this.description = description;
        this.start_date = start_date;
        this.end_date = end_date;
        this.budget = budget;
        this.is_smart = is_smart;
        this.address = address;
        this.postal_code = postal_code;
        this.cibles_json = cibles_json;
        this.video_file = video_file;
        this.is_active = is_active;
    }
}

    // Add a method or property here.


export default CampaignModel;
