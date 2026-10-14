import {client} from './client';
export interface User {id:number;email:string;name:string;created_at:string}
export interface LoginInput {email:string;password:string}
export interface RegisterInput extends LoginInput {name:string}
export interface AuthResponse {access_token:string;token_type:string;expires_in:number;user:User}
export async function login(body:LoginInput):Promise<AuthResponse> {return (await client.post('/auth/login',body)).data;}
export async function register(body:RegisterInput):Promise<AuthResponse> {return (await client.post('/auth/register',body)).data;}
export async function getCurrentUser():Promise<User> {return (await client.get('/auth/me')).data;}
export async function logout():Promise<void> {await client.post('/auth/logout');}
