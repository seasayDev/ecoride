import axios from 'axios'
export interface register {
  firstName: string
  lastName: string
  country: string
  address: string
  city: string
  province: string
  postalCode: string
  birthdate: string
  email: string
  phone: string
  password: string
  confirmPassword: string
}

export class RegisterUser {
  private url: string

  constructor(url: string) {
    this.url = url
  }

  public async registerUser(model: register): Promise<any> {
    try {
      const response = await axios.post(this.url, model)
      return response.data
    } catch (error) {
      return undefined
    }
  }
}
