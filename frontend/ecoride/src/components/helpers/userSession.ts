import { reactive } from 'vue'

interface User {
  email?: string
  fname?: string
  id?: string
  id_user?: string
  name?: string
  role?: string
}

export const userStore = reactive({
  user: null as User | null
})

export function setUser(user: User | null) {
  userStore.user = user
  if (user) {
    sessionStorage.setItem('user', JSON.stringify(user))
  } else {
    sessionStorage.removeItem('user')
  }
}

export function getUserFromStorage() {
  const userData = sessionStorage.getItem('user')
  userStore.user = userData ? JSON.parse(userData) : null
}
