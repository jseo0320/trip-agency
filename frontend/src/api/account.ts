import {client} from './client';
import type {User} from './auth';
import type {TouristPlace} from '../types';
export interface TravelPreferences {preferences:string[];transportation:'public'|'car';walking_preference:'low'|'normal'|'high';avoid_congestion:boolean}
export async function getPreferences():Promise<TravelPreferences> {return (await client.get('/account/preferences')).data;}
export async function savePreferences(body:TravelPreferences):Promise<TravelPreferences> {return (await client.put('/account/preferences',body)).data;}
export async function updateProfile(name:string):Promise<User> {return (await client.patch('/account/profile',{name})).data;}
export async function changePassword(current_password:string,new_password:string):Promise<void> {await client.post('/account/password',{current_password,new_password});}
export async function getFavorites():Promise<TouristPlace[]> {return (await client.get('/account/favorites')).data;}
export async function setFavorite(id:number,saved:boolean):Promise<void> {if(saved)await client.put(`/account/favorites/${id}`);else await client.delete(`/account/favorites/${id}`);}
