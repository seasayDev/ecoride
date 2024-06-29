import axios from 'axios'

export interface trotinette {
  available: number
  category: string
  id_trotinette: number
  image_id: number | null
  location_id: number
  name: string
  price: number
  qte: number
}

export class GetTrotinettes {
  private url: string
  constructor(url: string) {
    this.url = url
  }

  public async getTrotinettes(): Promise<Array<trotinette>> {
    try {
      const response = await axios.get(this.url + '/getTrotinettes')
      return response.data
    } catch (error) {
      throw error
    }
  }
}
