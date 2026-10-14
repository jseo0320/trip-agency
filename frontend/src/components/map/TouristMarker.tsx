import {CircleMarker,Popup} from 'react-leaflet';
import type {TouristPlace} from '../../types';
import CongestionCard from '../congestion/CongestionCard';
export default function TouristMarker({place}:{place:TouristPlace}) {return <CircleMarker center={[place.latitude,place.longitude]} radius={9} pathOptions={{color:'#163f3a',fillColor:'#e3b65a',fillOpacity:1}}><Popup><strong>{place.name}</strong><p>{place.opening_time.slice(0,5)}–{place.closing_time.slice(0,5)}</p><CongestionCard id={place.id}/></Popup></CircleMarker>;}
