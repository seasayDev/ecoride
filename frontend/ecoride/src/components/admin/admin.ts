import axios from 'axios'

export interface Address {
  id: number
  address: string
  country: string
  city: string
  province: string
  postal_code: string
}

export interface Location {
  id: number
  name: string
  id_address: number
}

export interface Image {
  id: number | null
  data: string | null
}

export interface Trotinette {
  id_trotinette: number
  name: string
  category: string
  price: number
  available: number
  location: Location
  image: Image
  qte: number
}

export interface Newscooter {
  name: string
  category: string
  price: number
  available: number
  location: Location
  image: Image
  qte: number
}

export interface Review {
  id: number
  user_email: string
  rating: number
  comment: string | null
  created_at: string
}

export interface ActiveRabais {
  id_rabais: number
  name: string
  value: number
  code: string
  start_date: string
  end_date: string
  active: number
}

export class GetTrotinettes {
  private url: string
  constructor(url: string) {
    this.url = url
  }

  public async getTrotinettes(): Promise<Array<Trotinette>> {
    const { data } = await axios.get(this.url + '/getTrotinettes')
    return data
  }
  public async getLocations(): Promise<Array<Location>> {
    const { data } = await axios.get(this.url + '/getLocations')
    return data
  }
  public async createScooter(model: Newscooter, token?: string): Promise<any> {
    const headers: Record<string, string> = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    const { data } = await axios.post(this.url + '/createScooter', model, { headers })
    return data
  }
  public async updateScooter(model: Newscooter, token?: string): Promise<any> {
    const headers: Record<string, string> = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    const { data } = await axios.put(this.url + '/updateScooter', model, { headers })
    return data
  }
  public async deleteScooter(id_trotinette: number, token?: string): Promise<any> {
    const headers: Record<string, string> = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    const { data } = await axios.post(this.url + '/deleteScooter', { id: id_trotinette }, { headers })
    return data
  }
  public async getAllReservations(token?: string): Promise<any> {
    const headers: Record<string, string> = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    const { data } = await axios.get(this.url + '/get_all_reservations', { headers })
    return data
  }
  public async deleteReservation(id_reservation: number, token?: string): Promise<any> {
    const headers: Record<string, string> = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    const { data } = await axios.delete(this.url + '/delete_reservation', { params: { id_reservation }, headers })
    return data
  }
  public async updateReservation(reservation: any, token?: string): Promise<any> {
    const headers: Record<string, string> = {}
    if (token) headers['Authorization'] = `Bearer ${token}`
    const { data } = await axios.put(this.url + '/update_reservation', reservation, { headers })
    return data
  }
}
