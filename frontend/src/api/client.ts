import axios from 'axios';
import {useAuthStore} from '../stores/authStore';
import {useTravelStore} from '../stores/travelStore';
export const client = axios.create({baseURL:import.meta.env.VITE_API_BASE_URL || '/api/v1',timeout:60000,withCredentials:true});
client.interceptors.response.use(response=>response,error=>{
  if(error.response?.status===401 && !['/auth/login','/auth/register'].includes(error.config?.url)) {
    useAuthStore.getState().setUser(null);
    useTravelStore.getState().clearResult();
  }
  return Promise.reject(error);
});
export function errorMessage(error:unknown):string {return axios.isAxiosError(error) ? error.response?.data?.error?.message || '서버에 연결할 수 없습니다.' : '요청 처리 중 오류가 발생했습니다.';}
