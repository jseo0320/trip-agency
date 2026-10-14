import {useState} from 'react';
import {Link} from 'react-router-dom';
import {useQuery} from '@tanstack/react-query';
import {getTravels,type TravelPeriod} from '../api/travels';
import {errorMessage} from '../api/client';
import {useAuthStore} from '../stores/authStore';
import {formatTravelDate} from '../utils/date';
import TravelNameForm from '../components/recommendation/TravelNameForm';

export default function MyTravelsPage() {
  const [page,setPage]=useState(0);const [period,setPeriod]=useState<TravelPeriod>('upcoming');const user=useAuthStore(s=>s.user);
  const query=useQuery({queryKey:['my-travels',user?.id,period,page],queryFn:()=>getTravels(page,period)});
  return <section className="page my-travels"><div className="saved-travels-heading"><div><span className="eyebrow">MY TRAVEL COLLECTION</span><h1>나의 여행</h1><p>{user?.name}님의 여행을 차곡차곡 모았어요. 새 코스를 만들어도 이전 여행은 그대로 보관됩니다.</p></div><Link className="button" to="/planner">＋ 새 여행 만들기</Link></div>
    <div className="travel-period-tabs" aria-label="여행 기간 선택">{([['upcoming','예정된 여행'],['past','지난 여행'],['all','전체 여행']] as const).map(([id,label])=><button key={id} className={period===id?'selected':''} aria-pressed={period===id} onClick={()=>{setPeriod(id);setPage(0);}}>{label}</button>)}</div><p className="muted">한국 시간 기준으로 오늘 여행은 예정된 여행에 포함됩니다.</p>
    {query.isPending?<p role="status">저장한 여행을 불러오는 중…</p>:query.isError?<div className="notice" role="alert"><p>{errorMessage(query.error)}</p><button className="chip" onClick={()=>void query.refetch()}>다시 불러오기</button></div>:<><p className="muted">총 {query.data.total}개의 저장된 코스</p>{!query.data.total?<div className="card empty-travels"><h2>{period==='past'?'지난 여행이 아직 없어요.':period==='upcoming'?'예정된 여행이 아직 없어요.':'첫 번째 여행을 만들어 보세요.'}</h2><p>코스를 만들면 계정에 자동으로 저장됩니다.</p><Link className="button" to="/planner">여행 만들기 ↗</Link></div>:<div className="saved-travel-grid">{query.data.items.map(travel=><article className="card saved-travel" key={travel.id}><div className="chips">{travel.is_current&&<span className="badge level-0">현재 선택된 여행</span>}{travel.is_revision&&<span className="badge level-1">챗봇 수정본</span>}</div><p className="eyebrow">{formatTravelDate(travel.result.travel_date)}</p><h2><Link to={`/my-travels/${travel.id}`}>{travel.title}</Link></h2><p className="muted">{travel.result.route.length}곳 · {new Intl.DateTimeFormat('ko-KR',{dateStyle:'medium',timeZone:'Asia/Seoul'}).format(new Date(travel.created_at))} 저장</p><p className="saved-route-preview">{travel.result.route.map(stop=>stop.place).join(' → ')||'방문 가능한 장소가 없는 일정'}</p><TravelNameForm id={travel.id} title={travel.title}/><Link className="button" to={`/my-travels/${travel.id}`}>여행 코스 보기 ↗</Link></article>)}</div>}{query.data.total>12&&<div className="travel-pagination"><button className="chip" disabled={!page} onClick={()=>setPage(p=>p-1)}>이전</button><span>{page+1} / {Math.ceil(query.data.total/12)}</span><button className="chip" disabled={(page+1)*12>=query.data.total} onClick={()=>setPage(p=>p+1)}>다음</button></div>}</>}
  </section>;
}
