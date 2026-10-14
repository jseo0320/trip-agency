import {useState} from 'react';
import {Link} from 'react-router-dom';
import {useQuery} from '@tanstack/react-query';
import {getFavorites} from '../api/account';
import {errorMessage} from '../api/client';
import {useAuthStore} from '../stores/authStore';
import TouristCard from '../components/tourism/TouristCard';

export default function FavoritesPage() {
  const user=useAuthStore(s=>s.user);const [selected,setSelected]=useState<number[]>([]);
  const query=useQuery({queryKey:['favorites',user?.id],queryFn:getFavorites});
  const names=(query.data||[]).filter(p=>selected.includes(p.id)).map(p=>p.name);
  return <section className="page"><span className="eyebrow">PLACES TO REMEMBER</span><h1>찜한 장소</h1><p>가고 싶은 장소를 모아두고 다음 여행의 필수 방문 장소로 추가하세요.</p>{query.isPending?<p>찜한 장소를 불러오는 중…</p>:query.isError?<div className="notice" role="alert"><p>{errorMessage(query.error)}</p><button className="chip" onClick={()=>void query.refetch()}>다시 불러오기</button></div>:!query.data.length?<div className="card empty-travels"><h2>아직 찜한 장소가 없어요.</h2><Link className="button" to="/map">여행지 탐색하기 ↗</Link></div>:<><div className="favorites-toolbar"><span>{query.data.length}개의 장소 · {names.length}개 선택</span>{names.length>0&&<Link className="button" to={`/planner?${new URLSearchParams({must_visit:JSON.stringify(names)})}`}>선택한 장소로 여행 만들기 ↗</Link>}</div><div className="cards">{query.data.map(place=><div className="favorite-place" key={place.id}><label className="check"><input type="checkbox" checked={selected.includes(place.id)} onChange={e=>setSelected(previous=>e.target.checked?[...previous,place.id]:previous.filter(id=>id!==place.id))}/>코스에 추가할 장소 선택</label><TouristCard place={place}/></div>)}</div></>}</section>;
}
