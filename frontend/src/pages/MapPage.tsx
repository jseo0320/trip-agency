import {useSearchParams} from 'react-router-dom';
import {usePlaces} from '../hooks/usePlaces';
import TripAgencyMap from '../components/map/TripAgencyMap';
import TouristList from '../components/tourism/TouristList';
export default function MapPage() {const [params,setParams]=useSearchParams();const city=params.get('city')||'busan';const {data=[],isPending,isError}=usePlaces(city);return <section className="page"><span className="eyebrow">EXPLORE THE REGION</span><h1>다음 여행을 발견하세요.</h1><div className="chips">{[['busan','부산'],['ulsan','울산'],['gyeongju','경주']].map(([id,name])=><button className={city===id?'chip selected':'chip'} key={id} onClick={()=>setParams({city:id})}>{name}</button>)}</div><p className="notice">샘플 모드에서는 관광지 운영시간과 혼잡도가 시연용 데이터입니다.</p>{isPending?<p>관광지 불러오는 중…</p>:isError?<p role="alert">관광지를 불러올 수 없습니다.</p>:<><TripAgencyMap places={data}/><TouristList places={data}/></>}</section>;}
