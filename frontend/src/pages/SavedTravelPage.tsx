import {Link,useNavigate,useParams} from 'react-router-dom';
import {useMutation,useQuery,useQueryClient} from '@tanstack/react-query';
import {getTravel,selectTravel} from '../api/travels';
import {errorMessage} from '../api/client';
import {useTravelStore} from '../stores/travelStore';
import {usePlaces} from '../hooks/usePlaces';
import RouteTimeline from '../components/recommendation/RouteTimeline';
import RecommendationCard from '../components/recommendation/RecommendationCard';
import TravelNameForm from '../components/recommendation/TravelNameForm';
import TripAgencyMap from '../components/map/TripAgencyMap';
import {useAuthStore} from '../stores/authStore';

export default function SavedTravelPage() {
  const {planId=''}=useParams();const navigate=useNavigate();const cache=useQueryClient();
  const user=useAuthStore(s=>s.user);
  const query=useQuery({queryKey:['travel',planId,user?.id],queryFn:()=>getTravel(planId),retry:false});
  const {data:places=[]}=usePlaces();const setResult=useTravelStore(s=>s.setResult);
  const select=useMutation({mutationFn:()=>selectTravel(planId),onSuccess:async(result)=>{
    await cache.cancelQueries({queryKey:['current-plan']});cache.setQueriesData({queryKey:['current-plan']},result);setResult(result);
    await cache.invalidateQueries({queryKey:['my-travels']});await cache.invalidateQueries({queryKey:['travel']});navigate('/chat');
  }});
  if(query.isPending)return <section className="page"><p>여행을 불러오는 중…</p></section>;
  if(query.isError)return <section className="page"><p className="notice" role="alert">{errorMessage(query.error)}</p><Link to="/my-travels">나의 여행으로 돌아가기</Link></section>;
  const travel=query.data;const ids=new Set(travel.result.route.map(stop=>stop.place_id));
  return <section className="page"><Link className="text-link" to="/my-travels">← 나의 여행</Link><span className="eyebrow saved-detail-label">SAVED TRAVEL</span><h1>{travel.title}</h1><TravelNameForm id={travel.id} title={travel.title}/><button className="button" onClick={()=>select.mutate()} disabled={select.isPending}>{select.isPending?'여행 선택 중…':'이 여행을 AI와 수정하기 ↗'}</button>{select.isError&&<p className="notice" role="alert">{errorMessage(select.error)}</p>}<p className="muted">이 여행을 선택하면 챗봇이 해당 코스를 참고합니다. 다른 저장 여행은 유지됩니다.</p><div className="result-layout"><RouteTimeline route={travel.result.route}/><TripAgencyMap places={places.filter(place=>ids.has(place.id))} route={travel.result.route}/></div><RecommendationCard result={travel.result}/></section>;
}
