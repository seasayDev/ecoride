import axios from 'axios';

export interface SupportRequest {
  user_id: number;
  support_option: string;
  message: string;
}

export class SupportService {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  public async submitRequest(model: SupportRequest): Promise<any> {
    try {
      const response = await axios.post(this.url, model);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}
