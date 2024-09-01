'use client'

import MovieCard from "@/components/MovieCard";
import { useEffect, useState } from "react";
import { useSession } from "next-auth/react"

type Movie = {
  id: number;
  rating: number | null;
  name: string;
  description: string;
};


export default function Home() {
  const { data: session } = useSession()  

  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    const fetchMovies = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/rated-movies?email=${session?.user?.email}`, {
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
          rating: movie.rating,
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

  if (loading) {
    return <div></div>;
  }

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
    </>
  )
}
