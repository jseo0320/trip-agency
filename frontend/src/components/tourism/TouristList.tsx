import type {TouristPlace} from '../../types';
import TouristCard from './TouristCard';
export default function TouristList({places}:{places:TouristPlace[]}) {return <div className="cards">{places.map(p=><TouristCard key={p.id} place={p}/>)}</div>;}
