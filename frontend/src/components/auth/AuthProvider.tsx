import {useEffect,type ReactNode} from 'react';
import {useQuery} from '@tanstack/react-query';
import {getCurrentUser} from '../../api/auth';
import {useAuthStore} from '../../stores/authStore';
import {getCurrentPlan} from '../../api/recommendation';
import {useTravelStore} from '../../stores/travelStore';
export default function AuthProvider({children}:{children:ReactNode}) {
  const setUser=useAuthStore(s=>s.setUser);
  const user=useAuthStore(s=>s.user);
  const plans=useQuery({queryKey:['current-plan',user?.id],queryFn:getCurrentPlan,enabled:!!user,retry:false,staleTime:0});
  useEffect(()=>{
    if(plans.isSuccess) {
      if(plans.data)useTravelStore.getState().setResult(plans.data);
      else useTravelStore.getState().clearResult();
    }
  },[plans.data,plans.isSuccess]);
  const session=useQuery({queryKey:['auth','me'],queryFn:getCurrentUser,retry:false,staleTime:0});
  useEffect(()=>{
    if(session.isSuccess)setUser(session.data);
    else if(session.isError)setUser(null);
  },[session.data,session.isSuccess,session.isError,setUser]);
  return <>{children}</>;
}
