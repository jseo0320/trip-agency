import {create} from 'zustand';
import type {User} from '../api/auth';
interface AuthState {user:User|null;ready:boolean;setUser:(user:User|null)=>void}
// JWT is stored in an HttpOnly cookie rather than browser storage.
export const useAuthStore=create<AuthState>((set)=>({user:null,ready:false,setUser:(user)=>set({user,ready:true})}));
