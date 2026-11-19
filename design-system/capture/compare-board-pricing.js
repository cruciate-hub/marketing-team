// Compare the Pricing board (local render) with Webflow staging, role by role.
const {chromium}=require('/Users/stefanpeek/Projects/marketing-team-ds/design-system/capture/node_modules/playwright');
const BOARD='file:///private/tmp/claude-501/-Users-stefanpeek-Downloads/5d261bf2-c94f-42f4-b496-c6d94ebfa889/scratchpad/artifact-files/60956531-056b-4d24-bd78-934cfcd613c4/project/Pricing.dc.html';
const STAGE='https://social-plus.webflow.io/pricing-conversational?x='+Date.now();
const dir='/private/tmp/claude-501/-Users-stefanpeek-Downloads/5d261bf2-c94f-42f4-b496-c6d94ebfa889/scratchpad/logo/';
const ROLES={
 hero:['section.section_contact .contact','.pricing-contact'],
 title:['.contact_title','.pricing-contact_title'],
 lead:['.contact_lead','.pricing-contact_lead'],
 points:['.contact_points','.pricing-contact_points'],
 check:['.contact_points svg','.pricing-contact_check'],
 card:['.gpc','.pricing-chat'],
 cardHead:['.gpc_head','.pricing-chat_head'],
 cardName:['.gpc_name','.pricing-chat_name'],
 thread:['.gpc_thread','.pricing-chat_thread'],
 botMsg:['.gpc_msg.is-bot p','.pricing-chat_msg'],
 chip:['.gpc_chip','.pricing-chat_chip'],
 foot:['.gpc_foot','.pricing-chat_foot'],
 logoRow:['.logo-wall_inline','.logo-wall_inline'],
 caption:['.logo-wall_inline-caption','.logo-wall_inline-caption'],
 marquee:['.logo-wall_marquee','.logo-wall_marquee'],
 compHeader:['.section_plan .section-header','#whats-included .pricing-header'],
 eyebrow:['.section_plan .eyebrow','#whats-included .pricing-eyebrow'],
 h2:['.section_plan .section-header_title','#whats-included .pricing-header_title'],
 h2lead:['.section_plan .section-header_lead','#whats-included .pricing-header_lead'],
 cell:['.feature-grid_item','.grid-4.c-pricing > *'],
 tile:['.icon-tile','.pricing-icon-tile'],
 cellTitle:['.feature-grid_title','.pricing-cell_title'],
 cellText:['.feature-grid_text','.grid-4 .pricing-cell_text'],
 addLabel:['.plan-row.is-addons .plan-row_label','.c-full-row'],
 addLabelP:['.plan-row.is-addons .plan-row_label p','.pricing-addons-note'],
 addon:['.addon','.grid-3.c-pricing > .card-v1:not(.c-full-row)'],
 addonName:['.addon_name','.pricing-addon_name'],
 addonText:['.addon_text','.pricing-cell_text.is-addon'],
 storyHdr:['section[aria-label="Customer stories"] .section-header','#section-cs-stories .pricing-header'],
 storyH2:['section[aria-label="Customer stories"] .section-header_title','#section-cs-stories .pricing-header_title'],
 storyLead:['section[aria-label="Customer stories"] .section-header_lead','#section-cs-stories .pricing-header_lead'],
 tileActive:['.story-tile.is-active','.cs-cta_link-block-wrapper:first-child'],
 tileOther:['.story-tile:not(.is-active)','.cs-cta_link-block-wrapper:nth-child(2)'],
 footer:['footer','footer'],
};
const KEYS=['fontSize','lineHeight','fontWeight','letterSpacing','color','paddingTop','paddingBottom','paddingLeft','marginTop','backgroundColor','borderRadius','gap'];
async function measure(p){return p.evaluate(([R,K])=>{const o={};for(const [k,[,]] of Object.entries(R)){}
 return null},[ROLES,KEYS]);}
(async()=>{const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
for(const W of (process.argv[2]||'1440,800,390').split(',').map(Number)){
 const res={};
 for(const [src,url,idx] of [['board',BOARD,0],['stage',STAGE,1]]){
  const p=await b.newPage({viewport:{width:W,height:900}});await p.goto(url,{waitUntil:'load'});await p.waitForTimeout(1200);
  await p.addStyleTag({content:'#iubenda-cs-banner,.iubenda-cs-container{display:none!important}'});
  res[src]=await p.evaluate(([R,K,idx])=>{const o={};const top0=(document.querySelector('section.section_contact')||document.querySelector('.pricing-contact')).getBoundingClientRect().top+scrollY;
   for(const [k,sels] of Object.entries(R)){const e=document.querySelector(sels[idx]);if(!e){o[k]='MISSING';continue}const r=e.getBoundingClientRect(),c=getComputedStyle(e);
    o[k]={x:Math.round(r.left),y:Math.round(r.top+scrollY-top0),w:Math.round(r.width),h:Math.round(r.height),...Object.fromEntries(K.map(x=>[x,c[x]]))}}return o},[ROLES,KEYS,idx]);
  await p.screenshot({path:dir+'cmp-'+src+'-'+W+'.png',fullPage:true});await p.close();
 }
 console.log('=== '+W);
 for(const k of Object.keys(ROLES)){const a=res.board[k],s=res.stage[k];if(a==='MISSING'||s==='MISSING'){console.log(k,'board:',a==='MISSING'?'MISSING':'ok','stage:',s==='MISSING'?'MISSING':'ok');continue}
  const d=[];for(const f of ['x','y','w','h']){if(Math.abs(a[f]-s[f])>3)d.push(`${f} ${a[f]}→${s[f]}`)}
  for(const f of KEYS){const av=a[f],sv=s[f];const n1=parseFloat(av),n2=parseFloat(sv);if(!isNaN(n1)&&!isNaN(n2)&&/px/.test(av+sv)){if(Math.abs(n1-n2)>1.5)d.push(`${f} ${av}→${sv}`)}else if(av!==sv)d.push(`${f} ${av}→${sv}`)}
  console.log((d.length?'✗ ':'✓ ')+k+(d.length?': '+d.join(' | '):''));}
}
await b.close();})();
