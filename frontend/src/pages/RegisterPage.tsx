import {useState,type FormEvent} from 'react';
import {Link,useNavigate} from 'react-router-dom';
import {useMutation,useQueryClient} from '@tanstack/react-query';
import {register} from '../api/auth';
import {errorMessage} from '../api/client';
import {useAuthStore} from '../stores/authStore';
export default function RegisterPage() {
  const [name,setName]=useState('');const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');const [confirmation,setConfirmation]=useState('');
  const [formError,setFormError]=useState('');const navigate=useNavigate();const cache=useQueryClient();
  const setUser=useAuthStore(s=>s.setUser);
  const mutation=useMutation({mutationFn:register,onSuccess:async(data)=>{
    await cache.cancelQueries({queryKey:['auth','me']});cache.setQueryData(['auth','me'],data.user);
    setUser(data.user);navigate('/planner',{replace:true});
  }});
  function submit(event:FormEvent) {
    event.preventDefault();setFormError('');
    if(!name.trim()){setFormError('이름을 입력하세요.');return;}
    if(password!==confirmation){setFormError('비밀번호가 일치하지 않습니다.');return;}
    mutation.mutate({name:name.trim(),email:email.trim(),password});
  }
  return <section className="page auth-page"><span className="eyebrow">YOUR JOURNEY STARTS HERE</span><h1>여행의 시작, 회원가입.</h1><p>계정을 만들고 당신만의 여행을 계획하세요.</p><form className="card travel-form" onSubmit={submit}>
    <label>이름<input required maxLength={80} autoComplete="name" value={name} onChange={e=>setName(e.target.value)}/></label>
    <label>이메일<input type="email" required maxLength={254} autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)}/></label>
    <label>비밀번호<input type="password" required minLength={10} maxLength={128} autoComplete="new-password" value={password} onChange={e=>setPassword(e.target.value)}/><small className="muted">10~128자로 입력하세요.</small></label>
    <label>비밀번호 확인<input type="password" required maxLength={128} autoComplete="new-password" value={confirmation} onChange={e=>setConfirmation(e.target.value)}/></label>
    {(formError||mutation.isError)&&<p className="notice" role="alert">{formError||errorMessage(mutation.error)}</p>}
    <button className="button" disabled={mutation.isPending}>{mutation.isPending?'가입 중…':'회원가입하고 시작하기'}</button><p className="auth-link">이미 계정이 있나요? <Link to="/login">로그인</Link></p>
  </form></section>;
}
