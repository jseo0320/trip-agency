import {Polyline} from 'react-leaflet';
import type {RouteStop} from '../../types';
export default function RoutePolyline({route}:{route:RouteStop[]}) {return <Polyline positions={route.map(p=>[p.latitude,p.longitude] as [number,number])} pathOptions={{color:'#163f3a',weight:4,dashArray:'8 8'}}/>;}
