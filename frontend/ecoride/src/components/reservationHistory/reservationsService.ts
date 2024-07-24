import axios from 'axios'

export interface Reservation {
  id_reservation: number
  start_date: string
  end_date: string
  pick_up_location: {
    name: string
  }
  drop_off_location: {
    name: string
  }
  total_cost: number
  trotinette: {
    model: string
    category: string
    price: number
    image: string | null
  }
  user: {
    id_user: number
    first_name: string
    last_name: string
  }
}

export class ReservationsService {
  private url: string

  constructor(url: string) {
    this.url = url
  }

  public async getReservations(userId: number): Promise<Reservation[]> {
    try {
      const response = await axios.get<Reservation[]>(this.url, {
        params: { user_id: userId },
        withCredentials: true
      })
      return response.data
    } catch (error) {
      console.error('Error fetching reservations:', error)
      throw error;
    }
  }
  public async cancelReservation(reservationId: number): Promise<void> {
    try {
      const fullUrl = `${this.url}/${reservationId}`;
      console.log('Canceling reservation at URL:', fullUrl);
      const response = await axios.delete(fullUrl, { withCredentials: true });
      console.log('Response from server:', response.data);
    } catch (error) {
      console.error('Error canceling reservation:', error.response ? error.response.data : error.message);
      throw new Error('Failed to cancel reservation');
    }
  }
}
const reservationsService = new ReservationsService('/api/reservations');
