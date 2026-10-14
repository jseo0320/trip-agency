import {client} from './client';
import type {TouristPlace} from '../types';
export async function getPlaces(city?:string):Promise<TouristPlace[]> {return (await client.get('/tourism/places',{params:{city}})).data;}
