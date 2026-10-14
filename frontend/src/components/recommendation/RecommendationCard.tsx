import type {Recommendation} from '../../types';
import {formatTravelDate} from '../../utils/date';
export default function RecommendationCard({result}:{result:Recommendation}) {return <article className="card"><span className="eyebrow">YOUR TRIP, EXPLAINED</span><h2>여행을 위한 안내</h2><p className="trip-date">{formatTravelDate(result.travel_date)}</p><p style={{whiteSpace:'pre-wrap'}}>{result.summary}</p>{result.warnings.map(w=><p className="notice" key={w}>{w}</p>)}</article>;}
