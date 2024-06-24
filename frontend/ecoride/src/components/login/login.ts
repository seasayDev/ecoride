import axios from 'axios'
export interface loginModel {
  email: string
  password: string
}

export class LoginUser {
  private url: string
  constructor(url: string) {
    this.url = url
  }

  public async connexion(model: loginModel): Promise<any> {
    try {
      const response = await axios.post(this.url + '/login', model)
      return response.data
    } catch (error) {
      throw error
    }
  }
  public async deconnexion(id_user: string) {
    try {
      const response = await axios.post(this.url + '/logout', { id: id_user })
      return response.data
    } catch (e) {}
  }
}
