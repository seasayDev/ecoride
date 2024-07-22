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

export class GetTrotinettes {
  private url: string
  constructor(url: string) {
    this.url = url
  }

  public async getTrotinettes(): Promise<Array<Trotinette>> {
    try {
      const response = await axios.get(this.url + '/getTrotinettes')
      return response.data
    } catch (error) {
      throw error
    }
  }
  public async getLocations(): Promise<Array<Location>> {
    try {
      const response = await axios.get(this.url + '/getLocations')
      return response.data
    } catch (error) {
      throw error
    }
  }
  public async createScooter(model: Newscooter): Promise<any> {
    try {
      const response = await axios.post(this.url + '/createScooter', model)
      return response.data
    } catch (error) {
      return response.error
    }
  }
  public async updateScooter(model: Newscooter): Promise<any> {
    try {
      const response = await axios.put(this.url + '/updateScooter', model)
      return response.data
    } catch (error) {
      return response.error
    }
  }
  public async deleteScooter(id_trotinette: number): Promise<any> {
    try {
      const response = await axios.post(this.url + '/deleteScooter', { id: id_trotinette })
      return response.data
    } catch (error) {
      return response.error
    }
  }

  public async getAllReservations(): Promise<any> {
    try {
      const response = await axios.get(this.url + '/get_all_reservations')
      return response.data
    } catch (error) {
      return response.error
    }
  }
}
