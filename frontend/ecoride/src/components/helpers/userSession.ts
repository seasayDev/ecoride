import { reactive } from 'vue'

interface User {
  message: string
  session: session
}
interface session {
  email?: string
  fname?: string
  id?: string
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
