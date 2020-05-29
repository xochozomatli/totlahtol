import { createContext, useContext } from 'react'

export const UserContext = createContext()

export function useUser() {
    useContext(UserContext)
}