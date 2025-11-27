// // script.js - minimal frontend to use the backend API
// // Configure base API URL
// const API_BASE = (function(){
//   // If serving statically from same host use same origin
//   return window.API_BASE || "http://127.0.0.1:5000/api";
// })();

// function storageSet(obj) {
//   localStorage.setItem("ai_doc", JSON.stringify(obj));
// }
// function storageGet(){
//   try {
//     return JSON.parse(localStorage.getItem("ai_doc") || "{}");
//   } catch(e){ return {}; }
// }

// function setToken(tok){
//   const s = storageGet();
//   s.token = tok;
//   storageSet(s);
// }
// function getToken(){ return storageGet().token; }
// function authHeaders(){
//   return { "Content-Type":"application/json", "Authorization": "Bearer " + getToken() };
// }

// async function post(path, body){
//   const res = await fetch(API_BASE + path, {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify(body)
//   });
//   return res.json();
// }
// async function get(path){
//   const res = await fetch(API_BASE + path, { headers: authHeaders() });
//   return res.json();
// }

// // ------------- index.html behavior -------------
// if (document.body.contains(document.getElementById("authForm"))){
//   document.getElementById("loginBtn").addEventListener("click", async () => {
//     const email = document.getElementById("email").value;
//     const password = document.getElementById("password").value;
//     try {
//       const r = await fetch(API_BASE + "/login", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({email,password})});
//       const data = await r.json();
//       if (r.ok) {
//         setToken(data.token);
//         window.location = "dashboard.html";
//       } else {
//         showAlert(data.error || "Login failed");
//       }
//     } catch(e){ showAlert("Network error"); }
//   });
//   document.getElementById("registerBtn").addEventListener("click", async () => {
//     const email = document.getElementById("email").value;
//     const password = document.getElementById("password").value;
//     try {
//       const r = await fetch(API_BASE + "/register", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({email,password})});
//       const data = await r.json();
//       if (r.ok) {
//         setToken(data.token);
//         window.location = "dashboard.html";
//       } else {
//         showAlert(data.error || "Register failed");
//       }
//     } catch(e){ showAlert("Network error"); }
//   });
// }

// function showAlert(msg, type="danger"){
//   const el = document.getElementById("alert");
//   if (!el) return alert(msg);
//   el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
//   setTimeout(()=> el.innerHTML = "", 4000);
// }

// // ------------- dashboard.html behavior -------------
// async function loadDashboard(){
//   const list = document.getElementById("projectsList");
//   if (!list) return;
//   const r = await fetch(API_BASE + "/projects", { headers: authHeaders() });
//   const data = await r.json();
//   if (!Array.isArray(data)) {
//     if (data.error) {
//       alert("Error: " + data.error);
//       return;
//     }
//   }
//   list.innerHTML = "";
//   data.forEach(p => {
//     const card = document.createElement("div");
//     card.className = "col-md-4";
//     card.innerHTML = `
//       <div class="card p-3">
//         <h5>${escapeHtml(p.topic || "(no topic)")}</h5>
//         <p class="text-muted">${p.doc_type.toUpperCase()}</p>
//         <div class="d-flex gap-2">
//           <button class="btn btn-sm btn-primary" onclick="openEditor(${p.id})">Open</button>
//         </div>
//       </div>
//     `;
//     list.appendChild(card);
//   });
// }

// async function createProject(){
//   const docType = document.getElementById("docType").value;
//   const topic = document.getElementById("topic").value || "Untitled Project";
//   // default empty config
//   const config = docType === "docx" ? { sections: [] } : { slides: [] };
//   const res = await fetch(API_BASE + "/projects", {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify({ doc_type: docType, topic, config })
//   });
//   const data = await res.json();
//   if (res.ok) {
//     window.location = `editor.html?project=${data.id}`;
//   } else {
//     alert(data.error || "Failed to create");
//   }
// }

// function openEditor(id){
//   window.location = `editor.html?project=${id}`;
// }

// // logout
// if (document.getElementById("logoutBtn")){
//   document.getElementById("logoutBtn").addEventListener("click", () => {
//     localStorage.removeItem("ai_doc");
//     window.location = "index.html";
//   });
// }

// // dashboard buttons
// if (document.getElementById("createProj")){
//   document.getElementById("createProj").addEventListener("click", createProject);
//   // load list
//   document.addEventListener("DOMContentLoaded", loadDashboard);
// }

// function getQueryParam(name){
//   const params = new URLSearchParams(window.location.search);
//   return params.get(name);
// }

// // ------------- editor.html behavior -------------
// async function loadEditor(){
//   const pid = getQueryParam("project");
//   if (!pid) { alert("No project id"); return; }
//   const res = await fetch(API_BASE + `/projects/${pid}`, { headers: authHeaders() });
//   const data = await res.json();
//   if (data.error) { alert(data.error); return; }
//   document.getElementById("projectTitle").innerText = data.topic;
//   document.getElementById("projectInfo").innerHTML = `<small class="text-muted">Type: ${data.doc_type}</small>`;
//   const container = document.getElementById("sectionsContainer");
//   container.innerHTML = "";
//   data.sections.forEach(s => {
//     const div = document.createElement("div");
//     div.className = "card p-3 section-card";
//     div.innerHTML = `
//       <div class="d-flex justify-content-between">
//         <h5>${escapeHtml(s.title || "(no title)")}</h5>
//         <div>
//           <button class="btn btn-sm btn-outline-secondary" onclick="likeSection(${s.id})">Like</button>
//           <button class="btn btn-sm btn-outline-secondary" onclick="dislikeSection(${s.id})">Dislike</button>
//         </div>
//       </div>
//       <div class="mt-2 section-content" id="content-${s.id}">${escapeHtml(s.content || "")}</div>
//       <div class="mt-2">
//         <textarea id="edit-${s.id}" class="form-control" rows="4">${escapeHtml(s.content || "")}</textarea>
//       </div>
//       <div class="mt-2 d-flex gap-2">
//         <button class="btn btn-primary" onclick="saveSection(${s.id})">Save</button>
//         <button class="btn btn-outline-info" onclick="refineSectionPrompt(${s.id})">AI Refine</button>
//         <button class="btn btn-outline-secondary" onclick="toggleComments(${s.id})">Comments</button>
//         <button class="btn btn-outline-dark" onclick="showHistory(${s.id})">History</button>
//       </div>
//       <div class="mt-2" id="comments-${s.id}" style="display:none;">
//         <h6>Comments</h6>
//         <div id="comment-list-${s.id}"></div>
//         <div class="input-group mt-2">
//           <input id="comment-input-${s.id}" class="form-control" placeholder="Add comment">
//           <button class="btn btn-sm btn-outline-primary" onclick="addComment(${s.id})">Add</button>
//         </div>
//       </div>
//     `;
//     container.appendChild(div);
//   });

//   // wire up buttons
//   document.getElementById("generateBtn").addEventListener("click", async () => {
//     const r = await fetch(API_BASE + `/projects/${pid}/generate`, { method: "POST", headers: authHeaders() });
//     const j = await r.json();
//     if (r.ok) {
//       alert("Generation complete. Refreshing page.");
//       window.location.reload();
//     } else {
//       alert(j.error || "Generation error");
//     }
//   });

//   // document.getElementById("exportDocBtn").addEventListener("click", () => {
//   //   window.location = API_BASE.replace("/api","/api") + `/projects/${pid}/export?type=docx`;
//   // });
//   // document.getElementById("exportPptBtn").addEventListener("click", () => {
//   //   window.location = API_BASE.replace("/api","/api") + `/projects/${pid}/export?type=pptx`;
//   // });
// document.getElementById("exportDocBtn").addEventListener("click", () => {
//     exportFile(pid, "docx");
// });

// document.getElementById("exportPptBtn").addEventListener("click", () => {
//     exportFile(pid, "pptx");
// });

// async function exportFile(pid, fileType) {
//     const token = getToken();

//     const res = await fetch(`${API_BASE}/projects/${pid}/export?type=${fileType}`, {
//         method: "GET",
//         headers: {
//             "Authorization": "Bearer " + token
//         }
//     });

//     if (!res.ok) {
//         alert("Export failed");
//         return;
//     }

//     // Download file
//     const blob = await res.blob();
//     const url = URL.createObjectURL(blob);

//     const a = document.createElement("a");
//     a.href = url;
//     a.download = fileType === "docx" ? "document.docx" : "presentation.pptx";

//     document.body.appendChild(a);
//     a.click();
//     a.remove();
//     URL.revokeObjectURL(url);
// }

//  document.getElementById("addSectionBtn").addEventListener("click", async () => {
//     const pid = getQueryParam("project");
//     const title = document.getElementById("newTitle").value.trim();
//     if (!title) {
//         alert("Title cannot be empty");
//         return;
//     }

//     const res = await fetch(API_BASE + `/projects/${pid}/sections`, {
//         method: "POST",
//         headers: authHeaders(),
//         body: JSON.stringify({ title })
//     });

//     const data = await res.json();
//     if (res.ok) {
//         alert("Section added!");
//         window.location.reload();
//     } else {
//         alert(data.error || "Error adding section");
//     }
// });


//   // populate comments
//   data.sections.forEach(s => {
//     const cl = document.getElementById(`comment-list-${s.id}`);
//     if (!cl) return;
//     cl.innerHTML = "";
//     (s.comments || []).forEach(c => {
//       const el = document.createElement("div");
//       el.innerHTML = `<small>${escapeHtml(c.text || c)}</small>`;
//       cl.appendChild(el);
//     });
//   });

//   // back button
//   document.getElementById("backBtn").addEventListener("click", () => {
//     window.location = "dashboard.html";
//   });
// }

// async function saveSection(id){
//   const text = document.getElementById(`edit-${id}`).value;
//   // we don't have a dedicated update-section endpoint; we can reuse refine with instruction 'replace with' to update quickly
//   const res = await fetch(API_BASE + `/sections/${id}/refine`, {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify({ instruction: "REPLACE_WITH: " + text })
//   });
//   const data = await res.json();
//   if (res.ok) {
//     document.getElementById(`content-${id}`).innerText = data.content;
//     alert("Saved");
//   } else {
//     alert(data.error || "save failed");
//   }
// }

// async function refineSectionPrompt(id){
//   const instr = prompt("Enter refinement instruction (e.g. Make more formal, Shorten to 100 words, Convert to bullets):");
//   if (!instr) return;
//   const res = await fetch(API_BASE + `/sections/${id}/refine`, {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify({ instruction: instr })
//   });
//   const data = await res.json();
//   if (res.ok) {
//     document.getElementById(`content-${id}`).innerText = data.content;
//     document.getElementById(`edit-${id}`).value = data.content;
//     alert("Refined");
//   } else {
//     alert(data.error || "refine failed");
//   }
// }

// async function likeSection(id){
//   await fetch(API_BASE + `/sections/${id}/feedback`, {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify({ action: "like" })
//   });
//   alert("Liked");
// }
// async function dislikeSection(id){
//   await fetch(API_BASE + `/sections/${id}/feedback`, {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify({ action: "dislike" })
//   });
//   alert("Disliked");
// }
// async function addComment(id){
//   const v = document.getElementById(`comment-input-${id}`).value;
//   if (!v) return;
//   await fetch(API_BASE + `/sections/${id}/feedback`, {
//     method: "POST",
//     headers: authHeaders(),
//     body: JSON.stringify({ action: "comment", comment: v })
//   });
//   alert("Comment added");
//   window.location.reload();
// }
// function toggleComments(id){
//   const el = document.getElementById(`comments-${id}`);
//   if (!el) return;
//   el.style.display = (el.style.display === "none") ? "block" : "none";
// }

// async function showHistory(sectionId) {
//     const res = await fetch(`${API_BASE}/sections/${sectionId}/history`, {
//         method: "GET",
//         headers: {
//             "Authorization": "Bearer " + getToken()
//         }
//     });

//     const history = await res.json();

//     if (!Array.isArray(history)) {
//         alert("No history found");
//         return;
//     }

//     let html = "";

//     history.forEach(h => {
//         html += `
//           <div class="border rounded p-2 mb-2 bg-light">
//               <p><strong>Instruction:</strong> ${escapeHtml(h.instruction)}</p>
//               <p><strong>Old:</strong> ${escapeHtml(h.old)}</p>
//               <p><strong>New:</strong> ${escapeHtml(h.new)}</p>
//               <small class="text-muted">${h.timestamp}</small>
//           </div>
//         `;
//     });

//     document.getElementById("historyBody").innerHTML = html;
//     document.getElementById("historyModal").style.display = "flex";
// }

// function closeHistory() {
//     document.getElementById("historyModal").style.display = "none";
// }


// function escapeHtml(s){
//   if (!s) return "";
//   return s.replaceAll("&", "&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");
// }

// // run editor loader if needed
// if (document.body.contains(document.getElementById("projectTitle"))){
//   document.addEventListener("DOMContentLoaded", loadEditor);
// }

// async function showHistory(id){
//     const res = await fetch(API_BASE + `/sections/${id}/history`, {
//         method: "GET",
//         headers: authHeaders()
//     });

//     const history = await res.json();
//     if (!Array.isArray(history)) {
//         alert("No history found");
//         return;
//     }

//     let html = "<h4>Revision History</h4>";
//     history.forEach(h => {
//         html += `
//         <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
//             <p><b>Instruction:</b> ${escapeHtml(h.instruction)}</p>
//             <p><b>Old:</b><br>${escapeHtml(h.old)}</p>
//             <p><b>New:</b><br>${escapeHtml(h.new)}</p>
//             <p><b>At:</b> ${h.timestamp}</p>
//         </div>`;
//     });

//     const win = window.open("", "_blank", "width=700,height=600,scrollbars=yes");
//     win.document.write(html);
//     win.document.close();
// }


// script.js - Complete frontend with all features
// const API_BASE = (function(){
//   return window.API_BASE || "http://127.0.0.1:5000/api";
// })();

const API_BASE = "https://ai-doc-platform-5.onrender.com/api";

function storageSet(obj) {
  localStorage.setItem("ai_doc", JSON.stringify(obj));
}
function storageGet(){
  try {
    return JSON.parse(localStorage.getItem("ai_doc") || "{}");
  } catch(e){ return {}; }
}

function setToken(tok){
  const s = storageGet();
  s.token = tok;
  storageSet(s);
}
function getToken(){ return storageGet().token; }
function authHeaders(){
  return { "Content-Type":"application/json", "Authorization": "Bearer " + getToken() };
}

async function post(path, body){
  const res = await fetch(API_BASE + path, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(body)
  });
  return res.json();
}
async function get(path){
  const res = await fetch(API_BASE + path, { headers: authHeaders() });
  return res.json();
}

// ------------- index.html behavior -------------
if (document.body.contains(document.getElementById("authForm"))){
  document.getElementById("loginBtn").addEventListener("click", async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    try {
      const r = await fetch(API_BASE + "/login", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({email,password})});
      const data = await r.json();
      if (r.ok) {
        setToken(data.token);
        window.location = "dashboard.html";
      } else {
        showAlert(data.error || "Login failed");
      }
    } catch(e){ showAlert("Network error"); }
  });
  document.getElementById("registerBtn").addEventListener("click", async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    try {
      const r = await fetch(API_BASE + "/register", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({email,password})});
      const data = await r.json();
      if (r.ok) {
        setToken(data.token);
        window.location = "dashboard.html";
      } else {
        showAlert(data.error || "Register failed");
      }
    } catch(e){ showAlert("Network error"); }
  });
}

function showAlert(msg, type="danger"){
  const el = document.getElementById("alert");
  if (!el) return alert(msg);
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(()=> el.innerHTML = "", 4000);
}

// ------------- dashboard.html behavior -------------
let suggestedOutline = null;

async function loadDashboard(){
  const list = document.getElementById("projectsList");
  if (!list) return;
  const r = await fetch(API_BASE + "/projects", { headers: authHeaders() });
  const data = await r.json();
  if (!Array.isArray(data)) {
    if (data.error) {
      alert("Error: " + data.error);
      return;
    }
  }
  list.innerHTML = "";
  data.forEach(p => {
    const card = document.createElement("div");
    card.className = "col-md-4";
    card.innerHTML = `
      <div class="card p-3">
        <h5>${escapeHtml(p.topic || "(no topic)")}</h5>
        <p class="text-muted">${p.doc_type.toUpperCase()}</p>
        <div class="d-flex gap-2">
          <button class="btn btn-sm btn-primary" onclick="openEditor(${p.id})">Open</button>
        </div>
      </div>
    `;
    list.appendChild(card);
  });
}

// AI Suggest Outline Feature
if (document.getElementById("aiSuggestBtn")) {
  document.getElementById("aiSuggestBtn").addEventListener("click", async () => {
    const topic = document.getElementById("aiTopic").value.trim();
    const docType = document.getElementById("aiDocType").value;
    
    if (!topic) {
      alert("Please enter a topic");
      return;
    }
    
    // Show loading
    document.getElementById("aiSuggestText").classList.add("d-none");
    document.getElementById("aiSuggestSpinner").classList.remove("d-none");
    document.getElementById("aiSuggestBtn").disabled = true;
    
    try {
      const res = await fetch(API_BASE + "/projects/suggest-outline", {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({ topic, doc_type: docType })
      });
      
      const data = await res.json();
      
      if (res.ok) {
        suggestedOutline = {
          topic,
          docType,
          outline: docType === "docx" ? data.sections : data.slides
        };
        displayOutline(suggestedOutline.outline);
      } else {
        alert(data.error || "Failed to generate outline");
      }
    } catch(e) {
      alert("Network error: " + e.message);
    } finally {
      document.getElementById("aiSuggestText").classList.remove("d-none");
      document.getElementById("aiSuggestSpinner").classList.add("d-none");
      document.getElementById("aiSuggestBtn").disabled = false;
    }
  });
}

function displayOutline(outline) {
  const previewDiv = document.getElementById("outlinePreview");
  const listDiv = document.getElementById("outlineList");
  
  previewDiv.classList.remove("d-none");
  listDiv.innerHTML = "";
  
  outline.forEach((title, idx) => {
    const item = document.createElement("div");
    item.className = "outline-item d-flex align-items-center gap-2";
    item.innerHTML = `
      <span class="badge bg-primary">${idx + 1}</span>
      <input type="text" class="form-control form-control-sm outline-title" value="${escapeHtml(title)}">
      <button class="btn btn-sm btn-danger" onclick="removeOutlineItem(${idx})">✗</button>
    `;
    listDiv.appendChild(item);
  });
  
  // Add "Add More" button
  const addBtn = document.createElement("button");
  addBtn.className = "btn btn-sm btn-outline-primary mt-2";
  addBtn.textContent = "+ Add Section";
  addBtn.onclick = addOutlineItem;
  listDiv.appendChild(addBtn);
}

function addOutlineItem() {
  const listDiv = document.getElementById("outlineList");
  const inputs = listDiv.querySelectorAll(".outline-title");
  const idx = inputs.length;
  
  const item = document.createElement("div");
  item.className = "outline-item d-flex align-items-center gap-2";
  item.innerHTML = `
    <span class="badge bg-primary">${idx + 1}</span>
    <input type="text" class="form-control form-control-sm outline-title" placeholder="New section title">
    <button class="btn btn-sm btn-danger" onclick="removeOutlineItem(${idx})">✗</button>
  `;
  
  // Insert before the "Add More" button
  const addBtn = listDiv.querySelector("button.btn-outline-primary");
  listDiv.insertBefore(item, addBtn);
}

function removeOutlineItem(idx) {
  const listDiv = document.getElementById("outlineList");
  const items = listDiv.querySelectorAll(".outline-item");
  if (items[idx]) {
    items[idx].remove();
    // Renumber remaining items
    const remainingItems = listDiv.querySelectorAll(".outline-item");
    remainingItems.forEach((item, i) => {
      item.querySelector(".badge").textContent = i + 1;
    });
  }
}

if (document.getElementById("acceptOutlineBtn")) {
  document.getElementById("acceptOutlineBtn").addEventListener("click", async () => {
    if (!suggestedOutline) return;
    
    // Collect edited titles
    const inputs = document.querySelectorAll(".outline-title");
    const titles = Array.from(inputs).map(input => input.value.trim()).filter(t => t);
    
    if (titles.length === 0) {
      alert("Please add at least one section/slide");
      return;
    }
    
    // Create project with outline
    const config = suggestedOutline.docType === "docx" 
      ? { sections: titles.map(t => ({ title: t })) }
      : { slides: titles.map(t => ({ title: t })) };
    
    const res = await fetch(API_BASE + "/projects", {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({
        doc_type: suggestedOutline.docType,
        topic: suggestedOutline.topic,
        config
      })
    });
    
    const data = await res.json();
    if (res.ok) {
      window.location = `editor.html?project=${data.id}`;
    } else {
      alert(data.error || "Failed to create project");
    }
  });
}

if (document.getElementById("discardOutlineBtn")) {
  document.getElementById("discardOutlineBtn").addEventListener("click", () => {
    document.getElementById("outlinePreview").classList.add("d-none");
    suggestedOutline = null;
  });
}

async function createProject(){
  const docType = document.getElementById("docType").value;
  const topic = document.getElementById("topic").value || "Untitled Project";
  const config = docType === "docx" ? { sections: [] } : { slides: [] };
  const res = await fetch(API_BASE + "/projects", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ doc_type: docType, topic, config })
  });
  const data = await res.json();
  if (res.ok) {
    window.location = `editor.html?project=${data.id}`;
  } else {
    alert(data.error || "Failed to create");
  }
}

function openEditor(id){
  window.location = `editor.html?project=${id}`;
}

if (document.getElementById("logoutBtn")){
  document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("ai_doc");
    window.location = "index.html";
  });
}

if (document.getElementById("createProj")){
  document.getElementById("createProj").addEventListener("click", createProject);
  document.addEventListener("DOMContentLoaded", loadDashboard);
}

function getQueryParam(name){
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

// ------------- editor.html behavior -------------
async function loadEditor(){
  const pid = getQueryParam("project");
  if (!pid) { alert("No project id"); return; }
  const res = await fetch(API_BASE + `/projects/${pid}`, { headers: authHeaders() });
  const data = await res.json();
  if (data.error) { alert(data.error); return; }
  document.getElementById("projectTitle").innerText = data.topic;
  document.getElementById("projectInfo").innerHTML = `<small class="text-muted">Type: ${data.doc_type}</small>`;
  const container = document.getElementById("sectionsContainer");
  container.innerHTML = "";
  data.sections.forEach(s => {
    const div = document.createElement("div");
    div.className = "card p-3 section-card";
    div.innerHTML = `
      <div class="d-flex justify-content-between">
        <h5>${escapeHtml(s.title || "(no title)")}</h5>
        <div>
          <button class="btn btn-sm btn-outline-secondary" onclick="likeSection(${s.id})">👍 Like</button>
          <button class="btn btn-sm btn-outline-secondary" onclick="dislikeSection(${s.id})">👎 Dislike</button>
        </div>
      </div>
      <div class="mt-2 section-content" id="content-${s.id}">${escapeHtml(s.content || "")}</div>
      <div class="mt-2">
        <textarea id="edit-${s.id}" class="form-control" rows="4">${escapeHtml(s.content || "")}</textarea>
      </div>
      <div class="mt-2 d-flex gap-2">
        <button class="btn btn-primary" onclick="saveSection(${s.id})">Save</button>
        <button class="btn btn-outline-info" onclick="refineSectionPrompt(${s.id})">AI Refine</button>
        <button class="btn btn-outline-secondary" onclick="toggleComments(${s.id})">Comments</button>
        <button class="btn btn-outline-dark" onclick="showHistory(${s.id})">History</button>
      </div>
      <div class="mt-2" id="comments-${s.id}" style="display:none;">
        <h6>Comments</h6>
        <div id="comment-list-${s.id}"></div>
        <div class="input-group mt-2">
          <input id="comment-input-${s.id}" class="form-control" placeholder="Add comment">
          <button class="btn btn-sm btn-outline-primary" onclick="addComment(${s.id})">Add</button>
        </div>
      </div>
    `;
    container.appendChild(div);
  });

  document.getElementById("generateBtn").addEventListener("click", async () => {
    const r = await fetch(API_BASE + `/projects/${pid}/generate`, { method: "POST", headers: authHeaders() });
    const j = await r.json();
    if (r.ok) {
      alert("Generation complete. Refreshing page.");
      window.location.reload();
    } else {
      alert(j.error || "Generation error");
    }
  });

  document.getElementById("exportDocBtn").addEventListener("click", () => {
    exportFile(pid, "docx");
  });

  document.getElementById("exportPptBtn").addEventListener("click", () => {
    exportFile(pid, "pptx");
  });

  document.getElementById("addSectionBtn").addEventListener("click", async () => {
    const title = document.getElementById("newTitle").value.trim();
    if (!title) {
      alert("Title cannot be empty");
      return;
    }

    const res = await fetch(API_BASE + `/projects/${pid}/sections`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify({ title })
    });

    const data = await res.json();
    if (res.ok) {
      alert("Section added!");
      window.location.reload();
    } else {
      alert(data.error || "Error adding section");
    }
  });

  data.sections.forEach(s => {
    const cl = document.getElementById(`comment-list-${s.id}`);
    if (!cl) return;
    cl.innerHTML = "";
    (s.comments || []).forEach(c => {
      const el = document.createElement("div");
      el.innerHTML = `<small>${escapeHtml(c.text || c)}</small>`;
      cl.appendChild(el);
    });
  });

  document.getElementById("backBtn").addEventListener("click", () => {
    window.location = "dashboard.html";
  });
}

async function exportFile(pid, fileType) {
  const token = getToken();
  const res = await fetch(`${API_BASE}/projects/${pid}/export?type=${fileType}`, {
    method: "GET",
    headers: { "Authorization": "Bearer " + token }
  });

  if (!res.ok) {
    alert("Export failed");
    return;
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = fileType === "docx" ? "document.docx" : "presentation.pptx";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

async function saveSection(id){
  const text = document.getElementById(`edit-${id}`).value;
  const res = await fetch(API_BASE + `/sections/${id}/refine`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ instruction: "REPLACE_WITH: " + text })
  });
  const data = await res.json();
  if (res.ok) {
    document.getElementById(`content-${id}`).innerText = data.content;
    alert("Saved");
  } else {
    alert(data.error || "save failed");
  }
}

async function refineSectionPrompt(id){
  const instr = prompt("Enter refinement instruction (e.g. Make more formal, Shorten to 100 words, Convert to bullets):");
  if (!instr) return;
  const res = await fetch(API_BASE + `/sections/${id}/refine`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ instruction: instr })
  });
  const data = await res.json();
  if (res.ok) {
    document.getElementById(`content-${id}`).innerText = data.content;
    document.getElementById(`edit-${id}`).value = data.content;
    alert("Refined");
  } else {
    alert(data.error || "refine failed");
  }
}

async function likeSection(id){
  await fetch(API_BASE + `/sections/${id}/feedback`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ action: "like" })
  });
  alert("Liked");
}

async function dislikeSection(id){
  await fetch(API_BASE + `/sections/${id}/feedback`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ action: "dislike" })
  });
  alert("Disliked");
}

async function addComment(id){
  const v = document.getElementById(`comment-input-${id}`).value;
  if (!v) return;
  await fetch(API_BASE + `/sections/${id}/feedback`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ action: "comment", comment: v })
  });
  alert("Comment added");
  window.location.reload();
}

function toggleComments(id){
  const el = document.getElementById(`comments-${id}`);
  if (!el) return;
  el.style.display = (el.style.display === "none") ? "block" : "none";
}

async function showHistory(id){
  const res = await fetch(API_BASE + `/sections/${id}/history`, {
    method: "GET",
    headers: authHeaders()
  });

  const history = await res.json();
  if (!Array.isArray(history) || history.length === 0) {
    alert("No revision history found");
    return;
  }

  let html = "<h4>Revision History</h4><hr>";
  history.forEach((h, idx) => {
    html += `
    <div style="border:1px solid #ccc; padding:15px; margin-bottom:15px; border-radius:5px;">
        <h6>Revision #${idx + 1}</h6>
        <p><strong>Instruction:</strong> ${escapeHtml(h.instruction)}</p>
        <p><strong>Old Content:</strong><br><small>${escapeHtml(h.old)}</small></p>
        <p><strong>New Content:</strong><br><small>${escapeHtml(h.new)}</small></p>
        <p><small class="text-muted">Timestamp: ${h.timestamp}</small></p>
    </div>`;
  });

  const win = window.open("", "_blank", "width=800,height=600,scrollbars=yes");
  win.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Revision History</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
      ${html}
    </body>
    </html>
  `);
  win.document.close();
}

function escapeHtml(s){
  if (!s) return "";
  return s.replaceAll("&", "&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");
}

if (document.body.contains(document.getElementById("projectTitle"))){
  document.addEventListener("DOMContentLoaded", loadEditor);
}