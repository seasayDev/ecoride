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
