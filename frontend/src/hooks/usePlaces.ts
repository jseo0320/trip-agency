import {useQuery} from '@tanstack/react-query';
import {getPlaces} from '../api/tourism';
export function usePlaces(city?:string) {return useQuery({queryKey:['places',city],queryFn:()=>getPlaces(city)});}
