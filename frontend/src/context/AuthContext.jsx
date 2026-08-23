import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!localStorage.getItem('school_access_token')) {
      setLoading(false)
      return
    }
    api.me().then(setUser).catch(() => localStorage.removeItem('school_access_token')).finally(() => setLoading(false))
  }, [])

  async function signIn(username, password) {
    const tokens = await api.login(username, password)
    localStorage.setItem('school_access_token', tokens.access_token)
    localStorage.setItem('school_refresh_token', tokens.refresh_token)
    setUser(await api.me())
  }

  function signOut() {
    localStorage.removeItem('school_access_token')
    localStorage.removeItem('school_refresh_token')
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, loading, signIn, signOut }}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
