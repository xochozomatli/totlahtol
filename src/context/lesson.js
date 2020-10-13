import { createContext, useContext } from 'react'

export const LessonContext = createContext()

export function useLesson() {
    return useContext(LessonContext)
}