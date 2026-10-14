import {useEffect} from 'react';
import {MapContainer,TileLayer,useMap} from 'react-leaflet';
import type {TouristPlace,RouteStop} from '../../types';
import TouristMarker from './TouristMarker';
import RoutePolyline from './RoutePolyline';
function Bounds({places}:{places:TouristPlace[]}) {const map=useMap();useEffect(()=>{if(places.length)map.fitBounds(places.map(p=>[p.latitude,p.longitude] as [number,number]),{padding:[35,35],maxZoom:13});},[places,map]);return null;}
export default function TripAgencyMap({places,route=[]}:{places:TouristPlace[];route?:RouteStop[]}) {return <div className="map-frame"><MapContainer center={[35.18,129.08]} zoom={10} scrollWheelZoom={false} style={{height:'100%',width:'100%'}}><TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/><Bounds places={places}/>{places.map(p=><TouristMarker key={p.id} place={p}/>)}<RoutePolyline route={route}/></MapContainer></div>;}
