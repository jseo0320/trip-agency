import type {TouristPlace} from '../../types';
import FavoriteButton from './FavoriteButton';
export default function TouristCard({place}:{place:TouristPlace}) {return <article className="card"><span className="eyebrow">{place.city} / {place.category}</span><h3>{place.name}</h3><p>{place.description}</p><p className="muted">평균 {place.average_stay_minutes}분 · {place.source==='mock'?'샘플 관광지 정보':place.source}</p><FavoriteButton placeId={place.id}/></article>;}
