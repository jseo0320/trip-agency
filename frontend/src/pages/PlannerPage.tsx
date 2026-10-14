import {useMutation,useQuery,useQueryClient} from '@tanstack/react-query';
import {useNavigate,useSearchParams} from 'react-router-dom';
import {recommend} from '../api/recommendation';
import {getPreferences,getFavorites} from '../api/account';
import {errorMessage} from '../api/client';
import {useTravelStore} from '../stores/travelStore';
import {useAuthStore} from '../stores/authStore';
import TravelForm from '../components/recommendation/TravelForm';

export default function PlannerPage() {
  const navigate=useNavigate();const cache=useQueryClient();const [params]=useSearchParams();
  const user=useAuthStore(s=>s.user);const setResult=useTravelStore(s=>s.setResult);
  const preferences=useQuery({queryKey:['preferences',user?.id],queryFn:getPreferences});
  let mustVisit:string[]=[];
  try {const parsed:unknown=JSON.parse(params.get('must_visit')||'[]');if(Array.isArray(parsed))mustVisit=parsed.filter((v):v is string=>typeof v==='string').slice(0,20);} catch {mustVisit=[];}
  const favorites=useQuery({queryKey:['favorites',user?.id],queryFn:getFavorites,enabled:mustVisit.length>0});
  const cities=[...new Set((favorites.data||[]).filter(place=>mustVisit.includes(place.name)).map(place=>place.city))];
  const mutation=useMutation({mutationFn:recommend,onSuccess:async(data)=>{
    await cache.cancelQueries({queryKey:['current-plan']});cache.setQueriesData({queryKey:['current-plan']},data);setResult(data);
    await cache.invalidateQueries({queryKey:['my-travels']});navigate('/result');
  }});
  const waiting=preferences.isPending||(mustVisit.length>0&&favorites.isPending);
  return <section className="page narrow"><span className="eyebrow">MAKE IT YOURS</span><h1>어떤 여행을 꿈꾸나요?</h1><p>시간과 취향을 알려주시면 방문 순서를 설계해 드려요.</p>{mutation.isError&&<p role="alert" className="notice">{errorMessage(mutation.error)}</p>}{waiting?<p>저장한 여행 취향을 불러오는 중…</p>:preferences.isError?<div className="notice" role="alert"><p>{errorMessage(preferences.error)}</p><button className="chip" onClick={()=>void preferences.refetch()}>다시 불러오기</button></div>:<>{mustVisit.length>0&&favorites.isError&&<p role="alert" className="notice">찜한 장소의 지역을 불러오지 못했습니다. 여행 지역을 직접 선택해 주세요.</p>}<p className="muted">저장한 여행 취향을 기본값으로 적용했어요. 이번 여행에 맞게 바꿀 수 있습니다.</p><TravelForm key={params.toString()} defaults={preferences.data} initialMustVisit={mustVisit} initialCities={cities.length?cities:['busan']} onSubmit={value=>mutation.mutate(value)} pending={mutation.isPending}/></>}</section>;
}
