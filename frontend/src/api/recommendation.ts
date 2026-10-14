import {client} from './client';
import type {TravelRequest,Recommendation} from '../types';
export async function recommend(body:TravelRequest):Promise<Recommendation> {return (await client.post('/recommendations',body)).data;}
export async function getCurrentPlan():Promise<Recommendation|null> {return (await client.get('/recommendations/current')).data;}
export async function applyPlan(id:string):Promise<Recommendation> {return (await client.post(`/recommendations/${id}/apply`)).data;}
