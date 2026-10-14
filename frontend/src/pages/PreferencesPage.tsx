import {useState,type FormEvent} from 'react';
import {useMutation,useQuery,useQueryClient} from '@tanstack/react-query';
import {getPreferences,savePreferences,type TravelPreferences} from '../api/account';
import {errorMessage} from '../api/client';
import {useAuthStore} from '../stores/authStore';
import PreferenceFields from '../components/recommendation/PreferenceFields';

function PreferencesForm({initial}:{initial:TravelPreferences}) {
  const [value,setValue]=useState(initial);const [saved,setSaved]=useState(false);
  const user=useAuthStore(s=>s.user);const cache=useQueryClient();
  const mutation=useMutation({mutationFn:savePreferences,onSuccess:data=>{cache.setQueryData(['preferences',user?.id],data);setSaved(true);}});
  function submit(event:FormEvent) {event.preventDefault();setSaved(false);mutation.mutate(value);}
  return <form className="card travel-form" onSubmit={submit}><PreferenceFields value={value} onChange={next=>{setValue(next);setSaved(false);}}/>{saved&&<p className="success-message" role="status">여행 취향을 저장했습니다. 다음 여행부터 기본값으로 적용돼요.</p>}{mutation.isError&&<p className="notice" role="alert">{errorMessage(mutation.error)}</p>}<button className="button" disabled={mutation.isPending}>{mutation.isPending?'저장 중…':'여행 취향 저장'}</button></form>;
}
export default function PreferencesPage() {
  const user=useAuthStore(s=>s.user);const query=useQuery({queryKey:['preferences',user?.id],queryFn:getPreferences});
  return <section className="page narrow"><span className="eyebrow">YOUR TRAVEL STYLE</span><h1>여행 취향</h1><p>좋아하는 여행을 한 번 저장하고, 다음 코스부터 편하게 시작하세요.</p>{query.isPending?<p>취향을 불러오는 중…</p>:query.isError?<div className="notice" role="alert"><p>{errorMessage(query.error)}</p><button className="chip" onClick={()=>void query.refetch()}>다시 불러오기</button></div>:<PreferencesForm initial={query.data}/>}</section>;
}
