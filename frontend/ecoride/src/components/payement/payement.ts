import axios from 'axios'

export interface PaymentForm {
  amount: string
  cardNumber: string
  expiry: string
  cvv: string
  cardName: string
  user_id: string
  trotinette: any
  reservationDate: string
  reservationTime: string
  reservationDuration: number
  dropOutLocation: string
  totalCost: number
}

export class PaymentService {
  private url: string

  constructor(url: string) {
    this.url = url
  }

  public async processPayment(form: PaymentForm): Promise<any> {
    try {
      const response = await axios.post(this.url, form, { withCredentials: true })
      return response.data
    } catch (error) {
      throw error
    }
  }
}
