import {Navigate,Outlet,useLocation} from 'react-router-dom';
import {useAuthStore} from '../../stores/authStore';
export default function RequireAuth() {
  const {user,ready}=useAuthStore();
  const location=useLocation();
  if(!ready)return <section className="page"><p>로그인 정보를 불러오는 중…</p></section>;
  return user?<Outlet/>:<Navigate to="/login" replace state={{from:location.pathname}}/>;
}
