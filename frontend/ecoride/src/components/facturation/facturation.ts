import axios from 'axios';

export interface FacturationInfo {
  nom: string;
  prenom: string;
  adresse: string;
  ville: string;
  province: string;
  codePostal: string;
  telephone: string;
  montant: number;
}

export class FacturationService {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  public async addFacturation(id_user: string, facturation: FacturationInfo): Promise<void> {
    try {
      await axios.post(`${this.url}/facturation`, { id_user, ...facturation }, {
        withCredentials: true
      });
    } catch (error) {
      throw new Error('Erreur lors de l\'ajout des informations de facturation');
    }
  }

  public async getFacturation(id_user: string): Promise<FacturationInfo> {
    try {
      const response = await axios.get(`${this.url}/facturation/${id_user}`, {
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      throw new Error('Erreur lors de la récupération des informations de facturation');
    }
  }

  public async updateFacturation(id_user: string, facturation: FacturationInfo): Promise<void> {
    try {
      await axios.put(`${this.url}/facturation/${id_user}`, facturation, {
        withCredentials: true
      });
    } catch (error) {
      throw new Error('Erreur lors de la mise à jour des informations de facturation');
    }
  }
}