import {useQuery} from '@tanstack/react-query';
import {getCongestion} from '../../api/congestion';
import CongestionBadge from './CongestionBadge';
export default function CongestionCard({id}:{id:number}) {const {data,isPending,isError}=useQuery({queryKey:['congestion',id],queryFn:()=>getCongestion(id)});if(isPending)return <p>혼잡도 불러오는 중…</p>;if(isError)return <p>혼잡도 정보 없음</p>;return <div><CongestionBadge score={data.current.score}/><p className="muted">{data.source.startsWith('mock')?'샘플 혼잡도':'저장된 관측값'}</p>{data.forecast.length ? data.forecast.map(f=><p key={f.hour}>{f.hour}시간 후: {f.score}</p>):<p className="muted">미래 예측 데이터 없음</p>}</div>;}
