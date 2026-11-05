document.documentElement.classList.add("js");
(function(){var B=window.BIZ,p=new Intl.DateTimeFormat("en-US",{timeZone:B.tz,weekday:"short",hour:"numeric",minute:"numeric",hourCycle:"h23"}).formatToParts(new Date()),g=function(t){return p.find(function(x){return x.type===t}).value},
d=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].indexOf(g("weekday")),m=(+g("hour"))*60+(+g("minute")),h=B.h[d],row=document.querySelector('tr[data-d="'+d+'"]'),el=document.querySelector("[data-live]");
if(row)row.className="today";
function t(x){var a=Math.floor(x/60),s=a<12?"AM":"PM",b=x%60;a=a%12||12;return a+(b?":"+(b<10?"0":"")+b:"")+" "+s}
if(el){if(h&&h[0]===0&&h[1]===1440)el.textContent="Open now";else if(h&&m>=h[0]&&m<h[1])el.textContent="Open now, until "+t(h[1]);else el.textContent="Closed right now";el.hidden=false}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px"});
document.querySelectorAll(".rv").forEach(function(n){io.observe(n)});
document.querySelectorAll("form[data-demo]").forEach(function(f){f.addEventListener("submit",function(ev){ev.preventDefault();f.querySelector(".ok").hidden=false;f.reset()})})})();
