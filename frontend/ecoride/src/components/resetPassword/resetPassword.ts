import axios from 'axios'
export interface resetEmailModel {
  email: string
}

export class ResetPassword {
  private url: string
  constructor(url: string) {
    this.url = url
  }

  public async resetPassword(model: resetEmailModel): Promise<any> {
    try {
      const response = await axios.post(this.url + '/resetPassword', model)
      return response.data
    } catch (error) {
      throw error
    }
  }
}
