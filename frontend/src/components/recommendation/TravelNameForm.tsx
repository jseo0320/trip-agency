import {useEffect,useState,type FormEvent} from 'react';
import {useMutation,useQueryClient} from '@tanstack/react-query';
import {renameTravel} from '../../api/travels';
import {errorMessage} from '../../api/client';
import {useTravelStore} from '../../stores/travelStore';

export default function TravelNameForm({id,title}:{id:string;title:string}) {
  const [editing,setEditing]=useState(false);const [name,setName]=useState(title);
  const cache=useQueryClient();
  useEffect(()=>setName(title),[title]);
  const mutation=useMutation({mutationFn:()=>renameTravel(id,name.trim()),onSuccess:async(travel)=>{
    setEditing(false);cache.setQueriesData({queryKey:['travel',id]},travel);
    if(useTravelStore.getState().result?.plan_id===id) {
      await cache.cancelQueries({queryKey:['current-plan']});
      cache.setQueriesData({queryKey:['current-plan']},travel.result);
      useTravelStore.getState().setResult(travel.result);
    }
    await cache.invalidateQueries({queryKey:['my-travels']});
  }});
  function submit(event:FormEvent) {event.preventDefault();if(name.trim())mutation.mutate();}
  return <div className="travel-name-editor">{editing?<form onSubmit={submit}><label>여행 이름<input autoFocus required maxLength={80} value={name} onChange={e=>setName(e.target.value)}/></label><div className="chips"><button className="button" disabled={mutation.isPending||!name.trim()}>저장</button><button className="chip" type="button" onClick={()=>{setEditing(false);setName(title);mutation.reset();}} disabled={mutation.isPending}>취소</button></div></form>:<button className="text-link rename-button" onClick={()=>{mutation.reset();setEditing(true);}}>이름 변경 ✎</button>}{mutation.isError&&<p className="notice" role="alert">{errorMessage(mutation.error)}</p>}</div>;
}
