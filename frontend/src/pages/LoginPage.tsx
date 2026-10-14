import {useState,type FormEvent} from 'react';
import {Link,useLocation,useNavigate} from 'react-router-dom';
import {useMutation,useQueryClient} from '@tanstack/react-query';
import {login} from '../api/auth';
import {errorMessage} from '../api/client';
import {useAuthStore} from '../stores/authStore';
export default function LoginPage() {
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');
  const navigate=useNavigate();const location=useLocation();const cache=useQueryClient();
  const setUser=useAuthStore(s=>s.setUser);
  const mutation=useMutation({mutationFn:login,onSuccess:async(data)=>{
    await cache.cancelQueries({queryKey:['auth','me']});
    cache.setQueryData(['auth','me'],data.user);setUser(data.user);
    const from=location.state?.from;
    navigate(typeof from==='string' && (/^\/(planner|result|chat|my-travels|favorites|preferences|settings)$/.test(from)||/^\/my-travels\/[a-f0-9]{32}$/.test(from))?from:'/my-travels',{replace:true});
  }});
  function submit(event:FormEvent) {event.preventDefault();mutation.mutate({email:email.trim(),password});}
  return <section className="page auth-page"><span className="eyebrow">WELCOME BACK</span><h1>다시 만나 반가워요.</h1><p>로그인하고 나만의 여행을 만들어 보세요.</p>{location.state?.passwordChanged&&<p className="success-message" role="status">비밀번호를 변경했습니다. 새 비밀번호로 다시 로그인하세요.</p>}<form className="card travel-form" onSubmit={submit}>
    <label>이메일<input type="email" required maxLength={254} autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)}/></label>
    <label>비밀번호<input type="password" required maxLength={128} autoComplete="current-password" value={password} onChange={e=>setPassword(e.target.value)}/></label>
    {mutation.isError&&<p className="notice" role="alert">{errorMessage(mutation.error)}</p>}
    <button className="button" disabled={mutation.isPending}>{mutation.isPending?'로그인 중…':'로그인'}</button><p className="auth-link">아직 계정이 없나요? <Link to="/register">회원가입</Link></p>
  </form></section>;
}
