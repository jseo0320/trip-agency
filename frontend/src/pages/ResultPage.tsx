import {Link} from 'react-router-dom';
import {useTravelStore} from '../stores/travelStore';
import {usePlaces} from '../hooks/usePlaces';
import RouteTimeline from '../components/recommendation/RouteTimeline';
import RecommendationCard from '../components/recommendation/RecommendationCard';
import TripAgencyMap from '../components/map/TripAgencyMap';
import TravelNameForm from '../components/recommendation/TravelNameForm';
import {useQuery} from '@tanstack/react-query';
import {getCurrentPlan} from '../api/recommendation';
import {useAuthStore} from '../stores/authStore';
export default function ResultPage() {
  const result=useTravelStore(s=>s.result);const {data=[]}=usePlaces();const user=useAuthStore(s=>s.user);
  const saved=useQuery({queryKey:['current-plan',user?.id],queryFn:getCurrentPlan,enabled:!!user,retry:false});
  if(!result&&saved.isPending)return <section className="page"><p>저장된 여행을 불러오는 중…</p></section>;
  if(!result&&saved.isError)return <section className="page"><p role="alert">저장된 여행을 불러올 수 없습니다.</p><Link to="/my-travels">나의 여행 보기</Link></section>;
  if(!result)return <section className="page"><h1>여행을 먼저 만들어 주세요.</h1><Link className="button" to="/planner">여행 만들기</Link><Link className="text-link" to="/my-travels">나의 여행 보기</Link></section>;
  const ids=new Set(result.route.map(s=>s.place_id));
  return <section className="page"><span className="eyebrow">YOUR NEXT CHAPTER</span><h1>{result.title||'당신을 위한 하루.'}</h1><p className="muted">계정에 자동 저장된 여행입니다.</p>{result.plan_id&&<TravelNameForm id={result.plan_id} title={result.title||'나의 여행'}/>}<div className="chips"><Link className="button" to="/chat">이 코스를 AI와 수정하기 ↗</Link><Link className="chip" to="/my-travels">나의 여행 보기</Link></div><p>지도 선은 방문 순서를 연결한 표시입니다.</p><div className="result-layout"><RouteTimeline route={result.route}/><TripAgencyMap places={data.filter(p=>ids.has(p.id))} route={result.route}/></div><RecommendationCard result={result}/><Link className="text-link" to="/planner">다른 여행 만들기 →</Link></section>;
}
