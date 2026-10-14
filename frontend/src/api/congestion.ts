import {client} from './client';
import type {Congestion} from '../types';
export async function getCongestion(id:number):Promise<Congestion> {return (await client.get(`/congestion/${id}`)).data;}
