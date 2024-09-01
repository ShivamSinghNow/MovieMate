'use client'
// import Footer from '@/components/Footer'
import { ReadonlyURLSearchParams, useSearchParams } from 'next/navigation'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { useSearchContext } from '@/context/searchContext'
import MovieCard from '@/components/MovieCard'
import { useSession } from 'next-auth/react'

type Movie = {
    id: number;
    rating: number | null;
    name: string;
    description: string;
};

export default function Home() {
    const router = useRouter()
    const searchParams = useSearchParams()
    const ctx = useSearchContext()
    const { data: session } = useSession()  

    function getURLParams(searchParams: ReadonlyURLSearchParams): string {
        const newParams = new URLSearchParams(searchParams.toString());
        newParams.delete("q")
        return `?${newParams.toString()}`;
    }

    useEffect(() => {
        if (ctx.searchInput === '') {
            router.push(ctx.lastPage + getURLParams(searchParams))
        }
    }, [ctx.searchInput])

    const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    const fetchMovies = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/all-movies?user_email=${session?.user?.email}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const fetchedMovies = result.data.map((movie:Movie) => ({
          id: movie.id,
          name: movie.name,
          description: movie.description,
          rating: null
        }));

        console.log("res",fetchedMovies)

        setMovies(fetchedMovies);
      } catch (error) {
        console.error('Failed to fetch movies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

    return (
        <>
            <main className='w-full flex flex-col h-full'>
            <div className='container mx-auto px-4 mt-8'>
          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
            {movies && movies.map((movie, id) => {
              console.log("movie",movie)
              return (
                // <h1>{movie.id}</h1>
                <MovieCard key={id} id={movie.id} name={movie.name} description={movie.description} rating={movie.rating}  />
              )
            })}
          </div>
        </div>

            </main>
            {/* <Footer /> */}
        </>
    )
}
