import {useEffect,useRef} from 'react';
import {Link,useLocation} from 'react-router-dom';
import type {User} from '../../api/auth';

export default function ProfileMenu({user,onLogout,pending}:{user:User;onLogout:()=>void;pending:boolean}) {
  const ref=useRef<HTMLDetailsElement>(null);const location=useLocation();
  useEffect(()=>{if(ref.current)ref.current.open=false;},[location.pathname]);
  useEffect(()=>{
    function close(event:PointerEvent) {if(ref.current&&!ref.current.contains(event.target as Node))ref.current.open=false;}
    document.addEventListener('pointerdown',close);return()=>document.removeEventListener('pointerdown',close);
  },[]);
  return <details ref={ref} className="profile-dropdown" onKeyDown={event=>{if(event.key==='Escape'&&ref.current){ref.current.open=false;ref.current.querySelector('summary')?.focus();}}}><summary className="profile-link" aria-label="프로필 메뉴"><span className="profile-avatar" aria-hidden="true">{user.name.slice(0,1)}</span><span className="user-name">{user.name}님</span><span aria-hidden="true">⌄</span></summary><div className="profile-panel"><div className="profile-identity"><strong>{user.name}</strong><span>{user.email}</span></div><Link to="/my-travels">나의 여행 <span>↗</span></Link><Link to="/favorites">찜한 장소 <span>♡</span></Link><Link to="/preferences">여행 취향 <span>✳</span></Link><Link to="/settings">계정 설정 <span>⚙</span></Link><button disabled={pending} onClick={onLogout}>{pending?'로그아웃 중…':'로그아웃'}</button></div></details>;
}
