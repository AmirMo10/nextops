# Next task / کار بعدی

## English — Phase 0: discovery and architecture review

Read the complete master prompt and all relevant guides. Inspect the current repository and preserve changes. Establish actual server access before reporting hardware observations. Use only authorized non-destructive discovery; do not install packages, stress hardware, download models, change networking or contact production targets.

Produce an evidence-backed report covering repository findings, verified versus unresolved host facts, requirement traceability, component/trust/deployment boundaries, source layout, CPU model/runtime shortlist and staged benchmark, resource-budget proposal, identity/secrets/approval threat model, data/workflow/evidence/topology/API/UI contracts, connector capability roadmap, CI/release/rollback, tests/offline/backup gates and explicit blockers.

Define operating scale: asset count, event/evidence volume, retention, concurrent investigations and target response times. Do not infer scale or measured performance from RAM capacity. Record CPU cores versus logical allocation, NUMA/ISA, available resources and existing workloads only when actually inspected.

Acceptance: owner reviews and approves architecture/roadmap; unsupported facts remain labeled; the smallest Phase 1 increment has a concrete acceptance test. Stop before platform implementation or host changes. A candidate first increment is the typed domain/policy contract with deny-by-default tests and a durable-state design, not all connectors or an unrestricted agent loop.

## فارسی — مرحلهٔ صفر: شناخت و بازبینی معماری

پرامپت کامل و راهنماهای مرتبط خوانده شوند. مخزن فعلی بررسی و تغییرات حفظ شوند. پیش از گزارش سخت‌افزار، دسترسی واقعی سرور مشخص شود. فقط شناسایی غیرمخرب و مجاز انجام شود؛ نصب بسته، آزمون فشار، دانلود مدل، تغییر شبکه و تماس با تجهیز عملیاتی انجام نشود.

گزارش مستند باید یافتهٔ مخزن، مشخصات تأییدشده و نامشخص میزبان، ردیابی نیاز، مرز جزء و اعتماد و استقرار، ساختار کد، فهرست مدل و محیط اجرای CPU و برنامهٔ سنجش مرحله‌ای، پیشنهاد بودجهٔ منابع، مدل تهدید هویت و اطلاعات ورود و تأیید، قرارداد داده و کار و شواهد و توپولوژی و API و رابط، نقشهٔ قابلیت اتصال، CI و انتشار و بازگشت، معیار آزمون و آفلاین و پشتیبان و موانع صریح را پوشش دهد.

تعداد تجهیز، حجم رویداد و شاهد، نگهداری، بررسی هم‌زمان و هدف زمان پاسخ مشخص شوند. ظرفیت واقعی از RAM حدس زده نشود. هسته در برابر سهم منطقی، NUMA و ISA، منابع آزاد و بار موجود فقط پس از مشاهده ثبت شوند.

معیار پذیرش: مالک معماری و نقشهٔ راه را بازبینی و تأیید کند؛ واقعیت بی‌شاهد برچسب داشته باشد؛ کوچک‌ترین گام مرحلهٔ یک آزمون پذیرش روشن داشته باشد. پیش از ساخت محصول یا تغییر میزبان توقف شود. قرارداد دارای نوع دامنه و سیاست با آزمون رد پیش‌فرض و طرح وضعیت ماندگار، نامزد گام اول است؛ نه همهٔ اتصال‌ها یا حلقهٔ عامل نامحدود.
