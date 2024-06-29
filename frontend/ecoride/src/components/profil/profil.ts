import axios from 'axios';

export interface UserProfile {
  firstName: string;
  lastName: string;
  email: string;
  dateOfBirth: string;
  phone: string;
  address: string;
  country: string;
  city: string;
  province: string;
  postalCode: string;
}

export class ProfileService {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  public async getUserProfile(email: string): Promise<UserProfile> {
    try {
      const response = await axios.get(this.url, {
        params: {
          email: email
        },
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      throw new Error('Erreur lors de la récupération du profil utilisateur');
    }
  }
}