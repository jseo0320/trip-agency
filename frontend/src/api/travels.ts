import {client} from './client';
import type {Recommendation} from '../types';
export interface SavedTravel {id:string;title:string;created_at:string;is_current:boolean;is_revision:boolean;result:Recommendation}
export type TravelPeriod='upcoming'|'past'|'all';
export async function getTravels(page=0,period:TravelPeriod='upcoming'):Promise<{items:SavedTravel[];total:number}> {
  return (await client.get('/travels',{params:{offset:page*12,limit:12,period}})).data;
}
export async function getTravel(id:string):Promise<SavedTravel> {return (await client.get(`/travels/${id}`)).data;}
export async function renameTravel(id:string,title:string):Promise<SavedTravel> {return (await client.patch(`/travels/${id}`,{title})).data;}
export async function selectTravel(id:string):Promise<Recommendation> {return (await client.post(`/travels/${id}/select`)).data;}
