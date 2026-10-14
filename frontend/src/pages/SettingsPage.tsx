import {useState,type FormEvent} from 'react';
import {useNavigate} from 'react-router-dom';
import {useMutation,useQueryClient} from '@tanstack/react-query';
import {updateProfile,changePassword} from '../api/account';
import {errorMessage} from '../api/client';
import {useAuthStore} from '../stores/authStore';
import {useTravelStore} from '../stores/travelStore';

export default function SettingsPage() {
  const {user,setUser}=useAuthStore();const cache=useQueryClient();const navigate=useNavigate();
  const [name,setName]=useState(user?.name||'');const [current,setCurrent]=useState('');const [next,setNext]=useState('');const [confirm,setConfirm]=useState('');const [formError,setFormError]=useState('');
  const profile=useMutation({mutationFn:()=>updateProfile(name.trim()),onSuccess:async(data)=>{await cache.cancelQueries({queryKey:['auth','me']});cache.setQueryData(['auth','me'],data);setUser(data);}});
  const password=useMutation({mutationFn:()=>changePassword(current,next),onSuccess:async()=>{await cache.cancelQueries();cache.clear();setUser(null);useTravelStore.getState().clearResult();navigate('/login',{replace:true,state:{passwordChanged:true}});}});
  function saveName(event:FormEvent) {event.preventDefault();profile.mutate();}
  function savePassword(event:FormEvent) {event.preventDefault();setFormError('');if(next!==confirm){setFormError('새 비밀번호가 일치하지 않습니다.');return;}password.mutate();}
  return <section className="page narrow"><span className="eyebrow">ACCOUNT SETTINGS</span><h1>계정 설정</h1><p>내 정보와 비밀번호를 관리하세요.</p><form className="card travel-form settings-card" onSubmit={saveName}><h2>내 정보</h2><label>이메일<input readOnly value={user?.email||''}/></label><label>이름<input required maxLength={80} autoComplete="name" value={name} onChange={e=>{setName(e.target.value);profile.reset();}}/></label>{profile.isSuccess&&<p className="success-message" role="status">이름을 변경했습니다.</p>}{profile.isError&&<p className="notice" role="alert">{errorMessage(profile.error)}</p>}<button className="button" disabled={profile.isPending||!name.trim()}>이름 저장</button></form><form className="card travel-form settings-card" onSubmit={savePassword}><h2>비밀번호 변경</h2><label>현재 비밀번호<input type="password" required maxLength={128} autoComplete="current-password" value={current} onChange={e=>setCurrent(e.target.value)}/></label><label>새 비밀번호<input type="password" required minLength={10} maxLength={128} autoComplete="new-password" value={next} onChange={e=>setNext(e.target.value)}/><small className="muted">10~128자로 입력하세요.</small></label><label>새 비밀번호 확인<input type="password" required maxLength={128} autoComplete="new-password" value={confirm} onChange={e=>setConfirm(e.target.value)}/></label><p className="muted">변경하면 모든 기기의 로그인 세션이 종료됩니다. 저장한 여행은 유지됩니다.</p>{(formError||password.isError)&&<p className="notice" role="alert">{formError||errorMessage(password.error)}</p>}<button className="button" disabled={password.isPending}>{password.isPending?'변경 중…':'비밀번호 변경'}</button></form></section>;
}
