import {client} from './client';
import type {Recommendation} from '../types';
export interface ChatMessage {role:'user'|'assistant';content:string}
export interface ChatResponse {message:string;model:string;current_plan:Recommendation|null;proposed_plan:Recommendation|null}
export async function sendChat(messages:ChatMessage[]):Promise<ChatResponse> {
  return (await client.post('/ai/chat',{messages},{timeout:370000})).data;
}
