import {create} from 'zustand';
import type {Recommendation} from '../types';
export const useTravelStore = create<{result:Recommendation|null;setResult:(result:Recommendation)=>void;clearResult:()=>void}>((set)=>({result:null,setResult:(result)=>set({result}),clearResult:()=>set({result:null})}));
