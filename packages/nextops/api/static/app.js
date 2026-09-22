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
    newQuestion: "New question", questionHelp: "Ask in English or Persian. The answer follows the selected language.",
    question: "Question", questionPlaceholder: "Explain a safe first response to a high CPU alert.", askAssistant: "Ask assistant",
    evidenceBoundary: "EVIDENCE BOUNDARY", modelOnlyTitle: "Model-only evaluation",
    modelOnlyBody: "This test panel does not yet query live Zabbix data. Its answers are language-model output, not current monitoring evidence.",
    boundaryLocal: "Local processing", boundaryLocalText: "No external model API is used.",
    boundaryAuth: "Authenticated path", boundaryAuthText: "The browser never receives the AI service credential.",
    boundaryZabbix: "Live Zabbix evidence", boundaryZabbixText: "Planned for the connector phase.",
    assistantResponse: "ASSISTANT RESPONSE", responseTitle: "Local model result", noLiveEvidence: "No live monitoring evidence",
    model: "Model", tokens: "Output tokens", completed: "Completed", requestId: "Request",
    footer: "Controlled local evaluation environment", invalidLogin: "The username or password is incorrect.",
    genericError: "The request could not be completed. Try again.", sessionExpired: "Your session expired. Please sign in again.",
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
    newQuestion: "پرسش جدید", questionHelp: "پرسش را به فارسی یا انگلیسی بنویسید؛ پاسخ به زبان انتخاب‌شده ارائه می‌شود.",
    question: "پرسش", questionPlaceholder: "برای هشدار مصرف بالای پردازنده، یک اقدام اولیه ایمن پیشنهاد کنید.", askAssistant: "ارسال به دستیار",
    evidenceBoundary: "مرز شواهد", modelOnlyTitle: "ارزیابی مدل، بدون داده زنده",
    modelOnlyBody: "این پنل آزمایشی هنوز به داده زنده Zabbix متصل نیست. پاسخ‌ها خروجی مدل زبانی‌اند و نباید به‌عنوان وضعیت فعلی سامانه‌ها تلقی شوند.",
    boundaryLocal: "پردازش داخلی", boundaryLocalText: "هیچ سرویس مدل بیرونی فراخوانی نمی‌شود.",
    boundaryAuth: "مسیر احراز هویت‌شده", boundaryAuthText: "اعتبارنامه سرویس هوش مصنوعی هرگز در اختیار مرورگر قرار نمی‌گیرد.",
    boundaryZabbix: "شواهد زنده Zabbix", boundaryZabbixText: "در مرحله اتصال امن کانکتور اضافه خواهد شد.",
    assistantResponse: "پاسخ دستیار", responseTitle: "خروجی مدل داخلی", noLiveEvidence: "فاقد شواهد زنده پایش",
    model: "مدل", tokens: "توکن‌های خروجی", completed: "زمان تکمیل", requestId: "شناسه درخواست",
    footer: "محیط کنترل‌شده و داخلی ارزیابی", invalidLogin: "نام کاربری یا گذرواژه صحیح نیست.",
    genericError: "انجام درخواست ممکن نشد. دوباره تلاش کنید.", sessionExpired: "نشست شما پایان یافته است. دوباره وارد شوید.",
    working: "در حال تولید پاسخ در محیط داخلی…"
  }
};

const state = { language: localStorage.getItem("nextops-language") || "en", answerLocale: "en", token: sessionStorage.getItem("nextops-session") || "" };
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

document.querySelectorAll(".choice").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".choice").forEach(item => item.classList.remove("active"));
  button.classList.add("active");
  state.answerLocale = button.dataset.locale;
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
    const result = await api("/api/v1/assistant/generate", { method: "POST", body: JSON.stringify({ locale: state.answerLocale, question: byId("question").value, max_output_tokens: 384 }) });
    byId("answer").textContent = result.answer;
    byId("answer").dir = result.locale === "fa" ? "rtl" : "ltr";
    byId("modelId").textContent = result.model_id;
    byId("tokenCount").textContent = result.completion_tokens;
    byId("completedAt").textContent = new Date(result.completed_at).toLocaleString(state.language === "fa" ? "fa-IR" : "en-GB");
    byId("requestId").textContent = result.request_id;
    byId("resultCard").classList.remove("hidden");
    byId("resultCard").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    if (error.status === 401) showLogin(translations[state.language].sessionExpired);
    else errorNode.textContent = translations[state.language].genericError;
  } finally { button.disabled = false; button.querySelector("span").textContent = original; }
});

applyLanguage(state.language);
if (state.token) showWorkspace().catch(() => showLogin(translations[state.language].sessionExpired));
