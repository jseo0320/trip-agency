import {Link} from 'react-router-dom';
import {useMutation,useQuery,useQueryClient} from '@tanstack/react-query';
import {getFavorites,setFavorite} from '../../api/account';
import {errorMessage} from '../../api/client';
import {useAuthStore} from '../../stores/authStore';

export default function FavoriteButton({placeId}:{placeId:number}) {
  const user=useAuthStore(s=>s.user);const cache=useQueryClient();
  const favorites=useQuery({queryKey:['favorites',user?.id],queryFn:getFavorites,enabled:!!user});
  const saved=!!favorites.data?.some(p=>p.id===placeId);
  const mutation=useMutation({mutationFn:()=>setFavorite(placeId,!saved),onSuccess:()=>cache.invalidateQueries({queryKey:['favorites',user?.id]})});
  if(!user)return <Link className="favorite-button" to="/login">♡ 찜하려면 로그인</Link>;
  return <div><button className={`favorite-button ${saved?'saved':''}`} aria-pressed={saved} disabled={mutation.isPending||favorites.isPending||favorites.isError} onClick={()=>mutation.mutate()}>{saved?'♥ 찜한 장소':'♡ 찜하기'}</button>{mutation.isError&&<p role="alert" className="muted">{errorMessage(mutation.error)}</p>}{favorites.isError&&<button className="favorite-button" onClick={()=>void favorites.refetch()}>찜 목록 다시 불러오기</button>}</div>;
}
