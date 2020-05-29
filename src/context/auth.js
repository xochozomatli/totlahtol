import { createContext, useContext } from 'react'

export const AuthContext = createContext()

export function useAuth() {
    useContext(AuthContext)
}