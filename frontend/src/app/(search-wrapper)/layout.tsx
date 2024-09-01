'use client'

import TopBar from "@/components/TopBar"
import { SearchContextProvider } from '@/context/searchContext'
import { useSearchParams, redirect } from "next/navigation"
import { useEffect } from "react"
import { useSession } from "next-auth/react"

export default function SearchWrapperLayout({
    children,
}: {
    children: React.ReactNode
}) {

    const searchParams = useSearchParams()
    const q = searchParams.get('q')

    const { data: session } = useSession()    
    useEffect(() => {
        console.log("session info",session)
    }, [session])

    return (
        <div>
            <SearchContextProvider initialSearchInput={q} >
                <TopBar />
                {session!= null && children}
                {session==null && <div style={{height:"calc(100vh - 80px)"}} className="w-full grid place-items-center" >Sign in to use app</div>}
                
            </SearchContextProvider>
        </div>
    )
}
