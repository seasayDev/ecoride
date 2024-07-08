import axios from 'axios';

export interface PaymentForm {
  amount: string;
  cardNumber: string;
  expiry: string;
  cvv: string;
  cardName: string;
}

export class PaymentService {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  public async processPayment(form: PaymentForm): Promise<any> {
    try {
      const response = await axios.post(this.url, form, { withCredentials: true });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}