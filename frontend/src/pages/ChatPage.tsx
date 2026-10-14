import {useEffect,useRef,useState,type FormEvent,type KeyboardEvent} from 'react';
import {Link} from 'react-router-dom';
import {sendChat,type ChatMessage} from '../api/chat';
import {errorMessage} from '../api/client';
import {useQueryClient} from '@tanstack/react-query';
import {applyPlan} from '../api/recommendation';
import {useTravelStore} from '../stores/travelStore';
import type {Recommendation} from '../types';
import {formatTravelDate} from '../utils/date';
import RouteTimeline from '../components/recommendation/RouteTimeline';

const suggestions=['부산에서 하루 동안 바다를 즐기는 여행을 추천해 줘','경주에서 부모님과 가기 좋은 곳이 궁금해','울산에서 조용히 산책할 만한 곳은 어디야?'];

export default function ChatPage() {
  const [messages,setMessages]=useState<ChatMessage[]>([]);
  const [input,setInput]=useState('');
  const [pending,setPending]=useState(false);
  const [error,setError]=useState('');
  const [failedHistory,setFailedHistory]=useState<ChatMessage[]|null>(null);
  const [proposal,setProposal]=useState<Recommendation|null>(null);
  const [applying,setApplying]=useState(false);
  const [applyError,setApplyError]=useState('');
  const currentPlan=useTravelStore(s=>s.result);
  const setPlan=useTravelStore(s=>s.setResult);
  const cache=useQueryClient();
  const endRef=useRef<HTMLDivElement>(null);
  const inputRef=useRef<HTMLTextAreaElement>(null);
  const busyRef=useRef(false);
  const requestId=useRef(0);

  useEffect(()=>{endRef.current?.scrollIntoView({behavior:'smooth',block:'nearest'});},[messages,pending,error]);
  useEffect(()=>()=>{requestId.current+=1;},[]);

  async function requestReply(history:ChatMessage[]) {
    if(busyRef.current)return;
    busyRef.current=true;const id=++requestId.current;
    setPending(true);setError('');setFailedHistory(null);
    setProposal(null);setApplyError('');
    try {
      // Keep complete recent turns within the API context budget.
      let context=history.slice(-19);
      while(context.length>1 && context.reduce((n,m)=>n+m.content.length,0)>24000)context=context.slice(2);
      const result=await sendChat(context);
      if(id!==requestId.current)return;
      if(result.current_plan)setPlan(result.current_plan);
      setProposal(result.proposed_plan);
      setMessages([...history,{role:'assistant',content:result.message}]);
    } catch(cause) {
      if(id!==requestId.current)return;
      setError(errorMessage(cause));setFailedHistory(history);
    } finally {
      if(id===requestId.current){busyRef.current=false;setPending(false);inputRef.current?.focus();}
    }
  }
  function send(text=input) {
    const content=text.trim();
    if(!content||busyRef.current||failedHistory||applying)return;
    const history=[...messages,{role:'user' as const,content}];
    setMessages(history);setInput('');void requestReply(history);
  }
  function submit(event:FormEvent) {event.preventDefault();send();}
  function keyDown(event:KeyboardEvent<HTMLTextAreaElement>) {
    if(event.key==='Enter'&&!event.shiftKey&&!event.nativeEvent.isComposing){event.preventDefault();send();}
  }
  function reset() {
    if(busyRef.current)return;
    setMessages([]);setInput('');setError('');setFailedHistory(null);setProposal(null);setApplyError('');inputRef.current?.focus();
  }
  async function acceptProposal() {
    if(!proposal?.plan_id||applying||pending)return;
    setApplying(true);setApplyError('');
    try {
      const updated=await applyPlan(proposal.plan_id);
      await cache.cancelQueries({queryKey:['current-plan']});
      cache.setQueriesData({queryKey:['current-plan']},updated);
      setPlan(updated);setProposal(null);
      await cache.invalidateQueries({queryKey:['my-travels']});
      await cache.invalidateQueries({queryKey:['travel']});
      setMessages(previous=>[...previous,{role:'assistant',content:'변경안을 적용했습니다. 추천 결과와 지도에 새 코스가 반영되었어요. 이어서 다른 부분도 조정할 수 있습니다.'}]);
    } catch(cause) {setApplyError(errorMessage(cause));}
    finally {setApplying(false);}
  }
  return <section className="chat-page">
    <aside className="chat-sidebar"><span className="eyebrow">TRIP AGENCY AI</span><h2>여행의 시작은<br/>대화부터.</h2><button className="button" onClick={reset} disabled={pending||applying}>＋ 새 대화</button><p>이전 메시지와 현재 코스를 함께 참고해요.</p>{currentPlan&&<div className="chat-current-plan"><strong>현재 여행 코스</strong><p>{formatTravelDate(currentPlan.travel_date)}</p><ol>{currentPlan.route.map(stop=><li key={stop.place_id}>{stop.arrival_time} {stop.place}</li>)}</ol><Link className="text-link" to="/result">일정과 지도 보기 ↗</Link></div>}<Link className="text-link" to="/planner">날짜를 정하고 코스 만들기 ↗</Link><small>코스는 계정에 저장됩니다. 대화는 페이지를 떠나면 초기화됩니다.</small></aside>
    <div className="chat-main"><div className="chat-heading"><div><strong>여행 도우미</strong><span>{currentPlan?'현재 코스를 참고하고 있어요 · 변경 요청을 알려주세요':'Qwen3 · 먼저 코스를 만들면 대화로 수정할 수 있어요'}</span></div><button className="chat-reset" onClick={reset} disabled={pending||applying}>새 대화</button></div>
      <div className="chat-messages" role="log" aria-label="여행 도우미와의 대화" aria-live="polite">
        {!messages.length&&<div className="chat-welcome"><span className="chat-symbol" aria-hidden="true">✳</span><h1>어떤 여행이 궁금하세요?</h1><p>가고 싶은 곳과 함께하는 사람,<br/>좋아하는 여행을 편하게 이야기해 주세요.</p><div className="chat-suggestions">{suggestions.map(text=><button key={text} onClick={()=>send(text)}>{text}<span>↗</span></button>)}</div></div>}
        {messages.map((message,index)=><article key={index} className={`chat-message ${message.role}`}><span className="chat-avatar" aria-hidden="true">{message.role==='user'?'나':'✳'}</span><div><strong>{message.role==='user'?'나':'Trip Agency'}</strong><p>{message.content}</p></div></article>)}
        {pending&&<div className="chat-waiting" role="status"><span className="thinking-dots">● ● ●</span> 여행 도우미가 답변을 준비하고 있어요.</div>}
        {error&&<div className="notice" role="alert"><p>{error}</p><button className="chip" onClick={()=>failedHistory&&void requestReply(failedHistory)} disabled={pending}>다시 시도</button><button className="chip" onClick={reset}>새 대화</button></div>}
        {proposal&&<section className="chat-proposal card"><span className="eyebrow">UPDATED ITINERARY</span><h2>이렇게 바꿔볼까요?</h2><p>{formatTravelDate(proposal.travel_date)}</p><p>{proposal.summary}</p><RouteTimeline route={proposal.route}/>{proposal.warnings.map(w=><p className="notice" key={w}>{w}</p>)}{applyError&&<p role="alert" className="notice">{applyError}</p>}<div className="chips"><button className="button" onClick={()=>void acceptProposal()} disabled={applying||pending}>{applying?'코스 변경 중…':'이 코스로 변경'}</button><button className="chip" onClick={()=>setProposal(null)} disabled={applying}>기존 코스 유지</button></div><p className="muted">적용 전까지 기존 코스가 유지됩니다.</p></section>}
        <div ref={endRef}/>
      </div>
      <form className="chat-composer" onSubmit={submit}><label className="sr-only" htmlFor="chat-input">여행 도우미에게 메시지 보내기</label><div className="chat-input-row"><textarea id="chat-input" ref={inputRef} rows={2} maxLength={4000} placeholder={currentPlan?'예: 저녁에 비가 온다는데 18시 이후는 실내로 바꿔줘':'여행에 대해 무엇이든 물어보세요…'} value={input} onChange={e=>setInput(e.target.value)} onKeyDown={keyDown} disabled={pending||applying||!!failedHistory}/><button className="button" type="submit" disabled={!input.trim()||pending||applying||!!failedHistory} aria-label="메시지 보내기">↑</button></div><p>Enter로 보내기 · Shift+Enter로 줄바꿈 · 날씨는 사용자 입력을 반영하며 실제 예보 조회는 아직 연결되지 않았어요.</p></form>
    </div>
  </section>;
}
