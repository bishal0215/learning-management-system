import { AlertCircle, LoaderCircle, SearchX } from 'lucide-react'

export function LoadingState() { return <div className="state"><LoaderCircle className="spin" size={24} /><span>Loading your school data...</span></div> }
export function EmptyState({ children = 'Nothing here yet.' }) { return <div className="state"><SearchX size={24} /><span>{children}</span></div> }
export function ErrorState({ message }) { return <div className="state error-state"><AlertCircle size={24} /><span>{message}</span></div> }
