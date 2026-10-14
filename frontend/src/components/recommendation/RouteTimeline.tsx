import type {RouteStop} from '../../types';
import CongestionBadge from '../congestion/CongestionBadge';
export default function RouteTimeline({route}:{route:RouteStop[]}) {return <ol className="timeline">{route.map(s=><li key={s.place_id}><span className="eyebrow">{s.arrival_time} — {s.departure_time}</span><h3>{s.order}. {s.place}</h3><CongestionBadge score={s.congestion_score}/><p>이전 위치에서 약 {s.travel_minutes}분 · 체류 {s.stay_minutes}분</p><p className="muted">{s.reason}</p></li>)}</ol>;}
