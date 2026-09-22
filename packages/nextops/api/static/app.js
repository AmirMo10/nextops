"use strict";

const translations = {
  en: {
    brandTagline: "Private infrastructure intelligence", localEnvironment: "Local environment",
    logout: "Sign out", evaluationLabel: "CONTROLLED USER EVALUATION",
    loginHeadline: "Operational insight,<br><span>kept inside your network.</span>",
    loginLead: "Sign in to evaluate the local bilingual AI service. Requests remain within the NextOps environment.",
    trustOne: "Local identity", trustTwo: "Encrypted access", trustThree: "CPU-only inference",
    welcome: "Welcome", credentialsPrompt: "Enter your evaluation credentials.", username: "Username",
    password: "Password", signIn: "Sign in securely", privacyNote: "Your session is stored only in this browser tab.",
    workspaceLabel: "USER EVALUATION WORKSPACE", workspaceHeadline: "Ask the local assistant",
    workspaceLead: "Evaluate bilingual response quality and the protected application-to-AI path.",
    appReady: "Application ready", aiChecking: "Checking AI", aiReady: "AI ready", aiUnavailable: "AI unavailable",
    monitoringChecking: "Checking monitoring", monitoringReady: "Monitoring ready", monitoringUnavailable: "Monitoring unavailable",
    newQuestion: "New question", questionHelp: "Ask in English or Persian. The answer follows the selected language.",
    answerMode: "Answer mode", generalMode: "General assistant", monitoringMode: "Live monitoring",
    generalModeHelp: "Answers the question directly without attaching Zabbix status.",
    monitoringModeHelp: "Uses current read-only Zabbix observations and shows the supporting evidence.",
    question: "Question", questionPlaceholder: "Explain a safe first response to a high CPU alert.", askAssistant: "Ask assistant",
    evidenceBoundary: "EVIDENCE BOUNDARY", liveEvidenceTitle: "Live evidence evaluation",
    liveEvidenceBody: "The read-only connector supplies current Zabbix observations and their timestamps to the local model.",
    boundaryLocal: "Local processing", boundaryLocalText: "No external model API is used.",
    boundaryAuth: "Authenticated path", boundaryAuthText: "The browser never receives the AI service credential.",
    boundaryZabbix: "Live Zabbix evidence", boundaryZabbixText: "Read-only, source-qualified and timestamped.",
    assistantResponse: "ASSISTANT RESPONSE", generalResponseTitle: "Direct local answer", responseTitle: "Evidence-grounded result",
    modelOnlyBadge: "Local model · no live evidence", liveEvidenceBadge: "Live Zabbix evidence",
    source: "Source", host: "Host", collected: "Collected", problems: "Active problems", stale: "stale",
    model: "Model", tokens: "Output tokens", completed: "Completed", requestId: "Request",
    footer: "Controlled local evaluation environment", invalidLogin: "The username or password is incorrect.",
    genericError: "The request could not be completed. Try again.", timeoutError: "The local model took too long. Please try a shorter question.",
    overloadedError: "The local model is busy. Please wait a moment and try again.", dependencyError: "A local service is temporarily unavailable. Please try again.",
    sessionExpired: "Your session expired. Please sign in again.",
    working: "Generating locally…"
  },
  fa: {
    brandTagline: "هوشمندی امن برای عملیات زیرساخت", localEnvironment: "محیط داخلی",
    logout: "خروج", evaluationLabel: "محیط کنترل‌شده ارزیابی کاربران",
    loginHeadline: "بینش عملیاتی؛<br><span>درون شبکه سازمان شما.</span>",
    loginLead: "برای ارزیابی سرویس هوش مصنوعی دوزبانه و داخلی وارد شوید. همه درخواست‌ها در محیط NextOps باقی می‌مانند.",
    trustOne: "هویت داخلی", trustTwo: "دسترسی رمزنگاری‌شده", trustThree: "پردازش صرفاً با CPU",
    welcome: "خوش آمدید", credentialsPrompt: "مشخصات دسترسی محیط ارزیابی را وارد کنید.", username: "نام کاربری",
    password: "گذرواژه", signIn: "ورود امن", privacyNote: "نشست شما فقط در همین برگه مرورگر نگهداری می‌شود.",
    workspaceLabel: "فضای ارزیابی کاربران", workspaceHeadline: "از دستیار داخلی بپرسید",
    workspaceLead: "کیفیت پاسخ‌های فارسی و انگلیسی و مسیر امن ارتباط برنامه با سرویس هوش مصنوعی را ارزیابی کنید.",
    appReady: "برنامه آماده است", aiChecking: "در حال بررسی سرویس هوش مصنوعی", aiReady: "سرویس هوش مصنوعی آماده است", aiUnavailable: "سرویس هوش مصنوعی در دسترس نیست",
    monitoringChecking: "در حال بررسی سامانه پایش", monitoringReady: "سامانه پایش آماده است", monitoringUnavailable: "سامانه پایش در دسترس نیست",
    newQuestion: "پرسش جدید", questionHelp: "پرسش را به فارسی یا انگلیسی بنویسید؛ پاسخ به زبان انتخاب‌شده ارائه می‌شود.",
    answerMode: "شیوهٔ پاسخ", generalMode: "دستیار عمومی", monitoringMode: "پایش زنده",
    generalModeHelp: "بدون افزودن وضعیت Zabbix، مستقیماً به همان پرسش پاسخ می‌دهد.",
    monitoringModeHelp: "از دادهٔ جاری و فقط‌خواندنی Zabbix استفاده می‌کند و شاهد را نیز نشان می‌دهد.",
    question: "پرسش", questionPlaceholder: "برای هشدار مصرف بالای پردازنده، یک اقدام اولیه ایمن پیشنهاد کنید.", askAssistant: "ارسال به دستیار",
    evidenceBoundary: "مرز شواهد", liveEvidenceTitle: "ارزیابی مبتنی بر شواهد زنده",
    liveEvidenceBody: "کانکتور فقط‌خواندنی، مشاهدات جاری Zabbix و زمان ثبت آن‌ها را در اختیار مدل داخلی قرار می‌دهد.",
    boundaryLocal: "پردازش داخلی", boundaryLocalText: "هیچ سرویس مدل بیرونی فراخوانی نمی‌شود.",
    boundaryAuth: "مسیر احراز هویت‌شده", boundaryAuthText: "اعتبارنامه سرویس هوش مصنوعی هرگز در اختیار مرورگر قرار نمی‌گیرد.",
    boundaryZabbix: "شواهد زنده Zabbix", boundaryZabbixText: "فقط‌خواندنی، دارای منبع مشخص و مُهر زمانی.",
    assistantResponse: "پاسخ دستیار", generalResponseTitle: "پاسخ مستقیم مدل محلی", responseTitle: "نتیجه مبتنی بر شواهد",
    modelOnlyBadge: "مدل محلی · بدون شاهد زنده", liveEvidenceBadge: "شواهد زنده Zabbix",
    source: "منبع", host: "میزبان", collected: "زمان گردآوری", problems: "مسائل فعال", stale: "قدیمی",
    model: "مدل", tokens: "توکن‌های خروجی", completed: "زمان تکمیل", requestId: "شناسه درخواست",
    footer: "محیط کنترل‌شده و داخلی ارزیابی", invalidLogin: "نام کاربری یا گذرواژه صحیح نیست.",
    genericError: "انجام درخواست ممکن نشد. دوباره تلاش کنید.", timeoutError: "زمان پردازش مدل محلی به پایان رسید. لطفاً پرسش کوتاه‌تری مطرح کنید.",
    overloadedError: "مدل محلی در حال پردازش درخواست دیگری است. لطفاً کمی بعد دوباره تلاش کنید.", dependencyError: "یکی از سرویس‌های داخلی موقتاً در دسترس نیست. لطفاً دوباره تلاش کنید.",
    sessionExpired: "نشست شما پایان یافته است. دوباره وارد شوید.",
    working: "در حال تولید پاسخ در محیط داخلی…"
  }
};

const state = {
  language: localStorage.getItem("nextops-language") || "en",
  answerLocale: "en",
  answerMode: "general",
  token: sessionStorage.getItem("nextops-session") || ""
};
const byId = id => document.getElementById(id);

function applyLanguage(language) {
  state.language = language;
  localStorage.setItem("nextops-language", language);
  document.documentElement.lang = language;
  document.documentElement.dir = language === "fa" ? "rtl" : "ltr";
  byId("languageButton").textContent = language === "fa" ? "English" : "فارسی";
  document.querySelectorAll("[data-i18n]").forEach(node => {
    const value = translations[language][node.dataset.i18n];
    if (value !== undefined) node.innerHTML = value;
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(node => {
    node.placeholder = translations[language][node.dataset.i18nPlaceholder];
  });
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(path, { ...options, headers, cache: "no-store" });
  let body = null;
  try { body = await response.json(); } catch (_) { body = {}; }
  if (!response.ok) {
    const error = new Error(body?.error?.message_key || "request.failed");
    error.status = response.status;
    error.code = body?.error?.code || "internal_error";
    throw error;
  }
  return body;
}

function showLogin(message = "") {
  state.token = "";
  sessionStorage.removeItem("nextops-session");
  byId("loginView").classList.remove("hidden");
  byId("workspaceView").classList.add("hidden");
  byId("logoutButton").classList.add("hidden");
  byId("loginError").textContent = message;
}

async function showWorkspace() {
  await api("/api/v1/me");
  byId("loginView").classList.add("hidden");
  byId("workspaceView").classList.remove("hidden");
  byId("logoutButton").classList.remove("hidden");
  checkAi();
  checkMonitoring();
}

async function checkAi() {
  const pill = byId("aiStatus");
  try {
    const ready = await api("/api/v1/assistant/ready");
    const ok = ready.state === "ready";
    pill.className = `status-pill ${ok ? "ready" : "failed"}`;
    pill.querySelector("span").textContent = translations[state.language][ok ? "aiReady" : "aiUnavailable"];
  } catch (_) {
    pill.className = "status-pill failed";
    pill.querySelector("span").textContent = translations[state.language].aiUnavailable;
  }
}

async function checkMonitoring() {
  const pill = byId("monitoringStatus");
  try {
    const summary = await api("/api/v1/monitoring/summary");
    const ok = summary.source === "zabbix";
    pill.className = `status-pill ${ok ? "ready" : "failed"}`;
    pill.querySelector("span").textContent = translations[state.language][ok ? "monitoringReady" : "monitoringUnavailable"];
  } catch (_) {
    pill.className = "status-pill failed";
    pill.querySelector("span").textContent = translations[state.language].monitoringUnavailable;
  }
}

function renderEvidence(evidence) {
  const locale = state.language === "fa" ? "fa-IR" : "en-GB";
  byId("evidenceSource").textContent = `Zabbix ${evidence.source_version}`;
  byId("evidenceHost").textContent = evidence.host;
  byId("evidenceCollected").textContent = new Date(evidence.collected_at).toLocaleString(locale);
  byId("problemCount").textContent = evidence.active_problems.length;
  const list = byId("metricList");
  list.replaceChildren();
  evidence.metrics.forEach(metric => {
    const item = document.createElement("div");
    item.className = "metric-item";
    const title = document.createElement("strong");
    title.textContent = metric.name;
    const value = document.createElement("span");
    value.textContent = `${metric.value}${metric.units ? ` ${metric.units}` : ""}`;
    const time = document.createElement("small");
    time.textContent = `${new Date(metric.measured_at).toLocaleString(locale)}${metric.stale ? ` · ${translations[state.language].stale}` : ""}`;
    item.append(title, value, time);
    list.append(item);
  });
}

function safeRequestError(error) {
  const keyByCode = {
    timeout: "timeoutError",
    overloaded: "overloadedError",
    dependency_unavailable: "dependencyError"
  };
  return translations[state.language][keyByCode[error.code] || "genericError"];
}

function setAnswerMode(mode) {
  state.answerMode = mode;
  document.querySelectorAll(".mode-choice").forEach(item => {
    item.classList.toggle("active", item.dataset.mode === mode);
  });
  const helpKey = mode === "monitoring" ? "monitoringModeHelp" : "generalModeHelp";
  byId("modeHelp").dataset.i18n = helpKey;
  byId("modeHelp").textContent = translations[state.language][helpKey];
  byId("resultCard").classList.add("hidden");
}

byId("languageButton").addEventListener("click", () => applyLanguage(state.language === "en" ? "fa" : "en"));
byId("logoutButton").addEventListener("click", () => showLogin());
byId("loginForm").addEventListener("submit", async event => {
  event.preventDefault();
  const button = event.currentTarget.querySelector("button[type=submit]");
  byId("loginError").textContent = "";
  button.disabled = true;
  try {
    const result = await api("/api/v1/login", { method: "POST", body: JSON.stringify({ username: byId("username").value, password: byId("password").value }) });
    state.token = result.session.access_token;
    sessionStorage.setItem("nextops-session", state.token);
    byId("password").value = "";
    await showWorkspace();
  } catch (_) {
    byId("loginError").textContent = translations[state.language].invalidLogin;
  } finally { button.disabled = false; }
});

document.querySelectorAll(".locale-choice").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".locale-choice").forEach(item => item.classList.remove("active"));
  button.classList.add("active");
  state.answerLocale = button.dataset.locale;
}));
document.querySelectorAll(".mode-choice").forEach(button => button.addEventListener("click", () => {
  setAnswerMode(button.dataset.mode);
}));
byId("question").addEventListener("input", event => { byId("characterCount").textContent = `${event.target.value.length} / 4000`; });
byId("assistantForm").addEventListener("submit", async event => {
  event.preventDefault();
  const button = byId("askButton");
  const errorNode = byId("assistantError");
  errorNode.textContent = "";
  button.disabled = true;
  const original = button.querySelector("span").textContent;
  button.querySelector("span").textContent = translations[state.language].working;
  try {
    const monitoring = state.answerMode === "monitoring";
    const path = monitoring ? "/api/v1/investigate" : "/api/v1/assistant/generate";
    const result = await api(path, { method: "POST", body: JSON.stringify({ locale: state.answerLocale, question: byId("question").value, max_output_tokens: 128 }) });
    const assistant = monitoring ? result.assistant : result;
    byId("answer").textContent = assistant.answer;
    byId("answer").dir = assistant.locale === "fa" ? "rtl" : "ltr";
    byId("modelId").textContent = assistant.model_id;
    byId("tokenCount").textContent = assistant.completion_tokens;
    byId("completedAt").textContent = new Date(assistant.completed_at).toLocaleString(state.language === "fa" ? "fa-IR" : "en-GB");
    byId("requestId").textContent = assistant.request_id;
    const titleKey = monitoring ? "responseTitle" : "generalResponseTitle";
    const badgeKey = monitoring ? "liveEvidenceBadge" : "modelOnlyBadge";
    byId("responseTitle").dataset.i18n = titleKey;
    byId("responseTitle").textContent = translations[state.language][titleKey];
    byId("evidenceBadge").dataset.i18n = badgeKey;
    byId("evidenceBadge").textContent = translations[state.language][badgeKey];
    byId("evidenceBadge").classList.toggle("live", monitoring);
    byId("evidencePanel").classList.toggle("hidden", !monitoring);
    if (monitoring) renderEvidence(result.evidence);
    byId("resultCard").classList.remove("hidden");
    byId("resultCard").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    if (error.status === 401) showLogin(translations[state.language].sessionExpired);
    else errorNode.textContent = safeRequestError(error);
  } finally { button.disabled = false; button.querySelector("span").textContent = original; }
});

applyLanguage(state.language);
if (state.token) showWorkspace().catch(() => showLogin(translations[state.language].sessionExpired));
