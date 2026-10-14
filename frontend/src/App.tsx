import {BrowserRouter,Routes,Route,NavLink,useNavigate} from 'react-router-dom';
import {useMutation,useQueryClient} from '@tanstack/react-query';
import HomePage from './pages/HomePage';
import PlannerPage from './pages/PlannerPage';
import MapPage from './pages/MapPage';
import ResultPage from './pages/ResultPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ChatPage from './pages/ChatPage';
import MyTravelsPage from './pages/MyTravelsPage';
import SavedTravelPage from './pages/SavedTravelPage';
import ProfileMenu from './components/auth/ProfileMenu';
import FavoritesPage from './pages/FavoritesPage';
import PreferencesPage from './pages/PreferencesPage';
import SettingsPage from './pages/SettingsPage';
import AuthProvider from './components/auth/AuthProvider';
import RequireAuth from './components/auth/RequireAuth';
import {useAuthStore} from './stores/authStore';
import {useTravelStore} from './stores/travelStore';
import {logout} from './api/auth';
import {errorMessage} from './api/client';

function Header() {
  const {user,ready,setUser}=useAuthStore();
  const cache=useQueryClient();const navigate=useNavigate();
  const clearResult=useTravelStore(s=>s.clearResult);
  const mutation=useMutation({mutationFn:logout,onSuccess:async()=>{
    await cache.cancelQueries();cache.clear();setUser(null);clearResult();navigate('/login');
  }});
  return <><header><NavLink className="brand" to="/">Trip Agency<span>✳</span></NavLink>
    <nav aria-label="메인 메뉴"><NavLink to="/map">여행지 탐색</NavLink><NavLink to="/planner">여행 만들기 ↗</NavLink><NavLink to="/chat">AI 챗봇</NavLink>
      {ready&&(user?<ProfileMenu user={user} onLogout={()=>mutation.mutate()} pending={mutation.isPending}/>:<NavLink to="/login">로그인</NavLink>)}
    </nav></header>{mutation.isError&&<p className="notice" role="alert">{errorMessage(mutation.error)}</p>}</>;
}
export default function App() {
  return <BrowserRouter><AuthProvider><Header/><main><Routes>
    <Route path="/" element={<HomePage/>}/><Route path="/map" element={<MapPage/>}/>
    <Route path="/login" element={<LoginPage/>}/><Route path="/register" element={<RegisterPage/>}/>
    <Route element={<RequireAuth/>}><Route path="/planner" element={<PlannerPage/>}/><Route path="/result" element={<ResultPage/>}/><Route path="/chat" element={<ChatPage/>}/><Route path="/my-travels" element={<MyTravelsPage/>}/><Route path="/my-travels/:planId" element={<SavedTravelPage/>}/><Route path="/favorites" element={<FavoritesPage/>}/><Route path="/preferences" element={<PreferencesPage/>}/><Route path="/settings" element={<SettingsPage/>}/></Route>
    <Route path="*" element={<section className="page"><h1>페이지를 찾을 수 없습니다.</h1></section>}/>
  </Routes></main><footer><strong>Trip Agency</strong><span>Plan Smarter. Travel Better.</span><small>부산 · 울산 · 경주</small></footer></AuthProvider></BrowserRouter>;
}
