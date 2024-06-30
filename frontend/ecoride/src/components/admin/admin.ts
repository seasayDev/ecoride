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
  address: Address
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
}
