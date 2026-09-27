#!/usr/bin/env node
import{createAccount,createClient}from'../../RuleDelta/frontend/node_modules/genlayer-js/dist/index.js';
import{studioDevnet}from'../../RuleDelta/frontend/node_modules/genlayer-js/dist/chains/index.js';
const CONTRACT=process.argv[2];if(!/^0x[0-9a-fA-F]{40}$/.test(CONTRACT||''))throw Error('Usage: node scripts/run_live_matrix.mjs <v2-contract-address>');
const chain={...studioDevnet,id:61997,name:'Studio Next',rpcUrls:{default:{http:['https://studio-next.genlayer.com/api']}}};
function hidden(prompt){return new Promise((resolve,reject)=>{process.stdout.write(prompt);process.stdin.setRawMode(true);process.stdin.resume();process.stdin.setEncoding('utf8');let value='';const done=()=>{process.stdin.off('data',onData);process.stdin.setRawMode(false);process.stdin.pause()};const onData=chunk=>{for(const ch of chunk){if(ch==='\u0003'){done();reject(Error('Interrupted'));return}if(ch==='\r'||ch==='\n'){done();process.stdout.write('\n');resolve(value.trim());return}if(ch==='\u007f'||ch==='\b')value=value.slice(0,-1);else value+=ch}};process.stdin.on('data',onData)})}
async function signer(label){const secret=await hidden(`${label} private key: `),account=createAccount(secret.startsWith('0x')?secret:`0x${secret}`);return{account,client:createClient({chain,account})}}
const read=(client,fn,args=[])=>client.readContract({address:CONTRACT,functionName:fn,args,stateStatus:'finalized',jsonSafeReturn:true});
async function write(s,fn,args,label){const fees=await s.client.estimateTransactionFees({leaderTimeunitsAllocation:260n,validatorTimeunitsAllocation:600n});const hash=await s.client.writeContract({account:s.account,address:CONTRACT,functionName:fn,args,value:0n,fees:{distribution:fees.distribution,feeValue:fees.feeValue}});console.log(`${label}.tx=${hash}`);const receipt=await s.client.waitForTransactionReceipt({hash,waitUntil:'finalized',interval:3000,retries:600,fullTransaction:false}),tx=await s.client.getTransaction({hash});console.log(`${label}.execution=${receipt?.txExecutionResultName||'unknown'} consensus=${tx.result_name||tx.result}`);return hash}
const authority=await signer('grant authority'),executor=await signer('spend executor');
if(authority.account.address.toLowerCase()===executor.account.address.toLowerCase())throw Error('Distinct operational wallets required');
const protocol=await read(authority.client,'get_protocol');console.log(`protocol=${JSON.stringify(protocol)}`);
const recipient='0x3333333333333333333333333333333333333333',action='sha256:'+'a'.repeat(64),amount=12500n;
await write(authority,'create_commitment',["Necessary audit services specifically required by the federal award and performed under the Single Audit Act.",'200.425',recipient,amount,action,executor.account.address,86400n],'create_allowable');
const id=Number(await read(authority.client,'get_total'));console.log(`pending=${JSON.stringify(await read(authority.client,'get_commitment',[id]))}`);
await write(authority,'assess_commitment',[id,1n],'assess_allowable');console.log(`authorized=${JSON.stringify(await read(authority.client,'get_commitment',[id]))}`);
await write(executor,'consume_authorization',[id,2n,recipient,amount+1n,action],'wrong_amount');console.log(`after_wrong_amount=${JSON.stringify(await read(authority.client,'get_commitment',[id]))}`);
await write(executor,'consume_authorization',[id,2n,recipient,amount,action],'consume_exact');console.log(`consumed=${JSON.stringify(await read(authority.client,'get_commitment',[id]))}`);
await write(executor,'consume_authorization',[id,3n,recipient,amount,action],'replay');console.log(`after_replay=${JSON.stringify(await read(authority.client,'get_commitment',[id]))}`);
await write(authority,'create_commitment',["Purchase alcoholic beverages for the grant-funded project celebration.",'200.423',recipient,500n,'sha256:'+'b'.repeat(64),executor.account.address,86400n],'create_blocked');
const blockedId=Number(await read(authority.client,'get_total'));await write(authority,'assess_commitment',[blockedId,1n],'assess_blocked');console.log(`blocked=${JSON.stringify(await read(authority.client,'get_commitment',[blockedId]))}`);
